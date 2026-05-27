const steps = [
  {
    step: "01",
    title: "Connect",
    body: "Point V-brain at the systems your firm already uses. It reads the artifacts of work — no migration, no data entry, no change to how anyone operates.",
  },
  {
    step: "02",
    title: "Capture",
    body: "It learns the patterns behind your decisions in the background: how staffing is balanced, how scope is set, what good looks like for your firm specifically.",
  },
  {
    step: "03",
    title: "Surface",
    body: "Products like V-allocate put that intelligence to work — ranked, explainable recommendations at the moment a decision needs to be made.",
  },
];

export function HowItWorks() {
  return (
    <section id="how" className="bg-offwhite">
      <div className="mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
        <div className="max-w-2xl">
          <p className="text-[13px] font-semibold uppercase tracking-[0.14em] text-green-accent">
            How it works
          </p>
          <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.1] tracking-tightish text-teal sm:text-[42px]">
            Three steps. No new workflow.
          </h2>
        </div>

        <div className="mt-14 grid gap-10 md:grid-cols-3">
          {steps.map((s) => (
            <div key={s.step} className="relative">
              <div className="flex items-center gap-3">
                <span className="text-[15px] font-semibold text-green-accent">
                  {s.step}
                </span>
                <span className="h-px flex-1 bg-teal/15" />
              </div>
              <h3 className="mt-5 text-[22px] font-semibold tracking-tightish text-teal">
                {s.title}
              </h3>
              <p className="mt-3 text-[15px] leading-relaxed text-teal/60">
                {s.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
