import React from 'react';

type Column<T> = { key: keyof T; header: string; render?: (row: T) => React.ReactNode };

type Props<T> = {
  columns: Column<T>[];
  rows: T[];
  page?: number;
  pageSize?: number;
  total?: number;
  onPageChange?: (p: number) => void;
  onSortChange?: (s: string) => void; // ex: "name:asc"
};

export function DataTable<T extends { id: number }>({ columns, rows }: Props<T>) {
  return (
    <div style={{ overflowX: 'auto', border: '1px solid #e5e7eb', borderRadius: 8 }}>
      <table style={{ width: '100%' }}>
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={String(c.key)} style={{ textAlign: 'left', padding: '8px 12px', background: '#f9fafb' }}>{c.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} style={{ borderTop: '1px solid #e5e7eb' }}>
              {columns.map((c) => (
                <td key={String(c.key)} style={{ padding: '8px 12px' }}>
                  {c.render ? c.render(r) : String(r[c.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
