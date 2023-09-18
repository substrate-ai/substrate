import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from "path"


// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src/@"),
      "src": path.resolve(__dirname, "./src"),
    },
  },
  assetsInclude: ['**/*.md'],
  build: {
    sourcemap: true,
  //   rollupOptions: {
  //       external: ["react", "react-router", "react-router-dom", "react-redux"],
  //       output: {
  //         globals: {
  //           react: "React",
  //         },
  //       },
  //     },
  }
})
