import type { CSSProperties, ReactNode } from 'react';

// Highlighter sweep for key phrases; `delay` staggers the sweeps (seconds).
// `org` marks a workplace rather than a topic, in its own colour.
function Mark({
  children,
  delay = 0,
  org = false,
}: {
  children: ReactNode;
  delay?: number;
  org?: boolean;
}) {
  return (
    <mark className={org ? 'mark mark-org' : 'mark'} style={{ '--d': `${delay}s` } as CSSProperties}>
      {children}
    </mark>
  );
}

// Serif italic for ideas rather than facts.
function Term({ children }: { children: ReactNode }) {
  return <em className="term">{children}</em>;
}

function Reveal({ children, delay }: { children: ReactNode; delay: number }) {
  return (
    <p className="reveal" style={{ '--d': `${delay}s` } as CSSProperties}>
      {children}
    </p>
  );
}

export default function Home() {
  return (
    <article>
      <img
        src="/me.jpg"
        alt="Shawn Jiang"
        width={288}
        height={288}
        className="mb-6 h-72 w-72 rounded-full border border-[color:var(--color-border)] object-cover"
      />
      <h1 className="italic">Shawn Jiang</h1>
      <p className="mt-3 text-[color:var(--color-muted)]">
        &ldquo;The man who says he can&apos;t, and the man who says he can are both right.&rdquo; &mdash; Confucius
      </p>

      <hr />

      <section className="space-y-5">
        <Reveal delay={0.05}>
          I&apos;m an Honours BSc student in{' '}
          <Mark delay={0.5}>Computer Science and Statistics</Mark>{' '}
          at the University of Toronto.
        </Reveal>

        <Reveal delay={0.2}>
          I&apos;m interested in <Mark delay={0.8}>agentic systems</Mark> and their
          capabilities in solving <Term>open-ended problems</Term>, and primarily
          methods of ensuring <Mark delay={1.05}>reliability and correctness</Mark>.
        </Reveal>

        <Reveal delay={0.35}>
          I&apos;m also interested in <Mark delay={1.3}>databases and systems</Mark> as a whole.
          Other than learning about traditional storage system internals,
          I believe in the emerging paradigm of{' '}
          <span className="chip">Agents4DB</span> and <span className="chip">DB4Agents</span>.
          In other words, the next frontier is building{' '}
          <Mark delay={1.55}>storage systems for agent artifacts</Mark>,
          and designing data environments with an{' '}
          <Term>&ldquo;agent as a first-class user&rdquo;</Term> lens.
          I&apos;m working on some of these topics at <Mark delay={1.7} org>Huawei</Mark> currently.
        </Reveal>
        {/* <p>
          Most recently I&apos;ve been working on{' '}
          <span className="font-serif italic">deep learning for cultural context in LLMs</span>{' '}
          at the Lee Language Lab, and before that I shipped backend features
          at Seequent and architected a peer assessment platform at U of T.
        </p> */}
        <Reveal delay={0.5}>
          I&apos;m also in the process of learning more about{' '}
          <Mark delay={1.8}>computer vision</Mark>. I&apos;m astounded that I didn&apos;t
          start looking at this stuff earlier.
        </Reveal>
      </section>

      <hr />

      <section>
        <h2 className="italic">elsewhere</h2>
        <ul className="mt-4 space-y-2">
          <li>
            → <a href="/experience/">[experience]</a> — where I&apos;ve worked
          </li>
          <li>
            → <a href="/projects/">[projects]</a> — things I&apos;ve built
          </li>
          <li>
            → <a href="/notes/">[notes]</a> — things I&apos;m learning
          </li>
          <li>
            → <a href="/reading/">[reading]</a> — what&apos;s on my shelf
          </li>
          <li>
            → <a href="/resume.pdf">[resume]</a> — the formal version
          </li>
          <li>
            →{' '}
            <a
              href="https://github.com/shawnjiang1019"
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center gap-1.5"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                fill="currentColor"
                className="inline h-3.5 w-3.5"
                aria-hidden="true"
              >
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
              </svg>
              [github]
            </a>{' '}
            — code I&apos;ve written
          </li>
          <li>
            → see the footer for how to reach me
          </li>
        </ul>
      </section>
    </article>
  );
}
