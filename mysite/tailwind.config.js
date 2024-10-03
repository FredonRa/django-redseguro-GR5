/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html'
  ],
  safelist: [
    "disabled:bg-gray-200",
    "bg-gray-400",
    "bg-indigo-500",
    "bg-indigo-400",
    "w-fit",
    "self-end",
    "opacity-0",
    "opacity-50",
    "justify-end",
    "w-1/2",
    "mt-5",
    "self-center",
    "h-12",
    "w-12",
    "pt-2"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}