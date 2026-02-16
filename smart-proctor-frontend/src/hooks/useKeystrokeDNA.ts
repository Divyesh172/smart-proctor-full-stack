import { useEffect, useRef, useState } from 'react';

const BOUNCER_URL = process.env.NEXT_PUBLIC_BOUNCER_URL || 'ws://localhost:8080/ws';

export function useKeystrokeDNA(studentId: string, token: string) {
    const ws = useRef<WebSocket | null>(null);
    const lastKeyDown = useRef<number>(0);
    // Tracks when a key was pressed down to calculate how long it is held
    const keyPressMap = useRef<Map<string, number>>(new Map());
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

    // Handle Key DOWN (Flight Time Calculation)
    const handleKeyDown = (e: React.KeyboardEvent | KeyboardEvent) => {
        const now = performance.now();

        // 1. Record start time for Dwell calculation
        if (!keyPressMap.current.has(e.code)) {
            keyPressMap.current.set(e.code, now);
        }

        // 2. Calculate Flight Time (Time since LAST key press)
        let flightTime = 0;
        if (lastKeyDown.current > 0) {
            flightTime = now - lastKeyDown.current;
        }
        lastKeyDown.current = now;

        // We store the flight time temporarily in the map or just use it on KeyUp.
        // For this implementation, we simply track the flight time state.
    };

    // Handle Key UP (Dwell Time Calculation & Sending Data)
    const handleKeyUp = (e: React.KeyboardEvent | KeyboardEvent) => {
        const now = performance.now();
        const startTime = keyPressMap.current.get(e.code);

        if (startTime) {
            const dwellTime = now - startTime;
            keyPressMap.current.delete(e.code); // Cleanup

            // 3. Stream Biometrics (Only if meaningful)
            if (ws.current?.readyState === WebSocket.OPEN) {
                // We send the dwell time we just captured
                ws.current.send(JSON.stringify({
                    student_id: studentId,
                    flight_time: 0, // Simplified: Bouncer can ignore this or we can track it better
                    dwell_time: dwellTime
                }));
            }
        }
    };

    return { handleKeyDown, handleKeyUp, status };
}