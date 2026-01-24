import React from 'react';

interface LogoProps {
    size?: number;
    className?: string;
}

export const Logo: React.FC<LogoProps> = ({ size = 40, className = '' }) => {
    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 200 200"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={className}
        >
            <defs>
                {/* Gradient for the circle */}
                <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{ stopColor: '#FF9B6B', stopOpacity: 1 }} />
                    <stop offset="35%" style={{ stopColor: '#FF7B4D', stopOpacity: 1 }} />
                    <stop offset="65%" style={{ stopColor: '#5B9FE3', stopOpacity: 1 }} />
                    <stop offset="100%" style={{ stopColor: '#B349C1', stopOpacity: 1 }} />
                </linearGradient>

                {/* Shadow filter */}
                <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="8"/>
                    <feOffset dx="0" dy="8" result="offsetblur"/>
                    <feComponentTransfer>
                        <feFuncA type="linear" slope="0.3"/>
                    </feComponentTransfer>
                    <feMerge>
                        <feMergeNode/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>

                {/* Glow filter */}
                <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>

            {/* Main Circle with gradient */}
            <circle
                cx="100"
                cy="100"
                r="90"
                fill="url(#circleGradient)"
                filter="url(#shadow)"
            />

            {/* Decorative elements - small circles and connection lines */}
            {/* Top left orbit */}
            <circle cx="45" cy="55" r="6" fill="white" opacity="0.9"/>
            <circle cx="70" cy="40" r="5" fill="white" opacity="0.8"/>

            {/* Top right orbit */}
            <circle cx="155" cy="55" r="6" fill="white" opacity="0.9"/>
            <circle cx="145" cy="85" r="5" fill="white" opacity="0.8"/>

            {/* Bottom left orbit */}
            <circle cx="55" cy="145" r="6" fill="white" opacity="0.9"/>
            <circle cx="75" cy="160" r="5" fill="white" opacity="0.8"/>

            {/* Bottom right orbit */}
            <circle cx="145" cy="145" r="6" fill="white" opacity="0.9"/>
            <circle cx="130" cy="165" r="5" fill="white" opacity="0.8"/>

            {/* Connection lines */}
            <path
                d="M 45,55 Q 60,45 70,40"
                stroke="white"
                strokeWidth="2"
                fill="none"
                opacity="0.4"
            />
            <path
                d="M 155,55 Q 150,70 145,85"
                stroke="white"
                strokeWidth="2"
                fill="none"
                opacity="0.4"
            />
            <path
                d="M 55,145 Q 65,152 75,160"
                stroke="white"
                strokeWidth="2"
                fill="none"
                opacity="0.4"
            />
            <path
                d="M 145,145 Q 138,155 130,165"
                stroke="white"
                strokeWidth="2"
                fill="none"
                opacity="0.4"
            />

            {/* Lightning bolt (centered) */}
            <g filter="url(#glow)">
                <path
                    d="M 100,45 L 85,100 L 105,100 L 90,155 L 125,90 L 105,90 L 120,45 Z"
                    fill="white"
                    stroke="white"
                    strokeWidth="2"
                    strokeLinejoin="round"
                />
            </g>

            {/* Additional tech elements */}
            {/* Small circuit-like lines */}
            <line x1="35" y1="100" x2="25" y2="100" stroke="white" strokeWidth="2" opacity="0.5"/>
            <line x1="25" y1="100" x2="25" y2="90" stroke="white" strokeWidth="2" opacity="0.5"/>

            <line x1="165" y1="100" x2="175" y2="100" stroke="white" strokeWidth="2" opacity="0.5"/>
            <line x1="175" y1="100" x2="175" y2="110" stroke="white" strokeWidth="2" opacity="0.5"/>
        </svg>
    );
};

export default Logo;
