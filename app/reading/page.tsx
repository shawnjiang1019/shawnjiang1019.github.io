import type { Metadata } from 'next';
import { reading } from '@/lib/reading';

export const metadata: Metadata = {
  title: 'reading',
  description: 'What I\'m currently reading.',
};

export default function ReadingPage() {
  return (
    <article>
      <h1 className="italic">reading list</h1>
      <p className="mt-3 text-[color:var(--color-muted)]">
        Books I&apos;m reading, have read, or want to get to.
      </p>

      <hr />

      <ul className="space-y-8">
        {reading.map((b) => (
          <li key={`${b.title}-${b.author}`}>
            <div className="flex items-baseline justify-between gap-4">
              <h2 className="italic">
                {b.href ? (
                  <a href={b.href} target="_blank" rel="noreferrer">
                    {b.title}
                  </a>
                ) : (
                  b.title
                )}
              </h2>
              {b.status && (
                <span className="shrink-0 text-xs text-[color:var(--color-muted)]">
                  [{b.status}]
                </span>
              )}
            </div>
            <p className="text-[color:var(--color-muted)]">{b.author}</p>
            {b.note && <p className="mt-2">{b.note}</p>}
          </li>
        ))}
      </ul>
    </article>
  );
}
