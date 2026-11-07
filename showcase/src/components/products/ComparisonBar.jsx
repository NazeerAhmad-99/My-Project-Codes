import { ArrowRight, X } from 'lucide-react';

export default function ComparisonBar({ count, onOpen, onClear }) {
  return (
    <div className="compare-bar">
      <span>{count} selected</span>
      <button onClick={onOpen} disabled={count < 2}>
        Compare gear <ArrowRight size={16} />
      </button>
      <button aria-label="Clear comparison" onClick={onClear}>
        <X size={17} />
      </button>
    </div>
  );
}
