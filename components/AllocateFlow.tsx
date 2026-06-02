const inputs = [
  {
    title: "Demand",
    note: "What the work needs",
    items: [
      "Project requirements & scope",
      "Seniority & headcount",
      "Profile / skill type required",
      "Pipeline & pre-PO signal",
      "Commercials & client expectations",
    ],
    highlight: false,
  },
  {
    title: "Supply",
    note: "What the bench can do",
    items: [
      "Availability (from your VMS / HR)",
      "Seniority, skills & profile",
      "Leave, joining & exit dates",
      "Past project history",
      "Development preferences",
    ],
    highlight: false,
  },
  {
    title: "Context",
    note: "What lives in partners' heads",
    items: [
      "Partner judgment & memory",
      "Client relationship notes",
      "Behavioural & soft profile",
      "Mentor input",
      "Informal performance & QA feedback",
    ],
    highlight: true,
  },
];

const confirmed = [
  "Named consultant confirmed",
  "Start date assigned",
  "QA & admin notified",
  "CRM / VMS updated (e.g. HubSpot)",
  "Consultant notified",
  "Partner briefed on plan B",
];

const added = [
  "Ranked rationale, not just a name",
  "Confidence & risk signal",
  "Seniority-mismatch flag",
  "Pool-wide supply-gap view",
  "Allocation reasoning record",
  "Outcome & near-miss feedback",
];

function Connector() {
  return (
    <div className="flex items-center justify-center" aria-hidden>
      {/* horizontal on desktop, vertical on mobile */}
      <div className="relative hidden h-px w-10 overflow-hidden bg-white/10 lg:block lg:w-14">
        <span className="absolute inset-0 bg-gradient-to-r from-transparent via-green-light/90 to-transparent [background-repeat:no-repeat] [background-size:60%_100%]" style={{ animation: "shimmer 2.4s linear infinite" }} />
      </div>
      <div className="relative my-1 h-8 w-px overflow-hidden bg-white/10 lg:hidden">
        <span className="absolute left-0 top-0 h-1/2 w-full bg-gradient-to-b from-green-light/90 to-transparent" style={{ animation: "shimmer 2s linear infinite" }} />
      </div>
    </div>
  );
}

export function AllocateFlow() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.02] p-5 sm:p-8">
      <div className="grid items-center gap-3 lg:grid-cols-[1fr_auto_1fr]">
        {/* INPUTS */}
        <div>
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-white/55">
            Inputs
          </p>
          <div className="space-y-3">
            {inputs.map((g) => (
              <div
                key={g.title}
                className={`rounded-2xl border p-4 transition-colors ${
                  g.highlight
                    ? "border-green-light/35 bg-green-light/[0.06] shadow-[0_0_30px_-12px_rgba(169,253,172,0.7)]"
                    : "border-white/8 bg-white/[0.03]"
                }`}
              >
                <div className="flex items-baseline justify-between gap-2">
                  <h4 className={`text-[15px] font-semibold tracking-tightish ${g.highlight ? "text-green-light" : "text-offwhite"}`}>
                    {g.title}
                  </h4>
                  <span className="text-[11px] text-white/40">{g.note}</span>
                </div>
                <ul className="mt-2 space-y-1">
                  {g.items.map((it) => (
                    <li key={it} className="flex gap-2 text-[12.5px] leading-snug text-white/60">
                      <span className={`mt-1.5 h-1 w-1 shrink-0 rounded-full ${g.highlight ? "bg-green-light" : "bg-green-accent/70"}`} />
                      {it}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* ENGINE + connectors */}
        <div className="flex flex-col items-center gap-2 lg:flex-row lg:gap-2 lg:px-2">
          <Connector />
          <div className="relative shrink-0">
            <span className="absolute inset-0 animate-spin-slow rounded-2xl border border-dashed border-green-light/20" />
            {[0, 1].map((i) => (
              <span
                key={i}
                className="absolute inset-0 rounded-2xl bg-green-accent/20"
                style={{ animation: "pulseRing 3.4s cubic-bezier(0.16,1,0.3,1) infinite", animationDelay: `${i * 1.5}s` }}
              />
            ))}
            <div className="relative flex h-24 w-24 flex-col items-center justify-center rounded-2xl bg-gradient-to-br from-green-accent to-teal text-center shadow-[0_0_44px_-8px_rgba(0,161,137,0.8)] ring-1 ring-green-light/30 sm:h-28 sm:w-28">
              <span className="text-[14px] font-semibold tracking-tightish text-offwhite sm:text-[15px]">
                V-allocate
              </span>
              <span className="text-[10px] uppercase tracking-[0.14em] text-green-light/80">
                engine
              </span>
              <span className="mt-1.5 text-[9px] leading-tight text-offwhite/55">
                allocate ·<br />validate · learn
              </span>
            </div>
          </div>
          <Connector />
        </div>

        {/* OUTPUTS */}
        <div>
          <p className="mb-4 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.14em] text-white/55">
            Outputs
          </p>
          <div className="space-y-3">
            <div className="rounded-2xl border border-white/8 bg-white/[0.03] p-4">
              <h4 className="text-[15px] font-semibold tracking-tightish text-offwhite">
                Confirmed &amp; actioned
              </h4>
              <ul className="mt-2 grid gap-1">
                {confirmed.map((it) => (
                  <li key={it} className="flex gap-2 text-[12.5px] leading-snug text-white/60">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-green-accent/70" />
                    {it}
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-green-light/25 bg-green-light/[0.05] p-4">
              <h4 className="text-[15px] font-semibold tracking-tightish text-green-light">
                Intelligence it adds
              </h4>
              <ul className="mt-2 grid gap-1">
                {added.map((it) => (
                  <li key={it} className="flex gap-2 text-[12.5px] leading-snug text-white/65">
                    <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-green-light" />
                    {it}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      <p className="mx-auto mt-6 max-w-2xl text-center text-[13px] leading-relaxed text-white/45">
        With full adoption, the manual updates on the left become redundant —
        V-allocate becomes the source of truth for who is working on what.
      </p>
    </div>
  );
}
