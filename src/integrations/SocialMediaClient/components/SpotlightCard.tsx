import React, { useRef } from 'react';

interface SpotlightCardProps {
    children: React.ReactNode;
    className?: string;
}

export const SpotlightCard: React.FC<SpotlightCardProps> = ({ children, className = "" }) => {
    const cardRef = useRef<HTMLDivElement>(null);
    
    const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
        if (!cardRef.current) return;
        const rect = cardRef.current.getBoundingClientRect();
        cardRef.current.style.setProperty("--x", `${e.clientX - rect.left}px`);
        cardRef.current.style.setProperty("--y", `${e.clientY - rect.top}px`);
    };

    return (
        <div 
            ref={cardRef} 
            onMouseMove={handleMouseMove} 
            className={`glass-panel spotlight-wrapper rounded-3xl ${className}`}
        >
            <div className="relative z-10 h-full">{children}</div>
        </div>
    );
};