"use client";
import * as React from "react";

type Toast = { id: number; message: string };
type Ctx = { show: (message: string) => void };

const ToastCtx = React.createContext<Ctx | null>(null);

export function useToast() {
  const ctx = React.useContext(ToastCtx);
  if (!ctx) throw new Error("ToastProvider ausente");
  return ctx;
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<Toast[]>([]);
  const idRef = React.useRef(1);

  const show = React.useCallback((message: string) => {
    const id = idRef.current++;
    setToasts((t) => [...t, { id, message }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 4500);
  }, []);

  React.useEffect(() => {
    const onRejection = (e: PromiseRejectionEvent) => {
      const r: any = e.reason;
      const msg = r?.message || String(r) || "Erro inesperado";
      show(msg);
    };
    const onError = (e: ErrorEvent) => {
      show(e.message || "Erro inesperado");
    };
    const onApiError = (e: Event) => {
      const ce = e as CustomEvent<string>;
      if (typeof ce.detail === "string" && ce.detail) show(ce.detail);
    };
    window.addEventListener("unhandledrejection", onRejection);
    window.addEventListener("error", onError);
    window.addEventListener("api-error", onApiError as EventListener);
    return () => {
      window.removeEventListener("unhandledrejection", onRejection);
      window.removeEventListener("error", onError);
      window.removeEventListener("api-error", onApiError as EventListener);
    };
  }, [show]);

  return (
    <ToastCtx.Provider value={{ show }}>
      {children}
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: "fixed",
          right: 16,
          bottom: 16,
          display: "grid",
          gap: 8,
          zIndex: 9999,
          pointerEvents: "none",
        }}
      >
        {toasts.map((t) => (
          <div
            key={t.id}
            role="alert"
            style={{
              pointerEvents: "auto",
              background: "#111827",
              color: "#fff",
              padding: "10px 12px",
              borderRadius: 8,
              boxShadow: "0 8px 24px rgba(0,0,0,0.2)",
              maxWidth: 360,
            }}
          >
            {t.message}
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}
