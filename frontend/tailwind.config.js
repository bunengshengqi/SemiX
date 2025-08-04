/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 工业风格色彩配置
        industrial: {
          50: '#f8f9fa',
          100: '#e9ecef',
          200: '#dee2e6',
          300: '#ced4da',
          400: '#adb5bd',
          500: '#6c757d',
          600: '#495057',
          700: '#343a40',
          800: '#212529',
          900: '#1a1d20',
        },
        steel: {
          50: '#f1f3f4',
          100: '#dfe3e6',
          200: '#c1c8cd',
          300: '#9aa5ac',
          400: '#6b7785',
          500: '#4a5568',
          600: '#3a4553',
          700: '#2d3748',
          800: '#1a202c',
          900: '#171923',
        },
        accent: {
          blue: '#2563eb',
          orange: '#ea580c',
          green: '#16a34a',
          red: '#dc2626',
          yellow: '#ca8a04',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        'industrial': '0.125rem',
      },
      boxShadow: {
        'industrial': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'industrial-lg': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      }
    },
  },
  plugins: [],
}
