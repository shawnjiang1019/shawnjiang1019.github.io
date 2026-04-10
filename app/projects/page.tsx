import type { Metadata } from 'next';
import { projects } from '@/lib/projects';

export const metadata: Metadata = {
  title: 'projects — Shawn Jiang',
  description: 'Selected projects by Shawn Jiang.',
};

export default function ProjectsPage() {
  return (
    <article>
      <h1 className="italic">projects</h1>
      <p className="mt-3 text-[color:var(--color-muted)]">
        A selection of things I&apos;ve built, tinkered with, or shipped.
      </p>

      <hr />

      <ul className="space-y-10">
        {projects.map((p) => (
          <li key={p.slug}>
            <div className="flex items-baseline justify-between gap-4">
              <h2 className="italic">
                {p.href ? <a href={p.href}>{p.title}</a> : p.title}
              </h2>
              <span className="shrink-0 text-xs text-[color:var(--color-muted)]">
                {p.year}
              </span>
            </div>
            <p className="mt-2">{p.description}</p>
            {p.tags && p.tags.length > 0 && (
              <p className="mt-2 text-xs text-[color:var(--color-muted)]">
                {p.tags.map((t) => `[${t}]`).join(' ')}
              </p>
            )}
          </li>
        ))}
      </ul>
    </article>
  );
}
