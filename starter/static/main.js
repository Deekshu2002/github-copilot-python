// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let currentDifficulty = 'easy';
let hintsUsed = 0;

window.sudokuGameState = {
  difficulty: currentDifficulty,
  hintsUsed,
};

const THEME_STORAGE_KEY = 'sudoku-theme';
const LIGHT_THEME = 'light';
const DARK_THEME = 'dark';

function getPreferredTheme() {
  const saved = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (saved === LIGHT_THEME || saved === DARK_THEME) {
    return saved;
  }
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    return DARK_THEME;
  }
  return LIGHT_THEME;
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    const isDarkTheme = theme === DARK_THEME;
    toggle.setAttribute('aria-pressed', String(isDarkTheme));
    toggle.setAttribute('aria-label', isDarkTheme ? 'Switch to light mode' : 'Switch to dark mode');
    toggle.querySelector('.theme-toggle__icon').textContent = isDarkTheme ? '☀️' : '🌙';
    toggle.querySelector('.theme-toggle__label').textContent = isDarkTheme ? 'Light mode' : 'Dark mode';
  }
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') === DARK_THEME ? DARK_THEME : LIGHT_THEME;
  const nextTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
  window.localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  applyTheme(nextTheme);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.setAttribute('aria-label', `Row ${i + 1}, Column ${j + 1}`);
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        const boardDiv = document.getElementById('sudoku-board');
        const inputs = boardDiv.getElementsByTagName('input');
        const board = window.sudokuValidation.getBoardState(inputs);
        window.sudokuValidation.applyConflictHighlighting(inputs, board);
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  window.sudokuGameState.difficulty = currentDifficulty;
  window.sudokuGameState.hintsUsed = hintsUsed;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className = 'sudoku-cell prefilled';
        inp.setAttribute('aria-readonly', 'true');
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.className = 'sudoku-cell';
        inp.setAttribute('aria-readonly', 'false');
      }
    }
  }
  window.sudokuValidation.resetBoardValidation(inputs);
  updateHintCount();
}

function updateHintCount() {
  const hintCount = document.getElementById('hint-count');
  if (hintCount) {
    hintCount.innerText = `Hints: ${hintsUsed}`;
  }
}

async function newGame() {
  const select = document.getElementById('difficulty-select');
  currentDifficulty = select ? select.value : currentDifficulty;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(currentDifficulty)}`);
  const data = await res.json();
  hintsUsed = data.hints_used ?? 0;
  window.sudokuGameState.difficulty = currentDifficulty;
  window.sudokuGameState.hintsUsed = hintsUsed;
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  window.sudokuTimer.resetTimer();
  window.sudokuTimer.startTimer();
  const difficultyDisplay = document.getElementById('difficulty-display');
  if (difficultyDisplay) {
    const label = currentDifficulty.charAt(0).toUpperCase() + currentDifficulty.slice(1);
    difficultyDisplay.innerText = `Current: ${label}`;
  }
}

async function applyHint() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }

  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  hintsUsed = data.hints_used ?? hintsUsed;
  window.sudokuGameState.hintsUsed = hintsUsed;
  updateHintCount();

  const boardInputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  for (let idx = 0; idx < boardInputs.length; idx++) {
    const inp = boardInputs[idx];
    inp.className = 'sudoku-cell';
    if (puzzle[Math.floor(idx / SIZE)][idx % SIZE] !== 0) {
      inp.className = 'sudoku-cell prefilled';
    }
  }

  if (data.position) {
    const [row, col] = data.position;
    const idx = row * SIZE + col;
    const inp = boardInputs[idx];
    inp.value = data.board[row][col];
    inp.className = 'sudoku-cell hint';
    inp.setAttribute('aria-readonly', 'false');
    inp.disabled = false;
    document.getElementById('message').innerText = 'Hint applied.';
  } else {
    document.getElementById('message').innerText = 'No hint available.';
  }
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-text)';
    msg.innerText = data.error;
    return;
  }

  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }

  if (data.status === 'incomplete') {
    msg.style.color = 'var(--message-warning)';
    msg.innerText = 'The puzzle is incomplete.';
  } else if (data.status === 'incorrect') {
    msg.style.color = 'var(--message-text)';
    msg.innerText = 'The puzzle contains incorrect values.';
  } else {
    msg.style.color = 'var(--message-success)';
    msg.innerText = 'Congratulations! You solved it!';
    window.sudokuTimer.completeGame();
  }
}

// Wire buttons
window.addEventListener('load', () => {
  const storedTheme = getPreferredTheme();
  applyTheme(storedTheme);

  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-solution').addEventListener('click', applyHint);
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('difficulty-select').addEventListener('change', (event) => {
    currentDifficulty = event.target.value;
    newGame();
  });
  window.sudokuTimer.renderScoreboard();
  // initialize
  newGame();
});