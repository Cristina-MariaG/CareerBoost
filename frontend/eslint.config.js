import pluginVue from 'eslint-plugin-vue'

export default [
  ...pluginVue.configs['flat/recommended'],
  {
    rules: {
      // Style formatting — turned off (Prettier's job, not ESLint's)
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/html-self-closing': 'off',
      'vue/attributes-order': 'off',
      'vue/html-indent': 'off',
      'vue/html-closing-bracket-newline': 'off',

      // Multi-word component names — off (App.vue, etc. are intentional)
      'vue/multi-word-component-names': 'off',

      // Real issues — error level
      'no-unused-vars': ['error', { varsIgnorePattern: '^_', argsIgnorePattern: '^_' }],
      'vue/no-unused-vars': 'error',

      // v-html is intentional (sanitized with DOMPurify before use)
      'vue/no-v-html': 'off',

      // No console in production code
      'no-console': 'error',
    },
  },
]
