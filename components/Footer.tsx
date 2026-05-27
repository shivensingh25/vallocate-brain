import { Wordmark } from "./Wordmark";

export function Footer() {
  return (
    <footer className="border-t border-white/8 bg-teal-black">
      <div className="mx-auto flex max-w-content flex-col gap-8 px-5 py-12 sm:px-8 md:flex-row md:items-center md:justify-between">
        <div>
          <Wordmark />
          <p className="mt-3 max-w-sm text-[14px] leading-relaxed text-white/45">
            The intelligence layer for how professional services firms decide.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-x-8 gap-y-3 text-[14px] text-white/55">
          <a href="#vbrain" className="transition-colors hover:text-offwhite">
            Platform
          </a>
          <a href="#agents" className="transition-colors hover:text-offwhite">
            Agents
          </a>
          <a href="#waitlist" className="transition-colors hover:text-offwhite">
            Early access
          </a>
          <a href="#book" className="transition-colors hover:text-offwhite">
            Book a call
          </a>
        </div>
      </div>
      <div className="border-t border-white/8">
        <div className="mx-auto flex max-w-content flex-col gap-2 px-5 py-6 text-[13px] text-white/35 sm:flex-row sm:items-center sm:justify-between sm:px-8">
          <span>© {new Date().getFullYear()} VisagioX. All rights reserved.</span>
          <span className="flex gap-6">
            <a href="#" className="transition-colors hover:text-white/60">
              Privacy
            </a>
            <a href="#" className="transition-colors hover:text-white/60">
              Terms
            </a>
          </span>
        </div>
      </div>
    </footer>
  );
}
