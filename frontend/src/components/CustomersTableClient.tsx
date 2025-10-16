"use client";
import * as React from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { DataTable } from "@/components/DataTable";

export type CustomerRow = {
  id: number;
  name: string;
  email: string;
  document?: string | null;
};

type Props = { rows: CustomerRow[] };

export default function CustomersTableClient({ rows }: Props) {
  const router = useRouter();
  const sp = useSearchParams();

  const page = Number(sp.get("page") || "1");
  const pageSize = Number(sp.get("page_size") || "20");
  const sortRaw = sp.get("sort") || "created_at:desc";
  const [sortKey, sortDir] = sortRaw.split(":");

  const buildUrl = React.useCallback(
    (patch: Record<string, string | number | null>) => {
      const next = new URLSearchParams(sp.toString());
      for (const [k, v] of Object.entries(patch)) {
        if (v === null) next.delete(k);
        else next.set(k, String(v));
      }
      return `?${next.toString()}`;
    },
    [sp]
  );

  return (
    <DataTable
      columns={[
        { key: "id", header: "ID" },
        { key: "name", header: "Nome" },
        { key: "email", header: "E-mail" },
        { key: "document", header: "Documento" },
      ]}
      rows={rows}
      page={page}
      pageSize={pageSize}
      sort={{ key: sortKey, dir: sortDir === "asc" ? "asc" : "desc" }}
      onPageChange={(p) => router.push(buildUrl({ page: p }))}
      onSortChange={({ key, dir }) =>
        router.push(buildUrl({ sort: `${key}:${dir}`, page: 1 }))
      }
    />
  );
}
