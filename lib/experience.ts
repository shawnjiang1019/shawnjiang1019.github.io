export type Experience = {
  role: string;
  company: string;
  stack: string;
  period: string;
  description: string;
};

export const experience: Experience[] = [
  {
    role: 'Research Intern',
    company: 'Lee Language Lab',
    stack: 'NLP, PyTorch, LLMs',
    period: 'April 2026',
    description:
      'Knowledge graphs and deep learning methods for cultural context in LLMs, supervised by Dr. Enas Altarawneh.',
  },
  {
    role: 'Software Engineer Intern',
    company: 'University of Toronto',
    stack: 'React, FastAPI, PostgreSQL, GCP',
    period: 'May 2025 — Sep 2025',
    description:
      'Architected and shipped a full-stack peer assessment platform now used by 200+ students. Built a drag-and-drop ingestion pipeline with CSV parsing and schema validation that cut instructor data entry time by 80%, and deployed a serverless REST API on GCP Run with a Vercel frontend. Supervised by Prof. Sohee Kang.',
  },
  {
    role: 'Software Engineer Intern',
    company: 'Seequent',
    stack: 'C#, .NET',
    period: 'Jan 2025 — Apr 2025',
    description:
      'Shipped backend features in C#/.NET for geophysical modeling software used by 10,000+ geoscientists worldwide, including object conversion modules on the Evo cloud platform. Refactored 300+ test suites, reduced test failures by 40%, and cut average CI runtime by 15 minutes. Triaged and resolved 50+ bugs in an agile sprint cadence.',
  },
  {
    role: 'Data Science Intern',
    company: 'Beijing Fanhan Investment Management',
    stack: 'Python, Pandas, Scikit-Learn',
    period: 'May 2024 — Aug 2024',
    description:
      'Built an automated ETF volume-trend analysis pipeline processing 100,000+ intraday data points daily, surfacing anomalous volume spikes 3x faster than manual screening. Constructed factor-adjusted portfolios using Fama-French and CAPM regression models, reducing tracking error by 18% and directly informing 3 trading strategy adjustments adopted by the portfolio management team.',
  },
];
