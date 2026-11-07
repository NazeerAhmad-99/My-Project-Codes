import { Plus, Check } from 'lucide-react';
import Modal from '../ui/Modal';
import { formatCurrency } from '../../utils/formatCurrency';

export default function ProductDialog({ product, isInSetup, onAdd, onClose }) {
  return (
    <Modal title={product.name} onClose={onClose}>
      {' '}
      <img
        className="detail-image"
        src={`/${product.img}.jpg`}
        alt={product.name}
      />
      <h2>
        {product.name}
        <span>.</span>
      </h2>
      <p className="detail-description">{product.desc}</p>
      <div className="detail-specs">
        {product.specs.map((s) => (
          <span key={s}>
            <Check size={14} />
            {s}
          </span>
        ))}
      </div>
      <div className="detail-action">
        <strong>{formatCurrency(product.price)}</strong>
        <button className="primary" onClick={() => onAdd(product)}>
          {isInSetup ? 'View setup' : 'Add to setup'}
          <Plus size={18} />
        </button>
      </div>
      <p className="demo-note">Concept product. Image is illustrative.</p>
    </Modal>
  );
}
