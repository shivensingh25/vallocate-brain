"use client";

import { useEffect, useRef } from "react";

declare global {
  interface Window {
    Tally?: { loadEmbeds: () => void };
  }
}

const TALLY_FORM_ID = "zxLo7E";
const TALLY_SCRIPT_SRC = "https://tally.so/widgets/embed.js";

export function WaitlistForm() {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    // Ensure Tally's auto-resize/embed script is loaded once.
    const existing = document.querySelector<HTMLScriptElement>(
      `script[src="${TALLY_SCRIPT_SRC}"]`
    );

    const onReady = () => {
      if (window.Tally) window.Tally.loadEmbeds();
    };

    if (existing) {
      onReady();
      return;
    }

    const script = document.createElement("script");
    script.src = TALLY_SCRIPT_SRC;
    script.async = true;
    script.onload = onReady;
    document.body.appendChild(script);
  }, []);

  const src = `https://tally.so/embed/${TALLY_FORM_ID}?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1`;

  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4 sm:p-5">
      <iframe
        ref={iframeRef}
        data-tally-src={src}
        src={src}
        title="Join the V-brain early-access waitlist"
        loading="lazy"
        width="100%"
        height="220"
        frameBorder={0}
        marginHeight={0}
        marginWidth={0}
        className="w-full"
      />
    </div>
  );
}
