import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      { source: "/web", destination: "/the-storefront", permanent: true },
    ];
  },
};

export default nextConfig;
