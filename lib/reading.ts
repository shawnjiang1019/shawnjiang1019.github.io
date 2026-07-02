export type Book = {
  title: string;
  author: string;
  status?: 'reading' | 'finished' | 'queued';
  note?: string;
  href?: string;
};

export const reading: Book[] = [
  {
    title: 'Designing Data Intensive Applications',
    author: 'Martin Kleppmann',
    status: 'reading',
  },
  {
    title: 'Inference Engineering',
    author: 'Philip Kiely',
    status: 'reading',
  },
];
