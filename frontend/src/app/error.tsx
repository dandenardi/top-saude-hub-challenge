"use client";
import * as React from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <main style={{ padding: 24 }}>
          <h1>Ocorreu um erro</h1>
          <div
            role="alert"
            style={{
              background: "#fee2e2",
              border: "1px solid #fecaca",
              padding: 12,
              borderRadius: 8,
            }}
          >
            {error.message || "Falha inesperada. Tente novamente."}
          </div>
          <button style={{ marginTop: 12 }} onClick={() => reset()}>
            Tentar novamente
          </button>
        </main>
      </body>
    </html>
  );
}
