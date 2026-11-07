import { Plus } from 'lucide-react';

export default function AnnouncementStrip() {
  return (
    <div className="ticker" aria-hidden="true">
      <span>PRECISION IN EVERY PRESS</span>
      <Plus />
      <span>LESS LATENCY. MORE LEGENDARY.</span>
      <Plus />
      <span>DESIGNED TO DISAPPEAR. BUILT TO PERFORM.</span>
      <Plus />
      <span>PLAY ON YOUR TERMS</span>
      <Plus />
    </div>
  );
}
