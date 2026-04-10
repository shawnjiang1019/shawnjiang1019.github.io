'use client';

import { useEffect, useState } from 'react';

type Theme = 'light' | 'dark';

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const current =
      (document.documentElement.getAttribute('data-theme') as Theme) || 'light';
    setTheme(current);
    setMounted(true);
  }, []);

  const toggle = () => {
    const next: Theme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    try {
      localStorage.setItem('theme', next);
    } catch {
      // ignore
    }
    setTheme(next);
  };

  // Render a stable placeholder on SSR to avoid hydration mismatch.
  const label = mounted ? (theme === 'light' ? 'dark' : 'light') : '…';

  return (
    <button
      type="button"
      onClick={toggle}
      className="font-mono text-sm no-underline hover:underline"
      aria-label="Toggle theme"
    >
      [{label}]
    </button>
  );
}
