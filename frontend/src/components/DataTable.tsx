import React from "react";

type Column<T> = {
  key: keyof T;
  header: string;
  render?: (row: T) => React.ReactNode;
};

type Props<T> = {
  columns: Column<T>[];
  rows: T[];
  page?: number;
  pageSize?: number;
  total?: number;
  sort?: { key: string; dir: "asc" | "desc" } | null;
  onPageChange?: (p: number) => void;
  onSortChange?: (s: { key: string; dir: "asc" | "desc" }) => void;
};

export function DataTable<T extends { id: number | string }>({
  columns,
  rows,
  page,
  pageSize,
  total,
  sort,
  onPageChange,
  onSortChange,
}: Props<T>) {
  const sortable = Boolean(onSortChange);
  const hasPagerInputs =
    typeof page === "number" && typeof pageSize === "number" && !!onPageChange;

  const shouldHidePager =
    hasPagerInputs &&
    !total &&
    (page as number) === 1 &&
    rows.length < (pageSize as number);

  const hasPager = hasPagerInputs && !shouldHidePager;

  const totalPages =
    hasPager && total && pageSize
      ? Math.max(1, Math.ceil(total / pageSize))
      : undefined;

  const disablePrev = hasPager ? (page as number) <= 1 : true;

  const disableNext = hasPager
    ? total
      ? typeof totalPages === "number" && (page as number) >= totalPages
      : rows.length < (pageSize as number)
    : true;

  return (
    <div>
      <table role="table" style={{ width: "100%", borderCollapse: "collapse" }}>
        <caption className="sr-only">Tabela de dados</caption>
        <thead>
          <tr>
            {columns.map((c) => {
              const key = String(c.key);
              const isSorted = sort?.key === key;
              const ariaSort: "none" | "ascending" | "descending" = isSorted
                ? sort!.dir === "asc"
                  ? "ascending"
                  : "descending"
                : "none";

              const toggleSort = () => {
                if (!onSortChange) return;
                onSortChange({
                  key,
                  dir: isSorted && sort?.dir === "asc" ? "desc" : "asc",
                });
              };

              return (
                <th
                  key={key}
                  scope="col"
                  aria-sort={ariaSort}
                  tabIndex={sortable ? 0 : -1}
                  onClick={sortable ? toggleSort : undefined}
                  onKeyDown={
                    sortable
                      ? (e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            toggleSort();
                          }
                        }
                      : undefined
                  }
                  style={{
                    textAlign: "left",
                    cursor: sortable ? "pointer" : "default",
                    padding: "8px 12px",
                  }}
                >
                  {c.header} {isSorted ? (sort!.dir === "asc" ? "▲" : "▼") : ""}
                </th>
              );
            })}
          </tr>
        </thead>

        <tbody>
          {rows.map((r) => (
            <tr
              key={String((r as any).id)}
              style={{ borderTop: "1px solid #e5e7eb" }}
            >
              {columns.map((c) => (
                <td key={String(c.key)} style={{ padding: "8px 12px" }}>
                  {c.render
                    ? c.render(r)
                    : String((r as any)[c.key as keyof T])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {hasPager && (
        <nav
          aria-label="Paginação"
          style={{
            display: "flex",
            gap: 8,
            alignItems: "center",
            marginTop: 12,
          }}
        >
          <button
            onClick={() => onPageChange!(Math.max(1, (page as number) - 1))}
            disabled={disablePrev}
            aria-disabled={disablePrev}
          >
            ← Anterior
          </button>

          <span>
            Página <strong>{page}</strong>
            {typeof totalPages === "number" ? (
              <>
                {" "}
                de <strong>{totalPages}</strong> — {total} itens
              </>
            ) : null}
          </span>

          <button
            onClick={() => onPageChange!((page as number) + 1)}
            disabled={disableNext}
            aria-disabled={disableNext}
          >
            Próxima →
          </button>
        </nav>
      )}
    </div>
  );
}
