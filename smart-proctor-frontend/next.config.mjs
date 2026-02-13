/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    // We strictly avoid 'output: export' here because we need the Node.js server
    // for our secure proxying and API routes to work correctly.
};

export default nextConfig;