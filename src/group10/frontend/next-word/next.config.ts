import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  "output": "export",
  async rewrites() {
    return [
      {
        "source": '/group10/signup',
        "destination": '/signup',
      },
      {
        "source": '/group10/login',
        "destination": '/login',
      },
      {
        "source": '/group10/',
        "destination": '/',
      },
    ];
  },

};

export default nextConfig;
