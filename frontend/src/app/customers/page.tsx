import { api, type Customer } from "@/lib/api";
import { DataTable } from "@/components/DataTable";

export default async function CustomersPage() {
  const rows: Customer[] = await api.customers.list(
    new URLSearchParams({ page: "1", page_size: "20" })
  );
  return (
    <main style={{ padding: 24 }}>
      <h1>Clientes</h1>
      <DataTable<Customer>
        columns={[
          { key: "id", header: "ID" },
          { key: "name", header: "Nome" },
          { key: "email", header: "Email" },
          { key: "document", header: "Documento" },
        ]}
        rows={rows}
      />
    </main>
  );
}
