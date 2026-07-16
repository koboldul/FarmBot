import { expect, test } from '@playwright/test';

test('shows the FarmBot schedule', async ({ page }) => {
  await page.goto('/#/Schedule');

  await expect(page.getByRole('heading', { name: 'FarmBot' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'View logs' })).toBeVisible();
});
