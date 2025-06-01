module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5003',
        changeOrigin: true,
        ws: true,
      },
    },
  },
}
