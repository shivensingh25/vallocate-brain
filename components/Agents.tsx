import { Reveal } from "./Reveal";

const agents = [
  {
    name: "V-allocate",
    status: "Available now",
    live: true,
    desc: "Project and resource allocation. Ranked candidate shortlists, availability unified across your existing systems, and recommendations that learn from outcomes.",
  },
  {
    name: "People & HR",
    status: "On the roadmap",
    live: false,
    desc: "Performance, development, and people decisions — informed by how your firm actually evaluates and grows its teams.",
  },
  {
    name: "Recruiting",
    status: "On the roadmap",
    live: false,
    desc: "Screening and matching candidates against the patterns of who succeeds in your firm, not a generic rubric.",
  },
  {
    name: "Admin & ops",
    status: "On the roadmap",
    live: false,
    desc: "The repetitive back-office decisions that quietly eat hours — handled by agents that already know how your firm runs.",
  },
];

export function Agents() {
  return (
    <section id="agents" className="relative bg-teal-black">
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-0 h-px w-2/3 -translate-x-1/2 bg-gradient-to-r from-transparent via-green-accent/40 to-transparent"
      />
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <Reveal className="max-w-2xl">
          <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-light">
            Agents on the brain
          </p>
          <h2 className="mt-3 text-balance text-[32px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[44px]">
            One layer. A growing set of agents.
          </h2>
          <p className="mt-5 text-[17px] leading-relaxed text-white/60">
            V-brain is the infrastructure. Agents are how you put it to work —
            each one inheriting everything the brain has learned. We&apos;re
            starting with allocation. The rest of the firm is next.
          </p>
        </Reveal>

        <div className="mt-16 grid gap-5 md:grid-cols-2">
          {agents.map((a, i) => (
            <Reveal
              key={a.name}
              delay={i * 90}
              className={`group relative overflow-hidden rounded-2xl border p-7 transition-all duration-300 sm:p-8 ${
                a.live
                  ? "border-green-light/30 bg-gradient-to-br from-green-accent/12 to-white/[0.02] hover:-translate-y-1 hover:border-green-light/50"
                  : "border-white/8 bg-white/[0.02] hover:-translate-y-1 hover:border-white/20"
              }`}
            >
              {a.live && (
                <span
                  aria-hidden
                  className="absolute -right-16 -top-16 h-40 w-40 rounded-full bg-green-accent/20 blur-3xl"
                />
              )}
              <div className="relative">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="text-[22px] font-semibold tracking-tightish text-offwhite sm:text-[24px]">
                    {a.name}
                  </h3>
                  <span
                    className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide ${
                      a.live
                        ? "bg-green-light/20 text-green-light"
                        : "bg-white/8 text-white/50"
                    }`}
                  >
                    <span
                      className={`h-1.5 w-1.5 rounded-full ${
                        a.live ? "bg-green-light animate-twinkle" : "bg-white/40"
                      }`}
                    />
                    {a.status}
                  </span>
                </div>
                <p className="mt-4 text-[15px] leading-relaxed text-white/60">
                  {a.desc}
                </p>
                {a.live && (
                  <a
                    href="/v-allocate"
                    className="mt-6 inline-flex items-center gap-1.5 text-[14px] font-medium text-green-light transition-colors hover:text-offwhite"
                  >
                    See how V-allocate works
                    <span aria-hidden className="transition-transform group-hover:translate-x-1">
                      →
                    </span>
                  </a>
                )}
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
