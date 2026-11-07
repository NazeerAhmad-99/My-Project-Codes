import { formatCurrency } from './formatCurrency';

// Browser-only work lives in a utility so the component can focus on the UI.
export function exportSetup(selected) {
  const text = selected
    .map((p) => `${p.name} — ${formatCurrency(p.price)}`)
    .join('\n');
  const url = URL.createObjectURL(
    new Blob(
      [
        `MY LEVEL SETUP\n\n${text}\n\nTotal: ${formatCurrency(selected.reduce((s, p) => s + p.price, 0))}\n\nFictional products. React showcase only.`,
      ],
      { type: 'text/plain' },
    ),
  );
  const a = document.createElement('a');
  a.href = url;
  a.download = 'my-level-setup.txt';
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
