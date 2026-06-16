/* global CodeMirror, CHALLENGE_ID */

let editor = null;

function initEditor(textareaId, startValue) {
  const el = document.getElementById(textareaId);
  if (!el) return;
  try {
    editor = CodeMirror.fromTextArea(el, {
      mode: 'text/x-sql',
      theme: 'dracula',
      lineNumbers: true,
      indentWithTabs: false,
      tabSize: 2,
      lineWrapping: true,
      autofocus: true,
      extraKeys: {
        'Ctrl-Enter': checkAnswer,
        'Cmd-Enter': checkAnswer,
        'Shift-Enter': runQuery,
      },
    });
    if (startValue) editor.setValue(startValue);
    editor.setSize(null, 'auto');
  } catch (e) {
    console.warn('CodeMirror failed, falling back to textarea', e);
  }
}

function getSQL() {
  if (editor) return editor.getValue().trim();
  const el = document.getElementById('sql-editor');
  return el ? el.value.trim() : '';
}

async function runQuery() {
  const sql = getSQL();
  if (!sql) return;
  showLoading();

  try {
    const res = await fetch('/api/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql }),
    });
    const data = await res.json();
    if (data.ok) {
      showResults(data.columns, data.rows, data.truncated, null);
    } else {
      showError(data.error);
    }
  } catch (e) {
    showError({ title: 'Network Error', message: e.message, tip: '', suggestions: [] });
  }
}

async function checkAnswer() {
  const sql = getSQL();
  if (!sql) return;
  showLoading();

  try {
    const res = await fetch(`/api/check/${CHALLENGE_ID}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql }),
    });
    const data = await res.json();

    if (data.status === 'correct') {
      showCorrect(data.columns, data.rows, data.row_count);
    } else if (data.status === 'incorrect') {
      showIncorrect(data);
    } else {
      showError(data.error);
    }
  } catch (e) {
    showError({ title: 'Network Error', message: e.message, tip: '', suggestions: [] });
  }
}

function showLoading() {
  const panel = document.getElementById('results-panel');
  const header = document.getElementById('results-header');
  panel.style.display = 'block';
  panel.className = 'results-panel';
  header.innerHTML = '<span style="color: var(--text-muted)">Running...</span>';
  document.getElementById('error-box').style.display = 'none';
  document.getElementById('results-table-wrap').innerHTML = '';
  document.getElementById('diff-panel').style.display = 'none';
}

function showError(err) {
  const panel = document.getElementById('results-panel');
  const header = document.getElementById('results-header');
  const errorBox = document.getElementById('error-box');

  panel.style.display = 'block';
  panel.className = 'results-panel incorrect';
  header.innerHTML = '<span style="color: var(--red)">❌ ' + escHtml(err.title || 'Error') + '</span>';
  errorBox.style.display = 'block';

  let html = `<h4>${escHtml(err.title || 'Error')}</h4>`;
  html += `<p>${escHtml(err.message || '')}</p>`;
  if (err.tip) html += `<p class="error-tip">💡 ${escHtml(err.tip)}</p>`;
  if (err.suggestions && err.suggestions.length) {
    html += '<ul class="suggestions">';
    err.suggestions.forEach(s => { html += `<li>${escHtml(s)}</li>`; });
    html += '</ul>';
  }
  errorBox.innerHTML = html;
  document.getElementById('results-table-wrap').innerHTML = '';
  document.getElementById('diff-panel').style.display = 'none';
}

function showResults(columns, rows, truncated, statusClass) {
  const panel = document.getElementById('results-panel');
  const header = document.getElementById('results-header');
  const wrap = document.getElementById('results-table-wrap');

  panel.style.display = 'block';
  panel.className = 'results-panel' + (statusClass ? ' ' + statusClass : '');
  document.getElementById('error-box').style.display = 'none';

  header.innerHTML = `<span>${rows.length} row${rows.length !== 1 ? 's' : ''} returned</span>`;
  if (truncated) {
    header.innerHTML += ' <span style="color:var(--yellow)">(result capped at 500 rows)</span>';
  }

  if (!columns || !columns.length) {
    wrap.innerHTML = '<p style="color:var(--text-muted)">No results.</p>';
    return;
  }

  let t = '<div class="table-scroll"><table class="results-table"><thead><tr>';
  columns.forEach(c => { t += `<th>${escHtml(c)}</th>`; });
  t += '</tr></thead><tbody>';
  rows.forEach(row => {
    t += '<tr>';
    row.forEach(cell => { t += `<td>${escHtml(cell == null ? 'NULL' : String(cell))}</td>`; });
    t += '</tr>';
  });
  t += '</tbody></table></div>';
  wrap.innerHTML = t;
}

function showCorrect(columns, rows, rowCount) {
  const header = document.getElementById('results-header');
  header.innerHTML = '<span class="correct-msg">✅ Correct! Great work.</span>';
  document.getElementById('results-panel').className = 'results-panel correct';
  document.getElementById('error-box').style.display = 'none';
  showResults(columns, rows, false, 'correct');
  document.getElementById('diff-panel').style.display = 'none';
}

function showIncorrect(data) {
  showError(data.error);
  if (data.columns && data.rows) {
    showResults(data.columns, data.rows, false, 'incorrect');
  }
  if (data.diff) {
    renderDiff(data.diff);
  }
}

function renderDiff(tokens) {
  const panel = document.getElementById('diff-panel');
  const userPre = document.getElementById('diff-user');
  const correctPre = document.getElementById('diff-correct');

  panel.style.display = 'block';

  let userHtml = '';
  let correctHtml = '';

  tokens.forEach(t => {
    const txt = escHtml(t.text);
    if (t.status === 'same') {
      userHtml += `<span class="diff-same">${txt}</span>`;
      correctHtml += `<span class="diff-same">${txt}</span>`;
    } else if (t.status === 'removed') {
      userHtml += `<span class="diff-removed">${txt}</span>`;
    } else if (t.status === 'added') {
      correctHtml += `<span class="diff-added">${txt}</span>`;
    }
  });

  userPre.innerHTML = userHtml;
  correctPre.innerHTML = correctHtml;
}

function toggleHint() {
  const el = document.getElementById('hints');
  if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

function toggleTable(name) {
  const el = document.getElementById('tbl-' + name);
  if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
