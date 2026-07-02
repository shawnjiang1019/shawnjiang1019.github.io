export type Note = {
  title: string;
  href: string;
  description?: string;
  tags?: string[];
};

// Links to my Notion notes. Add new entries here.
export const notes: Note[] = [
  {
    title: 'Example Note',
    href: 'https://www.notion.so/',
    description: 'Replace this with a link to one of your Notion pages.',
    tags: ['placeholder'],
  },
];
