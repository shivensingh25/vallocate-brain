import { WaitlistForm } from "./WaitlistForm";

export function CTASection() {
  return (
    <section className="relative overflow-hidden bg-teal-deep text-offwhite">
      <div
        aria-hidden
        className="pointer-events-none absolute -top-32 left-1/2 h-[460px] w-[760px] -translate-x-1/2 rounded-full bg-green-accent/15 blur-[130px]"
      />
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-20">
          {/* Waitlist */}
          <div id="waitlist" className="scroll-mt-24">
            <h2 className="text-balance text-[30px] font-semibold leading-[1.1] tracking-tightish sm:text-[38px]">
              Join the early-access waitlist.
            </h2>
            <p className="mt-4 max-w-md text-[16px] leading-relaxed text-white/65">
              We&apos;re onboarding a small number of mid-market firms first.
              Add your work email to be considered for the next cohort.
            </p>
            <div className="mt-7">
              <WaitlistForm />
            </div>
            <p className="mt-4 text-[13px] text-white/40">
              No spam. We&apos;ll only email you about early access.
            </p>
          </div>

          {/* Book a call */}
          <div
            id="book"
            className="flex scroll-mt-24 flex-col justify-between rounded-2xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-sm"
          >
            <div>
              <h2 className="text-balance text-[24px] font-semibold leading-[1.15] tracking-tightish sm:text-[28px]">
                Want to see it on your firm&apos;s data?
              </h2>
              <p className="mt-4 text-[16px] leading-relaxed text-white/65">
                Book a 30-minute discovery call. We&apos;ll walk through where
                V-brain fits, what V-allocate would surface for your teams, and
                what early access looks like.
              </p>
            </div>
            <a
              href="#book"
              className="mt-8 inline-flex w-fit items-center justify-center rounded-full border border-white/25 px-6 py-3.5 text-[15px] font-medium text-offwhite transition-colors hover:border-green-accent/60 hover:bg-white/5"
            >
              Book a discovery call
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
