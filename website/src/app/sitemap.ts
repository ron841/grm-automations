import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  const base = "https://getrootedmedia.com";
  const lastModified = new Date();
  return [
    { url: `${base}/`, lastModified, changeFrequency: "weekly", priority: 1.0 },
    { url: `${base}/web`, lastModified, changeFrequency: "monthly", priority: 0.9 },
    { url: `${base}/the-closing-table`, lastModified, changeFrequency: "monthly", priority: 0.8 },
    { url: `${base}/the-front-porch`, lastModified, changeFrequency: "monthly", priority: 0.8 },
    { url: `${base}/about`, lastModified, changeFrequency: "yearly", priority: 0.5 },
    { url: `${base}/contact`, lastModified, changeFrequency: "yearly", priority: 0.5 },
  ];
}
