"use client";
import dynamic from 'next/dynamic';
import { motion } from 'framer-motion';
import Link from 'next/link';

// Dynamically import Scene3D with no SSR (canvas needs window)
const Scene3D = dynamic(() => import('@/components/Scene3D'), { ssr: false });

export default function Home() {
  return (
    <main className="min-h-screen relative overflow-hidden bg-[#0b1121] text-white selection:bg-amber-500/30 font-sans">

      {/* 3D Background */}
      <div className="absolute inset-0 z-0">
        <Scene3D />
      </div>

      <div className="relative z-10 min-h-screen flex flex-col p-6 md:p-8 max-w-[1600px] mx-auto pointer-events-none">

        {/* Navbar */}
        <header className="flex justify-between items-center w-full pointer-events-auto mb-10 md:mb-20">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-tr from-amber-400 to-orange-600 rounded-full"></div>
            <span className="text-xl font-bold tracking-tight">Trip-Book</span>
          </div>

          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-300">
            <a href="#" className="hover:text-white transition-colors">Home</a>
            <a href="#" className="hover:text-white transition-colors">Destinations</a>
            <a href="#" className="hover:text-white transition-colors">About</a>

          </nav>
        </header>

        {/* Main Landing Content */}
        <div className="flex-1 flex flex-col items-center justify-center text-center pb-20 pointer-events-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl flex flex-col items-center"
          >



            <div>
              <Link href="/wizard">
                <button className="group relative px-8 py-4 bg-teal-500 hover:bg-teal-400 text-black font-bold rounded-full text-lg transition-all transform hover:scale-105 shadow-[0_0_40px_rgba(20,184,166,0.5)]">
                  <span className="relative z-10 flex items-center gap-2">
                    Plan Your Journey
                    <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
                  </span>
                </button>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Footer Line */}
        <div className="absolute bottom-10 left-0 right-0 flex justify-center pointer-events-auto">
          <p className="text-gray-400 font-mono text-lg tracking-widest uppercase opacity-80">
            One platform. Global travel. Total control.
          </p>
        </div>

      </div>
    </main>
  );
}
