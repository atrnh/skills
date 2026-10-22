# Notes file format

Directives at column zero. Everything between them is raw HTML, passed through untouched —
no escaping, no JSON, no quoting rules.

```
@meta title       Notes on “tadpoles”
@meta kicker      Notes · Baldur’s Gate 3 · chapter 2
@meta h1          <em>tadpoles</em>
@meta dek         Your prose on the left, my notes on the right. …
@meta metarow     <span><b>File</b> tadpoles.md · __PARA_COUNT__ paragraphs</span> …
@meta accent      #8c2f2f
@meta accent-dark #e08a86
@meta cont        #9a6414
@meta cont-dark   #e0b072

@letter
<h2>The short version</h2>
<p>…</p>
<dl class="verdict">
  <div><dt>Best thing here</dt><dd>The vision as plot engine</dd></div>
  …
</dl>

@banner 7 pass
Duplicated paragraph | ¶7 and ¶8 are two drafts of one beat, left stacked.

@banner 31 seam
<b>The splice.</b> ¶31 picks up from Astarion’s question in ¶27 …

@note 6
<div class="card cont"><span class="tag t-cont">continuity</span>
  <p class="hd">She knows things she hasn’t been told yet</p>
  <p>…</p></div>

@footer
Notes on <code>Areas/Fiction/bg3/tadpoles.md</code>, __DATE__. The manuscript is unchanged.
```

## Rules

- **`@note N`** attaches to paragraph N. Multiple `@note N` blocks for the same N stack in
  order. Paragraphs with no note render an empty comment column — that is correct and
  normal. Do not manufacture notes to fill gaps.
- **`@banner N <class>`** places a full-width band immediately *before* row N.
  - `pass` / `movement` — takes `Label | text`. Use `pass` to diagnose (two drafts, a
    duplicated beat); use `movement` to name a section of the chapter ("Movement 2 · the
    lecture"). They render identically; the distinction is what you are asserting.
  - `seam` — no label, dashed rule, one sentence. For the exact point where something
    breaks.
- **`__PARA_COUNT__` and `__DATE__`** may be used inside `metarow` and `footer`; they are
  substituted after those blocks are placed.
- Referencing a paragraph that doesn't exist is a hard error. Re-run `extract` — the
  manuscript has probably changed under you.

## Colours

Pick the accent first, then a continuity colour that is not adjacent to it on the wheel.
The other four tag colours never change.

| chapter | accent | continuity | why |
|---|---|---|---|
| tadpoles | `#8c2f2f` / `#e08a86` | `#9a6414` / `#e0b072` | default red accent, gold continuity |
| crash site | `#a8641a` / `#e0a95f` | `#8c2f2f` / `#e08a86` | orange accent collided with gold, so continuity took the red |

Give each chapter its own accent. It is how the author tells two open tabs apart.

## Cards

```html
<div class="card CLASS"><span class="tag t-CLASS">LABEL</span>
  <p class="hd">Claim, not a label</p>
  <p>Body.</p></div>
```

| class | label | for |
|---|---|---|
| `big` | structure | duplicated beats, splices, misplaced reveals, endings |
| `char` | character | who this person is, and whether the page agrees with the rest of the book |
| `cont` | continuity | facts contradicting another file — cite the filename |
| `prose` | prose | rhythm, register, image collisions |
| `nit` | nit | one-line word-level fixes, no `.hd`, no explanation |
| `good` | this works | see the rubric in `voice.md` §4 — earn it or omit it |

Inline helpers available inside cards and the letter: `<span class="quote">` for quoted
manuscript text, `<code>` for filenames.
