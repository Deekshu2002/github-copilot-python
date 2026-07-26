const TIMER_STORAGE_KEY = 'sudoku-scoreboard';

let timerIntervalId = null;
let elapsedSeconds = 0;

function formatTime(totalSeconds) {
  const safeSeconds = Number.isFinite(totalSeconds) ? Math.max(0, Math.floor(totalSeconds)) : 0;
  const minutes = Math.floor(safeSeconds / 60);
  const seconds = safeSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function createScoreboardEntry({ playerName, time, difficulty, hintsUsed, elapsedSeconds }) {
  const safeElapsedSeconds = Number.isInteger(elapsedSeconds) ? elapsedSeconds : 0;
  const safeHintsUsed = Number.isInteger(hintsUsed) ? hintsUsed : 0;
  return {
    playerName: String(playerName || 'Anonymous').trim() || 'Anonymous',
    time: String(time || formatTime(safeElapsedSeconds)),
    difficulty: String(difficulty || 'easy').trim() || 'easy',
    hintsUsed: safeHintsUsed,
    elapsedSeconds: Math.max(0, safeElapsedSeconds),
  };
}

function sortScoreboardEntries(entries) {
  return [...entries].sort((left, right) => {
    if (left.elapsedSeconds !== right.elapsedSeconds) {
      return left.elapsedSeconds - right.elapsedSeconds;
    }
    return left.time.localeCompare(right.time);
  });
}

function normalizeScoreboardEntries(rawEntries) {
  if (!Array.isArray(rawEntries)) {
    return [];
  }

  const normalized = rawEntries
    .filter(Boolean)
    .map((entry) => {
      if (!entry || typeof entry !== 'object') {
        return null;
      }
      const hasRequiredFields = typeof entry.elapsedSeconds === 'number' && Number.isFinite(entry.elapsedSeconds);
      if (!hasRequiredFields) {
        return null;
      }
      return createScoreboardEntry(entry);
    })
    .filter(Boolean);

  return sortScoreboardEntries(normalized).slice(0, 10);
}

function getStorage() {
  if (typeof window !== 'undefined' && window.localStorage) {
    return window.localStorage;
  }
  return null;
}

function getScoreboardEntries(storage = getStorage()) {
  if (!storage) {
    return [];
  }

  const storedValue = storage.getItem(TIMER_STORAGE_KEY);
  if (!storedValue) {
    return [];
  }

  try {
    return normalizeScoreboardEntries(JSON.parse(storedValue));
  } catch (error) {
    return [];
  }
}

function saveScoreboardEntries(entries, storage = getStorage()) {
  const normalizedEntries = normalizeScoreboardEntries(entries);
  if (!storage) {
    return normalizedEntries;
  }
  storage.setItem(TIMER_STORAGE_KEY, JSON.stringify(normalizedEntries));
  return normalizedEntries;
}

function saveScoreboardEntry(entry, storage = getStorage()) {
  const nextEntries = [...getScoreboardEntries(storage), createScoreboardEntry(entry)];
  return saveScoreboardEntries(nextEntries, storage);
}

function updateTimerDisplay() {
  const timerDisplay = document.getElementById('timer-display');
  if (timerDisplay) {
    timerDisplay.textContent = `Time: ${formatTime(elapsedSeconds)}`;
  }
}

function resetTimer() {
  if (timerIntervalId !== null) {
    window.clearInterval(timerIntervalId);
    timerIntervalId = null;
  }
  elapsedSeconds = 0;
  updateTimerDisplay();
}

function startTimer() {
  if (timerIntervalId !== null) {
    return;
  }
  timerIntervalId = window.setInterval(() => {
    elapsedSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerIntervalId !== null) {
    window.clearInterval(timerIntervalId);
    timerIntervalId = null;
  }
}

function getElapsedSeconds() {
  return elapsedSeconds;
}

function getFormattedTime() {
  return formatTime(elapsedSeconds);
}

function renderScoreboard(storage = getStorage()) {
  const scoreboardTable = document.getElementById('scoreboard-table');
  const scoreboardBody = document.getElementById('scoreboard-body');
  if (!scoreboardTable || !scoreboardBody) {
    return [];
  }

  const entries = getScoreboardEntries(storage);
  scoreboardBody.innerHTML = '';
  if (entries.length === 0) {
    const emptyRow = document.createElement('tr');
    emptyRow.innerHTML = '<td colspan="5">No completed games yet.</td>';
    scoreboardBody.appendChild(emptyRow);
    return entries;
  }

  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${escapeHtml(entry.playerName)}</td>
      <td>${escapeHtml(entry.time)}</td>
      <td>${escapeHtml(entry.difficulty)}</td>
      <td>${entry.hintsUsed}</td>
    `;
    scoreboardBody.appendChild(row);
  });
  return entries;
}

function completeGame() {
  stopTimer();
  const playerName = window.prompt('Enter your name for the scoreboard:')?.trim() || 'Anonymous';
  const entry = createScoreboardEntry({
    playerName,
    time: getFormattedTime(),
    difficulty: window.sudokuGameState?.difficulty || 'easy',
    hintsUsed: window.sudokuGameState?.hintsUsed || 0,
    elapsedSeconds: getElapsedSeconds(),
  });
  saveScoreboardEntry(entry);
  renderScoreboard();
  return entry;
}

const exportedHelpers = {
  TIMER_STORAGE_KEY,
  formatTime,
  escapeHtml,
  createScoreboardEntry,
  sortScoreboardEntries,
  normalizeScoreboardEntries,
  getScoreboardEntries,
  saveScoreboardEntries,
  saveScoreboardEntry,
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = exportedHelpers;
}

if (typeof window !== 'undefined') {
  window.sudokuTimer = {
    ...exportedHelpers,
    resetTimer,
    startTimer,
    stopTimer,
    getElapsedSeconds,
    getFormattedTime,
    completeGame,
    renderScoreboard,
  };
}
