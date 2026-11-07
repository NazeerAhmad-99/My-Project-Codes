import { Command } from 'lucide-react';
import { keyRows } from '../../data/keyboard';

export default function InteractiveKeyboard({ light, pressed, onKeyPress }) {
  return (
    <div
      className={`keyboard ${light.toLowerCase()}`}
      aria-label="Interactive keyboard. Click the keys to test them"
    >
      <div className="keyboard-top">
        <span>LEVEL / FORM 75</span>
        <div className="keyboard-lights">
          <i />
          <i />
          <i />
        </div>
        <div className="knob" />
      </div>
      {keyRows.map((row, i) => (
        <div className="key-row" key={i}>
          {row.map((k, j) => (
            <button
              key={`${k}-${j}`}
              aria-label={k === 'space' ? 'Space bar' : `${k} key`}
              onClick={() => onKeyPress(k)}
              className={`key ${k === 'space' ? 'space' : ''} ${['esc', 'enter', '↑'].includes(k) ? 'accent-key' : ''} ${['W', 'A', 'S', 'D'].includes(k) ? 'gaming-key' : ''} ${pressed.toLowerCase() === k.toLowerCase() ? 'pressed' : ''}`}
              style={{ '--delay': `${(i + j) * 0.14}s` }}
            >
              {k === 'win' ? (
                <Command size={9} />
              ) : k === 'space' ? (
                <span className="space-mark">L E V E L</span>
              ) : (
                k
              )}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}
