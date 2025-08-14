// Einfaches AIO Tool mit Logging

function debugLog(msg) {
  const out = document.getElementById('log-output');
  const time = new Date().toLocaleTimeString();
  const line = `[${time}] ${msg}\n`;
  out.textContent += line;
  out.scrollTop = out.scrollHeight;
  console.log(line);
}

function updateDashboard(todoCount, noteCount) {
  document.getElementById('todo-count').textContent = todoCount;
  document.getElementById('note-count').textContent = noteCount;
}

function initNotes() {
  const textarea = document.getElementById('notes');
  const saveBtn = document.getElementById('save-note');
  const stored = localStorage.getItem('notes') || '';
  textarea.value = stored;
  document.getElementById('note-count').textContent = stored.trim() ? 1 : 0;

  saveBtn.addEventListener('click', () => {
    localStorage.setItem('notes', textarea.value);
    const count = textarea.value.trim() ? 1 : 0;
    updateDashboard(getTodos().length, count);
    debugLog('Notizen gespeichert');
  });
}

function getTodos() {
  return JSON.parse(localStorage.getItem('todos') || '[]');
}

function getArchive() {
  return JSON.parse(localStorage.getItem('archive') || '[]');
}

function saveTodos(todos, archive) {
  localStorage.setItem('todos', JSON.stringify(todos));
  localStorage.setItem('archive', JSON.stringify(archive));
  updateDashboard(todos.length, document.getElementById('note-count').textContent);
}

function renderTodos() {
  const list = document.getElementById('todo-list');
  const archiveList = document.getElementById('todo-archive');
  list.innerHTML = '';
  archiveList.innerHTML = '';
  const todos = getTodos();
  const archive = getArchive();

  todos.forEach((t, idx) => {
    const li = document.createElement('li');
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.id = `todo-${idx}`;
    cb.addEventListener('change', () => {
      archive.push(t);
      todos.splice(idx, 1);
      saveTodos(todos, archive);
      renderTodos();
      debugLog(`Aufgabe archiviert: ${t.text}`);
    });
    const label = document.createElement('label');
    label.htmlFor = cb.id;
    label.textContent = `${t.text} (${t.date || 'kein Datum'})`;
    li.appendChild(cb);
    li.appendChild(label);
    list.appendChild(li);
  });

  archive.forEach(t => {
    const li = document.createElement('li');
    li.textContent = `${t.text} (${t.date || 'kein Datum'})`;
    archiveList.appendChild(li);
  });

  updateDashboard(todos.length, document.getElementById('note-count').textContent);
}

function initTodos() {
  renderTodos();
  const form = document.getElementById('todo-form');
  form.addEventListener('submit', e => {
    e.preventDefault();
    const text = document.getElementById('todo-text').value.trim();
    const date = document.getElementById('todo-date').value;
    if (!text) return;
    const todos = getTodos();
    todos.push({ text, date });
    saveTodos(todos, getArchive());
    renderTodos();
    form.reset();
    debugLog(`Aufgabe hinzugefügt: ${text}`);
  });
}

function initCalendar() {
  const calDiv = document.getElementById('calendar');
  const now = new Date();
  const year = now.getFullYear();
  const month = now.getMonth();
  const first = new Date(year, month, 1);
  const last = new Date(year, month + 1, 0);
  const table = document.createElement('table');
  const headerRow = document.createElement('tr');
  const days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];
  days.forEach(d => {
    const th = document.createElement('th');
    th.textContent = d;
    headerRow.appendChild(th);
  });
  table.appendChild(headerRow);
  let row = document.createElement('tr');
  for (let i = 1; i < (first.getDay() || 7); i++) {
    row.appendChild(document.createElement('td'));
  }
  for (let d = 1; d <= last.getDate(); d++) {
    const cell = document.createElement('td');
    cell.textContent = d;
    row.appendChild(cell);
    if ((first.getDay() + d - 1) % 7 === 0) {
      table.appendChild(row);
      row = document.createElement('tr');
    }
  }
  if (row.children.length) table.appendChild(row);
  calDiv.appendChild(table);
  debugLog('Kalender geladen');
}

function initHeader() {
  document.getElementById('today').textContent = new Date().toLocaleDateString();
}

document.addEventListener('DOMContentLoaded', () => {
  initHeader();
  initNotes();
  initTodos();
  initCalendar();
  debugLog('System gestartet');
});
