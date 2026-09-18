export default function DefenderShield({ size = 24, className = '', glow = true }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      style={{ display: 'inline-block', verticalAlign: 'middle' }}
    >
      <defs>
        <linearGradient id="shieldArmor" x1="3" y1="2" x2="21" y2="22" gradientUnits="userSpaceOnUse">
          <stop stopColor="#ff4d5e" />
          <stop offset="0.5" stopColor="#ef4444" />
          <stop offset="1" stopColor="#990f1d" />
        </linearGradient>
        <linearGradient id="radarCore" x1="12" y1="7" x2="12" y2="17" gradientUnits="userSpaceOnUse">
          <stop stopColor="#38bdf8" />
          <stop offset="1" stopColor="#0284c7" />
        </linearGradient>
        {glow && (
          <filter id="cyberGlow" x="-25%" y="-25%" width="150%" height="150%">
            <feDropShadow dx="0" dy="0" stdDeviation="2.2" floodColor="#ef4444" floodOpacity="0.6" />
          </filter>
        )}
      </defs>

      {/* Outer Defender Shield */}
      <path
        d="M12 2L3.5 5.8V11.2C3.5 16.6 7.1 21.6 12 22.8C16.9 21.6 20.5 16.6 20.5 11.2V5.8L12 2Z"
        fill="url(#shieldArmor)"
        stroke="#ff7b88"
        strokeWidth="1.2"
        strokeLinejoin="round"
        filter={glow ? 'url(#cyberGlow)' : undefined}
      />

      {/* Inner Cyber Plate */}
      <path
        d="M12 4.4L5.2 7.4V11.4C5.2 15.5 8.1 19.4 12 20.4C15.9 19.4 18.8 15.5 18.8 11.4V7.4L12 4.4Z"
        fill="#070b14"
        fillOpacity="0.9"
        stroke="rgba(255, 107, 107, 0.35)"
        strokeWidth="0.8"
      />

      {/* Center Radar / Defense Core */}
      <circle
        cx="12"
        cy="12"
        r="3.5"
        stroke="url(#radarCore)"
        strokeWidth="1.4"
        fill="rgba(56, 189, 248, 0.12)"
      />
      {/* Reticle / Crosshair */}
      <path
        d="M12 6.8V9.2M12 14.8V17.2M6.8 12H9.2M14.8 12H17.2"
        stroke="#38bdf8"
        strokeWidth="1.3"
        strokeLinecap="round"
      />
      <circle cx="12" cy="12" r="1.3" fill="#38bdf8" />
    </svg>
  )
}
