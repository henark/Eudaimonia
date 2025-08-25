const { withParaglide } = require("@inlang/paraglide-js-adapter-next/plugin");

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
};

module.exports = withParaglide(nextConfig);
