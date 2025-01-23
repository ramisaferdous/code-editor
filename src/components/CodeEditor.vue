<template>
    <div class="editor-container">
      <!-- Code Input -->
      <textarea
        v-model="code"
        @input="debouncedHandleInput"
        placeholder="Start typing your code here..."
      ></textarea>
  
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
  import axios from 'axios'; // For API requests
  
  export default {
    data() {
      return {
        code: '', // User's code input
        suggestions: [], // AI-generated suggestions
      };
    },
    methods: {
      // Debounce to limit the number of API calls
      debounce(func, delay) {
        let timeout;
        return (...args) => {
          clearTimeout(timeout);
          timeout = setTimeout(() => func.apply(this, args), delay);
        };
      },
  
      // Call Hugging Face API for suggestions
      async fetchSuggestions() {
  if (this.code.trim().length < 3) return; // Avoid requests for short inputs

  try {
    const response = await axios.post(
      'https://api-inference.huggingface.co/models/bigcode/starcoder',
      {
        inputs: this.code, // Send the current code as a prompt
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.VUE_APP_HUGGING_FACE_API_KEY}`,
        },
      }
    );

    console.log('Full API Response:', response.data); // Log the full API response

    // Extract suggestions from the API response
    this.suggestions = response.data?.length
      ? response.data.map((item) => item.generated_text.trim())
      : ['No valid suggestions returned by the AI.'];
  } catch (error) {
    console.error('Error fetching AI suggestions:', error.response?.data || error.message);
    this.suggestions = ['Failed to fetch suggestions. Please try again later.'];
  }
}

,
  
      // Apply the selected suggestion to the editor
      applySuggestion(suggestion) {
        this.code += `\n${suggestion}`;
      },
    },
    mounted() {
      // Debounce the API calls
      this.debouncedHandleInput = this.debounce(this.fetchSuggestions, 1000); // 1-second delay
    },
  };
  </script>
  
  <style scoped>
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
  