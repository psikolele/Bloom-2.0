import React, { useState, useEffect, useRef } from 'react';

export interface DropdownOption {
    value: string;
    label: string;
}

interface CustomDropdownProps {
    options: DropdownOption[];
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    disabled?: boolean;
    className?: string;
}

const CustomDropdown: React.FC<CustomDropdownProps> = ({
    options,
    value,
    onChange,
    placeholder = 'Seleziona…',
    disabled = false,
    className = '',
}) => {
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleOutside = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener('mousedown', handleOutside);
        return () => document.removeEventListener('mousedown', handleOutside);
    }, []);

    const selectedLabel = options.find(o => o.value === value)?.label ?? value;

    return (
        <div ref={ref} className={`relative ${className}`}>
            <button
                type="button"
                disabled={disabled}
                onClick={() => !disabled && setOpen(v => !v)}
                className={`w-full tech-input px-4 py-3 rounded-xl text-sm font-mono flex items-center justify-between gap-2 transition-colors
                    ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-accent/50 cursor-pointer'}
                    ${value ? 'text-white' : 'text-gray-500'}`}
            >
                <span>{value ? selectedLabel : placeholder}</span>
                <svg
                    width="16" height="16" viewBox="0 0 16 16" fill="none"
                    className={`text-gray-400 transition-transform duration-200 shrink-0 ${open ? 'rotate-180' : ''}`}
                >
                    <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
            </button>

            {open && !disabled && (
                <div className="absolute top-full left-0 right-0 mt-1 z-50 bg-[#0d0d0d] border border-white/10 rounded-xl overflow-y-auto max-h-60 shadow-[0_8px_32px_rgba(0,0,0,0.6)]">
                    {options.map(opt => (
                        <button
                            key={opt.value}
                            type="button"
                            onClick={() => { onChange(opt.value); setOpen(false); }}
                            className={`w-full text-left px-4 py-3 text-sm font-mono transition-colors border-l-2
                                ${value === opt.value
                                    ? 'bg-accent/15 text-accent border-accent'
                                    : 'text-gray-300 hover:bg-white/5 hover:text-white border-transparent'
                                }`}
                        >
                            {opt.label}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default CustomDropdown;
