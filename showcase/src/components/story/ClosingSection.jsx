import { ArrowUpRight } from 'lucide-react';

export default function ClosingSection() {
  return (
    <section className="closing section">
      <h2>
        Your next level
        <br />
        starts with <em>you.</em>
      </h2>
      <a
        href="#collection"
        className="closing-arrow"
        aria-label="Explore the gear"
      >
        <ArrowUpRight />
      </a>
    </section>
  );
}
