"use client";

import { useState, type FormEvent } from "react";

type Status = "idle" | "submitting" | "success" | "error";

const STATIC_FORMS_ENDPOINT = "https://api.staticforms.xyz/submit";
const ACCESS_KEY = process.env.NEXT_PUBLIC_STATICFORMS_KEY;

export default function PreviewIntakeForm() {
  const [status, setStatus] = useState<Status>("idle");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);

    // Custom honeypot: if a bot filled "company", silently "succeed" and bail.
    if (((data.get("company") as string | null) ?? "").trim() !== "") {
      setStatus("success");
      return;
    }

    const name = ((data.get("name") as string) ?? "").trim();
    const email = ((data.get("email") as string) ?? "").trim();
    const url = ((data.get("url") as string) ?? "").trim();

    setStatus("submitting");

    try {
      const res = await fetch(STATIC_FORMS_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          accessKey: ACCESS_KEY,
          name,
          email,
          subject: `Preview request from ${name} — ${url}`,
          message: `Current site: ${url}`,
          replyTo: email,
          honeypot: "",
        }),
      });
      setStatus(res.ok ? "success" : "error");
    } catch {
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <>
        <h3>Got it — we&apos;ll reply within one business day.</h3>
        <p className="note">
          We review every submission personally. Keep an eye on your inbox from ron@getrootedmedia.com.
        </p>
      </>
    );
  }

  return (
    <form onSubmit={handleSubmit} method="POST" data-form="preview-intake">
      <div className="field">
        <label htmlFor="name">Your name</label>
        <input id="name" name="name" type="text" required autoComplete="name" />
      </div>
      <div className="field">
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" required autoComplete="email" />
      </div>
      <div className="field full">
        <label htmlFor="url">Your current website URL</label>
        <input id="url" name="url" type="url" placeholder="https://" required />
      </div>
      {/* honeypot */}
      <input
        type="text"
        name="company"
        autoComplete="off"
        tabIndex={-1}
        style={{ position: "absolute", left: "-9999px" }}
        aria-hidden="true"
      />
      {status === "error" && (
        <div
          role="alert"
          style={{
            gridColumn: "1 / -1",
            color: "#b3261e",
            fontFamily: "var(--font-body)",
            fontSize: 14,
            lineHeight: 1.5,
          }}
        >
          Something went wrong. Try again or call (352) 598-7289.
        </div>
      )}
      <button type="submit" disabled={status === "submitting"}>
        {status === "submitting" ? "Sending…" : "Send me my preview →"}
      </button>
      <div className="fine">
        We reply within one business day. We never sell your email. Marion County contractors only.
      </div>
    </form>
  );
}
