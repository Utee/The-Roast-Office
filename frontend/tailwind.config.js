/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: "#050505",
        vintagePurple: "#A855F7",
        matrixGreen: "#22C55E",
      },
    },
  },
  plugins: [],
}