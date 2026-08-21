GitHub Copilot Instructions for Sudoku Application
Project Overview
This project is a modern 9x9 Sudoku web application built with Python Flask. The application is a refactored version of legacy Sudoku code and provides an interactive, responsive, and user-friendly Sudoku game.

The application should support different difficulty levels, puzzle validation, hints, a timer, score tracking, dark/light mode, and persistent Top 10 scores.

Code Standards and Architecture
Refactor Legacy Code to Modern Standards
Prefer clean, readable, modular Python code.
Use meaningful names for variables, functions, classes, and files.
Avoid unnecessary duplication.
Keep functions focused on one responsibility.
Replace obsolete or unnecessarily complicated code with simpler modern Python approaches.
Preserve existing functionality when refactoring unless a requirement specifically changes it.
Add comments only where they improve understanding.
Handle errors gracefully instead of allowing unexpected application crashes.
Flask Structure
Keep the application organized into logical components.

The Flask backend should be responsible for:

Creating and managing Sudoku puzzles.
Handling difficulty levels.
Validating Sudoku moves.
Checking whether a puzzle is solved.
Providing hints.
Managing game-related requests.
Frontend code should be responsible for:

Rendering the Sudoku board.
Handling user interactions.
Updating the timer.
Displaying validation feedback.
Managing dark/light mode.
Displaying the Top 10 scoreboard.
Keep HTML, CSS, JavaScript, and Python responsibilities separated whenever practical.

Sudoku Rules and Logic
The Sudoku board must always follow standard Sudoku rules:

The board contains 9 rows and 9 columns.
Each row must contain the numbers 1 through 9 without duplicates.
Each column must contain the numbers 1 through 9 without duplicates.
Each 3x3 sub-grid must contain the numbers 1 through 9 without duplicates.
Puzzle Generation
When generating a puzzle:

Generate a valid completed Sudoku solution first.
Remove cells according to the selected difficulty.
Ensure that the resulting puzzle has exactly one unique solution.
Do not provide a puzzle that has zero or multiple solutions.
Keep the solution separate from the player’s editable board where necessary.
Difficulty should control the number of prefilled cells:

Easy: more prefilled cells.
Medium: fewer prefilled cells.
Hard: the fewest prefilled cells.
Do not rely only on the number of empty cells to guarantee difficulty if that would compromise puzzle validity or uniqueness.

User Input Validation
User-entered values must be validated against Sudoku rules.

When a player enters an incorrect value:

Give immediate visual feedback.
Clearly identify the incorrect or conflicting cell.
Do not allow a user-entered value to overwrite a locked/pre-filled cell.
Keep the interface usable after an invalid entry.
When the puzzle is correctly completed, display a clear completion message.

Hint Feature
The Hint button should:

Find an empty cell.
Insert the correct value from the puzzle solution.
Mark the cell as filled by a hint.
Lock the hinted cell so the player cannot accidentally change it.
Not modify the original puzzle solution.
The hint operation should always insert a correct value.

Check Puzzle Feature
The Check Puzzle button should:

Compare user entries against the correct solution.
Highlight incorrect entries.
Leave correct entries unchanged.
Never modify locked cells.
Provide clear feedback to the player.
Timer
The timer should:

Start when a new puzzle begins.
Track the player’s solving time.
Stop when the puzzle is successfully completed.
Reset when a new puzzle is started.
Use a consistent time format.
The final completion time should be used for score calculation.

Top 10 Scoreboard
The application should maintain a Top 10 list containing:

Player name.
Completion time.
Difficulty level.
Scores should be sorted from fastest to slowest.

Only the 10 fastest scores should be retained.

Use browser localStorage so that scores remain available after:

Refreshing the page.
Closing and reopening the application.
Handle empty or invalid localStorage data safely.

Do not lose existing valid scores when adding a new score.

Dark and Light Mode
Provide a Dark/Light Mode toggle.

The selected mode should update the entire interface, including:

Background.
Text.
Sudoku cells.
Buttons.
Forms and controls.
Scoreboard.
Feedback messages.
Text must remain readable in both modes.

Avoid hard-coded styling that makes one mode difficult to use.

Responsive Design
The application should work on:

Desktop screens.
Laptop screens.
Tablet screens.
Mobile screens.
The Sudoku board should remain usable on smaller screens.

Controls should not overlap or become inaccessible.

The layout should scale smoothly between different screen sizes.

Sudoku Grid Styling
The 9x9 Sudoku board should visually distinguish the nine 3x3 sub-grids.

Use alternating or clearly different styling for the 3x3 blocks while maintaining good contrast.

The grid should remain readable in both light and dark modes.

Accessibility
Prefer accessible HTML and controls.

Use meaningful labels for form controls.
Ensure buttons have clear names.
Maintain sufficient text contrast.
Ensure keyboard users can interact with important controls.
Do not communicate important information through color alone.
Keep focus states visible.
Testing Requirements
Use a Python testing framework such as pytest.

Tests should verify important existing and new functionality.

At minimum, test:

Sudoku board validity.
Sudoku solution generation.
Unique solution validation.
Difficulty handling.
User input validation.
Puzzle completion.
Hint functionality where practical.
Flask routes where applicable.
Run the complete test suite after significant refactoring or feature changes.

Do not knowingly introduce changes that break existing tests.

Copilot Development Guidelines
When suggesting code:

Understand the existing project structure before modifying files.
Prefer modifying existing functionality over unnecessarily creating duplicate implementations.
Explain significant architectural changes when appropriate.
Keep changes focused on the requested feature.
Follow the coding standards described in this file.
Avoid introducing unnecessary external dependencies.
Do not remove working features during refactoring.
Consider existing tests before changing behavior.
When tests fail, identify the root cause and suggest a minimal fix.
Preserve Sudoku correctness and puzzle uniqueness when modifying puzzle-generation logic.
Error Handling
The application should handle invalid user input and unexpected conditions gracefully.

Avoid exposing unnecessary internal errors to users.

Use appropriate validation and defensive programming for:

User input.
LocalStorage data.
Puzzle state.
Difficulty values.
Flask requests.
Dependencies
Prefer the existing project dependencies.

Do not add a new library unless it provides a clear benefit and is compatible with the project requirements.

If a dependency is necessary, update the appropriate dependency file and document how to install it.

General Development Principle
The main priority is a reliable, maintainable, and user-friendly Sudoku application.

Any changes suggested by Copilot should:

Preserve existing functionality.
Follow the project’s architecture.
Keep the Sudoku logic correct.
Maintain unique puzzle solutions.
Keep the application responsive and accessible.
Avoid unnecessary complexity.
Pass the project’s test suite.
