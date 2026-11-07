# LEVEL — React Showcase

A local single-page gaming accessories experience. All products and prices are fictional.

```powershell
cd showcase
npm install
npm run dev
```

Open the URL Vite prints. Production build: `npm run build`.

## Learning your way around

Start with these files in order:

1. `index.html` contains the empty `root` element and loads the JavaScript.
2. `src/main.jsx` mounts React into that element, then `src/App.jsx` assembles the page from components.
3. `src/components/layout/Header.jsx` is a small first example of a component receiving props.
4. [LEARNING.md](LEARNING.md) explains every folder, the recommended reading order, and how one click flows through the app.

`useState` holds changing values. In `ProductCollection`, calling `setCategory` makes React render the collection with the new value. `.filter()` chooses products to display; `.map()` turns the chosen products into JSX. `useEffect` handles browser storage and event listeners. `useRef` remembers timer IDs and browser objects between renders without requesting a new render.

For a first experiment, change a product's name in `src/data/products.js`. Next, follow a filter button's `onClick` through `setCategory` to the product list. Then follow the setup button through `handleAddProduct` in `App` to `useSetup`.

Components are grouped by feature, hooks contain stateful behavior, utilities contain plain JavaScript helpers, and CSS lives in `src/styles`. `App` connects the features through props and callbacks.

Format the project with `npm run format`, or check formatting with `npm run format:check`. Prettier follows the settings in `.prettierrc.json`.

## Explore

- Interactive CSS-built keyboard, lighting modes, color themes, and optional synthesized key sounds.
- Product filters, detail dialogs, and comparisons of up to three accessories.
- Setup builder persisted in localStorage, with removal, reset, and text export.
- Reaction-time game with randomized delay and early-click detection.
- Responsive layouts, keyboard-accessible dialogs, focus trapping, Escape dismissal, and reduced-motion support.

React state coordinates the preview, filters, comparison tray, dialogs, and setup. Effects manage persistence, keyboard input, and timer cleanup. CSS handles responsive layout and hardware rendering.

Photos: Unsplash, downloaded locally. Source photo IDs: `1587829741301-dc798b83add3` (keyboard), `1527814050087-3793815479db` (mouse), `1618366712010-f4ae9c647dcb` (headphones), `1593305841991-05c297ba4575` (setup). These are illustrative photos, not actual LEVEL products. Space Grotesk and Manrope are served via Google Fonts with local system fallbacks. Product imagery works offline; fonts fall back if unavailable.

No backend, accounts, payments, or real commerce. Reaction timing is browser-dependent and is not a hardware benchmark.
