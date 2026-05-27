const facts = [
  { stat: "50–500", label: "consultants — the firm size V-brain is built for" },
  { stat: "0", label: "new tools your teams have to learn" },
  { stat: "Day 1", label: "value, because it learns from work already happening" },
];

export function Audience() {
  return (
    <section id="audience" className="bg-offwhite">
      <div className="mx-auto max-w-content px-5 pb-24 sm:px-8 sm:pb-28">
        <div className="rounded-3xl border border-teal/10 bg-white p-9 sm:p-14">
          <div className="grid gap-12 lg:grid-cols-[1fr_1fr] lg:gap-16">
            <div>
              <p className="text-[13px] font-semibold uppercase tracking-[0.14em] text-green-accent">
                Who it&apos;s for
              </p>
              <h2 className="mt-3 text-balance text-[28px] font-semibold leading-[1.12] tracking-tightish text-teal sm:text-[36px]">
                For the people accountable for how the firm runs.
              </h2>
              <p className="mt-5 text-[16px] leading-relaxed text-teal/65">
                Operations leaders and managing partners at mid-market
                consulting firms carry the staffing math, the utilization
                targets, and the judgment calls in their heads. V-brain makes
                that institutional knowledge durable — and puts it to work where
                decisions get made.
              </p>
            </div>

            <div className="grid content-center gap-6">
              {facts.map((f) => (
                <div
                  key={f.label}
                  className="flex items-baseline gap-5 border-b border-teal/10 pb-6 last:border-0 last:pb-0"
                >
                  <span className="w-28 shrink-0 text-[30px] font-semibold tracking-tightish text-teal sm:text-[34px]">
                    {f.stat}
                  </span>
                  <span className="text-[15px] leading-snug text-teal/60">
                    {f.label}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
