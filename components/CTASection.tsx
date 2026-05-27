import { WaitlistForm } from "./WaitlistForm";
import { Reveal } from "./Reveal";

export function CTASection() {
  return (
    <section className="relative overflow-hidden bg-teal-black">
      <div aria-hidden className="mesh pointer-events-none absolute inset-0 opacity-70" />
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-0 h-px w-2/3 -translate-x-1/2 bg-gradient-to-r from-transparent via-green-light/40 to-transparent"
      />
      <div className="relative mx-auto max-w-content px-5 py-24 sm:px-8 sm:py-32">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-20">
          {/* Waitlist */}
          <Reveal id="waitlist" className="scroll-mt-24" as="div">
            <h2 className="text-balance text-[30px] font-semibold leading-[1.08] tracking-tightish text-offwhite sm:text-[40px]">
              Put your firm&apos;s brain to work.
            </h2>
            <p className="mt-4 max-w-md text-[16px] leading-relaxed text-white/65">
              We&apos;re onboarding a small number of firms onto V-brain first,
              starting with V-allocate. Add your work email to be considered for
              the next cohort.
            </p>
            <div className="mt-7">
              <WaitlistForm />
            </div>
            <p className="mt-4 text-[13px] text-white/40">
              No spam. We&apos;ll only email you about early access.
            </p>
          </Reveal>

          {/* Book a call */}
          <Reveal
            id="book"
            as="div"
            delay={100}
            className="flex scroll-mt-24 flex-col justify-between rounded-2xl border border-white/10 bg-white/[0.04] p-8 backdrop-blur-sm"
          >
            <div>
              <h2 className="text-balance text-[24px] font-semibold leading-[1.15] tracking-tightish text-offwhite sm:text-[28px]">
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
              className="mt-8 inline-flex w-fit items-center justify-center rounded-full border border-white/25 px-6 py-3.5 text-[15px] font-medium text-offwhite transition-colors hover:border-green-light/60 hover:bg-white/5"
            >
              Book a discovery call
            </a>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
