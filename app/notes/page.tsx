import type { Metadata } from 'next';
import { notes } from '@/lib/notes';

export const metadata: Metadata = {
  title: 'notes — Shawn Jiang',
  description: 'Notes by Shawn Jiang, linked from Notion.',
};

export default function NotesPage() {
  return (
    <article>
      <h1 className="italic">notes</h1>
      <p className="mt-3 text-[color:var(--color-muted)]">
        Things I&apos;m learning, written up in Notion.
      </p>

      <hr />

      <ul className="space-y-8">
        {notes.map((n) => (
          <li key={n.href}>
            <h2 className="italic">
              <a href={n.href} target="_blank" rel="noreferrer">
                {n.title}
              </a>
            </h2>
            {n.description && <p className="mt-2">{n.description}</p>}
            {n.tags && n.tags.length > 0 && (
              <p className="mt-2 text-xs text-[color:var(--color-muted)]">
                {n.tags.map((t) => `[${t}]`).join(' ')}
              </p>
            )}
          </li>
        ))}
      </ul>
    </article>
  );
}
