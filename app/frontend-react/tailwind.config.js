/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f4ff',
          100: '#b3e0ff',
          200: '#80ccff',
          300: '#4db8ff',
          400: '#1aa4ff',
          500: '#409eff',
          600: '#3a8ee6',
          700: '#337ecc',
          800: '#2d6eb3',
          900: '#265e99',
        },
        success: {
          500: '#67c23a',
          600: '#5daf34',
        },
        warning: {
          500: '#e6a23c',
          600: '#cf9236',
        },
        danger: {
          500: '#f56c6c',
          600: '#dd6161',
        },
        info: {
          500: '#909399',
          600: '#82848a',
        },
      },
      fontFamily: {
        sans: [
          'Helvetica Neue',
          'Helvetica',
          'PingFang SC',
          'Hiragino Sans GB',
          'Microsoft YaHei',
          '微软雅黑',
          'Arial',
          'sans-serif'
        ],
      },
      boxShadow: {
        'element': '0 2px 12px 0 rgba(0, 0, 0, 0.1)',
        'element-light': '0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04)',
      },
      borderRadius: {
        'element': '4px',
      },
    },
  },
  plugins: [],
}
