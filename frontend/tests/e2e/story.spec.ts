import { expect, test } from "@playwright/test";

test("anonymous reader begins a story and sees the assembly surface", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "moonlight" }).click();
  await expect(
    page.getByRole("button", { name: "Create my story" }),
  ).toBeEnabled();
});
