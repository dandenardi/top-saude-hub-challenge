"use client";
import * as React from "react";

export function Typeahead({
  fetcher,
  onSelect,
}: {
  fetcher: (query: string) => Promise<any[]>;
  onSelect: (item: any) => void;
}) {
  const [query, setQuery] = React.useState("");
  const [items, setItems] = React.useState<any[]>([]);
  const [open, setOpen] = React.useState(false);
  const [activeIndex, setActiveIndex] = React.useState(-1);
  const listboxId = "typeahead-list";
  const optionId = (i: number) => `typeahead-option-${i}`;
  const inputRef = React.useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    const t = setTimeout(async () => {
      if (query.length < 2) {
        setItems([]);
        setOpen(false);
        setActiveIndex(-1);
        return;
      }
      try {
        const res = await fetcher(query);
        setItems(res);
        setOpen(res.length > 0);
        setActiveIndex(res.length > 0 ? 0 : -1);
      } catch {
        setItems([]);
        setOpen(false);
        setActiveIndex(-1);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [query, fetcher]);

  const commitSelection = (idx: number) => {
    const it = items[idx];
    if (!it) return;
    onSelect(it);
    setQuery("");
    setItems([]);
    setOpen(false);
    setActiveIndex(-1);
  };

  const onKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (!open && (e.key === "ArrowDown" || e.key === "ArrowUp")) {
      setOpen(items.length > 0);
      return;
    }
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setActiveIndex((i: number) => (i + 1) % items.length);
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((i: number) => (i - 1 + items.length) % items.length);
        break;
      case "Home":
        if (open) {
          e.preventDefault();
          setActiveIndex(0);
        }
        break;
      case "End":
        if (open) {
          e.preventDefault();
          setActiveIndex(items.length - 1);
        }
        break;
      case "Enter":
        if (open && activeIndex >= 0) {
          e.preventDefault();
          commitSelection(activeIndex);
        }
        break;
      case "Escape":
        if (open) {
          e.preventDefault();
          setOpen(false);
          setActiveIndex(-1);
        }
        break;
    }
  };

  React.useEffect(() => {
    if (!open) return;
    const el = document.getElementById(optionId(activeIndex));
    el?.scrollIntoView({ block: "nearest" });
  }, [activeIndex, open]);

  return (
    <div style={{ position: "relative" }}>
      <input
        ref={inputRef}
        role="combobox"
        aria-expanded={open}
        aria-controls={listboxId}
        aria-autocomplete="list"
        aria-activedescendant={
          open && activeIndex >= 0 ? optionId(activeIndex) : undefined
        }
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(false);
        }}
        onKeyDown={onKeyDown}
        placeholder="Buscar produto..."
        autoComplete="off"
        style={{
          width: "100%",
          border: "1px solid #e5e7eb",
          borderRadius: 6,
          padding: "8px 12px",
        }}
        onBlur={(e) => {
          const next = e.relatedTarget as HTMLElement | null;
          if (next?.getAttribute("role") === "option") return;
          setOpen(false);
        }}
      />

      {open && items.length > 0 && (
        <ul
          id={listboxId}
          role="listbox"
          tabIndex={-1}
          style={{
            position: "absolute",
            zIndex: 10,
            marginTop: 4,
            width: "100%",
            background: "#fff",
            border: "1px solid #e5e7eb",
            borderRadius: 6,
            boxShadow: "0 6px 24px rgba(0,0,0,0.06)",
            maxHeight: 240,
            overflowY: "auto",
          }}
        >
          {items.map((it, i) => {
            const isActive = i === activeIndex;
            return (
              <li
                key={it.id}
                id={optionId(i)}
                role="option"
                aria-selected={isActive}
                tabIndex={-1}
                style={{
                  padding: "8px 12px",
                  cursor: "pointer",
                  background: isActive ? "#f3f4f6" : "transparent",
                }}
                onMouseEnter={() => setActiveIndex(i)}
                onMouseDown={(e) => e.preventDefault()} // evita blur do input antes do click
                onClick={() => commitSelection(i)}
              >
                {it.name} —{" "}
                {(it.price / 100).toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                })}
              </li>
            );
          })}
        </ul>
      )}

      {/* opcional: região para anunciar quantidade de resultados */}
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: "absolute",
          width: 1,
          height: 1,
          overflow: "hidden",
          clip: "rect(1px, 1px, 1px, 1px)",
        }}
      >
        {open
          ? `${items.length} resultado${items.length !== 1 ? "s" : ""}`
          : ""}
      </div>
    </div>
  );
}
