import { useEffect, useState } from 'react';
import { products } from '../data/products';

const STORAGE_KEY = 'level-setup';

function readSavedSetup() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    if (!Array.isArray(saved)) return [];
    return saved.filter((id) => products.some((product) => product.id === id));
  } catch {
    return [];
  }
}

export function useSetup(notify) {
  // Passing the function asks React to read storage only during initialization.
  const [setup, setSetup] = useState(readSavedSetup);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(setup));
    } catch {
      notify('Your browser could not save this setup.');
    }
  }, [setup, notify]);

  function addProduct(product) {
    setSetup((current) =>
      current.includes(product.id) ? current : [...current, product.id],
    );
  }

  function removeProduct(productId) {
    setSetup((current) => current.filter((id) => id !== productId));
  }

  function resetSetup() {
    setSetup([]);
  }

  const selectedProducts = products.filter((product) =>
    setup.includes(product.id),
  );
  return { setup, selectedProducts, addProduct, removeProduct, resetSetup };
}
