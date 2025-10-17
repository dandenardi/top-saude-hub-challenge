"use client";
import * as React from "react";
import { useForm, Controller, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { api, newIdempotencyKey } from "@/lib/api";
import { Typeahead } from "@/components/Typeahead";
import { useToast } from "@/components/ToastProvider";
import { OrderCreateSchema, type OrderCreateInput } from "@/lib/validation";

export default function NewOrderPage() {
  const { show } = useToast();
  const [idemKey, setIdemKey] = React.useState(newIdempotencyKey());

  const {
    control,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isValid, isSubmitting },
  } = useForm<OrderCreateInput>({
    resolver: zodResolver(OrderCreateSchema),
    mode: "onChange",
    defaultValues: { customer_id: undefined as any, items: [] },
  });

  const { fields, append, update, remove } = useFieldArray({
    control,
    name: "items",
    keyName: "key",
  });
  const items = watch("items");

  const addItem = (product: { id: number; name: string; price: number }) => {
    const idx = items.findIndex((x: any) => x.product_id === product.id);
    idx >= 0
      ? update(idx, {
          ...items[idx],
          product_id: product.id,
          quantity: (items[idx] as any).quantity + 1,
          name: product.name,
          price: product.price,
        } as any)
      : append({
          product_id: product.id,
          quantity: 1,
          name: product.name,
          price: product.price,
        } as any);
  };

  const totalCents = items.reduce(
    (acc, item: any) => acc + (item.price ?? 0) * item.quantity,
    0
  );

  const onSubmit = async (data: OrderCreateInput) => {
    try {
      const payload = {
        customer_id: data.customer_id,
        items: data.items.map((i) => ({
          product_id: i.product_id,
          quantity: i.quantity,
        })),
      };
      const res = await api.orders.create(payload, idemKey);
      setIdemKey(newIdempotencyKey());
      show(
        `Pedido #${res.id} criado: ${(res.total_amount / 100).toLocaleString(
          "pt-BR",
          { style: "currency", currency: "BRL" }
        )}`
      );
    } catch (e: any) {
      show(e?.message ?? "Falha inesperada");
    }
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
            fetcher={async (q) =>
              api.products.list(
                new URLSearchParams({ q, page: "1", page_size: "10" })
              )
            }
            onSelect={addItem}
          />
          {errors.items && (
            <p style={{ color: "#b91c1c" }}>{errors.items.message}</p>
          )}
        </div>

        <div>
          <label style={{ fontSize: 12 }}>Cliente (ID)</label>
          <Controller
            control={control}
            name="customer_id"
            render={({ field }) => (
              <input
                type="number"
                value={field.value ?? ""}
                onChange={(e) =>
                  field.onChange(
                    e.target.value ? parseInt(e.target.value) : undefined
                  )
                }
                style={{
                  width: "100%",
                  border: "1px solid #e5e7eb",
                  borderRadius: 6,
                  padding: "8px 12px",
                }}
              />
            )}
          />
          {errors.customer_id && (
            <p style={{ color: "#b91c1c" }}>{errors.customer_id.message}</p>
          )}
        </div>
      </section>

      <section style={{ marginTop: 16 }}>
        <h2>Itens</h2>
        <div style={{ border: "1px solid #e5e7eb", borderRadius: 8 }}>
          {fields.map((f, index) => (
            <div
              key={f.key}
              style={{
                display: "flex",
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
                title={(items[index] as any)?.name}
              >
                {(items[index] as any)?.name}
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <input
                  type="number"
                  min={1}
                  value={items[index]?.quantity ?? 1}
                  onChange={(e) =>
                    setValue(
                      `items.${index}.quantity`,
                      Math.max(1, parseInt(e.target.value || "1")),
                      { shouldValidate: true }
                    )
                  }
                  style={{
                    width: 64,
                    border: "1px solid #e5e7eb",
                    borderRadius: 6,
                    padding: "4px 8px",
                  }}
                />
                <button
                  type="button"
                  onClick={() => remove(index)}
                  style={{
                    border: "1px solid #e5e7eb",
                    borderRadius: 6,
                    padding: "4px 8px",
                    background: "white",
                  }}
                >
                  Remover
                </button>
                <div style={{ width: 120, textAlign: "right" }}>
                  {(
                    (((items[index] as any)?.price ?? 0) *
                      (items[index]?.quantity ?? 1)) /
                    100
                  ).toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL",
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div
          data-testid="order-total"
          style={{ textAlign: "right", fontWeight: 600, marginTop: 8 }}
        >
          Total{" "}
          {(totalCents / 100).toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL",
          })}
        </div>

        <button
          onClick={handleSubmit(onSubmit)}
          disabled={!isValid || isSubmitting}
          style={{
            marginTop: 12,
            padding: "8px 16px",
            borderRadius: 8,
            border: "none",
            background: "#111827",
            color: "#fff",
            opacity: !isValid || isSubmitting ? 0.5 : 1,
          }}
        >
          {isSubmitting ? "Enviando..." : "Criar pedido"}
        </button>
      </section>
    </main>
  );
}
