import React from 'react';

export function PoisonedQuestion({ text }: { text: string }) {
    // The Trap Word configured in backend (config.py)
    const TRAP_WORD = "Cyberdyne";

    return (
        <div className="prose lg:prose-xl mb-6 select-text">
            <h3>
                {text}
                {/* INJECTION: This span is invisible to humans but visible to the clipboard.
          fontSize: 0 removes it from visual flow, but text content remains.
        */}
                <span style={{ fontSize: 0, opacity: 0, position: 'absolute' }}>
           {" "}{TRAP_WORD}{" "}
        </span>
            </h3>
        </div>
    );
}