import { BrainCore } from "./BrainCore";

export function Hero() {
  return (
    <section id="top" className="relative overflow-hidden bg-teal-deep">
      <div aria-hidden className="mesh pointer-events-none absolute inset-0" />
      <div aria-hidden className="dotgrid pointer-events-none absolute inset-0" />
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-teal-deep"
      />

      <div className="relative mx-auto grid max-w-content items-center gap-16 px-5 py-20 sm:px-8 sm:py-28 lg:grid-cols-[1.08fr_0.92fr] lg:py-32">
        <div>
          <span className="inline-flex animate-fade-up items-center gap-2 rounded-full border border-white/12 bg-white/[0.04] px-3 py-1 text-[12px] font-medium uppercase tracking-[0.14em] text-green-light">
            <span className="h-1.5 w-1.5 animate-twinkle rounded-full bg-green-light" />
            The company brain · by VisagioX
          </span>

          <h1 className="mt-6 animate-fade-up text-balance text-[42px] font-semibold leading-[1.02] tracking-tighter2 [animation-delay:80ms] sm:text-[58px] lg:text-[66px]">
            One brain behind
            <br className="hidden sm:block" /> every decision your{" "}
            <span className="text-glow text-green-light">firm makes.</span>
          </h1>

          <p className="mt-6 max-w-xl animate-fade-up text-pretty text-[17px] leading-relaxed text-white/70 [animation-delay:160ms] sm:text-[18px]">
            V-brain is a passive intelligence layer that learns how your people
            actually work — from the artifacts of daily work, not a pile of
            indexed documents. Agents run on top of it. V-allocate is the first.
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

          <p className="mt-6 animate-fade-up text-[13px] text-white/45 [animation-delay:320ms]">
            Built for professional services firms · 50–500 people
          </p>
        </div>

        <div className="animate-fade-up [animation-delay:200ms]">
          <BrainCore />
        </div>
      </div>
    </section>
  );
}
