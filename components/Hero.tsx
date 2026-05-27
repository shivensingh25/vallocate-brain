import { AllocateMock } from "./AllocateMock";

export function Hero() {
  return (
    <section
      id="top"
      className="relative overflow-hidden bg-teal text-offwhite"
    >
      {/* ambient glow */}
      <div
        aria-hidden
        className="pointer-events-none absolute -top-40 right-[-10%] h-[520px] w-[520px] rounded-full bg-green-accent/20 blur-[120px]"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute bottom-[-30%] left-[-10%] h-[420px] w-[420px] rounded-full bg-green-light/10 blur-[120px]"
      />
      <div aria-hidden className="grain absolute inset-0 opacity-60" />

      <div className="relative mx-auto grid max-w-content items-center gap-14 px-5 py-20 sm:px-8 sm:py-28 lg:grid-cols-[1.05fr_0.95fr] lg:py-32">
        <div className="animate-fade-up">
          <span className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-3 py-1 text-[12px] font-medium uppercase tracking-[0.14em] text-green-light">
            <span className="h-1.5 w-1.5 rounded-full bg-green-light" />
            V-brain · by VisagioX
          </span>

          <h1 className="mt-6 text-balance text-[40px] font-semibold leading-[1.05] tracking-tightish sm:text-[54px] lg:text-[60px]">
            Your firm already knows how to decide.{" "}
            <span className="text-green-light">V-brain learns it.</span>
          </h1>

          <p className="mt-6 max-w-xl text-pretty text-[17px] leading-relaxed text-white/70 sm:text-[18px]">
            A passive intelligence layer that captures how your consultants and
            partners actually make decisions — from the artifacts of daily work,
            not a pile of indexed documents. It runs in the background and gets
            sharper with every outcome.
          </p>

          <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:items-center">
            <a
              href="#waitlist"
              className="inline-flex items-center justify-center rounded-full bg-green-accent px-6 py-3.5 text-[15px] font-semibold text-teal transition-transform hover:-translate-y-px active:translate-y-0"
            >
              Join the early-access waitlist
            </a>
            <a
              href="#book"
              className="inline-flex items-center justify-center rounded-full border border-white/20 px-6 py-3.5 text-[15px] font-medium text-offwhite transition-colors hover:border-white/40 hover:bg-white/5"
            >
              Book a discovery call
            </a>
          </div>

          <p className="mt-6 text-[13px] text-white/45">
            Built for mid-market consulting firms · 50–500 consultants
          </p>
        </div>

        <div className="animate-fade-up [animation-delay:120ms]">
          <AllocateMock />
        </div>
      </div>
    </section>
  );
}
