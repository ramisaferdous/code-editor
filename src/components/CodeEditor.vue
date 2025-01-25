<template>
  <div class="editor-container">
    <!-- Language Selection -->
    <div class="language-selector">
      <label for="language">Select Language: </label>
      <select id="language" v-model="selectedLanguage" @change="onLanguageChange">
        <option value="javascript">JavaScript</option>
        <option value="python">Python</option>
        <option value="cpp">C++</option>
      </select>
    </div>

    <!-- Code Input -->
    <textarea
      v-model="code"
      @input="debouncedHandleInput"
      placeholder="Start typing your code here..."
    ></textarea>

    <!-- Execute Code Button -->
    <button @click="executeCode">Run Code</button>

    <!-- Output Section -->
    <div v-if="executionResult" class="output">
      <h3>Output:</h3>
      <pre>{{ executionResult }}</pre>
    </div>

    <!-- AI Suggestions -->
    <div v-if="suggestions.length" class="suggestions">
      <h3>AI Suggestions</h3>
      <ul>
        <li
          v-for="(suggestion, index) in suggestions"
          :key="index"
          @click="applySuggestion(suggestion)"
        >
          {{ suggestion }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No suggestions available. Try typing more code or check your API setup.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedLanguage: "javascript", // Default language
      code: "", // User's code input
      suggestions: [], // AI-generated suggestions
      executionResult: "", // Output of executed code
    };
  },
  methods: {
    // Handle language change
    onLanguageChange() {
      this.code = ""; // Clear the editor when the language changes
      this.suggestions = []; // Clear suggestions
      this.executionResult = ""; // Clear the output
    },

    // Debounce to limit the number of API calls
    debounce(func, delay) {
      let timeout;
      return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
      };
    },

    // Fetch AI suggestions
    async fetchSuggestions() {
  if (this.code.trim().length < 3) return; // Avoid API calls for short inputs

  try {
    const response = await axios.post(
      "https://api-inference.huggingface.co/models/bigcode/starcoder",
      { inputs: this.code },
      {
        headers: {
          Authorization: `Bearer ${process.env.VUE_APP_HUGGING_FACE_API_KEY}`,
        },
      }
    );

    console.log("API Response:", response.data);

    this.suggestions = response.data?.length
      ? response.data.map((item) => item.generated_text.trim())
      : ["No valid suggestions returned by the AI."];
  } catch (error) {
    console.error("Error fetching AI suggestions:", error.response?.data || error.message);

    // Handle different error statuses
    if (error.response?.status === 500) {
      this.suggestions = ["Server error: Please try again later."];
    } else if (error.response?.status === 401) {
      this.suggestions = ["Unauthorized: Check your API key."];
    } else {
      this.suggestions = ["Failed to fetch suggestions. Please try again later."];
    }
  }
}

,

    // Apply the selected suggestion to the editor
    applySuggestion(suggestion) {
      this.code += `\n${suggestion}`;
    },

    // Execute the user's code
    async executeCode() {
      if (!this.code.trim()) {
        this.executionResult = "No code provided.";
        return;
      }

      try {
        const response = await axios.post("http://localhost:5000/execute", {
          code: this.code,
          language: this.selectedLanguage, // Send the selected language to the backend
        });

        this.executionResult = response.data.output || response.data.error;
      } catch (error) {
        this.executionResult = "Error executing code. Please try again later.";
        console.error(error);
      }
    },
  },
  mounted() {
    this.debouncedHandleInput = this.debounce(this.fetchSuggestions, 1000); // 1-second delay
  },
};
</script>

<style scoped>
/* Your CSS remains the same */
.editor-container {
  padding: 20px;
}

textarea {
  width: 100%;
  height: 300px;
  font-family: monospace;
  padding: 10px;
  box-sizing: border-box;
}

button {
  margin-top: 10px;
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
}

.output {
  margin-top: 20px;
}

.output h3 {
  margin-bottom: 10px;
}

.output pre {
  background: #f4f4f4;
  padding: 10px;
  border-radius: 5px;
  font-family: monospace;
}

.suggestions {
  margin-top: 20px;
}

.suggestions h3 {
  margin-bottom: 10px;
}

.suggestions ul {
  list-style-type: none;
  padding: 0;
}

.suggestions li {
  background: #f4f4f4;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
  cursor: pointer;
}

.suggestions li:hover {
  background: #ddd;
}
</style>
