/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        forest: "#073B05",
        blush: "#FBDCE7",
        paper: "#FBF8F2",
        rose: "#C9788F",
        card: "#FFFDF8",
        oat: "#E3DCCE",
        leaf: "#E8F0E2",
        bark: "#1E2A19",
        sage: "#55604F",
        "blush-tint": "#FDEFF3",
        "blush-text": "#B5697F",
        plum: "#4A2A34",
        mist: "#C7D8BF",
        "mist-light": "#DCE7D6",
      },
    },
  },
  plugins: [],
};
