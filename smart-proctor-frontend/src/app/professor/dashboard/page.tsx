'use client';

import React, { useState } from 'react';
import {
    Users,
    FilePlus,
    Activity,
    Search,
    AlertTriangle,
    CheckCircle,
    Clock
} from 'lucide-react';

export default function ProfessorDashboard() {
    const [showCreateModal, setShowCreateModal] = useState(false);

    // Mock Data for Dashboard
    const activeExams = [
        { id: 'EX-101', title: 'Cybersecurity Finals', status: 'LIVE', students: 45, violations: 3 },
        { id: 'EX-102', title: 'Data Structures', status: 'SCHEDULED', students: 120, violations: 0 },
    ];

    const recentLogs = [
        { id: 1, student: 'John Doe', event: 'Tab Switch Detected', time: '10:45 AM', severity: 'HIGH' },
        { id: 2, student: 'Jane Smith', event: 'Multiple Faces Found', time: '10:42 AM', severity: 'MEDIUM' },
        { id: 3, student: 'Alice Johnson', event: 'Microphone Muted', time: '10:30 AM', severity: 'LOW' },
    ];

    return (
        <div className="min-h-screen bg-slate-50">
            {/* HEADER */}
            <header className="bg-white border-b border-slate-200 px-8 py-4">
                <div className="max-w-7xl mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-bold text-slate-800">Professor Portal</h1>
                    <div className="flex items-center space-x-4">
                        <button className="p-2 text-slate-400 hover:text-blue-600">
                            <Search className="w-5 h-5" />
                        </button>
                        <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-bold">
                            PR
                        </div>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-8 py-10">

                {/* STATS ROW */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-bold text-slate-400 uppercase">Active Students</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">165</h3>
                            </div>
                            <Users className="w-6 h-6 text-blue-500" />
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-bold text-slate-400 uppercase">Live Exams</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">1</h3>
                            </div>
                            <Activity className="w-6 h-6 text-green-500" />
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-xs font-bold text-slate-400 uppercase">Pending Review</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">12</h3>
                            </div>
                            <Clock className="w-6 h-6 text-orange-500" />
                        </div>
                    </div>

                    <button
                        onClick={() => setShowCreateModal(true)}
                        className="bg-blue-600 p-6 rounded-xl shadow-lg shadow-blue-200 hover:bg-blue-700 transition-all text-left group"
                    >
                        <FilePlus className="w-8 h-8 text-white mb-4 group-hover:scale-110 transition-transform" />
                        <p className="text-white font-bold text-lg">Create New Exam</p>
                        <p className="text-blue-200 text-sm mt-1">Schedule a secure session</p>
                    </button>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

                    {/* EXAM LIST */}
                    <div className="lg:col-span-2 space-y-6">
                        <h2 className="text-lg font-bold text-slate-800">Active Sessions</h2>
                        {activeExams.map((exam) => (
                            <div key={exam.id} className="bg-white p-6 rounded-xl border border-slate-200 flex justify-between items-center hover:border-blue-300 transition-colors cursor-pointer">
                                <div>
                                    <div className="flex items-center space-x-3 mb-1">
                                        <h3 className="font-bold text-slate-900">{exam.title}</h3>
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wide ${
                                            exam.status === 'LIVE' ? 'bg-green-100 text-green-700 animate-pulse' : 'bg-slate-100 text-slate-600'
                                        }`}>
                      {exam.status}
                    </span>
                                    </div>
                                    <p className="text-sm text-slate-500">ID: {exam.id} • {exam.students} Students Enrolled</p>
                                </div>
                                <div className="text-right">
                                    <p className="text-2xl font-bold text-slate-900">{exam.violations}</p>
                                    <p className="text-xs font-bold text-red-500 uppercase">Violations</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* LIVE LOGS */}
                    <div className="bg-slate-900 rounded-2xl p-6 text-white h-[500px] flex flex-col">
                        <h3 className="font-bold text-slate-100 mb-6 flex items-center">
                            <Activity className="w-4 h-4 mr-2 text-blue-400" /> Live Integrity Feed
                        </h3>
                        <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
                            {recentLogs.map((log) => (
                                <div key={log.id} className="bg-slate-800 p-4 rounded-lg border-l-4 border-red-500">
                                    <div className="flex justify-between items-start mb-1">
                                        <span className="font-bold text-sm text-slate-200">{log.student}</span>
                                        <span className="text-xs text-slate-500 font-mono">{log.time}</span>
                                    </div>
                                    <p className="text-xs text-red-300 font-medium flex items-center">
                                        <AlertTriangle className="w-3 h-3 mr-1" /> {log.event}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>

            {/* CREATE MODAL (Simplified) */}
            {showCreateModal && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
                    <div className="bg-white p-8 rounded-2xl w-full max-w-md shadow-2xl">
                        <h2 className="text-2xl font-bold text-slate-900 mb-6">Create Exam</h2>
                        <input type="text" placeholder="Exam Title" className="w-full p-3 border border-slate-200 rounded-lg mb-4" />
                        <input type="datetime-local" className="w-full p-3 border border-slate-200 rounded-lg mb-6" />
                        <div className="flex space-x-3">
                            <button
                                onClick={() => setShowCreateModal(false)}
                                className="flex-1 py-3 text-slate-600 font-bold hover:bg-slate-50 rounded-lg"
                            >
                                Cancel
                            </button>
                            <button className="flex-1 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700">
                                Create
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}