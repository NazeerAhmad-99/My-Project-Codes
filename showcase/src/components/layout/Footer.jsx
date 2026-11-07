export default function Footer() {
  return (
    <footer>
      <a className="logo" href="#">
        LEVEL<span>®</span>
      </a>
      <p>A playground for better play.</p>
      <span>Built with React. Made to interact.</span>
      <a href="#">Back to top ↑</a>
      <small>
        © {new Date().getFullYear()} LEVEL. A fictional concept by Nazeer’s
        Showcase.
      </small>
    </footer>
  );
}
