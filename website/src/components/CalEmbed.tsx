"use client";

import { useEffect } from "react";

export default function CalEmbed() {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://app.cal.com/embed/embed.js";
    script.async = true;
    script.onload = () => {
      // @ts-expect-error Cal is loaded from external script
      if (typeof Cal !== "undefined") {
        // @ts-expect-error Cal is loaded from external script
        Cal("inline", {
          elementOrSelector: "#cal-booking-embed",
          calLink: "ron-kolb-cdlgsw/30min",
          config: { layout: "month_view" },
        });
      }
    };
    document.head.appendChild(script);

    return () => {
      if (script.parentNode) {
        script.parentNode.removeChild(script);
      }
    };
  }, []);

  return (
    <div
      id="cal-booking-embed"
      style={{ minHeight: 600, width: "100%" }}
    />
  );
}
