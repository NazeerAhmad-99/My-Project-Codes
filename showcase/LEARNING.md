# How this React project works

Start small: understand one component and one click before reading every file.
This structure is one practical way to organize a small React app. Different teams
use different folder names; the useful rule is to group code by responsibility.

## The folder map

```text
showcase/
├── index.html                 HTML shell, including the root element
├── public/                    Pictures and a font stylesheet served by Vite
├── src/
│   ├── main.jsx               Starts React and loads the styles
│   ├── App.jsx                Assembles the page and connects shared state
│   ├── components/
│   │   ├── layout/            Header, footer, announcement strip
│   │   ├── hero/              Intro, color controls, interactive keyboard
│   │   ├── products/          Collection, cards, details, comparison
│   │   ├── setup/             Saved setup drawer
│   │   ├── playground/        Reaction game and its local state
│   │   ├── story/             Setup story and closing section
│   │   └── ui/                Shared dialog shell and notification
│   ├── hooks/                 State and effects grouped by behavior
│   ├── data/                  Product objects and keyboard rows
│   ├── utils/                 Currency formatting and file export
│   └── styles/                CSS grouped by page area
├── package.json               Dependencies and commands
└── .prettierrc.json            Automatic formatting rules
```

Files in `components` return JSX. Hooks call React hooks to manage behavior.
Utilities are ordinary JavaScript functions and do not call React hooks.
Data files describe content. CSS describes how the rendered elements look.

## Read in this order

1. **`index.html`, then `src/main.jsx`.** Find the root element and the call to
   `createRoot`. React renders `<App />` into that element.
2. **`src/App.jsx`.** Read its imports and returned JSX first. This is the page
   outline. You do not need to understand every handler yet.
3. **`components/layout/Header.jsx`.** A short example of props. `setupCount` is
   data from its parent; `onOpenSetup` is a function supplied by its parent.
4. **`data/products.js` and `components/products/ProductCard.jsx`.** Follow one
   product object into a card's `product` prop. Change its name and refresh.
5. **`components/products/ProductCollection.jsx`.** Understand `useState`, the
   filter buttons, `.filter()`, and `.map()`. The selected category belongs here
   because other page sections do not need it.
6. **`App.jsx` again, then `hooks/useSetup.js`.** Follow an add click using the
   example below. Read the storage effect after understanding the state update.
7. **`components/setup/SetupDrawer.jsx`.** Follow remove, reset, and export.
   `utils/formatCurrency.js` formats numbers; `utils/exportSetup.js` downloads text.
8. **`components/hero/Hero.jsx`, then `InteractiveKeyboard.jsx`.** The hero owns
   lighting and sound settings. The keyboard receives values and a callback.
   `hooks/useKeyboard.js` contains the more advanced timers, listeners, and audio.
9. **`components/playground/ReactionGame.jsx`.** This is a self-contained feature:
   read its state, refs, click handler, and JSX together.
10. **`components/ui/Modal.jsx` and the product dialogs.** Learn how `children`
    lets several dialogs share one accessible shell. Leave focus management until
    the opening and closing behavior makes sense.
11. **`hooks/useToast.js` and `components/ui/Toast.jsx`.** One hook manages the
    notification timer, while one component displays its message.
12. **`styles/index.css`.** This imports the CSS files in order. Start with
    `base.css`, then the file named after the feature you are studying. Read
    `responsive.css` and `animations.css` after the ordinary layouts.

## Follow one click: Add to setup

```text
ProductCard: user clicks "Add to setup"
  -> onAdd(product)
App: handleAddProduct(product)
  -> addProduct(product), supplied by useSetup
useSetup: setSetup(...) creates a new array of IDs
  -> React renders App and its children with the updated values
Header: receives the new count
ProductCard: receives isInSetup = true
SetupDrawer: receives the selected product objects when opened
useSetup's effect: saves the IDs to localStorage
```

`onAdd` is just a prop name. It works because the parent passes a function under
that name and the child calls it. React does not give that name special behavior.

## Who owns which state?

| State                         | Owner                           | Why it belongs there                                 |
| ----------------------------- | ------------------------------- | ---------------------------------------------------- |
| Accent color                  | `App`                           | The CSS variable changes the whole page              |
| Compared product IDs          | `App`                           | Cards, comparison bar, and dialog need them          |
| Open dialog                   | `App`                           | Several page sections can open a dialog              |
| Setup IDs                     | `useSetup`, called by `App`     | Several sections need the same saved setup           |
| Notification                  | `useToast`, called by `App`     | Different actions display messages                   |
| Category                      | `ProductCollection`             | Only the collection needs the active filter          |
| Lighting and sound            | `Hero`                          | These settings affect the keyboard preview           |
| Pressed key and audio objects | `useKeyboard`, called by `Hero` | Keyboard-specific behavior                           |
| Reaction-game state           | `ReactionGame`                  | The game works independently of the rest of the page |

Calling a custom hook does not create shared global state. Here `App` calls
`useSetup` once and passes the resulting values and functions to its children.
Calling it separately in several children would create separate state instances.

## Patterns to practise

- **Props down, actions up:** parents pass values and callback functions. Children
  call those callbacks rather than changing a parent's variables directly.
- **Keep state close to its users:** lift it into a common parent only when
  several components need the same value.
- **Calculate what you can:** `selectedProducts` comes from `products` and `setup`;
  it does not need its own independent state.
- **Update arrays without mutation:** use spread and `.filter()`, rather than
  modifying an existing state array with `.push()` or `.splice()`.
- **Effects need cleanup:** listeners, timeouts, and audio should be cleaned up
  when their owner is removed or the effect runs again.
- **Extract meaningful responsibilities:** a component can be several lines or
  a hundred lines. A new file for every `<span>` would make learning harder.

## Small exercises

1. Change the header text in `Header.jsx`.
2. Add a product in `data/products.js`. The All gear count updates automatically.
3. Add a color to the swatch array in `Hero.jsx`.
4. Add a short caption inside `ProductCard.jsx`; it appears on every card.
5. Trace why removing a setup item updates both the drawer and the header.
6. Change the random waiting period in `ReactionGame.jsx`.

After each change, look at the result and explain which state or prop produced it.
Run `npm run format` to tidy the code and `npm run build` to check the production
bundle. A build does not replace checking the behavior in a browser.
