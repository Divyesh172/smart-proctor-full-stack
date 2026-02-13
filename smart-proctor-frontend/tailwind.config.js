/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        // 🔴 OLD (Broken)
        // "./app/**/*.{js,ts,jsx,tsx,mdx}",
        // "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        // "./components/**/*.{js,ts,jsx,tsx,mdx}",

        // 🟢 NEW (Correct)
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/hooks/**/*.{js,ts,jsx,tsx,mdx}", // If you use classes in hooks
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}