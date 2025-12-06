import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";
import Link from "next/link";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Thorax - AI-Powered Smart Contract Security",
  description: "Real-time monitoring and AI-driven security analysis for Neo blockchain smart contracts. Built with SpoonOS agents for autonomous threat detection.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrainsMono.variable} antialiased font-sans`}>
        <nav className="w-full border-b border-primary/20 bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60 sticky top-0 z-50">
          <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 text-xl font-bold hover:text-primary transition-colors">
              <div className="relative">
                <div className="absolute inset-0 bg-primary/10 blur-lg rounded-full"></div>
                <svg className="h-8 w-8 text-primary relative" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                </svg>
              </div>
              <span className="text-foreground tracking-tight">
                Thorax
              </span>
            </Link>
            <div className="flex items-center gap-6 text-sm">
              <Link href="/" className="hover:text-primary transition-colors font-medium">Dashboard</Link>
              <Link href="/how-it-works" className="hover:text-primary transition-colors font-medium">How It Works</Link>
            </div>
          </div>
        </nav>
        {children}
        <footer className="w-full border-t border-primary/20 bg-background mt-12">
          <div className="mx-auto max-w-6xl px-6 py-6 text-center text-sm text-muted-foreground">
            <p>Built for SpoonOS & Neo Hackathon • AI-Powered Smart Contract Security</p>
            <p className="mt-2">Leveraging SpoonOS AI Agents, Neo Blockchain, and Google Gemini</p>
          </div>
        </footer>
        <Toaster />
      </body>
    </html>
  );
}
