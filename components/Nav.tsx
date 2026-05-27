import { Wordmark } from "./Wordmark";

const links = [
  { label: "Platform", href: "#vbrain" },
  { label: "Agents", href: "#agents" },
  { label: "How it works", href: "#how" },
  { label: "Who it's for", href: "#audience" },
];

export function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/8 bg-teal-deep/70 backdrop-blur-xl">
      <nav className="mx-auto flex h-16 max-w-content items-center justify-between px-5 sm:px-8">
        <Wordmark />

        <div className="hidden items-center gap-8 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-[14px] font-medium text-white/60 transition-colors hover:text-offwhite"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <a
            href="#book"
            className="hidden text-[14px] font-medium text-white/75 transition-colors hover:text-offwhite sm:inline-flex"
          >
            Book a call
          </a>
          <a
            href="#waitlist"
            className="group relative inline-flex items-center overflow-hidden rounded-full bg-green-accent px-4 py-2 text-[14px] font-semibold text-teal transition-transform hover:-translate-y-px active:translate-y-0"
          >
            <span className="relative z-10">Join early access</span>
            <span className="absolute inset-0 -translate-x-full bg-green-light/50 transition-transform duration-500 group-hover:translate-x-0" />
          </a>
        </div>
      </nav>
    </header>
  );
}
