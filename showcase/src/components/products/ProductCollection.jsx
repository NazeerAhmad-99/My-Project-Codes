import { useState } from 'react';
import { SlidersHorizontal } from 'lucide-react';
import { products } from '../../data/products';
import ProductCard from './ProductCard';

export default function ProductCollection({
  setup,
  compare,
  onAdd,
  onCompare,
  onView,
}) {
  // The active filter is local state: only this collection uses it.
  const [category, setCategory] = useState('All gear');
  return (
    <section className="collection section" id="collection">
      <div className="section-heading">
        <h2>
          The right tools.
          <br />
          <span>The unfair advantage.</span>
        </h2>
        <p>
          Find the missing piece in your setup.
          <br />
          Then make every session your best one.
        </p>
      </div>
      <div className="filter-bar">
        <div className="filters" role="group" aria-label="Filter accessories">
          {['All gear', 'Keyboards', 'Mice', 'Audio'].map((c) => (
            <button
              key={c}
              onClick={() => setCategory(c)}
              aria-pressed={category === c}
              className={category === c ? 'active' : ''}
            >
              {c}
              {c === 'All gear' && (
                <span>{products.length.toString().padStart(2, '0')}</span>
              )}
            </button>
          ))}
        </div>
        <span className="filter-caption">
          <SlidersHorizontal size={14} /> Curated for your play
        </span>
      </div>
      <div className="product-grid">
        {products
          .filter((p) => category === 'All gear' || p.type === category)
          .map((p) => (
            <ProductCard
              key={p.id}
              product={p}
              isInSetup={setup.includes(p.id)}
              isCompared={compare.includes(p.id)}
              onAdd={onAdd}
              onCompare={onCompare}
              onView={onView}
            />
          ))}
      </div>
      <p className="demo-note">
        Imagined by LEVEL. Products, prices, and specifications are
        illustrative; this is an interactive showcase.
      </p>
    </section>
  );
}
