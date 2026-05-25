import type { Metadata } from "next";
import Link from "next/link";
import "../styles/globals.css";

export const metadata: Metadata = {
  title: "StoryGen | Illustrated stories made together",
  description:
    "Create gentle, beautifully illustrated children's stories in real time.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <nav className="nav">
          <Link className="brand" href="/">
            StoryGen
          </Link>
          <Link href="/library">My stories</Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
