import type { Metadata } from 'next';
import { GeistMono } from 'geist/font/mono';
import { Newsreader } from 'next/font/google';
import Nav from '@/components/Nav';
import Footer from '@/components/Footer';
import './globals.css';

// Newsreader's italic is wider and more open than Instrument Serif's,
// which read as cramped at heading sizes.
const newsreader = Newsreader({
  subsets: ['latin'],
  variable: '--font-serif',
  weight: ['400'],
  style: ['normal', 'italic'],
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Shawn Jiang',
  description:
    'Shawn Jiang — CS & Statistics student at the University of Toronto. Software engineering, ML, and side projects.',
};

const themeScript = `(function(){try{var t=localStorage.getItem('theme');if(!t){t=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}document.documentElement.setAttribute('data-theme',t);}catch(e){document.documentElement.setAttribute('data-theme','light');}})();`;

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${GeistMono.variable} ${newsreader.variable}`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <div className="mx-auto flex min-h-screen max-w-prose flex-col px-6 py-12">
          <Nav />
          <main className="mt-12 flex-1">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
