"use client";

import { useState } from "react";

export function WaitlistForm() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    // Placeholder: wire this to your waitlist backend (e.g. Formspree, API route).
    if (!email) return;
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div className="rounded-2xl border border-green-accent/30 bg-green-light/10 p-6 text-left">
        <p className="text-[15px] font-semibold text-green-light">
          You&apos;re on the list.
        </p>
        <p className="mt-1.5 text-[14px] leading-relaxed text-white/70">
          We&apos;ll be in touch as early-access spots open up for{" "}
          <span className="text-green-light">{email}</span>.
        </p>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-3 sm:flex-row"
      noValidate
    >
      <label htmlFor="waitlist-email" className="sr-only">
        Work email
      </label>
      <input
        id="waitlist-email"
        type="email"
        required
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@firm.com"
        className="w-full flex-1 rounded-full border border-white/15 bg-white/5 px-5 py-3.5 text-[15px] text-offwhite placeholder:text-white/35 outline-none transition-colors focus:border-green-accent/60 focus:bg-white/10"
      />
      <button
        type="submit"
        className="shrink-0 rounded-full bg-green-accent px-6 py-3.5 text-[15px] font-semibold text-teal transition-transform hover:-translate-y-px active:translate-y-0"
      >
        Request access
      </button>
    </form>
  );
}
