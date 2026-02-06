"use client";
import { useState, useRef } from 'react';
import { TripPlan } from '@/lib/types';
import { motion, AnimatePresence } from 'framer-motion';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export default function TripResults({ plan }: { plan: TripPlan }) {
    const [activeTab, setActiveTab] = useState<'itinerary' | 'budget' | 'packing'>('itinerary');
    const contentRef = useRef<HTMLDivElement>(null);

    const handlePrint = async () => {
        if (!contentRef.current) return;
        const canvas = await html2canvas(contentRef.current);
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('trip-plan.pdf');
    };

    const downloadJSON = () => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(plan, null, 2));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", "trip-plan.json");
        document.body.appendChild(downloadAnchorNode);
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    };

    const icons = [
        { id: 'places', label: 'Places to Visit', icon: '/assets/icons/attractions.png', tab: 'itinerary', color: 'from-purple-500 to-indigo-500' },
        { id: 'flights', label: 'Flight Tickets', icon: '/assets/icons/flight.png', tab: 'budget', color: 'from-blue-500 to-cyan-500' },
        { id: 'hotels', label: 'Accommodation', icon: '/assets/icons/hotel.png', tab: 'budget', color: 'from-orange-500 to-amber-500' },
        { id: 'commute', label: 'Commute Services', icon: '/assets/icons/transport.png', tab: 'budget', color: 'from-emerald-500 to-teal-500' },
        { id: 'weather', label: 'Weather', icon: '/assets/icons/weather.png', tab: 'itinerary', color: 'from-yellow-400 to-orange-400' },
        { id: 'packing', label: 'Packing List', icon: '/assets/icons/checklist.png', tab: 'packing', color: 'from-pink-500 to-rose-500' },
    ];

    return (
        <div className="min-h-screen text-white p-4 md:p-8" ref={contentRef}>
            {/* Header / Title */}
            <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                className="max-w-7xl mx-auto mb-10 flex flex-col md:flex-row justify-between items-center gap-4"
            >
                <div>
                    <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-teal-200 via-white to-blue-200 bg-clip-text text-transparent">
                        Your Journey to {plan.itinerary?.[0]?.city || 'Paradise'}
                    </h1>
                    <p className="text-gray-400 mt-2 text-lg max-w-2xl">{plan.summary}</p>
                </div>
                <div className="flex gap-3">
                    <button onClick={handlePrint} className="px-5 py-2 bg-white/5 border border-white/10 rounded-full hover:bg-white/10 transition flex items-center gap-2">
                        <span>🖨️</span> Print Itinerary
                    </button>
                    <button onClick={downloadJSON} className="px-5 py-2 bg-teal-500/10 border border-teal-500/20 text-teal-300 rounded-full hover:bg-teal-500/20 transition flex items-center gap-2">
                        <span>💾</span> Export JSON
                    </button>
                </div>
            </motion.div>

            {/* 3D Icon Menu */}
            <div className="max-w-7xl mx-auto mb-12">
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                    {icons.map((item, index) => (
                        <motion.div
                            key={item.id}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -10, scale: 1.05 }}
                            onClick={() => setActiveTab(item.tab as any)}
                            className={`
                                relative cursor-pointer group rounded-3xl p-4 flex flex-col items-center justify-center gap-4
                                bg-gradient-to-br bg-white/5 border border-white/5 backdrop-blur-sm
                                hover:bg-white/10 hover:border-white/20 transition-all duration-300
                                ${activeTab === item.tab ? 'ring-2 ring-teal-500/50 bg-white/10' : ''}
                            `}
                        >
                            {/* Floating 3D Icon */}
                            <motion.div
                                animate={{ y: [0, -8, 0] }}
                                transition={{ repeat: Infinity, duration: 3 + index, ease: "easeInOut" }}
                                className="relative w-24 h-24 md:w-28 md:h-28 filter drop-shadow-[0_10px_10px_rgba(0,0,0,0.5)]"
                            >
                                <img
                                    src={item.icon}
                                    alt={item.label}
                                    className="w-full h-full object-contain"
                                />
                            </motion.div>

                            {/* Label */}
                            <div className="text-center z-10 relative">
                                <h3 className="text-sm font-bold text-gray-200 group-hover:text-white tracking-wide">{item.label}</h3>
                                <div className="h-0.5 w-0 group-hover:w-full bg-teal-400 transition-all duration-300 mt-1 mx-auto"></div>
                            </div>

                            {/* Glow Effect */}
                            <div className={`absolute inset-0 rounded-3xl bg-gradient-to-br ${item.color} opacity-0 group-hover:opacity-10 blur-2xl transition-opacity duration-500`}></div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Tab Content Display */}
            <div className="max-w-7xl mx-auto bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 min-h-[500px]">
                <AnimatePresence mode="wait">
                    {activeTab === 'itinerary' && (
                        <motion.div
                            key="itinerary"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-2xl font-bold text-white">📅 Daily Itinerary</h2>
                                <div className="text-sm text-gray-400">Detailed breakdown of your trip</div>
                            </div>

                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {(plan.itinerary || []).map((day) => (
                                    <div key={day.day_number} className="bg-white/5 border border-white/5 rounded-2xl p-6 hover:border-teal-500/30 transition-colors">
                                        <div className="flex justify-between items-center mb-4 pb-4 border-b border-white/5">
                                            <h3 className="text-xl font-bold text-teal-300">Day {day.day_number}</h3>
                                            <span className="text-sm bg-white/10 px-3 py-1 rounded-full text-gray-300">{day.date}</span>
                                        </div>

                                        {/* Weather Widget Mini */}
                                        {day.weather ? (
                                            <div className="flex items-center gap-3 mb-6 bg-blue-500/10 p-3 rounded-xl border border-blue-500/10">
                                                <span className="text-2xl">⛅</span>
                                                <div>
                                                    <div className="text-sm font-semibold text-blue-200">{day.weather.temperature_c}°C</div>
                                                    <div className="text-xs text-blue-300/70">{day.weather.condition}</div>
                                                </div>
                                            </div>
                                        ) : (
                                            <div className="flex items-center gap-3 mb-6 bg-white/5 p-3 rounded-xl border border-white/5">
                                                <span className="text-xl">📅</span>
                                                <div>
                                                    <div className="text-sm font-semibold text-gray-400">Forecast Pending</div>
                                                </div>
                                            </div>
                                        )}

                                        <div className="space-y-6">
                                            {[...(day.morning_activities || []), ...(day.afternoon_activities || []), ...(day.evening_activities || [])].map((activity, i) => (
                                                <div key={i} className="relative pl-6 border-l-2 border-white/10 hover:border-teal-500/50 transition-colors">
                                                    <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-slate-900 border-2 border-teal-500"></div>
                                                    <div className="mb-1 text-xs font-mono text-teal-400 uppercase tracking-widest">{activity.time_slot}</div>
                                                    <h4 className="font-semibold text-lg text-white">{activity.name}</h4>
                                                    <p className="text-sm text-gray-400 mb-2">{activity.description}</p>
                                                    <div className="flex items-center gap-4 text-xs text-gray-500">
                                                        <span>📍 {activity.location}</span>
                                                        <span>💰 ${activity.estimated_cost}</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    )}

                    {activeTab === 'budget' && (
                        <motion.div
                            key="budget"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">💰 Smart Budget & Bookings</h2>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                                <div className="bg-gradient-to-br from-emerald-900/50 to-emerald-800/20 border border-emerald-500/20 p-6 rounded-2xl">
                                    <div className="text-emerald-400 text-sm font-semibold uppercase tracking-wider mb-2">Total Estimated</div>
                                    <div className="text-4xl font-bold text-white">${plan.budget?.total_estimated || 0}</div>
                                    <div className="text-emerald-400/60 text-xs mt-1">Inclusive of all logistics</div>
                                </div>
                                <div className="col-span-2 bg-white/5 border border-white/10 p-6 rounded-2xl flex items-center gap-8 overflow-x-auto">
                                    <div className="flex-1 min-w-[150px]">
                                        <div className="text-gray-400 text-xs mb-1">Flights</div>
                                        <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden">
                                            <div className="h-full bg-blue-500 w-[60%]"></div>
                                        </div>
                                        <div className="text-white font-mono mt-1">${plan.budget?.flights || 0}</div>
                                    </div>
                                    <div className="flex-1 min-w-[150px]">
                                        <div className="text-gray-400 text-xs mb-1">Stay</div>
                                        <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden">
                                            <div className="h-full bg-orange-500 w-[40%]"></div>
                                        </div>
                                        <div className="text-white font-mono mt-1">${plan.budget?.accommodation || 0}</div>
                                    </div>
                                    <div className="flex-1 min-w-[150px]">
                                        <div className="text-gray-400 text-xs mb-1">Food & Fun</div>
                                        <div className="h-2 w-full bg-slate-700 rounded-full overflow-hidden">
                                            <div className="h-full bg-purple-500 w-[70%]"></div>
                                        </div>
                                        <div className="text-white font-mono mt-1">${(plan.budget?.food || 0) + (plan.budget?.activities || 0)}</div>
                                    </div>
                                </div>
                            </div>

                            <h3 className="text-xl font-bold text-white mb-4">Recommended Hotels</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {(plan.hotels_shortlist || []).map((hotel, i) => (
                                    <div key={i} className="group bg-slate-800/50 p-4 rounded-xl border border-white/5 hover:border-white/20 transition-all">
                                        <div className="h-32 bg-slate-700 rounded-lg mb-4 overflow-hidden relative">
                                            {/* Placeholder image if not live */}
                                            <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent"></div>
                                            <div className="absolute bottom-2 left-2 text-white font-bold">{hotel.name}</div>
                                        </div>
                                        <div className="flex justify-between items-center mb-2">
                                            <div className="text-yellow-400 text-sm">★ {hotel.rating}</div>
                                            <div className="text-teal-300 font-bold">${hotel.price_per_night}<span className="text-gray-500 text-xs font-normal">/night</span></div>
                                        </div>
                                        <p className="text-gray-400 text-xs mb-4 line-clamp-2">{hotel.description}</p>
                                        <a href={hotel.booking_link} target="_blank" className="block w-full py-2 bg-blue-600 hover:bg-blue-500 text-white text-center rounded-lg text-xs font-bold transition-colors">
                                            Check Availability
                                        </a>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    )}

                    {activeTab === 'packing' && (
                        <motion.div
                            key="packing"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                        >
                            <h2 className="text-2xl font-bold text-white mb-6">🎒 Smart Packing List</h2>
                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                                {(plan.packing_list || []).map((item, i) => (
                                    <div key={i} className="flex items-center gap-3 p-3 bg-white/5 rounded-xl border border-white/5 hover:bg-white/10 transition">
                                        <input type="checkbox" className="w-5 h-5 rounded border-gray-600 text-teal-500 focus:ring-teal-500 bg-slate-800" />
                                        <div>
                                            <div className="text-white font-medium">{item.item}</div>
                                            <div className="text-xs text-gray-500">{item.category}</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
