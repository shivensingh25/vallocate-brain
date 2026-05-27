import { Reveal } from "./Reveal";

const steps = [
  {
    step: "01",
    title: "Connect",
    body: "Point V-brain at the systems your firm already uses. It reads the artifacts of work — no migration, no data entry, no change to how anyone operates.",
  },
  {
    step: "02",
    title: "Capture",
    body: "It learns the patterns behind your decisions in the background: how work is staffed and shaped, what good looks like for your firm specifically.",
  },
  {
    step: "03",
    title: "Surface",
    body: "Agents put that intelligence to work — ranked, explainable recommendations at the moment a decision needs to be made.",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="relative bg-teal-black">
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <Reveal className="max-w-2xl">
          <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
            How it works
          </p>
          <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[44px]">
            Three steps. No new workflow.
          </h2>
        </Reveal>

        <div className="relative mt-16 grid gap-10 md:grid-cols-3">
          {steps.map((s, i) => (
            <Reveal key={s.step} delay={i * 120} className="relative">
              <div className="flex items-center gap-3">
                <span className="text-[15px] font-semibold text-green-light">
                  {s.step}
                </span>
                <span className="h-px flex-1 bg-gradient-to-r from-green-accent/40 to-transparent" />
              </div>
              <h3 className="mt-5 text-[22px] font-semibold tracking-tightish text-offwhite">
                {s.title}
              </h3>
              <p className="mt-3 text-[15px] leading-relaxed text-white/55">
                {s.body}
              </p>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
