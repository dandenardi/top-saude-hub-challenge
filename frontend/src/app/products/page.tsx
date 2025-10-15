import { api } from '@/lib/api';
import { DataTable } from '@/components/DataTable';

export default async function ProductsPage() {
  const params = new URLSearchParams({ page: '1', page_size: '20', sort: 'created_at:desc' });
  const rows = await api.products.list(params);
  return (
    <main style={{ padding: 24 }}>
      <h1>Produtos</h1>
      <DataTable columns={[
        { key: 'id', header: 'ID' },
        { key: 'name', header: 'Nome' },
        { key: 'sku', header: 'SKU' },
        { key: 'price', header: 'Preço', render: (r: any) => (r.price/100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) },
        { key: 'stock_qty', header: 'Estoque' },
      ]} rows={rows} />
    </main>
  );
}
