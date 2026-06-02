import type { Metadata } from "next";
import { Nav } from "@/components/Nav";
import { Footer } from "@/components/Footer";
import { CTASection } from "@/components/CTASection";
import { Reveal } from "@/components/Reveal";
import { AllocateFlow } from "@/components/AllocateFlow";

export const metadata: Metadata = {
  title: "V-allocate — The agent that staffs your firm | VisagioX",
  description:
    "V-allocate is an agent that allocates people across every live project and hands partners a decision to confirm. Built on V-brain, it weighs the judgment that lives in partners' heads — not just who's free.",
};

const contrasts = [
  {
    tool: "Sees who is free next week.",
    brain: "Knows she's ready to step up to lead, and this is the project to prove it.",
  },
  {
    tool: "Matches a skill tag to a requirement.",
    brain: "Remembers he clashed with this client's CFO last time — and quietly routes around it.",
  },
  {
    tool: "Lists everyone on the bench.",
    brain: "Weighs an owed rotation, a mentor pairing, and a soft-skill gap at once.",
  },
];

const loop = [
  {
    step: "01",
    title: "It allocates",
    body: "V-allocate staffs across every live and pipeline project at once — not one request at a time. It produces a confirmed plan, a fallback, and the reasoning behind both.",
  },
  {
    step: "02",
    title: "A partner confirms",
    body: "The human stays in the loop to validate, adjust, or override. The agent shows its reasoning; the partner stays accountable. Confirming takes seconds, not meetings.",
  },
  {
    step: "03",
    title: "It learns",
    body: "Every confirmation, override, and outcome feeds back through V-brain — so the next allocation reflects how your firm actually decides, not a generic rule set.",
  },
];

export default function VAllocatePage() {
  return (
    <main>
      <Nav />

      {/* HERO */}
      <section className="relative overflow-hidden bg-teal-deep">
        <div aria-hidden className="mesh pointer-events-none absolute inset-0" />
        <div aria-hidden className="dotgrid pointer-events-none absolute inset-0" />
        <div
          aria-hidden
          className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-teal-deep"
        />
        <div className="relative mx-auto max-w-content px-5 py-20 sm:px-8 sm:py-28 lg:py-32">
          <a
            href="/#agents"
            className="inline-flex animate-fade-up items-center gap-2 rounded-full border border-white/12 bg-white/[0.04] px-3 py-1 text-[12px] font-medium uppercase tracking-[0.14em] text-green-light transition-colors hover:border-green-light/40"
          >
            <span className="h-1.5 w-1.5 animate-twinkle rounded-full bg-green-light" />
            An agent on V-brain
          </a>

          <h1 className="mt-6 max-w-3xl animate-fade-up text-balance text-[40px] font-semibold leading-[1.04] tracking-tighter2 [animation-delay:80ms] sm:text-[56px] lg:text-[62px]">
            Staffing, decided for you —{" "}
            <span className="text-glow text-green-light">not suggested to you.</span>
          </h1>

          <p className="mt-6 max-w-2xl animate-fade-up text-pretty text-[17px] leading-relaxed text-white/70 [animation-delay:160ms] sm:text-[19px]">
            V-allocate is an agent that allocates your people across every live
            project, then hands a partner a decision to confirm. It runs on
            V-brain — so it weighs what your partners actually know, not just
            who happens to be free.
          </p>

          <div className="mt-9 flex animate-fade-up flex-col gap-3 [animation-delay:240ms] sm:flex-row sm:items-center">
            <a
              href="#waitlist"
              className="group relative inline-flex items-center justify-center overflow-hidden rounded-full bg-green-accent px-6 py-3.5 text-[15px] font-semibold text-teal transition-transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <span className="relative z-10">Join the early-access waitlist</span>
              <span className="absolute inset-0 -translate-x-full bg-green-light/50 transition-transform duration-500 group-hover:translate-x-0" />
            </a>
            <a
              href="#book"
              className="inline-flex items-center justify-center rounded-full border border-white/20 px-6 py-3.5 text-[15px] font-medium text-offwhite transition-colors hover:border-green-light/50 hover:bg-white/5"
            >
              Book a discovery call
            </a>
          </div>
        </div>
      </section>

      {/* NOT A RECOMMENDER */}
      <section className="relative bg-teal-deep">
        <div aria-hidden className="grain pointer-events-none absolute inset-0 opacity-50" />
        <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
          <Reveal className="max-w-2xl">
            <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
              Why it&apos;s different
            </p>
            <h2 className="mt-3 text-balance text-[30px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[42px]">
              Availability matching is the easy 10%.
            </h2>
            <p className="mt-5 text-[17px] leading-relaxed text-white/60">
              Any tool can read a calendar. None of them know the things that
              actually decide an allocation — the judgment that lives in your
              partners&apos; heads and in the conversations they have with each
              other. V-allocate captures that through V-brain, and acts on it.
            </p>
          </Reveal>

          <div className="mt-14 grid gap-4 md:grid-cols-3">
            {contrasts.map((c, i) => (
              <Reveal
                key={c.tool}
                delay={i * 100}
                className="rounded-2xl border border-white/8 bg-white/[0.02] p-6"
              >
                <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-white/35">
                  A normal tool
                </p>
                <p className="mt-2 text-[15px] leading-relaxed text-white/55">
                  {c.tool}
                </p>
                <div className="my-4 h-px w-full bg-gradient-to-r from-green-accent/40 to-transparent" />
                <p className="text-[12px] font-semibold uppercase tracking-[0.12em] text-green-light">
                  V-allocate
                </p>
                <p className="mt-2 text-[15px] leading-relaxed text-offwhite">
                  {c.brain}
                </p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* FLOW DIAGRAM */}
      <section className="relative bg-teal-black">
        <div
          aria-hidden
          className="pointer-events-none absolute left-1/2 top-0 h-px w-2/3 -translate-x-1/2 bg-gradient-to-r from-transparent via-green-accent/40 to-transparent"
        />
        <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
          <Reveal className="mx-auto max-w-2xl text-center">
            <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-light">
              Under the hood
            </p>
            <h2 className="mt-3 text-balance text-[30px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[42px]">
              Every input. One confirmed decision.
            </h2>
            <p className="mt-5 text-[17px] leading-relaxed text-white/60">
              Demand, supply, and the context that usually never leaves a
              partner&apos;s head — all weighed by the engine, all the way to a
              named consultant on a start date.
            </p>
          </Reveal>

          <Reveal className="mt-14" delay={120}>
            <AllocateFlow />
          </Reveal>
        </div>
      </section>

      {/* AGENTIC + HUMAN IN THE LOOP */}
      <section className="relative bg-teal-deep">
        <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-28">
          <Reveal className="max-w-2xl">
            <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
              Agentic, with a human in the loop
            </p>
            <h2 className="mt-3 text-balance text-[30px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[42px]">
              An agent that acts. A partner who confirms.
            </h2>
          </Reveal>

          <div className="mt-14 grid gap-10 md:grid-cols-3">
            {loop.map((s, i) => (
              <Reveal key={s.step} delay={i * 120}>
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

      {/* SOURCE OF TRUTH */}
      <section className="relative bg-teal-black">
        <div className="mx-auto max-w-content px-5 pb-24 pt-4 sm:px-8 sm:pb-28">
          <Reveal className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-9 sm:p-14">
            <div className="grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:gap-16">
              <div>
                <p className="text-[13px] font-semibold uppercase tracking-[0.16em] text-green-accent">
                  The source of truth
                </p>
                <h2 className="mt-3 text-balance text-[28px] font-semibold leading-[1.1] tracking-tightish text-offwhite sm:text-[36px]">
                  One place that knows who&apos;s on what.
                </h2>
                <p className="mt-5 text-[16px] leading-relaxed text-white/60">
                  As adoption grows, V-allocate replaces the scattered
                  spreadsheets, system updates, and inbox threads. It becomes the
                  system of record for staffing — and everything it learns flows
                  back into V-brain, making every other agent sharper too.
                </p>
              </div>
              <div className="grid gap-3">
                {[
                  "Live, firm-wide view of every allocation",
                  "Reasoning recorded for every decision",
                  "Outcomes tracked and fed back",
                  "Feeds the brain that powers every agent",
                ].map((t) => (
                  <div
                    key={t}
                    className="flex items-center gap-3 rounded-xl border border-white/8 bg-white/[0.02] px-4 py-3 text-[14px] text-white/70"
                  >
                    <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-green-light shadow-[0_0_10px_rgba(169,253,172,0.8)]" />
                    {t}
                  </div>
                ))}
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <CTASection />
      <Footer />
    </main>
  );
}
