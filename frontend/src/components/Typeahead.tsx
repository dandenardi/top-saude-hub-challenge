'use client';
import * as React from 'react';

export function Typeahead({ fetcher, onSelect }: { fetcher: (q: string) => Promise<any[]>; onSelect: (item: any) => void }) {
  const [q, setQ] = React.useState('');
  const [items, setItems] = React.useState<any[]>([]);

  React.useEffect(() => {
    const t = setTimeout(async () => {
      if (q.length < 2) return setItems([]);
      try {
        setItems(await fetcher(q));
      } catch {
        setItems([]);
      }
    }, 250);
    return () => clearTimeout(t);
  }, [q, fetcher]);

  return (
    <div style={{ position: 'relative' }}>
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Buscar produto..." style={{ width: '100%', border: '1px solid #e5e7eb', borderRadius: 6, padding: '8px 12px' }} />
      {items.length > 0 && (
        <ul style={{ position: 'absolute', zIndex: 10, marginTop: 4, width: '100%', background: '#fff', border: '1px solid #e5e7eb', borderRadius: 6, boxShadow: '0 6px 24px rgba(0,0,0,0.06)' }}>
          {items.map((it) => (
            <li key={it.id} style={{ padding: '8px 12px', cursor: 'pointer' }}
                onClick={() => { onSelect(it); setQ(''); setItems([]); }}>
              {it.name} — {(it.price/100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
