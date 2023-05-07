import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue()
  ],
  server: {
    host: "127.0.0.1",
    port: 8080,
    proxy:{
			'/api': {
				target: 'http://localhost:8000/api',
				changeOrigin: true,
        ws: true,
				rewrite: path => path.replace(/^\/api/, '')
			}
		} 
  },
})
