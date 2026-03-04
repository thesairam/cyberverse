/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        cyber: {
          900: "#0a0e1a", 800: "#0d1224", 700: "#111827",
          600: "#1a2235", 500: "#243044",
          accent: "#00d8ff", green: "#00ff9d", red: "#ff4560",
          yellow: "#ffd700", purple: "#9d4edd",
        },
      },
      fontFamily: { mono: ["JetBrains Mono", "Fira Code", "monospace"] },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "glow": "glow 2s ease-in-out infinite alternate",
      },
    },
  },
  plugins: [],
};
