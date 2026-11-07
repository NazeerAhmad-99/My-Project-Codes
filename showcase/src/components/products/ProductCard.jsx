import { ArrowUpRight, Plus, Check } from 'lucide-react';
import { formatCurrency } from '../../utils/formatCurrency';

export default function ProductCard({
  product,
  isInSetup,
  isCompared,
  onAdd,
  onCompare,
  onView,
}) {
  return (
    <article className="product" key={product.id}>
      <div className="product-photo" style={{ background: product.color }}>
        <span className="product-category">
          {product.type} /{' '}
          {product.id === 'k1' ? 'THE ORIGINAL' : 'LEVEL COLLECTION'}
        </span>
        <button
          className="product-image-button"
          onClick={() => onView(product)}
          aria-label={`Explore ${product.name}`}
        >
          <img
            src={`/${product.img}.jpg`}
            alt={`${product.type === 'Keyboards' ? 'Mechanical keyboard' : product.type === 'Mice' ? 'Gaming mouse' : 'Over-ear headphones'} — ${product.name} concept`}
            loading="lazy"
          />
        </button>
        <button
          className={`compare-toggle ${isCompared ? 'selected' : ''}`}
          aria-label={`Compare ${product.name}`}
          aria-pressed={isCompared}
          onClick={() => onCompare(product.id)}
        >
          {isCompared ? <Check size={15} /> : <Plus size={15} />} Compare
        </button>
      </div>
      <div className="product-title">
        <button onClick={() => onView(product)}>
          {product.name}
          <ArrowUpRight size={17} />
        </button>
        <span>{formatCurrency(product.price)}</span>
      </div>
      <p>{product.tag}</p>
      <button
        className={`add-button ${isInSetup ? 'added' : ''}`}
        onClick={() => onAdd(product)}
      >
        {isInSetup ? 'In your setup' : 'Add to setup'}
        {isInSetup ? <Check size={16} /> : <Plus size={16} />}
      </button>
    </article>
  );
}
