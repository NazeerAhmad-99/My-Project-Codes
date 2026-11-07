import { useEffect, useRef, useState } from 'react';

export function useKeyboard(soundEnabled, isDialogOpen) {
  const [pressed, setPressed] = useState('');
  const pressedTimer = useRef();
  const audioContext = useRef();

  function highlightKey(key) {
    setPressed(key);
    clearTimeout(pressedTimer.current);
    pressedTimer.current = setTimeout(() => setPressed(''), 180);
  }

  function hit(key) {
    highlightKey(key);
    if (!soundEnabled) return;

    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      audioContext.current ||= new AudioContext();
      const context = audioContext.current;
      context.resume();
      const oscillator = context.createOscillator();
      const volume = context.createGain();
      oscillator.type = 'triangle';
      oscillator.frequency.value = 180 + Math.random() * 100;
      volume.gain.setValueAtTime(0.05, context.currentTime);
      volume.gain.exponentialRampToValueAtTime(
        0.001,
        context.currentTime + 0.06,
      );
      oscillator.connect(volume);
      volume.connect(context.destination);
      oscillator.start();
      oscillator.stop(context.currentTime + 0.07);
    } catch {
      // Audio is optional; keep the visual keyboard working if it is unavailable.
    }
  }

  useEffect(() => {
    function handleKeyDown(event) {
      if (
        isDialogOpen ||
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        event.ctrlKey ||
        event.metaKey ||
        event.altKey
      )
        return;
      setPressed(event.key === ' ' ? 'space' : event.key.toUpperCase());
      clearTimeout(pressedTimer.current);
      pressedTimer.current = setTimeout(() => setPressed(''), 180);
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isDialogOpen]);

  useEffect(
    () => () => {
      clearTimeout(pressedTimer.current);
      audioContext.current?.close();
    },
    [],
  );

  return { pressed, hit };
}
