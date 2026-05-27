export function Wordmark({ light = false }: { light?: boolean }) {
  return (
    <a
      href="#top"
      className="group inline-flex items-baseline gap-2 select-none"
      aria-label="VisagioX home"
    >
      <span
        className={`text-[17px] font-semibold tracking-tightish ${
          light ? "text-offwhite" : "text-teal"
        }`}
      >
        Visagio
        <span className="text-green-accent">X</span>
      </span>
      <span
        className={`h-3 w-px ${light ? "bg-white/25" : "bg-teal/20"}`}
        aria-hidden
      />
      <span
        className={`text-[13px] font-medium ${
          light ? "text-white/55" : "text-teal/55"
        }`}
      >
        V-brain
      </span>
    </a>
  );
}
