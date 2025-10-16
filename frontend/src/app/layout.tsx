import { ToastProvider } from "@/components/ToastProvider";

export const metadata = {
  title: "Catálogo",
  description: "Catálogo e Pedidos",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>
        <ToastProvider>{children}</ToastProvider>
      </body>
    </html>
  );
}
