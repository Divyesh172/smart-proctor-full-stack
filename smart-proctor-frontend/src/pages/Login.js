import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            // 1. Get Token from Python Backend
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const res = await axios.post('http://localhost:8000/api/v1/auth/login', formData);

            // 2. CRITICAL: Save Token for Bouncer
            localStorage.setItem('token', res.data.access_token);

            // 3. Redirect to Identity Dashboard
            navigate('/dashboard');
        } catch (err) {
            alert('Login Failed: ' + (err.response?.data?.detail || err.message));
        }
    };

    return (
        <div className="login-container">
            <h1>VerifAI Login</h1>
            <form onSubmit={handleLogin}>
                <input
                    type="email"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Authenticate</button>
            </form>
        </div>
    );
}

export default Login;