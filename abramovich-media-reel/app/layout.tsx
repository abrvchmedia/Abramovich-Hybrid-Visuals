import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Abramovich Media Producing Reel",
  description: "Quality cinematography and commercial production for streaming platforms",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
