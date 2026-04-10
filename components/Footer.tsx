export default function Footer() {
  return (
    <footer className="mt-16 flex flex-col gap-4 border-t border-[color:var(--color-border)] pt-6 text-xs sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-wrap gap-4">
        <a href="mailto:shawn.jiang@mail.utoronto.ca" className="no-underline hover:underline">
          [email]
        </a>
        <a
          href="https://github.com/shawnjiang1019"
          className="no-underline hover:underline"
          target="_blank"
          rel="noreferrer"
        >
          [github]
        </a>
        <a
          href="https://linkedin.com/in/placeholder"
          className="no-underline hover:underline"
          target="_blank"
          rel="noreferrer"
        >
          [linkedin]
        </a>
      </div>
      <div className="text-[color:var(--color-muted)]">
        &copy; {new Date().getFullYear()} Shawn Jiang
      </div>
    </footer>
  );
}
