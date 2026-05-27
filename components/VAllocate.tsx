import { Reveal } from "./Reveal";
import { AllocateMock } from "./AllocateMock";

const features = [
  {
    title: "Ranked candidate shortlists",
    body: "Ask who to staff and get a ranked list — scored on skills, sector history, seniority, and fit. A recommendation you can defend, not a database query.",
  },
  {
    title: "Availability, unified",
    body: "Pulls real availability from the systems you already run into one view. No more pinging three people to find out who's free.",
  },
  {
    title: "Learns from outcomes",
    body: "When a call works — or doesn't — V-allocate notices. It improves against how your firm actually performs, not a generic benchmark.",
  },
];

export function VAllocate() {
  return (
    <section id="vallocate" className="relative bg-teal-deep">
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <div className="grid items-center gap-14 lg:grid-cols-[0.95fr_1.05fr]">
          <Reveal className="order-2 lg:order-1">
            <AllocateMock />
          </Reveal>

          <Reveal className="order-1 lg:order-2" delay={80}>
            <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
              The first agent
            </p>
            <h2 className="mt-3 text-balance text-[30px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[40px]">
              V-allocate: staffing, decided in seconds.
            </h2>
            <p className="mt-5 text-[16px] leading-relaxed text-white/60">
              It turns &ldquo;who should we put on this?&rdquo; from a week of
              back-and-forth into a shortlist you can act on — and it gets better
              every time the firm makes a call.
            </p>

            <div className="mt-8 space-y-5">
              {features.map((f) => (
                <div key={f.title} className="flex gap-4">
                  <span
                    aria-hidden
                    className="mt-1.5 h-2 w-2 shrink-0 rounded-full bg-green-light shadow-[0_0_12px_rgba(169,253,172,0.8)]"
                  />
                  <div>
                    <h3 className="text-[16px] font-semibold tracking-tightish text-offwhite">
                      {f.title}
                    </h3>
                    <p className="mt-1 text-[14px] leading-relaxed text-white/55">
                      {f.body}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
