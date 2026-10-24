import type { Metadata } from 'next';
import { experience } from '@/lib/experience';

export const metadata: Metadata = {
  title: 'experience — Shawn Jiang',
  description: 'Work and research experience of Shawn Jiang.',
};

export default function ExperiencePage() {
  return (
    <article>
      <h1 className="italic">experience</h1>
      <p className="mt-3 text-[color:var(--color-muted)]">
        Formative work and research experiences for me.
      </p>

      <hr />

      <ul className="space-y-10">
        {experience.map((e) => (
          <li key={`${e.company}-${e.period}`}>
            <div className="flex items-baseline justify-between gap-4">
              <h2 className="italic">{e.role}</h2>
              <span className="shrink-0 text-xs text-[color:var(--color-muted)]">
                {e.period}
              </span>
            </div>
            <p className="text-[color:var(--color-muted)]">
              {e.company} &middot; {e.stack}
            </p>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {e.points.map((pt) => (
                <li key={pt}>{pt}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </article>
  );
}
