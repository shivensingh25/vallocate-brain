import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "V-brain by VisagioX — The intelligence layer for how your firm decides",
  description:
    "V-brain is a passive intelligence layer that captures how consultants and partners actually make decisions — learning from the artifacts of daily work. V-allocate is the first product: AI-driven project allocation for consulting firms.",
  openGraph: {
    title: "V-brain by VisagioX",
    description:
      "A passive intelligence layer that learns how your firm decides. V-allocate is the first product, built for project allocation.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
