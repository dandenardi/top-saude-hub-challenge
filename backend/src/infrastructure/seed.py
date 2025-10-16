import asyncio
from sqlalchemy.dialects.postgresql import insert
from .db import AsyncSessionLocal
from .models import ProductORM, CustomerORM

PRODUCTS = [
    ("Café Especial 250g", "SKU-CAF-250", 3990, 120, True),
    ("Chá Verde 100g", "SKU-CHA-100", 2190, 80, True),
    ("Biscoito Integral 200g", "SKU-BIS-200", 1290, 65, True),
    ("Geleia de Frutas 300g", "SKU-GEL-300", 1990, 40, True),
    ("Granola 500g", "SKU-GRA-500", 2890, 50, True),
    ("Azeite Extra Virgem 500ml", "SKU-AZE-500", 4590, 30, True),
    ("Mel Orgânico 300g", "SKU-MEL-300", 3490, 35, True),
    ("Pasta de Amendoim 1kg", "SKU-PAS-1000", 5490, 25, True),
    ("Barra de Cereal 25g", "SKU-BAR-025", 490, 300, True),
    ("Água com Gás 500ml", "SKU-AG-500", 590, 150, True),
    ("Café Moído 500g", "SKU-CAF-500", 6890, 70, True),
    ("Chá Preto 100g", "SKU-CHP-100", 1990, 90, True),
    ("Chocolate 70% 80g", "SKU-CHO-080", 1590, 110, True),
    ("Farinha de Aveia 1kg", "SKU-FAR-1000", 2190, 60, True),
    ("Quinoa 500g", "SKU-QUI-500", 3290, 45, True),
    ("Molho de Tomate 340g", "SKU-MOL-340", 1090, 85, True),
    ("Atum em Água 170g", "SKU-ATU-170", 1590, 75, True),
    ("Arroz Integral 1kg", "SKU-ARR-1000", 1990, 80, True),
    ("Feijão Carioca 1kg", "SKU-FEJ-1000", 1890, 90, True),
    ("Macarrão Integral 500g", "SKU-MAC-500", 1390, 60, True),
]

CUSTOMERS = [
    ("Ana Silva", "ana@example.com", "11122233344"),
    ("Bruno Souza", "bruno@example.com", "22233344455"),
    ("Carla Pereira", "carla@example.com", "33344455566"),
    ("Diego Ramos", "diego@example.com", "44455566677"),
    ("Elisa Torres", "elisa@example.com", "55566677788"),
    ("Felipe Costa", "felipe@example.com", "66677788899"),
    ("Gabriela Lima", "gabriela@example.com", "77788899900"),
    ("Henrique Alves", "henrique@example.com", "88899900011"),
    ("Isabela Rocha", "isabela@example.com", "99900011122"),
    ("João Pedro", "joao@example.com", "00011122233"),
]

async def run():
    async with AsyncSessionLocal() as session:  
        
        for n, sku, price, qty, active in PRODUCTS:
            stmt = (
                insert(ProductORM)
                .values(name=n, sku=sku, price=price, stock_qty=qty, is_active=active)
                .on_conflict_do_nothing(index_elements=["sku"])
            )
            await session.execute(stmt)

        
        for n, email, doc in CUSTOMERS:
            stmt = (
                insert(CustomerORM)
                .values(name=n, email=email, document=doc)
                .on_conflict_do_nothing(index_elements=["document"])
            )
            await session.execute(stmt)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(run())