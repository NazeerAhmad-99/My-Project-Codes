import {
  ArrowUpRight,
  ArrowRight,
  X,
  RotateCcw,
  ShoppingBag,
} from 'lucide-react';
import Modal from '../ui/Modal';
import { formatCurrency } from '../../utils/formatCurrency';
import { exportSetup } from '../../utils/exportSetup';

export default function SetupDrawer({
  selected,
  onRemove,
  onReset,
  onClose,
  notify,
}) {
  function handleExport() {
    exportSetup(selected);
    notify('Your setup has been exported.');
  }
  return (
    <Modal title="Your setup" variant="drawer" onClose={onClose}>
      {' '}
      <h2>
        Your setup<span>.</span>
      </h2>
      <p className="modal-subtitle">A little more you. One piece at a time.</p>
      {selected.length ? (
        <>
          <div className="setup-list">
            {selected.map((p) => (
              <div className="setup-item" key={p.id}>
                <img src={`/${p.img}.jpg`} alt={p.name} />
                <div>
                  <h3>{p.name}</h3>
                  <span>
                    {p.type} · {formatCurrency(p.price)}
                  </span>
                </div>
                <button
                  aria-label={`Remove ${p.name}`}
                  onClick={() => onRemove(p.id)}
                >
                  <X size={18} />
                </button>
              </div>
            ))}
          </div>
          <div className="setup-total">
            <span>Your concept setup</span>
            <strong>
              {formatCurrency(selected.reduce((s, p) => s + p.price, 0))}
            </strong>
          </div>
          <button className="primary wide" onClick={handleExport}>
            Export my setup <ArrowUpRight size={18} />
          </button>
          <button className="text-button" onClick={onReset}>
            Start fresh <RotateCcw size={14} />
          </button>
        </>
      ) : (
        <div className="empty">
          <ShoppingBag size={46} />
          <h3>Room for something great.</h3>
          <p>Add a keyboard, mouse, or headset to start your dream setup.</p>
          <button
            className="primary"
            onClick={() => {
              onClose();
              document
                .getElementById('collection')
                .scrollIntoView({ behavior: 'smooth' });
            }}
          >
            Explore the gear <ArrowRight size={17} />
          </button>
        </div>
      )}
      <p className="demo-note">
        Saved in this browser. A demo setup builder — no purchases or payments.
      </p>
    </Modal>
  );
}
