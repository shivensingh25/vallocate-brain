const features = [
  {
    title: "Ranked candidate shortlists",
    body: "Ask who to staff on a project and get a ranked list — scored on skills, sector history, seniority, and fit. Not a database query. A recommendation you can defend.",
  },
  {
    title: "Availability, unified",
    body: "Pulls real availability from the systems you already run — HR, time tracking, project tools — into one view. No more pinging three people to find out who's free.",
  },
  {
    title: "Learns from outcomes",
    body: "When a staffing call works (or doesn't), V-allocate notices. Recommendations improve against how your firm actually performs, not a generic benchmark.",
  },
];

export function VAllocate() {
  return (
    <section id="vallocate" className="relative bg-teal text-offwhite">
      <div aria-hidden className="grain absolute inset-0 opacity-40" />
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="max-w-2xl">
            <p className="text-[13px] font-semibold uppercase tracking-[0.14em] text-green-light">
              The first product on V-brain
            </p>
            <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.1] tracking-tightish sm:text-[42px]">
              V-allocate: project staffing, decided.
            </h2>
          </div>
          <p className="max-w-md text-[16px] leading-relaxed text-white/65">
            An AI agent for project allocation. It turns the question
            &ldquo;who should we put on this?&rdquo; from a week of back-and-forth
            into a shortlist in seconds.
          </p>
        </div>

        <div className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/10 md:grid-cols-3">
          {features.map((f, i) => (
            <div key={f.title} className="bg-teal-deep/60 p-8 backdrop-blur-sm">
              <p className="text-[13px] font-semibold text-green-light/70">
                0{i + 1}
              </p>
              <h3 className="mt-4 text-[19px] font-semibold tracking-tightish text-offwhite">
                {f.title}
              </h3>
              <p className="mt-3 text-[15px] leading-relaxed text-white/60">
                {f.body}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
