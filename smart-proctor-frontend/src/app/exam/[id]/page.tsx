'use client';

import { useForm } from 'react-hook-form';
import { useKeystrokeDNA } from '@/src/hooks/useKeystrokeDNA';
import { HoneypotField } from '@/src/components/exam/HoneypotField';
import { PoisonedQuestion } from '@/src/components/exam/PoisonedQuestion';

export default function ExamPage({ params }: { params: { id: string } }) {
    // Mock Data (Replace with real Props/Context)
    const studentId = "1";
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') || '' : '';

    // 1. Initialize DNA Hook
    const { handleKeyDown, status } = useKeystrokeDNA(studentId, token);

    const { register, handleSubmit } = useForm();

    const onSubmit = async (data: any) => {
        // Determine start time for "Speed Check"
        const timeTaken = 120; // Mock calculation

        const payload = {
            student_id: studentId,
            exam_id: params.id,
            question_id: "q1",
            answer_text: data.answer_text,
            time_taken_seconds: timeTaken,
            // The honeypot value is included automatically by register
            phone_extension_secondary: data.phone_extension_secondary
        };

        const res = await fetch('http://localhost:8000/api/v1/exam/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(payload),
        });

        const result = await res.json();
        if(result.status === 'FLAGGED') {
            alert("Exam Flagged: " + result.security_remarks);
        } else {
            alert("Exam Passed!");
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-8" onKeyDown={handleKeyDown}>
            {/* Visual Indicator of Secure Connection */}
            <div className={`fixed top-4 right-4 px-3 py-1 rounded-full text-xs font-bold ${
                status === 'secure' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
                {status === 'secure' ? '🔒 SECURE CONNECTION' : '⚠ DISCONNECTED'}
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">

                {/* PILLAR 1: Poisoned Question */}
                <PoisonedQuestion text="Explain the impact of distributed ledger technology on supply chain transparency." />

                <textarea
                    {...register("answer_text")}
                    className="w-full p-4 border rounded-lg h-40"
                    placeholder="Type your answer here..."
                />

                {/* PILLAR 2: Honeypot Trap (Invisible) */}
                <HoneypotField register={register} />

                <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded">
                    Submit Exam
                </button>
            </form>
        </div>
    );
}