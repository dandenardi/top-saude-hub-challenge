import { api } from "@/lib/api";
import ProductsTableClient from "@/components/ProductsTableClient";

export default async function ProductsPage({
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

  const rows = await api.products.list(params);

  return (
    <main style={{ padding: 24 }}>
      <h1>Produtos</h1>
      <form method="get" style={{ margin: "12px 0", display: "flex", gap: 8 }}>
        <label htmlFor="q">Filtro</label>
        <input
          id="q"
          name="q"
          defaultValue={q}
          placeholder="Buscar por nome/SKU"
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

      <ProductsTableClient rows={rows} />
    </main>
  );
}
