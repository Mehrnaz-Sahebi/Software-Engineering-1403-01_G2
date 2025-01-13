import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  "output": "export",
  "assetPrefix": "/group10",
  async rewrites() {
    return [
      {
        "source": '/group10/signup.html',
        "destination": '/signup',
      },
      {
        "source": '/group10/login.html',
        "destination": '/login',
      },
      {
        "source": '/group10/index.html',
        "destination": '/',
      },
    ];
  },
};

export default nextConfig;
