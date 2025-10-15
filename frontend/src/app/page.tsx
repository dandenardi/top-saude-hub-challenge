export default function Home() {
  return (
    <main style={{ padding: 24 }}>
      <h1>Catálogo & Pedidos</h1>
      <ul>
        <li><a href="/products">Produtos</a></li>
        <li><a href="/customers">Clientes</a></li>
        <li><a href="/orders/new">Novo Pedido</a></li>
      </ul>
    </main>
  );
}
