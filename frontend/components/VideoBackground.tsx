"use client";
import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const videos = [
    '/videos/background.mp4',
    '/videos/background 2.mp4',
    '/videos/background 3.mp4',
    '/videos/background 4.mp4',
    '/videos/background 5.mp4',
    '/videos/backgorund 6.mp4'
];

export default function VideoBackground() {
    const [currentVideo, setCurrentVideo] = useState(0);

    const handleVideoEnd = () => {
        setCurrentVideo((prev) => (prev + 1) % videos.length);
    };

    return (
        <div className="fixed inset-0 z-[-1] overflow-hidden bg-black">
            <AnimatePresence mode="popLayout">
                <motion.div
                    key={currentVideo}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 1.5 }}
                    className="absolute inset-0 w-full h-full"
                >
                    <video
                        autoPlay
                        muted
                        loop={false} // We handle looping manually via onEnded
                        playsInline
                        className="object-cover w-full h-full opacity-60" // Reduced opacity for readability
                        onEnded={handleVideoEnd}
                        src={videos[currentVideo]}
                    />
                </motion.div>
            </AnimatePresence>
            {/* Overlay gradient to ensure text readability */}
            <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/60 pointer-events-none" />
        </div>
    );
}
