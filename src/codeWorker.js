self.onmessage = function (e) {
  const { code, language } = e.data;

  try {
      if (language === "javascript") {
          const result = eval(code); // Safely evaluate JavaScript code
          self.postMessage({ success: true, result: result !== undefined ? result : "Code executed successfully, no output." });
      } else {
          self.postMessage({ success: false, result: `Execution for ${language} is not supported.` });
      }
  } catch (error) {
      self.postMessage({ success: false, result: `Error: ${error.message}` });
  }
};
