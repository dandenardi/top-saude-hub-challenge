import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repos import ProductRepo

@pytest.mark.asyncio
async def test_products_api_smoke_create_get_update_delete(api_client: AsyncClient):
    body = {"name": "Camiseta", "sku": "TS-001", "price": 9900, "stock_qty": 5, "is_active": True}

    r = await api_client.post("/api/products", json=body)
    assert r.status_code in (200, 201)
    env = r.json()
    assert env["cod_retorno"] == 0
    pid = env["data"]["id"]

    r = await api_client.get(f"/api/products/{pid}")
    assert r.status_code == 200
    assert r.json()["data"]["sku"] == "TS-001"

    r = await api_client.put(f"/api/products/{pid}", json={"price": 10900})
    assert r.status_code == 200
    assert r.json()["data"]["price"] == 10900

    r = await api_client.delete(f"/api/products/{pid}")
    assert r.status_code == 200
    assert r.json()["cod_retorno"] == 0

@pytest.mark.asyncio
async def test_products_repo_filter_sort_pagination(session: AsyncSession, mk_product):
    
    await mk_product(name="Abacaxi", sku="A-1", price=100, stock_qty=1)
    await mk_product(name="Banana",  sku="B-1", price=200, stock_qty=2)
    await mk_product(name="Caju",    sku="C-1", price=300, stock_qty=3)
    await mk_product(name="Damasco", sku="D-1", price=400, stock_qty=4)
    await mk_product(name="Cacau",   sku="C-2", price=350, stock_qty=5)

    
    rows, total = await ProductRepo.list(session, q="Ca", page=1, page_size=50, sort="name:asc")
    names = [r.name for r in rows]
    assert all("ca" in n.lower() for n in names)
    assert names == sorted(names) 
    assert len(names) >= 2
    
    rows_p1, total = await ProductRepo.list(session, q=None, page=1, page_size=2, sort="created_at:desc")
    rows_p2, _     = await ProductRepo.list(session, q=None, page=2, page_size=2, sort="created_at:desc")

    ids_p1 = {r.id for r in rows_p1}
    ids_p2 = {r.id for r in rows_p2}


    assert ids_p1.isdisjoint(ids_p2)
    assert total >= len(rows_p1) + len(rows_p2)