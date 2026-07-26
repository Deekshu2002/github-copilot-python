const assert = require('assert');
const timer = require('../static/timer.js');

function run() {
  const sanitized = timer.createScoreboardEntry({
    playerName: '  <script>alert(1)</script>  ',
    time: '00:42',
    difficulty: 'Hard',
    hintsUsed: 1,
    elapsedSeconds: 42,
  });

  assert.strictEqual(sanitized.playerName, '<script>alert(1)</script>');
  assert.strictEqual(sanitized.time, '00:42');
  assert.strictEqual(sanitized.difficulty, 'Hard');
  assert.strictEqual(sanitized.elapsedSeconds, 42);

  const entries = timer.normalizeScoreboardEntries([
    { playerName: 'Alice', time: '00:30', difficulty: 'easy', hintsUsed: 0, elapsedSeconds: 30 },
    { playerName: 'Bob', time: '00:20', difficulty: 'hard', hintsUsed: 2, elapsedSeconds: 20 },
    { playerName: 'Carl', time: '00:25', difficulty: 'medium', hintsUsed: 1, elapsedSeconds: 25 },
    null,
  ]);

  assert.deepStrictEqual(entries.map((entry) => entry.playerName), ['Bob', 'Carl', 'Alice']);
  assert.strictEqual(entries[0].elapsedSeconds, 20);
}

run();
console.log('timer helper tests passed');
