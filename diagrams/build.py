"""Render the project architecture figures to PNG.

Each figure is laid out as HTML, screenshotted with headless Chrome, and
trimmed with Pillow. Output goes to public/diagrams/<slug>.png.

Every figure has its own visual style, so each one returns its own CSS
along with its HTML:

    chord-transformer      paper figure: serif, tinted panels, tables
    musdb                  blueprint: pipeline band + zoom-in callouts
    intersync              cards: A/B/C panels with numbered sections
    media-bias-detection   swimlanes: lanes x user flows

    python diagrams/build.py            # all figures
    python diagrams/build.py musdb      # one figure
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public' / 'diagrams'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
WIDTH = 1500
SCALE = 2

# ---------------------------------------------------------------- shared

_ICON_PATHS = {
    'db': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    'doc': '<path d="M6 2h9l5 5v15H6z"/><path d="M15 2v5h5"/><path d="M9 13h8M9 17h8"/>',
    'music': '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
    'wave': '<path d="M2 12h3l3-8 4 16 4-12 3 4h3"/>',
    'grid': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/>',
    'chip': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    'code': '<path d="M8 6l-6 6 6 6M16 6l6 6-6 6"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    'server': '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    'key': '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L21 2M16 7l3 3M19 4l2 2"/>',
    'lock': '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    'video': '<rect x="2" y="6" width="14" height="12" rx="2"/><path d="M16 10l6-3v10l-6-3z"/>',
    'bolt': '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    'spark': '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/>',
    'list': '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    'layers': '<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 12l10 5 10-5M2 17l10 5 10-5"/>',
    'speaker': '<path d="M11 5L6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/>',
    'box': '<path d="M21 8l-9-5-9 5 9 5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
    'term': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M6 9l3 3-3 3M12 15h5"/>',
    'puzzle': '<path d="M4 7h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4H4v-4a2 2 0 1 0 0-4z"/>',
    'filter': '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',
    'graph': '<circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7 7.5l3.5 8.5M17 7.5l-3.5 8.5M7.5 6h9"/>',
}


def icon(name, cls='ic'):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{_ICON_PATHS[name]}</svg>'
    )


def tile(name, color):
    """A coloured square with a white icon, like a file-type badge."""
    return f'<span class="tile" style="background:{color}">{icon(name, "tic")}</span>'


RA = '<svg class="ra" viewBox="0 0 28 12"><path d="M1 6h24M20 1.5L26 6l-6 4.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
LRA = '<svg class="ra" viewBox="0 0 28 12"><path d="M3 6h22M20 1.5L26 6l-6 4.5M8 1.5L2 6l6 4.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
DA = '<div class="da"><svg viewBox="0 0 12 22"><path d="M6 1v18M1.5 14L6 20l4.5-6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></div>'
UA = '<div class="da"><svg viewBox="0 0 12 22"><path d="M6 21V3M1.5 8L6 2l4.5 6" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></div>'

BASE_CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; background: #fff; }
body { width: %dpx; padding: 18px; }
.ic { width: 17px; height: 17px; flex: none; }
.tile { display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 7px; flex: none; }
.tic { width: 20px; height: 20px; color: #fff; }
.ra { width: 26px; height: 12px; flex: none; }
.da { display: flex; justify-content: center; margin: 3px 0; }
.da svg { width: 12px; height: 22px; }
.flow { display: flex; align-items: center; justify-content: center; gap: 6px; flex-wrap: wrap; row-gap: 8px; }
.step { display: inline-flex; align-items: center; gap: 6px; }
.mono { font-family: Menlo, Consolas, monospace; }
""" % WIDTH


def flow(*items, arrow=RA):
    # Keep each arrow attached to the item after it, so a wrapped line starts
    # with an arrow instead of ending on one.
    rest = ''.join(f'<span class="step">{arrow}{item}</span>' for item in items[1:])
    return f'<div class="flow">{items[0]}{rest}</div>'


def chroma(*levels):
    return '<span class="chroma">' + ''.join(f'<i style="height:{h}px"></i>' for h in levels) + '</span>'


# ================================================================ cards style
# Used by InterSync: three A/B/C panels, each with numbered sections.

CARDS_CSS = """
body { font: 15px/1.35 "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1f2328; }
.fig { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; align-items: stretch; }
.panel { border: 2px solid var(--c); border-radius: 12px; background: var(--t); padding: 0 12px 12px;
         display: flex; flex-direction: column; }
.panel .sec { flex: 1 1 auto; }
.pa { --c: #b4533a; --t: #fdf6f3; --s: #e9c4b8; }
.pb { --c: #85489a; --t: #faf5fb; --s: #dcc5e4; }
.pc { --c: #2c5591; --t: #f3f6fb; --s: #bfd0e8; }
h2 { margin: 0 -12px 12px; padding: 9px 14px; font-size: 20px; color: var(--c); background: #fff;
     border-bottom: 2px solid var(--c); border-radius: 10px 10px 0 0; text-align: center; }
.sec { background: #fff; border: 1.5px solid var(--s); border-radius: 9px; padding: 10px 12px 12px; margin-top: 12px; }
.sec:first-of-type { margin-top: 0; }
h3 { margin: 0 0 10px; font-size: 16.5px; display: flex; align-items: center; gap: 8px; color: var(--c); }
.num { display: inline-grid; place-items: center; width: 24px; height: 24px; border-radius: 50%;
       background: var(--c); color: #fff; font-size: 14px; flex: none; }
.box { display: inline-flex; align-items: center; gap: 6px; padding: 5px 9px; border: 1.5px solid #8b929c;
       border-radius: 7px; background: #fff; white-space: nowrap; }
.box.hl { border-color: var(--c); background: var(--t); }
.ic { color: var(--c); }
.ra, .da { color: #5b6170; }
.card { border: 1.5px solid #8b929c; border-radius: 8px; padding: 7px 10px; background: #fff; }
.card.hl { border-color: var(--c); background: var(--t); }
.ct { display: flex; align-items: center; gap: 7px; }
.cb { margin-top: 3px; color: #555b66; font-size: 13.5px; }
.row { display: grid; gap: 8px; }
.r2 { grid-template-columns: 1fr 1fr; }
.r3 { grid-template-columns: 1fr 1fr 1fr; }
.note { margin-top: 8px; font-size: 13px; color: #555b66; text-align: center; }
"""


def box(text, ic=None, cls=''):
    return f'<span class="box {cls}">{icon(ic) if ic else ""}<span>{text}</span></span>'


def card(title, body, ic=None, cls=''):
    head = f'<div class="ct">{icon(ic) if ic else ""}<b>{title}</b></div>'
    return f'<div class="card {cls}">{head}<div class="cb">{body}</div></div>'


def sec(n, title, body):
    return f'<div class="sec"><h3><span class="num">{n}</span>{title}</h3>{body}</div>'


def panel(letter, title, color, *secs):
    return f'<section class="panel p{color}"><h2>{letter}. {title}</h2>' + ''.join(secs) + '</section>'


def intersync():
    a = panel('A', 'Clients', 'a',
        sec(1, 'Two Roles', '<div class="row r2">'
            + card('Candidate', 'Next.js + React + MUI', 'user')
            + card('Interviewer', 'Next.js + React + MUI', 'user')
            + '</div>'),
        sec(2, 'Peer-to-Peer Video', flow(
            box('Browser A', 'video'), box('Browser B', 'video'), arrow=LRA,
        ) + '<div class="note">WebRTC media flows directly between browsers;<br>the server only relays signaling</div>'),
        sec(3, 'Auth', flow(
            box('sign in / sign up', 'lock'), box('Supabase Auth', 'key', 'hl'), box('route guard', 'lock'),
        ) + '<div class="note">email + password, password reset, middleware guard</div>'),
    )

    b = panel('B', 'Node.js Backend', 'b',
        sec(1, 'Express REST API', '<div class="row r2">'
            + card('Rooms', '/interview-rooms<br>/practice-rooms', 'server')
            + card('Content', '/questions /resumes<br>/recordings /profiles', 'server')
            + '</div>'),
        sec(2, 'Socket.IO Server', '<div class="row r3">'
            + card('Signaling', 'offer · answer · ICE', 'bolt')
            + card('Matchmaking', 'queue pairs users', 'user')
            + card('Judge result', 'first to pass wins', 'spark')
            + '</div>'),
        sec(3, 'Code Execution', flow(
            box('submission', 'code'), box('SSH', 'term'), box('remote VM', 'server', 'hl'), box('output', 'list'),
        ) + '<div class="note">compile and run on an isolated VM with a timeout</div>'),
    )

    c = panel('C', 'AI &amp; Data', 'c',
        sec(1, 'Semantic Resume Search', flow(
            box('PDF', 'doc'), box('chunk'), box('Gemini embed', 'chip'), box('pgvector HNSW', 'db', 'hl'),
        ) + DA + flow(box('query', 'search'), box('top chunks'), box('Gemini re-rank', 'spark', 'hl'))
            + '<div class="note">768-d gemini-embedding-001 · re-rank with Gemini 2.5 Flash</div>'),
        sec(2, 'Transcript Summaries', flow(
            box('saved transcript', 'doc'), box('Gemini', 'spark', 'hl'), box('summary', 'list'),
        )),
        sec(3, 'Supabase + Delivery', '<div class="row r2">'
            + card('Supabase', 'Postgres · pgvector<br>Storage · Auth', 'db', 'hl')
            + card('CI/CD', 'GitHub Actions<br>Docker image', 'box')
            + '</div>'),
    )
    return CARDS_CSS, f'<div class="fig">{a}{b}{c}</div>'


# ================================================================ paper style
# Used by Chord Transformer: serif type, tinted panels with stacked
# sub-panels, data tables and drawn model blocks.

PAPER_CSS = """
body { font: 15px/1.35 Georgia, "Times New Roman", serif; color: #1d1f24; }
.fig { display: grid; grid-template-columns: 1fr 1.1fr 1.1fr; gap: 16px; }
.pn { border: 2.5px solid var(--c); border-radius: 14px; padding: 12px 14px 14px; background: var(--t);
      display: flex; flex-direction: column; }
.pg { --c: #7d8794; --t: #f5f6f8; --k: #e6e9ee; }
.pt { --c: #1d8577; --t: #eff7f5; --k: #d5ece7; }
.pv { --c: #6b3fa0; --t: #f5f1fa; --k: #e6dcf2; }
.pn > h2 { margin: 0 0 10px; text-align: center; font-size: 22px; font-weight: 700; }
.sub { background: #fff; border: 1.5px solid #cfd4db; border-radius: 10px; padding: 9px 12px 12px;
       flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; }
.nw { white-space: nowrap; font-size: 12px; }
.loopflow .chip { padding: 4px 8px; font-size: 14px; }
.loopflow { gap: 3px; }
.loopflow .step { gap: 3px; }
.sub h3 { margin: 0 0 9px; text-align: center; font-size: 18px; font-weight: 700; }
.da, .ra { color: var(--c); }
.pn > .da svg { width: 14px; height: 24px; }
.cap { margin-top: 8px; text-align: center; font-size: 13.5px; font-style: italic; color: #4c525c; }
.chip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px; border: 1.5px solid #9aa1ab;
        border-radius: 7px; background: #fff; white-space: nowrap; }
.chip.k { border-color: var(--c); background: var(--k); }
.chip .ic { color: var(--c); }
.seqs { display: grid; grid-template-columns: 1fr 1.25fr 1fr; gap: 8px; }
.seq { border: 1.5px solid #9aa1ab; border-radius: 8px; padding: 6px; text-align: center; background: #fff; }
.seq small { display: block; font-size: 12.5px; color: #5c636d; margin-bottom: 4px; font-style: italic; }
.seq b { font-size: 16px; letter-spacing: .06em; }
.seq.gap { border: 1.8px dashed var(--c); background: var(--t); }
.chroma { display: inline-flex; align-items: flex-end; gap: 2px; height: 24px; }
.chroma i { display: block; width: 5px; background: var(--c); border-radius: 1px; opacity: .8; }
.stk { border: 1.8px solid var(--c); background: #fff; border-radius: 8px; padding: 8px 10px; text-align: center;
       margin: 10px 10px 0 0;
       box-shadow: 5px -5px 0 -1.8px #fff, 5px -5px 0 0 var(--c), 10px -10px 0 -1.8px #fff, 10px -10px 0 0 var(--c); }
.stk b { display: block; font-size: 16px; }
.stk span { font-size: 13px; color: #4c525c; }
.ed { display: grid; grid-template-columns: 1fr 74px 1fr; align-items: center; gap: 0 4px; }
.ed .mid { text-align: center; font-size: 12.5px; font-style: italic; color: var(--c); }
.ed .mid svg { width: 60px; height: 14px; display: block; margin: 0 auto 2px; }
.tbl { width: 100%; border-collapse: collapse; font-size: 14px; }
.tbl th { background: var(--k); font-weight: 700; padding: 4px 6px; border-bottom: 1.5px solid var(--c); }
.tbl td { padding: 4px 6px; border-bottom: 1px solid #e3e6ea; text-align: center; }
.tbl td:first-child { text-align: left; }
.tok { display: inline-block; padding: 1px 7px; border-radius: 5px; font-family: Menlo, Consolas, monospace; font-size: 12.5px; }
.tr { background: #fbe1d8; } .tq { background: #e5d9f3; } .tv { background: #d8e6f6; }
.beats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 8px; }
.beat { border: 1.5px solid #cfd4db; border-radius: 7px; padding: 5px 4px 4px; text-align: center; background: #fff; }
.beat small { display: block; font-size: 11.5px; color: #6a707a; }
.beat .chroma { height: 30px; }
.beat .chroma i { width: 4px; }
.beat b { display: block; margin-top: 2px; font-size: 14px; }
.lay { border: 1.5px solid #9aa1ab; border-radius: 7px; padding: 6px 10px; text-align: center; background: #fff; }
.lay.k { border-color: var(--c); background: var(--k); }
.lay small { display: block; font-size: 12.5px; color: #4c525c; font-style: italic; }
.blk { border: 1.8px solid var(--c); border-radius: 9px; padding: 8px; background: var(--t); margin: 10px 10px 0 0;
       box-shadow: 5px -5px 0 -1.8px var(--t), 5px -5px 0 0 var(--c), 10px -10px 0 -1.8px var(--t), 10px -10px 0 0 var(--c); }
.blk .bt { text-align: center; font-weight: 700; color: var(--c); margin-bottom: 6px; }
.blk .lay + .lay { margin-top: 6px; }
.loop { display: block; width: 100%; height: 34px; color: var(--c); }
.stat { display: grid; grid-template-columns: auto 1fr; gap: 12px; align-items: center; }
.big { font-size: 40px; font-weight: 700; color: var(--c); line-height: 1; }
.data { margin-top: 12px; padding-top: 10px; border-top: 1.5px dashed #b6bcc5; }
.data h4 { margin: 0 0 8px; text-align: center; font-size: 17px; }
.src { display: flex; gap: 10px; align-items: center; }
.src + .src { margin-top: 8px; }
.src span { font-size: 13.5px; color: #4c525c; }
"""


def chip(text, ic=None, cls=''):
    return f'<span class="chip {cls}">{icon(ic) if ic else ""}<span>{text}</span></span>'


def chord_transformer():
    harmonizer = f'''
<section class="pn pg"><h2>Melody Harmonizer</h2>
  <div class="sub"><h3>Input</h3>
    <div class="seqs">
      <div class="seq"><small>past chords</small><b>C F G C</b></div>
      <div class="seq gap"><small>melody to harmonize</small>{chroma(18, 4, 9, 3, 16, 5, 2, 20, 4, 8, 3, 11)}</div>
      <div class="seq"><small>future chords</small><b>F C G C</b></div>
    </div>
  </div>
  {DA}
  <div class="sub grow"><h3>ChordHarmonizer</h3>
    <div class="ed">
      <div class="stk"><b>Encoder × 4</b><span>bidirectional over<br><span class="mono nw">past|SEP|future</span></span></div>
      <div class="mid"><svg viewBox="0 0 60 14"><path d="M1 7h56M51 2l7 5-7 5" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>cross-<br>attention</div>
      <div class="stk"><b>Decoder × 4</b><span>causal, generates<br>chord tokens</span></div>
    </div>
    <div class="ed" style="margin-top:6px">
      <div></div><div></div>
      <div>{UA}<div class="lay k">melody chroma<small>Linear(12 → 256), added per token</small></div></div>
    </div>
    <div class="cap">each chord is embedded as emb(root) + emb(quality) + emb(voicing)</div>
  </div>
  {DA}
  <div class="sub"><h3>Output</h3>
    {flow(chip('3 tokens per melody beat'), chip('chord names for the gap', cls='k'))}
  </div>
  <div class="data"><h4>Training Data</h4>
    <div class="src">{tile('db', '#4a6fa5')}<div><b>Chordonomicon</b><br><span>chord progressions → chord LM</span></div></div>
    <div class="src">{tile('music', '#b4533a')}<div><b>Wikifonia</b><br><span>~6K MusicXML lead sheets → harmonizer</span></div></div>
  </div>
</section>'''

    tokens = ''.join(
        f'<tr><td class="mono">{c}</td><td><span class="tok tr">{r}</span></td>'
        f'<td><span class="tok tq">{q}</span></td><td><span class="tok tv">{v}</span></td></tr>'
        for c, r, q, v in [
            ('C', 'C', 'maj', 'none'),
            ('Amin', 'A', 'min', 'none'),
            ('Fs7', 'Fs', 'dom7', 'none'),
            ('Cadd9', 'C', 'maj', 'add9'),
            ('Bbmin7', 'As', 'min7', 'none'),
        ])
    beats = ''.join(
        f'<div class="beat"><small>beat {i}</small>{chroma(*lv)}<b>{ch}</b></div>'
        for i, (ch, lv) in enumerate([
            ('C', (26, 3, 6, 2, 18, 4, 2, 22, 3, 5, 2, 4)),
            ('C', (12, 2, 8, 3, 26, 3, 2, 14, 2, 6, 2, 3)),
            ('F', (8, 2, 6, 3, 4, 26, 2, 5, 3, 20, 2, 4)),
            ('G', (4, 2, 18, 3, 6, 3, 4, 26, 2, 5, 3, 16)),
        ], 1))
    prep = f'''
<section class="pn pt"><h2>Tokenize &amp; Prepare Data</h2>
  <div class="sub"><h3>Chord Tokenizer</h3>
    <table class="tbl"><tr><th>chord</th><th>root</th><th>quality</th><th>voicing</th></tr>{tokens}</table>
    <div class="cap">every chord becomes 3 tokens; flats are respelled (B♭ → A♯) and slash bass is dropped</div>
  </div>
  {DA}
  <div class="sub grow"><h3>Lead-Sheet Processing</h3>
    {flow(chip('.mxl lead sheet', 'doc'), chip('beat grid', 'grid'), chip('(chroma, chord) per beat', cls='k'))}
    <div class="beats">{beats}</div>
    <div class="cap">12-d melody chroma per beat, saved as .npz with a manifest</div>
  </div>
  {DA}
  <div class="sub"><h3>Training Objectives</h3>
    <table class="tbl">
      <tr><th>model</th><th>data</th><th>objective</th></tr>
      <tr><td>Chord LM</td><td>Chordonomicon</td><td>next chord token</td></tr>
      <tr><td>Harmonizer</td><td>Wikifonia pairs</td><td>chords for the gap</td></tr>
    </table>
  </div>
</section>'''

    loop = ('<svg class="loop" viewBox="0 0 400 34" preserveAspectRatio="none">'
            '<path d="M372 2 V18 Q372 28 362 28 H38 Q28 28 28 18 V8" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4"/>'
            '<path d="M23 12 L28 3 L33 12" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>')
    lm = f'''
<section class="pn pv"><h2>Chord Language Model</h2>
  <div class="sub grow"><h3>Decoder-only Transformer</h3>
    <div class="lay k">logits over the chord vocabulary</div>
    {UA}
    <div class="lay">LayerNorm → linear head</div>
    {UA}
    <div class="blk"><div class="bt">Transformer block × 4</div>
      <div class="lay">causal self-attention<small>fused QKV projection · 4 heads</small></div>
      <div class="lay">MLP</div>
    </div>
    {UA}
    <div class="lay">token embedding + position embedding<small>d<sub>model</sub> = 256</small></div>
    {UA}
    <div style="text-align:center"><span class="tok tr">C</span> <span class="tok tq">maj</span> <span class="tok tv">none</span>
      &nbsp;<span class="tok tr">F</span> <span class="tok tq">maj</span> <span class="tok tv">none</span> &nbsp;…</div>
  </div>
  {DA}
  <div class="sub"><h3>Autoregressive Decoding</h3>
    <div class="loopflow">{flow(chip('÷ temperature', cls='k'), chip('top-k', cls='k'), chip('rep. penalty', cls='k'), chip('sample'))}</div>
    {loop}
    <div class="cap" style="margin-top:0">append the token and repeat until EOS</div>
  </div>
  {DA}
  <div class="sub"><h3>Result</h3>
    <div class="stat"><div class="big">1.44</div><div>next-token perplexity<br><i style="color:#4c525c">weights reused to initialize the harmonizer decoder</i></div></div>
  </div>
</section>'''
    return PAPER_CSS, f'<div class="fig">{harmonizer}{prep}{lm}</div>'


# ================================================================ blueprint style
# Used by musdb: a pipeline band across the top, with zoom-in callouts below.

BLUEPRINT_CSS = """
body { font: 14.5px/1.35 "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: #0f172a; }
.band { position: relative; border: 2px solid #1e293b; border-radius: 12px; padding: 30px 16px 16px;
        background-color: #f8fafc;
        background-image: linear-gradient(#e2e8f0 1px, transparent 1px), linear-gradient(90deg, #e2e8f0 1px, transparent 1px);
        background-size: 22px 22px; }
.lbl { position: absolute; top: -12px; left: 18px; background: #1e293b; color: #fff; font-size: 12.5px; font-weight: 700;
       letter-spacing: .12em; padding: 3px 10px; border-radius: 5px; }
.stages { display: flex; align-items: stretch; gap: 0; }
.stage { flex: 1; background: #fff; border: 2px solid #1e293b; border-radius: 10px; padding: 10px; text-align: center; position: relative; }
.stage.pl { border-style: dashed; border-color: #64748b; }
.stage .n { position: absolute; top: -12px; left: -10px; width: 26px; height: 26px; border-radius: 50%; background: #d97706;
            color: #fff; font-weight: 700; display: grid; place-items: center; font-size: 14px; }
.stage .tile { display: grid; margin: 0 auto; width: 44px; height: 44px; border-radius: 10px; }
.lane .node { white-space: nowrap; }
.call .body .dist { flex: 1; }
.bar { height: 100% !important; min-height: 150px; }
.col { height: 100%; }
.stage .tic { width: 25px; height: 25px; }
.stage b { display: block; margin-top: 6px; font-size: 16px; }
.stage span { display: block; font-size: 13px; color: #475569; margin-top: 2px; }
.pill { display: inline-block; margin-top: 7px; font-size: 11.5px; font-weight: 700; padding: 2px 9px; border-radius: 10px; letter-spacing: .03em; }
.built { background: #dcfce7; color: #166534; }
.plan { background: #fef3c7; color: #92400e; }
.part { background: #e0f2fe; color: #075985; }
.arrow { display: flex; align-items: center; color: #1e293b; padding: 0 6px; }
.arrow svg { width: 30px; height: 16px; }
.zoom { display: grid; grid-template-columns: repeat(3, 1fr); position: relative; height: 34px; }
.zoom svg { width: 100%; height: 34px; color: #94a3b8; }
.calls { display: grid; grid-template-columns: 1fr 1fr 1.15fr; gap: 16px; }
.call { border: 2px solid #1e293b; border-radius: 12px; overflow: hidden; background: #fff; display: flex; flex-direction: column; }
.call > h3 { margin: 0; background: #1e293b; color: #fff; font-size: 16px; padding: 8px 12px; display: flex; align-items: center; gap: 8px; }
.call > h3 .n { width: 22px; height: 22px; border-radius: 50%; background: #d97706; display: grid; place-items: center; font-size: 13px; }
.call .body { padding: 12px; flex: 1; display: flex; flex-direction: column; gap: 10px; }
.cap { font-size: 13px; color: #475569; text-align: center; }
.dist { display: grid; grid-template-columns: repeat(8, 1fr); gap: 6px; align-items: end; }
.col { display: flex; flex-direction: column; align-items: center; gap: 3px; }
.bar { width: 100%; height: 130px; display: flex; flex-direction: column-reverse; border: 1px solid #cbd5e1; border-radius: 4px; overflow: hidden; }
.bar i { display: block; }
.col small { font-size: 11.5px; color: #64748b; }
.col b { font-size: 12.5px; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 12px; justify-content: center; font-size: 12.5px; }
.legend span { display: inline-flex; align-items: center; gap: 5px; }
.legend i { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.lane { display: flex; align-items: center; gap: 8px; justify-content: center; }
.node { border: 1.8px solid #1e293b; border-radius: 8px; padding: 6px 10px; background: #fff; text-align: center; font-size: 13.5px; }
.node.pl { border-style: dashed; }
.node small { display: block; color: #64748b; font-size: 12px; }
.node.acc { border-color: #d97706; background: #fffbeb; }
.ra { color: #1e293b; }
.da { color: #1e293b; }
.segs { border: 1.8px dashed #1e293b; border-radius: 8px; overflow: hidden; }
.segs table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.segs th { background: #e2e8f0; padding: 4px; font-weight: 700; }
.segs td { padding: 4px; text-align: center; border-top: 1px solid #e2e8f0; color: #334155; }
.segs td:first-child { font-family: Menlo, Consolas, monospace; font-size: 12px; }
.idx { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.code { background: #0f172a; color: #e2e8f0; border-radius: 8px; padding: 8px 10px; font-family: Menlo, Consolas, monospace; font-size: 13px; text-align: center; }
.code em { color: #fbbf24; font-style: normal; }
.toks { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; }
.toks span { font-family: Menlo, Consolas, monospace; font-size: 12.5px; background: #fef3c7; border: 1px solid #f59e0b; border-radius: 5px; padding: 2px 7px; }
.paths { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.path { border: 1.8px dashed #1e293b; border-radius: 9px; padding: 8px; text-align: center; }
.path b { display: block; font-size: 14px; }
.path > small { display: block; font-size: 12.5px; color: #475569; margin-top: 4px; }
.sw { display: grid; grid-template-columns: repeat(7, 13px); gap: 2px; justify-content: center; margin: 6px auto 0; }
.sw i { width: 13px; height: 13px; background: #e2e8f0; border-radius: 2px; }
.sw i.on { background: #d97706; }
.foot { margin-top: 12px; display: flex; justify-content: center; gap: 22px; font-size: 13px; color: #475569; align-items: center; }
.foot .node { font-size: 12.5px; padding: 2px 9px; }
"""


def node(text, sub=None, cls=''):
    return f'<div class="node {cls}">{text}{f"<small>{sub}</small>" if sub else ""}</div>'


def musdb():
    arrow = '<div class="arrow"><svg viewBox="0 0 30 16"><path d="M1 8h25M20 2l7 6-7 6" fill="none" stroke="currentColor" stroke-width="2.2"/></svg></div>'
    stages = [
        ('wave', '#0f766e', 'Sources', 'audio files · scores', ('part', 'audio built')),
        ('chip', '#0f766e', 'Front End', 'decode · 22.05 kHz · STFT · CQT', ('built', 'built')),
        ('music', '#64748b', 'Analysis', 'chords · beats · key · sections', ('plan', 'planned')),
        ('list', '#64748b', 'Facts Layer', 'one record per song, with source + confidence', ('plan', 'planned')),
        ('db', '#64748b', 'Storage', 'WAL · column segments · indexes', ('plan', 'planned')),
        ('search', '#64748b', 'Query', 'DSL · planner · two match paths', ('plan', 'planned')),
    ]
    cards = []
    for i, (ic, color, title, sub, (pk, pt)) in enumerate(stages, 1):
        cls = '' if pk != 'plan' else 'pl'
        cards.append(f'<div class="stage {cls}"><div class="n">{i}</div>{tile(ic, color)}<b>{title}</b>'
                     f'<span>{sub}</span><div class="pill {pk}">{pt}</div></div>')
    band = (f'<div class="band"><div class="lbl">PIPELINE · C++20 LIBRARY + CLI</div>'
            f'<div class="stages">{arrow.join(cards)}</div></div>')

    # Dashed leaders from stages 3, 5 and 6 down to their callouts.
    zoom = ('<svg style="display:block;width:100%;height:34px;color:#94a3b8" viewBox="0 0 1464 34" preserveAspectRatio="none">'
            '<path d="M612 0 V14 H244 V34" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="6 5"/>'
            '<path d="M1110 0 V14 H720 V34" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="6 5"/>'
            '<path d="M1360 0 V14 H1220 V34" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="6 5"/></svg>')

    # Illustrative per-beat chord distributions for Am7 → D7 → Gmaj7 → Cmaj7.
    colors = {'Am7': '#0f766e', 'D7': '#2563eb', 'Gmaj7': '#7c3aed', 'Cmaj7': '#d97706', 'Em': '#f59e0b', 'C': '#fbbf24', 'other': '#cbd5e1'}
    beats = [
        ('Am7', [('Am7', 70), ('C', 12), ('other', 18)]),
        ('Am7', [('Am7', 64), ('C', 16), ('other', 20)]),
        ('D7', [('D7', 72), ('Am7', 10), ('other', 18)]),
        ('D7', [('D7', 66), ('other', 34)]),
        ('Gmaj7', [('Gmaj7', 74), ('other', 26)]),
        ('Gmaj7', [('Gmaj7', 68), ('Em', 12), ('other', 20)]),
        ('Cmaj7?', [('Cmaj7', 50), ('Em', 35), ('other', 15)]),
        ('Cmaj7?', [('Cmaj7', 48), ('Em', 38), ('other', 14)]),
    ]
    cols = ''.join(
        '<div class="col"><b>' + top + '</b><div class="bar">'
        + ''.join(f'<i style="height:{p}%;background:{colors[c]}"></i>' for c, p in parts)
        + f'</div><small>beat {i}</small></div>'
        for i, (top, parts) in enumerate(beats, 1))
    legend = ''.join(f'<span><i style="background:{colors[c]}"></i>{c}</span>' for c in colors)
    call1 = f'''
<div class="call"><h3><span class="n">3</span>Chords stored as distributions</h3><div class="body">
  <div class="dist">{cols}</div>
  <div class="legend">{legend}</div>
  <div class="cap">top-5 chords + leftover mass per beat (~10 bytes).<br>Cmaj7 vs Em stays ambiguous instead of being forced. <i>(illustration)</i></div>
</div></div>'''

    call2 = f'''
<div class="call"><h3><span class="n">5</span>OLAP-style storage engine</h3><div class="body">
  <div class="lane">{node('single writer', cls='pl')}{RA}{node('WAL', 'append, checksummed', 'pl')}{RA}{node('manifest', 'lists live segments', 'pl')}</div>
  {DA}
  <div class="segs"><table>
    <tr><th>segment</th><th>chords</th><th>chroma</th><th>vectors</th><th>scalars</th></tr>
    <tr><td>seg-001</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td></tr>
    <tr><td>seg-002</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td></tr>
    <tr><td>seg-003</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td><td>▮▮▮</td></tr>
  </table></div>
  <div class="cap">immutable, column-per-feature, mmap reads, background compaction</div>
  <div class="idx">{node('B-tree', 'BPM · key · duration', 'pl')}{node('postings', 'chord k-mers', 'pl')}{node('HNSW', 'chroma vectors', 'pl')}</div>
  {node('blob store', 'audio + scores, addressed by content hash', 'pl')}
</div></div>'''

    sw = ''.join('<i class="on"></i>' if r == c - 1 and 1 <= c <= 5 else '<i></i>' for r in range(5) for c in range(7))
    call3 = f'''
<div class="call"><h3><span class="n">6</span>Same progression, any key</h3><div class="body">
  <div class="code">prog:from(<em>"Song A"</em>, <em>0:45..1:05</em>)</div>
  <div class="lane">{node('Am7 → D7 → Gmaj7 → Cmaj7', 'chords in the range')}</div>
  {DA}
  <div class="toks"><span>+5 · m7→7</span><span>+5 · 7→maj7</span><span>+5 · maj7→maj7</span></div>
  <div class="cap">chord-change tokens: root interval + quality change, so key and tempo drop out</div>
  <div class="paths">
    <div class="path"><b>Path A · same chords</b><div class="sw">{sw}</div><small>Smith–Waterman local alignment<br>with music-aware costs</small></div>
    <div class="path"><b>Path B · similar harmony</b>
      <div class="lane" style="margin-top:6px">{node('chroma')}{RA}{node('|2D FFT|')}{RA}{node('HNSW')}</div>
      <small>catches substitutions and<br>reharmonizations</small></div>
  </div>
  <div class="lane">{node('RRF fusion', cls='pl acc')}{RA}{node('hits', 'song · start · end · alignment', 'pl')}</div>
</div></div>'''

    foot = (f'<div class="foot">{node("solid")} built {node("dashed", cls="pl")} planned'
            '<span>· CLI today: <span class="mono">musdb ingest</span>, <span class="mono">musdb cqt</span></span></div>')
    return BLUEPRINT_CSS, f'{band}{zoom}<div class="calls">{call1}{call2}{call3}</div>{foot}'


# ================================================================ swimlane style
# Used by Media Bias Detection: one lane per tier, one column per user flow.

LANES_CSS = """
body { font: 14.5px/1.35 "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: #10231b; }
.grid { display: grid; grid-template-columns: 190px repeat(3, 1fr); border: 2px solid #14532d; border-radius: 12px; overflow: hidden; }
.hd { background: #14532d; color: #fff; padding: 12px 14px; display: flex; align-items: center; gap: 10px; font-size: 17px; font-weight: 600; }
.hd .n { width: 28px; height: 28px; border-radius: 50%; background: #fbbf24; color: #14532d; display: grid; place-items: center; font-weight: 800; flex: none; }
.hd small { display: block; font-weight: 400; font-size: 12.5px; color: #bbf7d0; }
.corner { background: #0f3d22; color: #bbf7d0; font-size: 12px; letter-spacing: .12em; font-weight: 700; display: grid; place-items: center; }
.ln { padding: 12px; display: flex; flex-direction: column; gap: 6px; align-items: center; gap: 8px; text-align: center;
      border-top: 1.5px solid #bbd9c6; }
.ln.side { background: #e8f3ec; justify-content: center; border-right: 1.5px solid #bbd9c6; }
.ln.side b { font-size: 16px; }
.ln.side span { font-size: 12.5px; color: #3f5f4f; }
.ln.side .tile { width: 42px; height: 42px; border-radius: 10px; }
.ln.side .tic { width: 24px; height: 24px; }
.r1 { background: #fff; } .r2 { background: #f6fbf8; } .r3 { background: #fffbf0; }
.ln + .ln:not(.side) { border-left: 1.5px dashed #bbd9c6; }
.call { font-family: Menlo, Consolas, monospace; font-size: 12px; color: #14532d; background: #dcfce7; border: 1px solid #86efac;
        border-radius: 5px; padding: 2px 7px; }
.pill { display: inline-flex; align-items: center; gap: 6px; border: 1.6px solid #2f6b4a; border-radius: 18px; padding: 5px 12px; background: #fff; white-space: nowrap; }
.pill .ic { color: #2f6b4a; }
.pill.ext { border-color: #c2410c; background: #fff7ed; }
.pill.ext .ic { color: #c2410c; }
.pill.out { background: #14532d; color: #fff; border-color: #14532d; }
.pill.out .ic { color: #fbbf24; }
.da, .ra { color: #2f6b4a; }
.note { font-size: 12.5px; color: #4b6a5a; }
.ret { grid-column: 2 / span 3; border-top: 1.5px solid #bbd9c6; background: #14532d; color: #dcfce7; padding: 8px 14px;
       font-size: 13.5px; text-align: center; }
.ret b { color: #fbbf24; }
.graph { display: flex; align-items: center; gap: 6px; }
.legend { margin-top: 10px; display: flex; gap: 18px; justify-content: center; font-size: 13px; color: #3f5f4f; align-items: center; }
"""


def pill(text, ic=None, cls=''):
    return f'<span class="pill {cls}">{icon(ic) if ic else ""}{text}</span>'


def media_bias():
    head = (
        '<div class="corner">LANE ↓ · FLOW →</div>'
        '<div class="hd"><span class="n">1</span><div>Watch a YouTube video<small>summary + fact checks</small></div></div>'
        '<div class="hd"><span class="n">2</span><div>Read a news article<small>find opposing viewpoints</small></div></div>'
        '<div class="hd"><span class="n">3</span><div>Debate a claim<small>two agents argue it out</small></div></div>'
    )
    ext = (
        f'<div class="ln side">{tile("puzzle", "#2f6b4a")}<b>Chrome Extension</b><span>Manifest V3 · React + Vite</span></div>'
        f'<div class="ln r1">{pill("content script on youtube.com", "video")}{DA}{pill("transcript popup", "list")}</div>'
        f'<div class="ln r1">{pill("content script on any page", "globe")}{DA}{pill("article popup", "doc")}</div>'
        f'<div class="ln r1">{pill("debate view", "user")}{DA}{pill("enter a claim", "puzzle")}</div>'
    )
    api = (
        f'<div class="ln side">{tile("server", "#2f6b4a")}<b>FastAPI Backend</b><span>Python · 3 routers</span></div>'
        f'<div class="ln r2"><span class="call">GET /vid/youtube-transcript/{{id}}</span>{DA}'
        f'{pill("fetch transcript", "doc")}{DA}{pill("build summary + fact-check prompts", "list")}</div>'
        f'<div class="ln r2"><span class="call">GET /article/alternative?url=</span>{DA}'
        f'{pill("extract article text", "doc")}{DA}{pill("ask for bias + 3 opposing search terms", "filter")}</div>'
        f'<div class="ln r2"><span class="call">WS /debate/run-ws · SSE /run-stream</span>{DA}'
        f'{pill("LangGraph StateGraph", "graph")}'
        f'<div class="graph">{pill("pro_agent", "user")}{LRA}{pill("con_agent", "user")}</div>'
        f'<span class="note">alternate until max rounds → END</span></div>'
    )
    svc = (
        f'<div class="ln side">{tile("spark", "#c2410c")}<b>External Services</b><span>LLMs · search · vectors · voice</span></div>'
        f'<div class="ln r3">{pill("Gemini 2.5 Flash", "spark", "ext")}{DA}{pill("summary + fact checks (JSON)", "list", "out")}</div>'
        f'<div class="ln r3">{pill("Gemini 2.5 Flash", "spark", "ext")}{DA}{pill("SerpAPI Google search", "search", "ext")}{DA}'
        f'{pill("alternative sources", "globe", "out")}</div>'
        f'<div class="ln r3">{pill("Pinecone · top-5 evidence", "db", "ext")}{DA}{pill("Gemini 2.5 Pro", "spark", "ext")}{DA}'
        f'{pill("argument per turn", "doc", "out")}<span class="note">optional: ElevenLabs reads each turn aloud</span></div>'
    )
    ret = ('<div class="corner" style="border-top:1.5px solid #bbd9c6">RETURN ↑</div>'
           '<div class="ret">Results go back up to the extension: <b>JSON</b> for flows 1 and 2, '
           '<b>one streamed message per debate turn</b> for flow 3</div>')
    legend = (f'<div class="legend">{pill("our code", "code")} {pill("external API", "spark", "ext")} '
              f'{pill("what the user sees", "list", "out")}</div>')
    return LANES_CSS, f'<div class="grid">{head}{ext}{api}{svc}{ret}</div>{legend}'


FIGURES = {
    'chord-transformer': chord_transformer,
    'musdb': musdb,
    'intersync': intersync,
    'media-bias-detection': media_bias,
}

# ---------------------------------------------------------------- render


def render(slug, css, body, tmp):
    html = tmp / f'{slug}.html'
    html.write_text(f'<!doctype html><meta charset="utf-8"><style>{BASE_CSS}{css}</style>{body}', encoding='utf-8')
    raw = tmp / f'{slug}.png'
    subprocess.run([
        CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
        f'--force-device-scale-factor={SCALE}', f'--window-size={WIDTH},2400',
        f'--screenshot={raw}', html.as_uri(),
    ], check=True, capture_output=True)

    img = Image.open(raw).convert('RGB')
    bbox = ImageChops.difference(img, Image.new('RGB', img.size, 'white')).getbbox()
    pad = 16 * SCALE
    img = img.crop((0, 0, img.width, min(img.height, bbox[3] + pad)))
    OUT.mkdir(parents=True, exist_ok=True)
    # Write then rename, so the dev server never serves a half-written PNG.
    part = OUT / f'{slug}.png.part'
    img.save(part, format='PNG', optimize=True)
    part.replace(OUT / f'{slug}.png')
    print(f'{slug}: {img.width}x{img.height}')


def main():
    slugs = sys.argv[1:] or list(FIGURES)
    with tempfile.TemporaryDirectory() as d:
        for slug in slugs:
            css, body = FIGURES[slug]()
            render(slug, css, body, Path(d))


if __name__ == '__main__':
    main()
