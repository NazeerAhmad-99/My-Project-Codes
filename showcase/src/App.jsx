import { useCallback, useState } from 'react';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import AnnouncementStrip from './components/layout/AnnouncementStrip';
import Hero from './components/hero/Hero';
import ProductCollection from './components/products/ProductCollection';
import ProductDialog from './components/products/ProductDialog';
import ComparisonBar from './components/products/ComparisonBar';
import ComparisonDialog from './components/products/ComparisonDialog';
import SetupDrawer from './components/setup/SetupDrawer';
import ReactionGame from './components/playground/ReactionGame';
import SetupStory from './components/story/SetupStory';
import ClosingSection from './components/story/ClosingSection';
import Toast from './components/ui/Toast';
import { useSetup } from './hooks/useSetup';
import { useToast } from './hooks/useToast';

export default function App() {
  // Shared state belongs in the closest parent of the components that need it.
  const [accent, setAccent] = useState('#f4512a');
  const [compare, setCompare] = useState([]);
  // A single dialog value prevents several dialogs from being open at once.
  const [dialog, setDialog] = useState(null);
  const { message, notify } = useToast();
  const { setup, selectedProducts, addProduct, removeProduct, resetSetup } =
    useSetup(notify);

  // A stable callback lets Modal keep its focus effect active across renders.
  const closeDialog = useCallback(() => setDialog(null), []);

  function openSetup() {
    setDialog({ type: 'setup' });
  }

  function handleAddProduct(product) {
    if (setup.includes(product.id)) {
      openSetup();
      return;
    }
    addProduct(product);
    notify(`${product.name} added to your setup`);
  }

  function handleToggleCompare(productId) {
    if (compare.includes(productId)) {
      setCompare(compare.filter((id) => id !== productId));
      return;
    }
    if (compare.length >= 3) {
      notify('Compare up to three accessories.');
      return;
    }
    setCompare([...compare, productId]);
  }

  // Props send data down; callback props let children request actions up here.
  return (
    <div style={{ '--accent': accent }}>
      <Header setupCount={setup.length} onOpenSetup={openSetup} />
      <main>
        <Hero
          accent={accent}
          onAccentChange={setAccent}
          isDialogOpen={dialog !== null}
        />
        <AnnouncementStrip />
        <ProductCollection
          setup={setup}
          compare={compare}
          onAdd={handleAddProduct}
          onCompare={handleToggleCompare}
          onView={(product) => setDialog({ type: 'product', product })}
        />
        <ReactionGame />
        <SetupStory onOpenSetup={openSetup} />
        <ClosingSection />
      </main>
      <Footer />
      {compare.length > 0 && !dialog && (
        <ComparisonBar
          count={compare.length}
          onOpen={() => setDialog({ type: 'comparison' })}
          onClear={() => setCompare([])}
        />
      )}
      <Toast message={message} />
      {dialog?.type === 'setup' && (
        <SetupDrawer
          selected={selectedProducts}
          onRemove={removeProduct}
          onReset={resetSetup}
          onClose={closeDialog}
          notify={notify}
        />
      )}
      {dialog?.type === 'product' && (
        <ProductDialog
          product={dialog.product}
          isInSetup={setup.includes(dialog.product.id)}
          onAdd={handleAddProduct}
          onClose={closeDialog}
        />
      )}
      {dialog?.type === 'comparison' && (
        <ComparisonDialog
          compare={compare}
          setup={setup}
          onAdd={handleAddProduct}
          onClose={closeDialog}
        />
      )}
    </div>
  );
}
