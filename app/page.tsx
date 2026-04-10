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
        <p>
          I&apos;m an Honours BSc student in{' '}
          Computer Science and Statistics{' '}
          at the University of Toronto. 
          I like building things with code.
        </p>
        {/* <p>
          Most recently I&apos;ve been working on{' '}
          <span className="font-serif italic">deep learning for cultural context in LLMs</span>{' '}
          at the Lee Language Lab, and before that I shipped backend features
          at Seequent and architected a peer assessment platform at U of T.
        </p> */}
        <p>
          When I&apos;m not studying you can find me taking pictures of food,
          shipping things, and occasionally wandering offline.
        </p>
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
            → <a href="/resume.pdf">[resume]</a> — the formal version
          </li>
          <li>
            → see the footer for how to reach me
          </li>
        </ul>
      </section>
    </article>
  );
}
