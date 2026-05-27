import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "V-brain by VisagioX — One brain behind every decision your firm makes",
  description:
    "V-brain is a passive intelligence layer that learns how professional services firms actually work — from the artifacts of daily work, not indexed documents. Agents run on top of it. V-allocate, for project allocation, is the first.",
  openGraph: {
    title: "V-brain by VisagioX — the company brain",
    description:
      "A passive intelligence layer that learns how your firm works. Agents run on top of it — V-allocate is the first.",
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
