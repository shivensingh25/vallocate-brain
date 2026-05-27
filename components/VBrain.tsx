import { Reveal } from "./Reveal";

const points = [
  {
    title: "Passive by design",
    body: "No new tool to adopt, no forms to fill. V-brain learns from the artifacts your teams already produce — staffing calls, scoping notes, proposals, reviews.",
  },
  {
    title: "Captures judgment, not files",
    body: "Document search returns pages. V-brain captures the reasoning behind choices: who decided what, why work was shaped a certain way, which trade-offs your people actually make.",
  },
  {
    title: "Compounds over time",
    body: "Every decision and its outcome feeds back in. The model of how your firm works gets sharper — it doesn't go stale the day someone stops updating a wiki.",
  },
];

export function VBrain() {
  return (
    <section id="vbrain" className="relative bg-teal-deep">
      <div aria-hidden className="grain pointer-events-none absolute inset-0 opacity-50" />
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <Reveal className="max-w-2xl">
          <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
            The intelligence layer
          </p>
          <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[44px]">
            Your firm&apos;s real expertise lives in its decisions.
          </h2>
          <p className="mt-5 text-[17px] leading-relaxed text-white/60">
            Most of it is never written down. V-brain captures that judgment
            from the work itself — so it stays with the firm even when people
            move on, and so every agent built on top inherits it from day one.
          </p>
        </Reveal>

        <div className="mt-16 grid gap-5 md:grid-cols-3">
          {points.map((p, i) => (
            <Reveal
              key={p.title}
              delay={i * 110}
              className="group relative overflow-hidden rounded-2xl border border-white/8 bg-white/[0.03] p-7 transition-all duration-300 hover:-translate-y-1 hover:border-green-light/25 hover:bg-white/[0.05]"
            >
              <span
                aria-hidden
                className="absolute -right-10 -top-10 h-28 w-28 rounded-full bg-green-accent/10 blur-2xl transition-opacity duration-300 group-hover:opacity-100 opacity-0"
              />
              <div className="relative">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-light/10 ring-1 ring-inset ring-green-light/20">
                  <span className="text-[14px] font-semibold text-green-light">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                </div>
                <h3 className="mt-5 text-[18px] font-semibold tracking-tightish text-offwhite">
                  {p.title}
                </h3>
                <p className="mt-2.5 text-[15px] leading-relaxed text-white/55">
                  {p.body}
                </p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
