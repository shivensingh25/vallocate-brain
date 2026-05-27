const points = [
  {
    title: "Passive by design",
    body: "No new tool to adopt, no forms to fill. V-brain observes the artifacts your teams already produce — staffing decisions, scoping notes, proposals, reviews.",
  },
  {
    title: "Learns the judgment, not the files",
    body: "Document search returns pages. V-brain captures the reasoning behind choices: who got staffed where, why a pitch was shaped a certain way, which trade-offs partners actually make.",
  },
  {
    title: "Sharper with every outcome",
    body: "Each decision and its result feeds back in. The model of how your firm decides compounds over time — it doesn't go stale the day someone stops updating a wiki.",
  },
];

export function VBrain() {
  return (
    <section id="vbrain" className="bg-offwhite">
      <div className="mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
        <div className="max-w-2xl">
          <p className="text-[13px] font-semibold uppercase tracking-[0.14em] text-green-accent">
            The intelligence layer
          </p>
          <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.1] tracking-tightish text-teal sm:text-[42px]">
            Not another place to search documents.
          </h2>
          <p className="mt-5 text-[17px] leading-relaxed text-teal/65">
            Your firm&apos;s real expertise lives in the decisions people make
            every day — and most of it is never written down. V-brain captures
            that judgment from the work itself, so it stays with the firm even
            when people move on.
          </p>
        </div>

        <div className="mt-14 grid gap-5 md:grid-cols-3">
          {points.map((p) => (
            <div
              key={p.title}
              className="group rounded-2xl border border-teal/10 bg-white p-7 transition-shadow hover:shadow-lg hover:shadow-teal/5"
            >
              <div className="h-9 w-9 rounded-lg bg-green-light/40 ring-1 ring-inset ring-green-accent/20 transition-colors group-hover:bg-green-light/70" />
              <h3 className="mt-5 text-[18px] font-semibold tracking-tightish text-teal">
                {p.title}
              </h3>
              <p className="mt-2.5 text-[15px] leading-relaxed text-teal/60">
                {p.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
