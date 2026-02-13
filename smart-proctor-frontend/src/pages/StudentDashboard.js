import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function StudentDashboard() {
    const [profile, setProfile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        // Fetch User Profile to check "Keystroke DNA"
        axios.get('http://localhost:8000/api/v1/users/me', {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then(res => setProfile(res.data))
            .catch(() => navigate('/login'));
    }, [navigate]);

    if (!profile) return <div>Loading Identity...</div>;

    const hasBiometrics = profile.typing_baseline && profile.typing_baseline > 0;

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <h1>Student Identity Center</h1>

            {/* IDENTITY CARD */}
            <div style={{
                border: hasBiometrics ? '2px solid green' : '2px solid orange',
                padding: '1.5rem',
                borderRadius: '8px',
                backgroundColor: hasBiometrics ? '#f0fff4' : '#fffaf0',
                marginBottom: '2rem'
            }}>
                <h2>🛡️ Keystroke DNA Status</h2>
                {hasBiometrics ? (
                    <>
                        <h3 style={{ color: 'green', margin: 0 }}>VERIFIED</h3>
                        <p>Baseline Latency: <strong>{profile.typing_baseline.toFixed(2)}ms</strong></p>
                        <small>Your typing pattern is established. Secure exams are enabled.</small>
                    </>
                ) : (
                    <>
                        <h3 style={{ color: 'orange', margin: 0 }}>CALIBRATION NEEDED</h3>
                        <p>The system needs to learn your typing pattern.</p>
                        <button onClick={() => navigate('/exam/calibration')} style={{ marginTop: '10px' }}>
                            Start Calibration Exam
                        </button>
                    </>
                )}
            </div>

            {/* EXAM LIST */}
            <h3>Available Exams</h3>
            <div className="exam-card" style={{ border: '1px solid #ccc', padding: '1rem', borderRadius: '8px' }}>
                <h4>Distributed Systems Final</h4>
                <button
                    onClick={() => navigate('/exam/1')}
                    style={{
                        backgroundColor: '#2563eb',
                        color: 'white',
                        padding: '0.5rem 1rem',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                >
                    Launch Secure Exam
                </button>
            </div>
        </div>
    );
}

export default StudentDashboard;