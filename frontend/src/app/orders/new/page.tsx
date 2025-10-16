"use client";
import * as React from "react";
import { api } from "@/lib/api";
import { Typeahead } from "@/components/Typeahead";

export default function NewOrderPage() {
  const [customerId, setCustomerId] = React.useState<number | null>(1);
  const [items, setItems] = React.useState<
    { id: number; name: string; price: number; qty: number }[]
  >([]);

  const addItem = (p: any) => {
    setItems((prev) => {
      const idx = prev.findIndex((x) => x.id === p.id);
      if (idx >= 0) {
        const c = [...prev];
        c[idx].qty += 1;
        return c;
      }
      return [...prev, { id: p.id, name: p.name, price: p.price, qty: 1 }];
    });
  };

  const total = items.reduce((acc, it) => acc + it.price * it.qty, 0);

  const submit = async () => {
    if (!customerId || items.length === 0)
      return alert("Selecione cliente e itens");
    const payload = {
      customer_id: customerId,
      items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
    };
    const res = await api.orders.create(payload);
    alert(
      `Pedido criado #${res.id} total ${(res.total_amount / 100).toLocaleString(
        "pt-BR",
        { style: "currency", currency: "BRL" }
      )}`
    );
  };

  return (
    <main style={{ padding: 24 }}>
      <h1>Novo Pedido</h1>
      <section
        style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }}
      >
        <div>
          <label style={{ fontSize: 12 }}>Produtos</label>
          <Typeahead
            fetcher={async (q) => {
              const params = new URLSearchParams({
                q,
                page: "1",
                page_size: "10",
              });
              return await api.products.list(params);
            }}
            onSelect={addItem}
          />
        </div>
        <div>
          <label style={{ fontSize: 12 }}>Cliente (ID)</label>
          <input
            type="number"
            value={customerId ?? ""}
            onChange={(e) => setCustomerId(parseInt(e.target.value))}
            style={{
              width: "100%",
              border: "1px solid #e5e7eb",
              borderRadius: 6,
              padding: "8px 12px",
            }}
          />
        </div>
      </section>

      <section style={{ marginTop: 16 }}>
        <h2>Itens</h2>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 8 }}>
          {items.map((it) => (
            <div
              key={it.id}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "8px 12px",
                borderTop: "1px solid #e5e7eb",
              }}
            >
              <div
                style={{
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                }}
              >
                {it.name}
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <input
                  type="number"
                  min={1}
                  value={it.qty}
                  onChange={(e) =>
                    setItems((prev) =>
                      prev.map((p) =>
                        p.id === it.id
                          ? { ...p, qty: Math.max(1, parseInt(e.target.value)) }
                          : p
                      )
                    )
                  }
                  style={{
                    width: 64,
                    border: "1px solid #e5e7eb",
                    borderRadius: 6,
                    padding: "4px 8px",
                  }}
                />
                <div style={{ width: 120, textAlign: "right" }}>
                  {((it.price * it.qty) / 100).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
        <div style={{ textAlign: "right", fontWeight: 600, marginTop: 8 }}>
          Total{" "}
          {(total / 100).toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL",
          })}
        </div>
        <button
          onClick={submit}
          disabled={!customerId || items.length === 0}
          style={{
            marginTop: 12,
            padding: "8px 16px",
            borderRadius: 8,
            border: "none",
            background: "#111827",
            color: "#fff",
            opacity: !customerId || items.length === 0 ? 0.5 : 1,
            cursor:
              !customerId || items.length === 0 ? "not-allowed" : "pointer",
          }}
        >
          Criar pedido
        </button>
      </section>
    </main>
  );
}
