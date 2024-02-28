module.exports = {
    extends: [
      'plugin:vue/vue3-recommended',
      'eslint:recommended',
    ],
    overrides: [
      {
        files: ['*.js', '*.vue'],
      },
    ],
    rules: {
      camelcase: 0,
      'vue/no-v-for-template-key': 0,
      'vue/no-multiple-template-root': 0,
      'newline-per-chained-call': [2, { ignoreChainWithDepth: 2 }],
      'vue/no-unused-vars': 'error',
      "no-trailing-spaces": "error",
      semi: ["error", "always"],
    },
    env: {
        node: true,
    },
  };
