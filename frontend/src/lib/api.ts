export type ApiEnvelope<T> = { cod_retorno: 0 | 1; mensagem?: string | null; data: T | null };

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    cache: 'no-store',
  });
  const json: ApiEnvelope<T> = await res.json();
  if (!res.ok || json.cod_retorno === 1) {
    throw new Error(json.mensagem || 'Erro desconhecido');
  }
  return json.data as T;
}

export const api = {
  products: {
    list: (params?: URLSearchParams) => apiFetch(`/api/products?${params?.toString() ?? ''}`),
    create: (body: any) => apiFetch('/api/products', { method: 'POST', body: JSON.stringify(body) }),
  },
  customers: {
    list: (params?: URLSearchParams) => apiFetch(`/api/customers?${params?.toString() ?? ''}`),
  },
  orders: {
    create: (body: any, idempotencyKey?: string) => apiFetch('/api/orders', {
      method: 'POST',
      body: JSON.stringify(body),
      headers: { 'Idempotency-Key': idempotencyKey ?? (globalThis.crypto?.randomUUID?.() ?? 'manual-key') },
    }),
  },
};
