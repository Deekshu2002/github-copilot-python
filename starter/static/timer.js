const TIMER_STORAGE_KEY = 'sudoku-scoreboard';

let timerIntervalId = null;
let elapsedSeconds = 0;

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
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

function getScoreboardEntries() {
  const stored = window.localStorage.getItem(TIMER_STORAGE_KEY);
  if (!stored) {
    return [];
  }
  try {
    return JSON.parse(stored);
  } catch (error) {
    return [];
  }
}

function saveScoreboardEntry(entry) {
  const entries = getScoreboardEntries();
  entries.push(entry);
  entries.sort((a, b) => a.elapsedSeconds - b.elapsedSeconds);
  if (entries.length > 10) {
    entries.length = 10;
  }
  window.localStorage.setItem(TIMER_STORAGE_KEY, JSON.stringify(entries));
}

function renderScoreboard() {
  const scoreboardList = document.getElementById('scoreboard-list');
  if (!scoreboardList) {
    return;
  }
  const entries = getScoreboardEntries();
  scoreboardList.innerHTML = '';
  if (entries.length === 0) {
    const emptyItem = document.createElement('li');
    emptyItem.textContent = 'No completed games yet.';
    scoreboardList.appendChild(emptyItem);
    return;
  }

  entries.forEach((entry) => {
    const item = document.createElement('li');
    item.textContent = `${entry.playerName} — ${entry.time} — ${entry.difficulty} — hints: ${entry.hintsUsed}`;
    scoreboardList.appendChild(item);
  });
}

function completeGame() {
  stopTimer();
  const playerName = window.prompt('Enter your name for the scoreboard:')?.trim() || 'Anonymous';
  const entry = {
    playerName,
    time: getFormattedTime(),
    difficulty: window.sudokuGameState?.difficulty || 'easy',
    hintsUsed: window.sudokuGameState?.hintsUsed || 0,
    elapsedSeconds: getElapsedSeconds(),
  };
  saveScoreboardEntry(entry);
  renderScoreboard();
  return entry;
}

if (typeof window !== 'undefined') {
  window.sudokuTimer = {
    resetTimer,
    startTimer,
    stopTimer,
    getElapsedSeconds,
    getFormattedTime,
    completeGame,
    renderScoreboard,
  };
}
