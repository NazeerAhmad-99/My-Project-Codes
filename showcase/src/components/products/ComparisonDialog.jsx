import { Plus } from 'lucide-react';
import Modal from '../ui/Modal';
import { products } from '../../data/products';
import { formatCurrency } from '../../utils/formatCurrency';

export default function ComparisonDialog({ compare, setup, onAdd, onClose }) {
  return (
    <Modal
      title="Compare accessories"
      variant="comparison-modal"
      onClose={onClose}
    >
      {' '}
      <h2>
        Find your fit<span>.</span>
      </h2>
      <p className="modal-subtitle">A closer look, side by side.</p>
      <div className="compare-grid" style={{ '--columns': compare.length }}>
        {products
          .filter((p) => compare.includes(p.id))
          .map((p) => (
            <div key={p.id}>
              <img src={`/${p.img}.jpg`} alt={p.name} />
              <h3>{p.name}</h3>
              <strong>{formatCurrency(p.price)}</strong>
              <p>{p.type}</p>
              {p.specs.map((s) => (
                <p className="spec" key={s}>
                  {s}
                </p>
              ))}
              <button className="primary" onClick={() => onAdd(p)}>
                {setup.includes(p.id) ? 'View setup' : 'Add to setup'}
                <Plus size={16} />
              </button>
            </div>
          ))}
      </div>
    </Modal>
  );
}
