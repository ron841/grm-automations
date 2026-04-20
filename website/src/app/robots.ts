import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "GPTBot", allow: "/" },
      { userAgent: "ClaudeBot", allow: "/" },
      { userAgent: "Claude-SearchBot", allow: "/" },
      { userAgent: "PerplexityBot", allow: "/" },
      { userAgent: "Bingbot", allow: "/" },
      { userAgent: "Googlebot", allow: "/" },
      { userAgent: "*", allow: "/" },
    ],
    sitemap: "https://getrootedmedia.com/sitemap.xml",
  };
}
