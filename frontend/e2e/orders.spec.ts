import { test, expect } from "@playwright/test";

test("criação de pedido com typeahead e cálculo de total", async ({ page }) => {
  await page.goto("/orders/new");

  const customerSelect = page
    .getByLabel(/cliente/i)
    .or(page.getByPlaceholder(/cliente/i));
  if (await customerSelect.isVisible()) {
    await customerSelect.click();
  }

  const input = page.getByPlaceholder(/buscar produto/i);
  await input.fill("caf");

  await page.waitForTimeout(500);

  const firstOpt = page.getByRole("option").first();
  await expect(firstOpt).toBeVisible();
  await firstOpt.click();

  const qtySpin = page
    .getByLabel(/quantidade/i)
    .first()
    .or(page.getByRole("spinbutton").first());
  if (await qtySpin.isVisible()) {
    await qtySpin.fill("1");
  }

  await expect(page.getByTestId("order-total")).toBeVisible();
  await expect(page.getByTestId("order-total")).toHaveText(/total\s+R\$/i);

  const dialogPromise = page.waitForEvent("dialog");

  const submit = page.getByRole("button", {
    name: /criar pedido|finalizar|salvar/i,
  });
  await expect(submit).toBeEnabled();
  await submit.click();

  const dialog = await dialogPromise;
  await expect(dialog.message()).toMatch(/pedido criado/i);
  await dialog.dismiss(); // ou dialog.accept();

  await expect(submit).toBeEnabled();
});
