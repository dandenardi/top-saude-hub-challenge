import { ApiError, parseJsonSafe } from "./api-error";

export type ApiEnvelope<T> = {
  cod_retorno: 0 | 1;
  mensagem?: string | null;
  data: T | null;
};

export type Product = {
  id: number;
  name: string;
  sku: string;
  price: number;
  stock_qty: number;
  is_active: boolean;
};

export type Customer = {
  id: number;
  name: string;
  email: string;
  document: string;
};

export type OrderItemOut = {
  id: number;
  product_id: number;
  unit_price: number;
  quantity: number;
  line_total: number;
};
export type OrderOut = {
  id: number;
  customer_id: number;
  total_amount: number;
  status: string;
  items: OrderItemOut[];
};

const isServer = typeof window === "undefined";

const BASE = isServer ? process.env.API_INTERNAL_URL || "http://api:8000" : "";

function emitApiError(msg: string) {
  if (typeof window !== "undefined") {
    window.dispatchEvent(new CustomEvent("api-error", { detail: msg }));
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const clean = path.startsWith("/api") ? path : `/api${path}`;
  const url = `${BASE}${clean}`;
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });

  const json = await parseJsonSafe(res);
  if (json && typeof json === "object" && "cod_retorno" in json) {
    if (!res.ok || json.cod_retorno === 1) {
      const msg = (json as any).mensagem || `Erro ${res.status}`;
      emitApiError(msg);
      throw new ApiError(res.status, msg);
    }
    return (json as any).data as T;
  }

  if (!res.ok) {
    let msg = `Erro ${res.status}`;
    try {
      const text = await res.clone().text();
      if (text && text !== "" && text.length < 500) msg = text;
    } catch {}
    emitApiError(msg);
    throw new ApiError(res.status, msg);
  }

  return json as T;
}

export const api = {
  products: {
    list: (params?: URLSearchParams) =>
      apiFetch<Product[]>(`/api/products?${params?.toString() ?? ""}`),
    get: (id: number) => apiFetch(`/api/products/${id}`),
    create: (body: Omit<Product, "id" | "created_at">) =>
      apiFetch<Product>("/api/products", {
        method: "POST",
        body: JSON.stringify(body),
      }),
    update: (id: number, body: any) =>
      apiFetch(`/api/products/${id}`, {
        method: "PUT",
        body: JSON.stringify(body),
      }),
    remove: (id: number) =>
      apiFetch(`/api/products/${id}`, { method: "DELETE" }),
  },
  customers: {
    list: (params?: URLSearchParams) =>
      apiFetch<Customer[]>(`/api/customers?${params?.toString() ?? ""}`),
    create: (body: Omit<Customer, "id">) =>
      apiFetch<Customer>("/api/customers", {
        method: "POST",
        body: JSON.stringify(body),
      }),
  },
  orders: {
    create: (
      body: {
        customer_id: number;
        items: { product_id: number; quantity: number }[];
      },
      idempotencyKey?: string
    ) =>
      apiFetch<OrderOut>("/api/orders", {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Idempotency-Key":
            idempotencyKey ?? globalThis.crypto?.randomUUID?.() ?? "manual-key",
        },
      }),
  },
};
