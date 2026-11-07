import { useState } from 'react';
import { ArrowUpRight, ArrowDown, Check, Volume2 } from 'lucide-react';
import InteractiveKeyboard from './InteractiveKeyboard';
import { useKeyboard } from '../../hooks/useKeyboard';

export default function Hero({ accent, onAccentChange, isDialogOpen }) {
  // Lighting and sound belong here because no other section needs them.
  const [light, setLight] = useState('Wave');
  const [sound, setSound] = useState(false);
  const { pressed, hit } = useKeyboard(sound, isDialogOpen);
  return (
    <section className="hero" aria-labelledby="hero-title">
      <div className="hero-copy">
        <div className="availability">
          <span /> BUILT FOR YOUR NEXT MOVE
        </div>
        <h1 id="hero-title">
          Good gear.
          <br />
          Great games.
          <br />
          <span>Your level.</span>
        </h1>
        <p>
          For the late-night squads. The one-more-rounds.
          <br className="desktop-break" /> The plays you’ll talk about tomorrow.
        </p>
        <a className="primary" href="#collection">
          Find your edge <ArrowUpRight size={19} />
        </a>
        <div className="hero-note">
          <span className="tiny-cross">+</span> Less distraction. More play.
        </div>
      </div>
      <div className="hero-stage">
        <div className="stage-top">
          <span>FORM 75 / INTERACTIVE PREVIEW</span>
          <span className="live-dot">LIVE</span>
        </div>
        <div className="orbit orbit-one" />
        <div className="orbit orbit-two" />
        <div className="stage-word" aria-hidden="true">
          PLAY.
        </div>
        <InteractiveKeyboard light={light} pressed={pressed} onKeyPress={hit} />
        <div className="floating-note">
          <span className="note-line" />
          <span>
            YOUR INPUT.
            <br />
            <strong>YOUR EXPRESSION.</strong>
          </span>
        </div>
        <div className="stage-bottom">
          <span>
            <span className="status-dot" /> Go on. Press a key.
          </span>
          <button onClick={() => setSound(!sound)} aria-pressed={sound}>
            <Volume2 size={15} /> Sound {sound ? 'on' : 'off'}
          </button>
        </div>
      </div>
      <div className="hero-controls">
        <span>Make it yours</span>
        <div className="swatches">
          {['#f4512a', '#a2b78b', '#9183cc', '#50a6b5'].map((c) => (
            <button
              aria-label={`Set accent ${c}`}
              aria-pressed={accent === c}
              key={c}
              style={{ background: c }}
              onClick={() => onAccentChange(c)}
            >
              {accent === c && <Check size={13} />}
            </button>
          ))}
        </div>
        <span className="control-separator" />
        <div className="lighting" role="group" aria-label="Keyboard lighting">
          {['Wave', 'Static', 'Off'].map((l) => (
            <button
              aria-pressed={light === l}
              className={light === l ? 'active' : ''}
              key={l}
              onClick={() => setLight(l)}
            >
              {l}
            </button>
          ))}
        </div>
        <a href="#collection" className="scroll-hint">
          Scroll to explore <ArrowDown size={15} />
        </a>
      </div>
    </section>
  );
}
