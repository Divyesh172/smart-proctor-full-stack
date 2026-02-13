// Matches app/schemas/exam.py
export interface ExamSubmission {
    student_id: number; // Changed to number to match Postgres ID
    exam_id: string;
    question_id: string;
    answer_text: string;
    time_taken_seconds: number;

    // The Honeypot (Mapped to 'hp_check' in Python)
    phone_extension_secondary?: string;
}

export interface ExamResult {
    student_id: number;
    status: 'PASSED' | 'FLAGGED' | 'REVIEW_REQUIRED';
    score: number;
    security_remarks?: string;
}

// Matches app/schemas/token.py
export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export interface User {
    id: number;
    email: string;
    full_name: string;
}