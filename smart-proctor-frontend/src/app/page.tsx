import Link from "next/link";
import { ShieldCheck, Lock, Fingerprint, Eye, Server, Zap } from "lucide-react";

export default function LandingPage() {
  return (
      <div className="min-h-screen flex flex-col bg-white">
        {/* ---------------------------------------------------------
          1. NAVIGATION BAR
         --------------------------------------------------------- */}
        <header className="border-b border-gray-100 bg-white/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-bold text-slate-900 tracking-tight">VerifAI</span>
            </div>

            <div className="flex items-center space-x-4">
              <Link
                  href="/login"
                  className="px-5 py-2 text-sm font-medium text-slate-700 hover:text-blue-600 transition-colors"
              >
                Sign In
              </Link>
              <Link
                  href="/register"
                  className="px-5 py-2 text-sm font-medium bg-slate-900 text-white rounded-full hover:bg-slate-800 transition-all shadow-lg shadow-blue-900/20"
              >
                Get Started
              </Link>
            </div>
          </div>
        </header>

        <main className="flex-1">
          {/* ---------------------------------------------------------
            2. HERO SECTION
           --------------------------------------------------------- */}
          <section className="relative pt-32 pb-24 overflow-hidden">
            <div className="max-w-7xl mx-auto px-6 text-center relative z-10">
              <div className="inline-flex items-center space-x-2 bg-blue-50 border border-blue-100 rounded-full px-3 py-1 mb-8">
                <span className="flex h-2 w-2 rounded-full bg-blue-600 animate-pulse"></span>
                <span className="text-xs font-semibold text-blue-700 uppercase tracking-wide">Sovereign-Cloud Ready</span>
              </div>

              <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 tracking-tight mb-6 leading-tight">
                Identity Verification <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                Without the Surveillance.
              </span>
              </h1>

              <p className="text-lg md:text-xl text-slate-600 max-w-2xl mx-auto mb-10 leading-relaxed">
                The world's first proctoring platform powered by <strong>Keystroke DNA™</strong> and
                <strong> Privacy-First Honeypots</strong>. Secure your exams without invading student privacy.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
                <Link
                    href="/login"
                    className="w-full sm:w-auto px-8 py-4 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all shadow-xl shadow-blue-500/30 flex items-center justify-center"
                >
                  Start Proctoring
                  <Zap className="w-4 h-4 ml-2" />
                </Link>
                <Link
                    href="https://github.com/your-repo"
                    target="_blank"
                    className="w-full sm:w-auto px-8 py-4 bg-white text-slate-700 font-bold border border-gray-200 rounded-xl hover:border-gray-300 hover:bg-gray-50 transition-all flex items-center justify-center"
                >
                  View Documentation
                </Link>
              </div>
            </div>

            {/* Background Gradient Blob */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-gradient-to-tr from-blue-100 to-indigo-50 rounded-full blur-3xl -z-10 opacity-60 pointer-events-none" />
          </section>

          {/* ---------------------------------------------------------
            3. FEATURES GRID
           --------------------------------------------------------- */}
          <section className="py-24 bg-slate-50 border-t border-slate-100">
            <div className="max-w-7xl mx-auto px-6">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold text-slate-900 mb-4">Enterprise-Grade Security</h2>
                <p className="text-slate-500">Built for Universities, Certification Bodies, and Government Agencies.</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Feature 1 */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6">
                    <Fingerprint className="w-6 h-6 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">Keystroke DNA™</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Our <strong>Go Bouncer</strong> analyzes typing rhythms in real-time via WebSockets.
                    If a student's typing pattern changes drastically, we flag the session instantly.
                  </p>
                </div>

                {/* Feature 2 */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="w-12 h-12 bg-rose-100 rounded-lg flex items-center justify-center mb-6">
                    <Eye className="w-6 h-6 text-rose-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">Invisible Honeypots</h3>
                  <p className="text-slate-600 leading-relaxed">
                    We inject hidden DOM elements that only bots can see. If a script tries to
                    auto-fill the exam, our <strong>Python Brain</strong> catches it immediately.
                  </p>
                </div>

                {/* Feature 3 */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                  <div className="w-12 h-12 bg-emerald-100 rounded-lg flex items-center justify-center mb-6">
                    <Server className="w-6 h-6 text-emerald-600" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 mb-3">Data Sovereignty</h3>
                  <p className="text-slate-600 leading-relaxed">
                    Self-hostable via Docker. Your student data never leaves your VPC.
                    Compliant with GDPR, FERPA, and ISO 27001 standards.
                  </p>
                </div>
              </div>
            </div>
          </section>
        </main>

        {/* ---------------------------------------------------------
          4. FOOTER
         --------------------------------------------------------- */}
        <footer className="bg-white border-t border-gray-100 py-12">
          <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Lock className="w-5 h-5 text-gray-400" />
              <span className="text-sm font-semibold text-gray-500">Secured by VerifAI</span>
            </div>
            <p className="text-sm text-gray-400">
              © {new Date().getFullYear()} VerifAI Inc. All rights reserved.
            </p>
          </div>
        </footer>
      </div>
  );
}