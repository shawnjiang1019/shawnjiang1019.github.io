import Link from 'next/link';
import ThemeToggle from './ThemeToggle';

export default function Nav() {
  return (
    <nav className="flex items-center justify-between text-sm">
      <Link href="/" className="no-underline hover:underline">
        [shawn]
      </Link>
      <div className="flex items-center gap-4">
        <Link href="/" className="no-underline hover:underline">
          [home]
        </Link>
        <Link href="/experience/" className="no-underline hover:underline">
          [experience]
        </Link>
        <Link href="/projects/" className="no-underline hover:underline">
          [projects]
        </Link>
        <a href="/resume.pdf" className="no-underline hover:underline">
          [resume]
        </a>
        <ThemeToggle />
      </div>
    </nav>
  );
}
