/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html'
  ],
  safelist: [
    "disabled:bg-gray-200",
    "bg-indigo-500",
    "w-fit",
    "self-end",
    "opacity-0",
    "opacity-50",
    "justify-end",
    "w-1/2",
    "mt-5"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}