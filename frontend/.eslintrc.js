module.exports = {
    root: true,
    env: {
      node: true
    },
    extends: [
      'plugin:vue/essential',
      'eslint:recommended'
    ],
    rules: {
      'no-console': process.env.BUILD_ENV === 'production' ? 'error' : 'off',
      'no-debugger': process.env.BUILD_ENV === 'production' ? 'error' : 'warn',
      'no-unused-vars': process.env.BUILD_ENV === 'production' ? 'error' : 'warn'
    },
    parserOptions: {
      parser: 'babel-eslint'
    }
  }
