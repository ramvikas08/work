import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Technical Recruiter",
  description: "Generate Technical Talent Scorecards from GitHub URLs"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
