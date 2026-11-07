import { useEffect, useRef, useState } from 'react';
import { ArrowRight, ArrowUpRight, Zap } from 'lucide-react';

export default function ReactionGame() {
  const [test, setTest] = useState('idle');
  const [reaction, setReaction] = useState(null);
  const timer = useRef();
  const start = useRef();
  useEffect(() => () => clearTimeout(timer.current), []);
  // Game states: idle -> waiting -> ready -> done. An early click uses early.
  const reactionClick = () => {
    if (test === 'waiting') {
      clearTimeout(timer.current);
      setTest('early');
      return;
    }
    if (test === 'ready') {
      setReaction(Math.round(performance.now() - start.current));
      setTest('done');
      return;
    }
    setReaction(null);
    setTest('waiting');
    timer.current = setTimeout(
      () => {
        start.current = performance.now();
        setTest('ready');
      },
      1500 + Math.random() * 2500,
    );
  };

  return (
    <section className="playground section" id="playground">
      <div className="playground-intro">
        <div className="play-icon">
          <Zap size={28} />
        </div>
        <h2>
          Don’t just look.
          <br />
          <span>Play a little.</span>
        </h2>
        <p>
          Great gear is only half the equation.
          <br />
          Let’s see what you bring to the game.
        </p>
        <span className="lab-label">
          THE REACTION LAB <ArrowRight size={17} />
        </span>
      </div>
      <button className={`reaction ${test}`} onClick={reactionClick}>
        <span className="reaction-status">
          {test === 'idle'
            ? 'READY WHEN YOU ARE'
            : test === 'waiting'
              ? 'HOLD STEADY'
              : test === 'ready'
                ? 'NOW. NOW. NOW.'
                : test === 'early'
                  ? 'JUMPED THE GUN'
                  : 'NICE REFLEXES'}
        </span>
        <span className="reaction-main">
          {test === 'idle' ? (
            <>
              <span className="target">
                <i />
              </span>
              How fast are you?
            </>
          ) : test === 'waiting' ? (
            'Wait for orange…'
          ) : test === 'ready' ? (
            'CLICK!'
          ) : test === 'early' ? (
            'A little too eager.'
          ) : (
            <>
              {reaction}
              <small>ms</small>
            </>
          )}
        </span>
        <span className="reaction-bottom">
          {test === 'idle'
            ? 'Click to start. Then wait for the signal.'
            : test === 'done'
              ? 'Your browser-measured reaction time. Click to go again.'
              : test === 'early'
                ? 'Wait for the color to change. Click to retry.'
                : test === 'waiting'
                  ? 'Stay focused. The signal is coming.'
                  : 'Hit the button!'}
          <ArrowUpRight size={20} />
        </span>
      </button>
    </section>
  );
}
