import type { Metadata } from "next";
import SwitchHeader from "@/components/switchheader/SwitchHeader";
import "./globals.css";

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
        {/* <Particles /> */}
        <div className="background">
          <SwitchHeader />
          <div className="top-margin">{children}</div>
        </div>
      </body>
    </html>
  );
}




