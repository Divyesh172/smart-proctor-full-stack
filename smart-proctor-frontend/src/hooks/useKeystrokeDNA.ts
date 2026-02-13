import { useEffect, useRef, useState } from 'react';

const BOUNCER_URL = process.env.NEXT_PUBLIC_BOUNCER_URL || 'ws://localhost:8080/ws';

export function useKeystrokeDNA(studentId: string, token: string) {
    const ws = useRef<WebSocket | null>(null);
    const lastKeyDown = useRef<number>(0);
    const [status, setStatus] = useState('disconnected');

    useEffect(() => {
        if (!token) return;

        // 1. Connect to Go Bouncer
        ws.current = new WebSocket(`${BOUNCER_URL}?token=${token}`);

        ws.current.onopen = () => setStatus('secure');
        ws.current.onclose = () => setStatus('disconnected');

        // 2. Handle "Red Screen" Alerts from Bouncer
        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.status === 'TERMINATE') {
                alert(`SECURITY VIOLATION: ${data.message}`);
                window.location.href = '/dashboard'; // Kick user out
            }
        };

        return () => ws.current?.close();
    }, [token]);

    const handleKeyDown = (e: React.KeyboardEvent | KeyboardEvent) => {
        const now = performance.now();

        // Calculate Flight Time (Time since last key press)
        let flightTime = 0;
        if (lastKeyDown.current > 0) {
            flightTime = now - lastKeyDown.current;
        }
        lastKeyDown.current = now;

        // 3. Stream Biometrics (Only if meaningful)
        if (ws.current?.readyState === WebSocket.OPEN && flightTime > 0) {
            ws.current.send(JSON.stringify({
                student_id: studentId,
                flight_time: flightTime,
                dwell_time: 0 // We can add dwell logic later
            }));
        }
    };

    return { handleKeyDown, status };
}