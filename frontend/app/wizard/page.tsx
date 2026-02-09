"use client";
import TripWizard from '@/components/TripWizard';
import { motion } from 'framer-motion';
import VideoBackground from '@/components/VideoBackground';

export default function WizardPage() {
    return (
        <main className="min-h-screen relative overflow-hidden text-white font-sans">
            <VideoBackground />

            <div className="relative z-10 min-h-screen flex flex-col p-6 md:p-8 max-w-400 mx-auto">
                {/* Navbar (Simplified for Wizard flow) */}
                <header className="flex justify-between items-center w-full mb-12">
                        <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-linear-to-tr from-teal-400 to-blue-500 rounded-full"></div>
                        <span className="text-xl font-bold tracking-tight">Trip-Book</span>
                    </div>
                    <a href="/" className="text-sm text-gray-300 hover:text-teal-400 transition-colors">Back to Home</a>
                </header>

                {/* Wizard Content */}
                <div className="flex-1 flex items-center justify-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        className="w-full max-w-md"
                    >
                        <div className="mb-8 text-center">
                            <h1 className="text-4xl md:text-5xl font-bold mb-3 bg-linear-to-r from-teal-200 via-white to-blue-200 bg-clip-text text-transparent">Plan Your Trip</h1>
                            <p className="text-gray-300 text-lg">Tell us your dreams, we'll make them real</p>
                        </div>
                        <TripWizard />
                    </motion.div>
                </div>
            </div>
        </main>
    );
}
