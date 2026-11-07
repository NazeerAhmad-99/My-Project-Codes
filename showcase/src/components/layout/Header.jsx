import { ShoppingBag } from 'lucide-react';

export default function Header({ setupCount, onOpenSetup }) {
  return (
    <header>
      <a className="logo" href="#" aria-label="LEVEL home">
        LEVEL<span>®</span>
      </a>
      <nav aria-label="Main navigation">
        <a href="#collection">The gear</a>
        <a href="#playground">The playground</a>
        <a href="#story">Our mindset</a>
      </nav>
      <button className="bag" onClick={onOpenSetup}>
        Your setup <span>{setupCount}</span>
        <ShoppingBag size={17} />
      </button>
    </header>
  );
}
