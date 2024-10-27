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
    "w-4",
    "w-12",
    "h-4",
    "h-12",
    "pt-2",
    "py-4",
    "transition-transform",
    "duration-300",
    "rotate-180"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}