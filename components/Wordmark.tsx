export function Wordmark() {
  return (
    <a
      href="/"
      className="group inline-flex items-baseline gap-2 select-none"
      aria-label="VisagioX home"
    >
      <span className="text-[17px] font-semibold tracking-tightish text-offwhite">
        Visagio<span className="text-green-accent">X</span>
      </span>
      <span className="h-3 w-px bg-white/20" aria-hidden />
      <span className="text-[13px] font-medium text-white/50">V-brain</span>
    </a>
  );
}
