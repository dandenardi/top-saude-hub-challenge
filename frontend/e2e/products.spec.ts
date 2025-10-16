import { test, expect } from "@playwright/test";

test("lista de produtos renderiza e pagina navega", async ({ page }) => {
  await page.goto("/products");

  await expect(page.getByRole("table")).toBeVisible();

  const search = page.getByPlaceholder(/buscar/i);
  if (await search.isVisible()) {
    await search.fill("café");

    await page.waitForTimeout(400);
  }

  await expect(page.getByRole("columnheader", { name: /nome/i })).toBeVisible();
  await expect(page.getByRole("columnheader", { name: /sku/i })).toBeVisible();

  const nextBtn = page
    .getByRole("button", { name: /próxima|seguinte|next/i })
    .first();
  if (await nextBtn.isVisible()) {
    await nextBtn.click();
    await expect(page).toHaveURL(/page=\d+/);
  }
});
