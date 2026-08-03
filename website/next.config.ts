import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      { source: "/web", destination: "/the-storefront", permanent: true },
      // Canonical host: 301 www to apex so search engines index one site
      {
        source: "/:path*",
        has: [{ type: "host", value: "www.getrootedmedia.com" }],
        destination: "https://getrootedmedia.com/:path*",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
