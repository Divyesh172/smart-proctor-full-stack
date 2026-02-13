import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/src/lib/api';
import { User, AuthResponse } from '@/src/lib/types';

interface LoginCredentials {
    username: string; // Maps to OAuth2 'username' (email)
    password: string;
}

export const useAuth = () => {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // ---------------------------------------------------------
    // 1. INITIAL SESSION CHECK
    // ---------------------------------------------------------
    // On mount, check if we have a token and if it's still valid
    // by hitting the /users/me endpoint.
    const checkSession = useCallback(async () => {
        const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

        if (!token) {
            setIsLoading(false);
            return;
        }

        try {
            const { data } = await api.get<User>('/users/me');
            setUser(data);
        } catch (err) {
            // If /me fails (401), the token is expired/invalid.
            console.warn('Session expired or invalid');
            logout(); // Clean up local state
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        checkSession();
    }, [checkSession]);

    // ---------------------------------------------------------
    // 2. LOGIN ACTION
    // ---------------------------------------------------------
    const login = async ({ username, password }: LoginCredentials) => {
        setIsLoading(true);
        setError(null);

        try {
            // OAuth2 Standard expects URL-encoded form data
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const { data } = await api.post<AuthResponse>('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            });

            // Save token
            localStorage.setItem('access_token', data.access_token);

            // Fetch User Details immediately
            await checkSession();

            // Redirect
            router.push('/dashboard');
            return true;
        } catch (err: any) {
            const msg = err.response?.data?.detail || 'Login failed. Check your credentials.';
            setError(msg);
            setIsLoading(false);
            return false;
        }
    };

    // ---------------------------------------------------------
    // 3. LOGOUT ACTION
    // ---------------------------------------------------------
    const logout = () => {
        localStorage.removeItem('access_token');
        setUser(null);
        router.push('/login');
    };

    // ---------------------------------------------------------
    // 4. REGISTER ACTION (Optional wrapper)
    // ---------------------------------------------------------
    const register = async (payload: any) => {
        try {
            await api.post('/users/open', payload);
            return true;
        } catch (err: any) {
            throw new Error(err.response?.data?.detail || 'Registration failed');
        }
    };

    return {
        user,
        isLoading,
        error,
        isAuthenticated: !!user,
        login,
        logout,
        register
    };
};