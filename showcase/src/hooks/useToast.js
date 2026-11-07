import { useCallback, useEffect, useRef, useState } from 'react';

// A custom hook groups state and effects for one reusable behavior.
export function useToast() {
  const [message, setMessage] = useState('');
  const timer = useRef();

  const notify = useCallback((nextMessage) => {
    setMessage(nextMessage);
    clearTimeout(timer.current);
    timer.current = setTimeout(() => setMessage(''), 2800);
  }, []);

  useEffect(() => () => clearTimeout(timer.current), []);

  return { message, notify };
}
