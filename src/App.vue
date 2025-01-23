<template>
  <div id="app">
    <h1>AI-Powered Code Editor</h1>
    <CodeEditor />
  </div>
</template>

<script>
import CodeEditor from './components/CodeEditor.vue';

export default {
  name: 'App',
  components: {
    CodeEditor,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}
</style>
