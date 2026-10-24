export type Project = {
  slug: string;
  title: string;
  description: string;
  points?: string[];
  // Path to an architecture figure in public/, rendered by diagrams/build.py.
  diagram?: string;
  href?: string;
  year: string;
  tags?: string[];
};

export const projects: Project[] = [
  {
    slug: 'chord-transformer',
    title: 'Chord Transformer',
    description:
      'A small decoder-only transformer built from scratch in PyTorch for chord progression generation.',
    points: [
      'Trained on 666,000 songs from the Chordonomicon dataset',
      'Multi-head causal self-attention with fused QKV projections',
      'Autoregressive decoding with temperature sampling, top-k, and repetition penalty',
      'Achieved next-token perplexity of 1.44',
    ],
    href: 'https://github.com/shawnjiang1019/chord-transformer',
    year: '2026',
    diagram: '/diagrams/chord-transformer.png',
    tags: ['pytorch', 'transformer', 'nlp'],
  },
  {
    slug: 'musdb',
    title: 'musdb',
    description:
      'A content-based music retrieval engine in C++20 (in progress).',
    points: [
      'Derives key, tempo and chords from audio and MusicXML instead of metadata',
      'Designed to find songs with the same chord progression in any key',
    ],
    href: 'https://github.com/shawnjiang1019/musdb',
    year: '2026',
    diagram: '/diagrams/musdb.png',
    tags: ['c++', 'mir', 'databases', 'dsp'],
  },
  {
    slug: 'intersync',
    title: 'InterSync',
    description:
      'A real-time collaborative interview platform with video calls and live code execution.',
    points: [
      'WebRTC video conferencing',
      'Codeforces-style automated judge with server-side validation and real-time winner declaration',
      'Resume chunking and semantic search via Gemini embeddings and HNSW graphs',
      'CI/CD through GitHub Actions and Docker',
    ],
    href: 'https://github.com/shawnjiang1019',
    year: '2025',
    diagram: '/diagrams/intersync.png',
    tags: ['webrtc', 'node.js', 'jwt', 'real-time'],
  },
  {
    slug: 'media-bias-detection',
    title: 'Media Bias Detection',
    description:
      'A real-time bias and sentiment detection web extension for videos and news articles.',
    points: [
      'Built with FastAPI and PineconeDB',
      'LangGraph multi-agent RAG pipeline with memory-augmented context retrieval',
      'Reduced LLM hallucination by 35% by grounding responses with SerpAPI-sourced links',
    ],
    href: 'https://github.com/shawnjiang1019',
    year: '2024',
    diagram: '/diagrams/media-bias-detection.png',
    tags: ['fastapi', 'langgraph', 'pinecone', 'rag'],
  },
];
