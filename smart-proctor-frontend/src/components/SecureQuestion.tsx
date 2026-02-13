'use client';

import React, { useEffect, useRef } from 'react';

interface SecureQuestionProps {
    text: string;
    watermarkId: string;
}

export const SecureQuestion: React.FC<SecureQuestionProps> = ({ text, watermarkId }) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        // High DPI Rendering for Retina Displays
        const dpr = window.devicePixelRatio || 1;
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        ctx.scale(dpr, dpr);

        // Text Config
        ctx.font = '16px Inter, sans-serif';
        ctx.fillStyle = '#1e293b'; // Slate-800
        ctx.textBaseline = 'top';

        // Word Wrap Logic
        const words = text.split(' ');
        let line = '';
        let y = 20;
        const lineHeight = 28;
        const maxWidth = rect.width - 40;

        for (let n = 0; n < words.length; n++) {
            const testLine = line + words[n] + ' ';
            const metrics = ctx.measureText(testLine);
            if (metrics.width > maxWidth && n > 0) {
                ctx.fillText(line, 20, y);
                line = words[n] + ' ';
                y += lineHeight;
            } else {
                line = testLine;
            }
        }
        ctx.fillText(line, 20, y);

        // Security: Invisible Noise (Watermark)
        ctx.fillStyle = 'rgba(0,0,0,0.03)';
        ctx.font = '10px monospace';
        for(let i=0; i<5; i++) {
            ctx.fillText(`ID:${watermarkId}`, Math.random()*rect.width, Math.random()*rect.height);
        }

    }, [text, watermarkId]);

    return (
        <div className="w-full bg-white rounded-xl shadow-sm border border-gray-200 p-1 select-none">
            <div className="bg-gray-50 px-4 py-2 border-b border-gray-100 rounded-t-xl flex justify-between items-center">
                <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">Secure View</span>
                <span className="text-xs text-green-600 font-mono">Protected</span>
            </div>
            <canvas ref={canvasRef} className="w-full h-48 cursor-default" />
        </div>
    );
};