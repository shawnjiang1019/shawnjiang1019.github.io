export type Project = {
  slug: string;
  title: string;
  description: string;
  href?: string;
  year: string;
  tags?: string[];
};

export const projects: Project[] = [
  {
    slug: 'chord-transformer',
    title: 'Chord Transformer',
    description:
      'A 3.3M-parameter decoder-only transformer built from scratch in PyTorch for chord progression generation. Trained on 666,000 songs from the Chordonomicon dataset with multi-head causal self-attention, fused QKV projections, and an autoregressive decoding pipeline (temperature sampling, top-k, repetition penalty). Achieved next-token perplexity of 1.44.',
    href: 'https://github.com/shawnjiang1019/chord-transformer',
    year: '2026',
    tags: ['pytorch', 'transformer', 'nlp'],
  },
  {
    slug: 'intersync',
    title: 'InterSync',
    description:
      'A real-time collaborative interview platform with WebRTC video conferencing and live code execution. Includes a Codeforces-style automated judge with server-side validation and real-time winner declaration, plus resume chunking and semantic search via Gemini embeddings and HNSW graphs. CI/CD through GitHub Actions and Docker.',
    href: 'https://github.com/shawnjiang1019',
    year: '2025',
    tags: ['webrtc', 'node.js', 'jwt', 'real-time'],
  },
  {
    slug: 'media-bias-detection',
    title: 'Media Bias Detection',
    description:
      'A real-time bias and sentiment detection web extension for videos and news articles, built with FastAPI, PineconeDB, and a LangGraph multi-agent RAG pipeline with memory-augmented context retrieval. Reduced LLM hallucination by 35% by grounding responses with SerpAPI-sourced contextual links.',
    href: 'https://github.com/shawnjiang1019',
    year: '2024',
    tags: ['fastapi', 'langgraph', 'pinecone', 'rag'],
  },
];
