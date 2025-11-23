import Particles from "../components/main/Particles";
import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Game Recommender",
  description: "Game recommendation app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>
        <Particles />
        {children}
      </body>
    </html>
  );
}




