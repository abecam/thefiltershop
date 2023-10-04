/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'templates/**/*.html',
    './filtershop_main/templates/thefiltershop/**/*.html',
  ],
  theme: {
    extend: {
      colors:{
        'base': {
          DEFAULT: '#8B5CF6',
          50: '#EBE3FD',
          100: '#DED0FC',
          200: '#C2A9FA',
          300: '#A783F8',
          400: '#8B5CF6',
          500: '#6527F3',
          600: '#4A0CD6',
          700: '#3709A1',
          800: '#25066C',
          900: '#130336',
          950: '#0A021C'
        },
      }
    },
  },
  plugins: [],
}
