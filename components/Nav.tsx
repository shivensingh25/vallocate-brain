import { Wordmark } from "./Wordmark";

const links = [
  { label: "V-brain", href: "#vbrain" },
  { label: "V-allocate", href: "#vallocate" },
  { label: "How it works", href: "#how" },
  { label: "Who it's for", href: "#audience" },
];

export function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b border-teal/10 bg-offwhite/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 max-w-content items-center justify-between px-5 sm:px-8">
        <Wordmark />

        <div className="hidden items-center gap-8 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-[14px] font-medium text-teal/70 transition-colors hover:text-teal"
            >
              {l.label}
            </a>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <a
            href="#book"
            className="hidden text-[14px] font-medium text-teal/80 transition-colors hover:text-teal sm:inline-flex"
          >
            Book a call
          </a>
          <a
            href="#waitlist"
            className="inline-flex items-center rounded-full bg-teal px-4 py-2 text-[14px] font-medium text-offwhite transition-transform hover:-translate-y-px active:translate-y-0"
          >
            Join early access
          </a>
        </div>
      </nav>
    </header>
  );
}
