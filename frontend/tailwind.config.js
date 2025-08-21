/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        matrix: {
          bg: '#1a1a1a',
          text: '#f0f0f0',
          accent: '#00ff41'
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}