import type { Metadata } from "next";
import { Comfortaa, Grand_Hotel, Nunito, Merriweather } from "next/font/google";
import "./globals.css";
import Nav from "@/components/layout/Nav";
import Footer from "@/components/layout/Footer";

const comfortaa = Comfortaa({
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  variable: "--font-comfortaa",
  display: "swap",
});

const grandHotel = Grand_Hotel({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-grand-hotel",
  display: "swap",
});

const merriweather = Merriweather({
  subsets: ["latin"],
  weight: ["300", "400"],
  style: ["normal", "italic"],
  variable: "--font-merriweather",
  display: "swap",
});

const nunito = Nunito({
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  variable: "--font-nunito",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Get Rooted Media | Marion County's Premium Local Media Company",
  description:
    "Two publications serving Marion County. The Closing Table for top-producing real estate agents. The Front Porch for new homeowners. Locally rooted. Professionally grown.",
  openGraph: {
    title: "Get Rooted Media | Marion County's Premium Local Media Company",
    description:
      "Two publications serving Marion County. The Closing Table for top-producing real estate agents. The Front Porch for new homeowners. Locally rooted. Professionally grown.",
    type: "website",
    url: "https://getrootedmedia.com",
    siteName: "Get Rooted Media",
    images: [{ url: "/images/ct-hero.webp" }],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${comfortaa.variable} ${grandHotel.variable} ${merriweather.variable} ${nunito.variable}`}
    >
      <body className="font-nunito bg-grm-cream text-grm-black antialiased">
        <Nav />
        {children}
        <Footer />
      </body>
    </html>
  );
}
