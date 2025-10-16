import { api, type Customer } from "@/lib/api";
import CustomersTableClient from "@/components/CustomersTableClient";

export default async function CustomersPage({
  searchParams,
}: {
  searchParams: Record<string, string | undefined>;
}) {
  const page = searchParams.page ?? "1";
  const page_size = searchParams.page_size ?? "20";
  const sort = searchParams.sort ?? "created_at:desc";
  const q = searchParams.q ?? "";

  const params = new URLSearchParams({ page, page_size, sort });
  if (q) params.set("q", q);

  const rows = (await api.customers.list(params)) as Customer[];

  return (
    <main style={{ padding: 24 }}>
      <h1>Clientes</h1>
      <form method="get" style={{ margin: "12px 0", display: "flex", gap: 8 }}>
        <label htmlFor="q">Filtro</label>
        <input
          id="q"
          name="q"
          defaultValue={q}
          placeholder="Buscar por nome/e-mail"
        />
        <button type="submit">Filtrar</button>
        {q ? (
          <a
            href="?page=1&page_size=20&sort=created_at:desc"
            style={{ marginLeft: 8 }}
          >
            Limpar
          </a>
        ) : null}
      </form>

      <CustomersTableClient rows={rows} />
    </main>
  );
}
