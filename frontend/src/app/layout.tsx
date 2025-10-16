export const metadata = { title: 'Catálogo', description: 'Catálogo e Pedidos' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
