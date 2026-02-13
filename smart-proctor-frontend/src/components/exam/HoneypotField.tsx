import React from 'react';

export function HoneypotField({ register }: { register: any }) {
    return (
        <div
            aria-hidden="true"
            style={{ opacity: 0, position: 'absolute', top: 0, left: 0, height: 0, width: 0, zIndex: -1 }}
        >
            {/* We name it "phone_extension_secondary" to trick autofill
        into thinking it's a legitimate contact field.
      */}
            <label htmlFor="phone_extension_secondary">Phone Extension</label>
            <input
                id="phone_extension_secondary"
                autoComplete="off"
                tabIndex={-1}
                {...register("phone_extension_secondary")}
            />
        </div>
    );
}