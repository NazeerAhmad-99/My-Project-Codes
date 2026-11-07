import { Check } from 'lucide-react';

export default function Toast({ message }) {
  return (
    <div className={`toast ${message ? 'visible' : ''}`} role="status">
      <Check size={17} />
      {message}
    </div>
  );
}
