// Mapping from logical chapters to markdown files in ../llm
const chapters = [
  { id: 'foundation',        title: '1. Foundation',        file: '../llm/1.foundation.md' },
  { id: 'pretraining',         title: '2. Pretraining',         file: '../llm/2.pretraining.md' },
  { id: 'post_training',       title: '3. Post-training',       file: '../llm/3.post_training.md' },
  { id: 'common_models',       title: '4. Common Models',       file: '../llm/4.common_models.md' },
  { id: 'applications',        title: '5. Applications',        file: '../llm/5.applications.md' },
  { id: 'training_inference',  title: '6. Training & Inference',file: '../llm/6.training_inference.md' },
  { id: 'compression',         title: '7. Compression',         file: '../llm/7.compression.md' },
  { id: 'multimodal',          title: '8. Multimodal',          file: '../llm/8.multimodal.md' },
];


function buildToc() {
  const toc = document.getElementById('toc');
  chapters.forEach((ch) => {
    const a = document.createElement('a');
    a.href = `#${ch.id}`;
    a.textContent = ch.title;
    a.className = 'toc-link';
    a.addEventListener('click', (e) => {
      e.preventDefault();
      loadChapter(ch.id);
    });
    toc.appendChild(a);
  });
}

async function loadChapter(id) {
  const chapter = chapters.find((c) => c.id === id);
  if (!chapter) return;

  const contentEl = document.getElementById('content');
  contentEl.innerHTML = '<p style="color:#6b665a;">Loading…</p>';

  try {
    const res = await fetch(chapter.file);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const md = await res.text();

    // Basic markdown -> HTML, with heading ids for in-page navigation
    marked.setOptions({
      breaks: true,
      headerIds: true,
      mangle: false,
    });

    const html = marked.parse(md);

    // Wrap as a "document" (no per-page meta; meta is in sidebar)
    const doc = document.createElement('div');
    doc.className = 'doc-wrapper';
    const inner = document.createElement('div');
    inner.className = 'doc-inner';
    const contentContainer = document.createElement('div');
    contentContainer.innerHTML = html;

    // Meta header with chapter title only (intent removed)
    const metaHeader = document.createElement('div');
    metaHeader.className = 'doc-meta-header';
    const chapterTitleEl = document.createElement('h1');
    chapterTitleEl.className = 'doc-chapter-title';
    chapterTitleEl.textContent = chapter.title.replace(/^\d+\.\s*/, ''); // strip leading number for cleaner heading
    metaHeader.appendChild(chapterTitleEl);

    // Build a simple in-page TOC from headings
    const toc = buildDocToc(contentContainer);
    if (toc) {
      inner.appendChild(metaHeader);
      inner.appendChild(toc);
    } else {
      inner.appendChild(metaHeader);
    }
    inner.appendChild(contentContainer);
    doc.appendChild(inner);

    contentEl.innerHTML = '';
    contentEl.appendChild(doc);

    // Simple inline/blocked LaTeX detection: $...$ and $$...$$
    renderMathInElement(contentEl);

    updateActiveLink(id);
    window.history.replaceState({}, '', `#${id}`);
  } catch (err) {
    contentEl.innerHTML = `<p style="color:#b00020;">Failed to load chapter: ${err.message}</p>`;
  }
}

// Very small KaTeX auto-render wrapper
function renderMathInElement(root) {
  const textNodes = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
  while (walker.nextNode()) {
    textNodes.push(walker.currentNode);
  }

  textNodes.forEach((node) => {
    const text = node.textContent;
    if (!text || (!text.includes('$') && !text.includes('\\('))) return;

    const span = document.createElement('span');
    let html = text
      // Display $$...$$
      .replace(/\$\$([^$]+)\$\$/g, (_, expr) =>
        `<span class="katex-display">${katex.renderToString(expr, { throwOnError: false })}</span>`
      )
      // Inline $...$
      .replace(/\$([^$]+)\$/g, (_, expr) =>
        katex.renderToString(expr, { throwOnError: false })
      );

    // Skip if nothing changed
    if (html === text) return;

    span.innerHTML = html;
    node.parentNode.replaceChild(span, node);
  });
}

// Build a small in-page TOC from h1–h3 headings
function buildDocToc(root) {
  // h1 + h2 only for cleaner outline
  const headings = root.querySelectorAll('h1, h2');
  if (!headings.length) return null;

  const toc = document.createElement('nav');
  toc.className = 'doc-toc';

  const title = document.createElement('div');
  title.className = 'doc-toc-title';
  title.textContent = 'Contents';
  toc.appendChild(title);

  const list = document.createElement('ul');
  headings.forEach((h) => {
    const id = h.id || h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-');
    if (!h.id) h.id = id;
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = `#${id}`;
    a.textContent = h.textContent.trim();
    if (h.tagName.toLowerCase() === 'h2') {
      li.classList.add('doc-toc-level-2');
    }
    li.appendChild(a);
    list.appendChild(li);
  });

  toc.appendChild(list);
  return toc;
}

function updateActiveLink(id) {
  document.querySelectorAll('.toc-link').forEach((el) => {
    if (el.getAttribute('href') === `#${id}`) {
      el.classList.add('active');
    } else {
      el.classList.remove('active');
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  buildToc();
  const hash = window.location.hash.replace('#', '');
  if (hash && chapters.some((c) => c.id === hash)) {
    loadChapter(hash);
  } else {
    loadChapter('foundation');
  }
});
