from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get("code")
    language = data.get("language")

    if not code or not language:
        return jsonify({"error": "Code and language are required"}), 400

    try:
        # Command for different languages
        if language == "python":
            # Wrap the code for proper execution and capturing output
            command = ["python", "-c", f"exec('''{code}''')"]

        elif language == "javascript":
            # Wrap JavaScript code to evaluate expressions and capture output
            command = ["node", "-e", f"console.log(eval(`{code}`))"]

        elif language == "cpp":
            temp_filename = f"temp_{uuid.uuid4().hex}.cpp"  # Temporary file for C++ code
            try:
                # Write C++ code to a temporary file
                with open(temp_filename, "w") as f:
                    f.write(code)

                # Compile the C++ code
                compile_command = ["g++", "-o", "temp_output", temp_filename]
                compile_process = subprocess.run(
                    compile_command, capture_output=True, text=True, timeout=10
                )

                if compile_process.returncode != 0:
                    # Compilation failed
                    return jsonify({
                        "error": f"Compilation error: {compile_process.stderr.strip()}"
                    }), 400

                # Run the compiled executable
                run_command = ["./temp_output"]
                run_process = subprocess.run(
                    run_command, capture_output=True, text=True, timeout=10
                )

                # Return the output or error
                return jsonify({
                    "output": run_process.stdout.strip(),
                    "error": run_process.stderr.strip()
                })

            finally:
                # Cleanup temporary files
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                if os.path.exists("temp_output"):
                    os.remove("temp_output")

        else:
            # Return error if the language is unsupported
            return jsonify({"error": f"Language '{language}' is not supported"}), 400

        # Run the subprocess for Python and JavaScript
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        # Prepare the response
        response = {
            "output": result.stdout.strip() if result.stdout else None,
            "error": result.stderr.strip() if result.stderr else None
        }
        return jsonify(response)

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Code execution timed out"}), 408
    except Exception as e:
        # Log the full traceback for debugging
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
