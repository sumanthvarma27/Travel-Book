"use strict";
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Float, Text, Sparkles } from '@react-three/drei';
import { useRef, useState, Suspense, useMemo } from 'react';
import * as THREE from 'three';

function Earth() {
    const earthRef = useRef<THREE.Group>(null);
    const [hovered, setHover] = useState(false);

    // Create procedural earth-like texture
    const earthTexture = useMemo(() => {
        const canvas = document.createElement('canvas');
        canvas.width = 1024;
        canvas.height = 512;
        const ctx = canvas.getContext('2d')!;

        // Ocean blue gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 512);
        gradient.addColorStop(0, '#1e3a8a');
        gradient.addColorStop(0.5, '#0ea5e9');
        gradient.addColorStop(1, '#1e3a8a');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, 1024, 512);

        // Add land masses (procedural)
        ctx.fillStyle = '#22c55e';
        for (let i = 0; i < 50; i++) {
            const x = Math.random() * 1024;
            const y = Math.random() * 512;
            const size = Math.random() * 100 + 50;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }

        // Add some green tones
        ctx.fillStyle = '#15803d';
        for (let i = 0; i < 30; i++) {
            const x = Math.random() * 1024;
            const y = Math.random() * 512;
            const size = Math.random() * 60 + 30;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        }

        const texture = new THREE.CanvasTexture(canvas);
        texture.needsUpdate = true;
        return texture;
    }, []);

    useFrame((state, delta) => {
        if (earthRef.current) {
            earthRef.current.rotation.y += delta * (hovered ? 0.15 : 0.05);
        }
    });

    return (
        <group
            ref={earthRef}
            onPointerOver={() => { document.body.style.cursor = 'pointer'; setHover(true); }}
            onPointerOut={() => { document.body.style.cursor = 'auto'; setHover(false); }}
            scale={hovered ? 1.02 : 1}
        >
            {/* Main Earth Sphere with Procedural Texture */}
            <mesh>
                <sphereGeometry args={[1.6, 32, 32]} />
                <meshStandardMaterial
                    map={earthTexture}
                    roughness={0.7}
                    metalness={0.1}
                />
            </mesh>

            {/* Thin wireframe overlay */}
            <mesh scale={1.005}>
                <sphereGeometry args={[1.6, 32, 32]} />
                <meshStandardMaterial
                    color="#2dd4bf"
                    wireframe
                    transparent
                    opacity={0.05}
                />
            </mesh>

            {/* Atmosphere Glow */}
            <mesh scale={1.15}>
                <sphereGeometry args={[1.6, 32, 32]} />
                <meshStandardMaterial
                    color="#60a5fa"
                    transparent
                    opacity={0.12}
                    side={THREE.BackSide}
                    blending={THREE.AdditiveBlending}
                />
            </mesh>
        </group>
    );
}

function LoadingFallback() {
    return (
        <mesh>
            <sphereGeometry args={[1.6, 16, 16]} />
            <meshStandardMaterial color="#1e3a8a" wireframe />
        </mesh>
    );
}

function OrbitalRings() {
    return (
        <group rotation={[Math.PI / 3, 0, 0]}>
            {/* Inner Ring */}
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
                <ringGeometry args={[2.2, 2.22, 64]} />
                <meshBasicMaterial color="#5eead4" side={THREE.DoubleSide} transparent opacity={0.6} blending={THREE.AdditiveBlending} />
            </mesh>

            {/* Outer Ring */}
            <mesh rotation={[-Math.PI / 2, 0, 0]}>
                <ringGeometry args={[2.8, 2.82, 64]} />
                <meshBasicMaterial color="#2dd4bf" side={THREE.DoubleSide} transparent opacity={0.4} blending={THREE.AdditiveBlending} />
            </mesh>

            {/* Orbiting Text 1 */}
            <group rotation={[0, 0, 0]}>
                <Text
                    position={[2.5, 0, 0]}
                    rotation={[-Math.PI / 2, 0, -Math.PI / 2]}
                    fontSize={0.15}
                    color="#ccfbf1"
                    font="https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff"
                    anchorX="center"
                    anchorY="middle"
                >
                    DESIGN YOUR JOURNEY
                </Text>
            </group>

            {/* Orbiting Text 2 */}
            <group rotation={[0, Math.PI, 0]}>
                <Text
                    position={[3.1, 0, 0]}
                    rotation={[-Math.PI / 2, 0, -Math.PI / 2]}
                    fontSize={0.25}
                    fontWeight={800}
                    color="#ffffff"
                    font="https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff"
                    anchorX="center"
                    anchorY="middle"
                    letterSpacing={0.1}
                >
                    TRIP-BOOK
                </Text>
            </group>
        </group>
    );
}

function ConnectionPaths() {
    const count = 8;
    const radius = 1.6;

    const lines = useMemo(() => {
        const curves = [];
        for (let i = 0; i < count; i++) {
            const phi1 = Math.random() * Math.PI * 2;
            const theta1 = Math.random() * Math.PI;
            const phi2 = Math.random() * Math.PI * 2;
            const theta2 = Math.random() * Math.PI;
            const start = new THREE.Vector3().setFromSphericalCoords(radius, theta1, phi1);
            const end = new THREE.Vector3().setFromSphericalCoords(radius, theta2, phi2);
            const mid = start.clone().add(end).multiplyScalar(0.5).normalize().multiplyScalar(radius * 1.4);
            const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
            curves.push(curve);
        }
        return curves;
    }, []);

    return (
        <group>
            {lines.map((curve, i) => (
                <mesh key={i}>
                    <tubeGeometry args={[curve, 32, 0.003, 8, false]} />
                    <meshBasicMaterial color="#fbbf24" transparent opacity={0.6} blending={THREE.AdditiveBlending} />
                </mesh>
            ))}
        </group>
    );
}

function CityMarkers() {
    // City positions on the globe (approximate spherical coordinates)
    // Format: {name, theta (latitude-ish), phi (longitude-ish), color}
    const cities = [
        { name: "London", theta: Math.PI / 2.2, phi: 0, color: "#5eead4" },
        { name: "New York", theta: Math.PI / 2.5, phi: -1.2, color: "#60a5fa" },
        { name: "Tokyo", theta: Math.PI / 2.8, phi: 2.3, color: "#f59e0b" },
    ];

    const radius = 1.65;

    return (
        <group>
            {cities.map((city, i) => {
                const position = new THREE.Vector3().setFromSphericalCoords(radius, city.theta, city.phi);

                return (
                    <group key={i} position={position.toArray()}>
                        {/* Glowing marker point */}
                        <mesh>
                            <sphereGeometry args={[0.03, 16, 16]} />
                            <meshBasicMaterial color={city.color} />
                        </mesh>

                        {/* Pulsing ring */}
                        <Float speed={2} floatIntensity={0.3}>
                            <mesh rotation={[-Math.PI / 2, 0, 0]}>
                                <ringGeometry args={[0.04, 0.06, 32]} />
                                <meshBasicMaterial
                                    color={city.color}
                                    transparent
                                    opacity={0.6}
                                    side={THREE.DoubleSide}
                                    blending={THREE.AdditiveBlending}
                                />
                            </mesh>
                        </Float>

                        {/* City label */}
                        <Text
                            position={[0, 0.12, 0]}
                            fontSize={0.08}
                            color="white"
                            anchorX="center"
                            anchorY="middle"
                            outlineWidth={0.01}
                            outlineColor="#000000"
                            font="https://fonts.gstatic.com/s/inter/v12/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hjp-Ek-_EeA.woff"
                        >
                            {city.name}
                        </Text>
                    </group>
                );
            })}
        </group>
    );
}

export default function Scene3D() {
    return (
        <div className="absolute inset-0 z-0 bg-[#0b1121]">
            <Suspense fallback={<div className="w-full h-full flex items-center justify-center text-white">Loading Globe...</div>}>
                <Canvas
                    camera={{ position: [2, 1, 6], fov: 40 }}
                    gl={{ antialias: true, alpha: true }}
                    dpr={[1, 1.5]}
                >
                    <fog attach="fog" args={['#0b1121', 5, 15]} />
                    <ambientLight intensity={0.3} />
                    <pointLight position={[10, 5, 10]} intensity={0.8} color="#2dd4bf" />
                    <spotLight position={[-5, 5, -5]} angle={0.5} penumbra={1} intensity={1.5} color="#3b82f6" />

                    <Stars radius={100} depth={50} count={3000} factor={4} saturation={0} fade speed={0.5} />
                    <Sparkles count={80} scale={6} size={3} speed={0.2} opacity={0.4} color="#5eead4" />

                    <Float speed={1} rotationIntensity={0.2} floatIntensity={0.2}>
                        <group position={[1.5, 0, 0]}> {/* Shift planet to the right */}
                            <Suspense fallback={<LoadingFallback />}>
                                <Earth />
                            </Suspense>

                            {/* Animated Ring System */}
                            <group rotation={[0, 0, 0.2]}>
                                <OrbitalRings />
                            </group>

                            <ConnectionPaths />

                            {/* City Markers */}
                            <CityMarkers />
                        </group>
                    </Float>

                    <OrbitControls
                        enableZoom={false}
                        enablePan={false}
                        autoRotate={true}
                        autoRotateSpeed={0.5}
                        maxPolarAngle={Math.PI / 1.5}
                        minPolarAngle={Math.PI / 3}
                    />
                </Canvas>
            </Suspense>

            {/* Cinematic Vignette */}
            <div className="absolute inset-0 bg-radial-gradient from-transparent via-[#0b1121]/40 to-[#0b1121]/90 pointer-events-none"></div>
        </div>
    );
}
