/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        cream: "#FBF9F7",
        sage: "#B2C9BA",
        terracotta: "#964B35",
        charcoal: "#333333",
        brick: "#E07A5F",
      },
      fontFamily: {
        display: ['"Playfair Display"', "serif"],
      },
    },
  },
  plugins: [],
};
