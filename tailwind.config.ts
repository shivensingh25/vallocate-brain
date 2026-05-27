import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        teal: {
          DEFAULT: "#00363D",
          deep: "#00282D",
          black: "#001A1D",
        },
        green: {
          accent: "#00A189",
          light: "#A9FDAC",
        },
        offwhite: "#F7F3F5",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      maxWidth: {
        content: "1180px",
      },
      letterSpacing: {
        tightish: "-0.02em",
        tighter2: "-0.035em",
      },
      animation: {
        float: "float 6s ease-in-out infinite",
        "spin-slow": "spinSlow 38s linear infinite",
        "spin-slow-rev": "spinSlowReverse 52s linear infinite",
        twinkle: "twinkle 3.5s ease-in-out infinite",
        "fade-up": "fadeUp 0.7s cubic-bezier(0.16,1,0.3,1) both",
      },
    },
  },
  plugins: [],
};

export default config;
