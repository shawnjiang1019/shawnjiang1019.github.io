export type Experience = {
  role: string;
  company: string;
  stack: string;
  period: string;
  points: string[];
};

export const experience: Experience[] = [
  {
    role: 'Software Engineer Intern',
    company: 'Huawei Canada',
    stack: 'Rust, Python, AI Agents, Databases',
    period: 'Aug 2026 — Present',
    points: [
      'Working on data agents in the Distributed Data Storage and Management Lab, supervised by Tianqing Wang',
      'Researching grounding methods and architectures for more efficient data agents, aiming for conference publication',
      'Built an offline annotation pipeline for clustering and deriving entity relations, giving a +7% increase on KramaBench',
      'Building agent harness and control mechanisms for observability and autonomous analysis in heterogeneous data lakes',
    ],
  },
  {
    role: 'Undergraduate Researcher',
    company: 'Lee Language Lab',
    stack: 'Python, PyTorch, RL, LLMs',
    period: 'Apr 2026 — Present',
    points: [
      'Researching methods for pluralistic reasoning in LLMs, supervised by Dr. Annie Lee and Dr. Enas Altarawneh',
      'Fine-tuned models with LoRA and RL methods to enable structural interpretation and reasoning on graph structures',
      'Designed a test-time dissimilarity injection mechanism, raising the OvertonBench metric from 0.48 to 0.54',
    ],
  },
  {
    role: 'Software Engineer',
    company: 'Remeda',
    stack: 'Python, React, Deep Learning',
    period: 'Apr 2026 — Jul 2026',
    points: [
      'Worked on job scheduling and CI/CD build deployment',
      'Built features integrating auscultation audio and medical imaging with clinical text for diagnostic reasoning models',
    ],
  },
  {
    role: 'Software Engineer',
    company: 'University of Toronto',
    stack: 'Python, React, FastAPI, PostgreSQL, GCP',
    period: 'May 2025 — Sep 2025',
    points: [
      'Architected and shipped a full-stack peer assessment platform that lets instructors benchmark student-group performance, now used by 200+ students',
      'Engineered a drag-and-drop ingestion pipeline with CSV parsing and schema validation, cutting manual data entry time by 80%',
      'Deployed a serverless REST API on GCP Cloud Run behind a reverse proxy. Supervised by Prof. Sohee Kang',
    ],
  },
  {
    role: 'Software Engineer Intern',
    company: 'Seequent',
    stack: 'C#, .NET',
    period: 'Jan 2025 — Apr 2025',
    points: [
      'Shipped production backend features in C#/.NET for geophysical modeling software used by 10,000+ geoscientists, including object conversion modules on the Evo cloud platform',
      'Triaged and resolved 50+ bugs across automated test suites in an agile sprint cadence, shipping fixes to production within the same sprint',
    ],
  },
  {
    role: 'Data Science Intern',
    company: 'Fanhan Investment Management',
    stack: 'Python, Pandas, Scikit-Learn',
    period: 'May 2024 — Aug 2024',
    points: [
      'Constructed factor-adjusted portfolios using Fama-French and CAPM regression models in Scikit-Learn',
      'Identified overexposed risk factors and rebalanced allocations, reducing tracking error by 18%',
    ],
  },
];
