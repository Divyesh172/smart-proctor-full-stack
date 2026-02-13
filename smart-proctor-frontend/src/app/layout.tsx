import type { Metadata } from "next";
import { Inter } from "next/font/google"; // 1. Use 'Inter' instead of 'Geist'
import "./globals.css";

// 2. Configure the font
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "VerifAI - Secure Proctoring Platform",
    description: "Enterprise Identity Verification & Anti-Cheating System",
};

export default function RootLayout({
                                       children,
                                   }: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
        {/* 3. Apply the font class to the body */}
        <body className={inter.className}>{children}</body>
        </html>
    );
}