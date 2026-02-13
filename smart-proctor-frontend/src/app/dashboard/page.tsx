'use client';

import { useEffect, useState } from 'react';

export default function Dashboard() {
    const [profile, setProfile] = useState<any>(null);

    useEffect(() => {
        // Fetch User Profile to check "Keystroke DNA" status
        const token = localStorage.getItem('token');
        if(!token) window.location.href = '/login';

        fetch('http://localhost:8000/api/v1/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        })
            .then(res => res.json())
            .then(data => setProfile(data));
    }, []);

    if (!profile) return <div className="p-8">Loading Identity Profile...</div>;

    // LOGIC: Does the user have a typing baseline?
    // Note: We added 'typing_baseline' to the backend model, ensure it's in the UserSchema response!
    const hasBiometrics = profile.typing_baseline !== null && profile.typing_baseline > 0;

    return (
        <div className="max-w-4xl mx-auto p-8">
            <h1 className="text-3xl font-bold mb-8">Student Identity Center</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">

                {/* CARD 1: BIOMETRIC STATUS */}
                <div className={`p-6 rounded-xl border-2 ${
                    hasBiometrics ? 'border-green-500 bg-green-50' : 'border-yellow-500 bg-yellow-50'
                }`}>
                    <h2 className="text-xl font-bold mb-2">🛡️ Keystroke DNA</h2>
                    {hasBiometrics ? (
                        <div>
                            <p className="text-green-800 font-bold text-lg">VERIFIED</p>
                            <p className="text-sm text-green-700 mt-1">
                                Baseline: {profile.typing_baseline?.toFixed(2)}ms latency
                            </p>
                            <p className="text-xs text-green-600 mt-2">
                                Your typing pattern is established. You can take exams securely.
                            </p>
                        </div>
                    ) : (
                        <div>
                            <p className="text-yellow-800 font-bold text-lg">CALIBRATION NEEDED</p>
                            <p className="text-sm text-yellow-700 mt-1">
                                System is learning your pattern.
                            </p>
                            <p className="text-xs text-yellow-600 mt-2">
                                Please take the "Calibration Exam" or complete your first test to establish identity.
                            </p>
                        </div>
                    )}
                </div>

                {/* CARD 2: TRUST SCORE (Placeholder for Integrity Logs) */}
                <div className="p-6 rounded-xl border border-gray-200 bg-white shadow-sm">
                    <h2 className="text-xl font-bold mb-2">⚖️ Trust Score</h2>
                    <div className="text-4xl font-bold text-blue-600">100%</div>
                    <p className="text-gray-500 text-sm mt-2">No violations detected in last 30 days.</p>
                </div>
            </div>

            {/* EXAM LIST */}
            <h3 className="text-xl font-bold mb-4">Pending Exams</h3>
            <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
                <div className="p-4 border-b hover:bg-gray-50 flex justify-between items-center">
                    <div>
                        <p className="font-bold">Distributed Systems Final</p>
                        <p className="text-sm text-gray-500">Duration: 60 mins</p>
                    </div>
                    <a
                        href="/exam/1"
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
                    >
                        Launch Exam
                    </a>
                </div>
            </div>
        </div>
    );
}