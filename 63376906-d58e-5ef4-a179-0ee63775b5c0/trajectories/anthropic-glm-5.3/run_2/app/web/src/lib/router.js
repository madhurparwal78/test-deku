import { useState, useEffect } from 'preact/hooks';

let listeners = [];

export function navigate(path, { replace = false } = {}) {
  if (replace) history.replaceState({}, '', path);
  else history.pushState({}, '', path);
  listeners.forEach((l) => l(path));
}

export function usePath() {
  const [path, setPath] = useState(location.pathname + location.search);
  useEffect(() => {
    const on = () => setPath(location.pathname + location.search);
    listeners.push(on);
    window.addEventListener('popstate', on);
    return () => {
      listeners = listeners.filter((l) => l !== on);
      window.removeEventListener('popstate', on);
    };
  }, []);
  return path;
}

