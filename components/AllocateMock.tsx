const candidates = [
  { name: "M. Okonkwo", role: "Senior Manager", match: 96, free: "Now", tag: "Led 2 similar deals" },
  { name: "R. Castellano", role: "Manager", match: 91, free: "Mon", tag: "Sector match" },
  { name: "J. Adeyemi", role: "Consultant", match: 84, free: "Now", tag: "Travel-ready" },
];

export function AllocateMock() {
  return (
    <div className="relative">
      <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/30 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-[12px] uppercase tracking-[0.12em] text-green-light/80">
              V-allocate
            </p>
            <p className="mt-1 text-[15px] font-medium text-offwhite">
              Staffing — Retail Ops diagnostic
            </p>
          </div>
          <span className="rounded-full bg-green-accent/15 px-2.5 py-1 text-[11px] font-medium text-green-light">
            Ranked
          </span>
        </div>

        <div className="mt-5 space-y-2.5">
          {candidates.map((c, i) => (
            <div
              key={c.name}
              className="flex items-center gap-3 rounded-xl border border-white/8 bg-white/[0.03] px-3.5 py-3"
            >
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-accent/20 text-[12px] font-semibold text-green-light">
                {i + 1}
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-2">
                  <p className="truncate text-[14px] font-medium text-offwhite">
                    {c.name}
                  </p>
                  <p className="shrink-0 text-[13px] font-semibold text-green-light">
                    {c.match}%
                  </p>
                </div>
                <div className="mt-0.5 flex items-center gap-2 text-[12px] text-white/45">
                  <span>{c.role}</span>
                  <span className="h-1 w-1 rounded-full bg-white/25" />
                  <span className="text-green-light/70">Free {c.free}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 flex items-center justify-between rounded-xl bg-white/[0.03] px-3.5 py-2.5 text-[12px] text-white/50">
          <span>Availability unified across 3 systems</span>
          <span className="text-green-light/70">Live</span>
        </div>
      </div>

      <div
        aria-hidden
        className="absolute -bottom-4 -right-4 -z-10 h-full w-full rounded-2xl border border-white/5 bg-white/[0.02]"
      />
    </div>
  );
}
