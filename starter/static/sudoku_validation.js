const BOARD_SIZE = window.SUDOKU_SIZE ?? 9;

function getCellIndex(row, col) {
  return row * BOARD_SIZE + col;
}

function getBoardState(inputs) {
  const board = [];
  for (let row = 0; row < BOARD_SIZE; row += 1) {
    board[row] = [];
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      const idx = getCellIndex(row, col);
      const value = inputs[idx].value;
      board[row][col] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function clearConflictState(inputs) {
  for (let idx = 0; idx < inputs.length; idx += 1) {
    const input = inputs[idx];
    input.classList.remove('conflict');
    input.classList.remove('conflict-source');
    input.setAttribute('aria-invalid', 'false');
    input.setAttribute('aria-describedby', '');
  }
}

function applyConflictHighlighting(inputs, board) {
  clearConflictState(inputs);

  const conflicts = new Set();
  const sources = new Set();

  for (let row = 0; row < BOARD_SIZE; row += 1) {
    for (let col = 0; col < BOARD_SIZE; col += 1) {
      const value = board[row][col];
      if (value === 0) {
        continue;
      }

      const currentIndex = getCellIndex(row, col);
      const currentInput = inputs[currentIndex];
      if (currentInput.disabled) {
        continue;
      }

      const seen = [];
      for (let otherCol = 0; otherCol < BOARD_SIZE; otherCol += 1) {
        if (otherCol === col) {
          continue;
        }
        if (board[row][otherCol] === value) {
          seen.push(getCellIndex(row, otherCol));
        }
      }
      for (let otherRow = 0; otherRow < BOARD_SIZE; otherRow += 1) {
        if (otherRow === row) {
          continue;
        }
        if (board[otherRow][col] === value) {
          seen.push(getCellIndex(otherRow, col));
        }
      }

      const startRow = Math.floor(row / 3) * 3;
      const startCol = Math.floor(col / 3) * 3;
      for (let boxRow = startRow; boxRow < startRow + 3; boxRow += 1) {
        for (let boxCol = startCol; boxCol < startCol + 3; boxCol += 1) {
          if (boxRow === row && boxCol === col) {
            continue;
          }
          if (board[boxRow][boxCol] === value) {
            seen.push(getCellIndex(boxRow, boxCol));
          }
        }
      }

      if (seen.length > 0) {
        conflicts.add(currentIndex);
        sources.add(currentIndex);
        for (const conflictIndex of seen) {
          conflicts.add(conflictIndex);
        }
      }
    }
  }

  for (const idx of conflicts) {
    const input = inputs[idx];
    if (!input) {
      continue;
    }
    const isSource = sources.has(idx);
    input.classList.add('conflict');
    if (isSource) {
      input.classList.add('conflict-source');
    }
    input.setAttribute('aria-invalid', 'true');
    input.setAttribute('aria-describedby', 'cell-feedback');
  }
}

function resetBoardValidation(inputs) {
  clearConflictState(inputs);
}

if (typeof window !== 'undefined') {
  window.sudokuValidation = {
    getBoardState,
    applyConflictHighlighting,
    resetBoardValidation,
  };
}
