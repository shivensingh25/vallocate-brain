import { Reveal } from "./Reveal";

const facts = [
  { stat: "50–500", label: "people — the firm size V-brain is built for" },
  { stat: "0", label: "new tools your teams have to learn" },
  { stat: "Day 1", label: "value, because it learns from work already happening" },
];

export function Audience() {
  return (
    <section id="audience" className="relative bg-teal-deep">
      <div className="mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <Reveal className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-9 sm:p-14">
          <div className="grid gap-12 lg:grid-cols-[1fr_1fr] lg:gap-16">
            <div>
              <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
                Who it&apos;s for
              </p>
              <h2 className="mt-3 text-balance text-[28px] font-semibold leading-[1.1] tracking-tightish text-offwhite sm:text-[36px]">
                For the people accountable for how the firm runs.
              </h2>
              <p className="mt-5 text-[16px] leading-relaxed text-white/60">
                Operations leaders and managing partners at mid-market
                professional services firms carry the staffing math, the
                utilization targets, and the judgment calls in their heads.
                V-brain makes that institutional knowledge durable — and puts it
                to work where decisions get made.
              </p>
            </div>

            <div className="grid content-center gap-6">
              {facts.map((f, i) => (
                <Reveal
                  key={f.label}
                  delay={i * 120}
                  className="flex items-baseline gap-5 border-b border-white/10 pb-6 last:border-0 last:pb-0"
                >
                  <span className="w-28 shrink-0 text-[30px] font-semibold tracking-tightish text-green-light sm:text-[34px]">
                    {f.stat}
                  </span>
                  <span className="text-[15px] leading-snug text-white/55">
                    {f.label}
                  </span>
                </Reveal>
              ))}
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
