const agents = [
  { label: "V-allocate", status: "Live", live: true, x: 36, y: 10 },
  { label: "People & HR", status: "Soon", live: false, x: 80, y: 30 },
  { label: "Recruiting", status: "Soon", live: false, x: 70, y: 87 },
  { label: "Admin & ops", status: "Soon", live: false, x: 19, y: 66 },
];

export function BrainCore() {
  return (
    <div className="relative mx-auto aspect-square w-full max-w-[540px]">
      {/* connecting lines + rings */}
      <svg
        viewBox="0 0 100 100"
        className="absolute inset-0 h-full w-full"
        aria-hidden
      >
        <defs>
          <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#A9FDAC" stopOpacity="0.35" />
            <stop offset="100%" stopColor="#00A189" stopOpacity="0" />
          </radialGradient>
        </defs>

        {agents.map((a) => (
          <line
            key={a.label}
            x1="50"
            y1="50"
            x2={a.x}
            y2={a.y}
            stroke={a.live ? "#A9FDAC" : "#00A189"}
            strokeWidth="0.4"
            strokeOpacity={a.live ? 0.55 : 0.25}
            strokeDasharray="1.5 2"
          >
            <animate
              attributeName="stroke-dashoffset"
              from="0"
              to="-7"
              dur={a.live ? "1.6s" : "3.2s"}
              repeatCount="indefinite"
            />
          </line>
        ))}

        <circle cx="50" cy="50" r="34" fill="url(#coreGlow)" />
        {[20, 30, 40].map((r, i) => (
          <circle
            key={r}
            cx="50"
            cy="50"
            r={r}
            fill="none"
            stroke="#A9FDAC"
            strokeOpacity={0.12 - i * 0.02}
            strokeWidth="0.3"
          />
        ))}
      </svg>

      {/* rotating dashed rings */}
      <div className="absolute inset-[14%] animate-spin-slow rounded-full border border-dashed border-green-light/15" />
      <div className="absolute inset-[26%] animate-spin-slow-rev rounded-full border border-dashed border-green-accent/20" />

      {/* core */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="relative">
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="absolute inset-0 rounded-full bg-green-accent/30"
              style={{
                animation: `pulseRing 3.6s cubic-bezier(0.16,1,0.3,1) infinite`,
                animationDelay: `${i * 1.2}s`,
              }}
            />
          ))}
          <div className="relative flex h-28 w-28 flex-col items-center justify-center rounded-full bg-gradient-to-br from-green-accent to-teal text-center shadow-[0_0_50px_-6px_rgba(0,161,137,0.7)] ring-1 ring-green-light/30 sm:h-32 sm:w-32">
            <span className="text-[11px] uppercase tracking-[0.18em] text-green-light/80">
              The
            </span>
            <span className="text-[19px] font-semibold tracking-tightish text-offwhite sm:text-[21px]">
              V-brain
            </span>
            <span className="text-[10px] tracking-[0.16em] text-offwhite/55">
              core
            </span>
          </div>
        </div>
      </div>

      {/* agent chips */}
      {agents.map((a, i) => (
        <div
          key={a.label}
          className="absolute -translate-x-1/2 -translate-y-1/2"
          style={{
            left: `${a.x}%`,
            top: `${a.y}%`,
          }}
        >
          <div
            className={`flex animate-float items-center gap-1.5 whitespace-nowrap rounded-full border px-2.5 py-1.5 backdrop-blur-sm transition-colors sm:gap-2 sm:px-3 ${
              a.live
                ? "border-green-light/40 bg-green-light/10 shadow-[0_0_24px_-8px_rgba(169,253,172,0.8)]"
                : "border-white/12 bg-white/[0.04]"
            }`}
            style={{ animationDelay: `${i * 0.8}s` }}
          >
            <span
              className={`h-1.5 w-1.5 rounded-full ${
                a.live ? "bg-green-light animate-twinkle" : "bg-white/35"
              }`}
            />
            <span
              className={`text-[12px] font-medium sm:text-[13px] ${
                a.live ? "text-offwhite" : "text-white/65"
              }`}
            >
              {a.label}
            </span>
            <span
              className={`rounded-full px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide ${
                a.live
                  ? "bg-green-light/20 text-green-light"
                  : "bg-white/8 text-white/45"
              }`}
            >
              {a.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
