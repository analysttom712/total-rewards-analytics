---
description: Quick quiz on recent concepts (spaced review + today's topic + one cert question)
---
Run a short quiz for Thomas as his lead analytics engineer. Teaching rules from CLAUDE.md section 5 and `docs/COACHING.md` apply.

Topic: $ARGUMENTS (if empty, pick from the sources below).

1. Read `docs/REVIEW_QUEUE.md` (due and overdue items), the last 3 entries of `docs/LEARNING_LOG.md`, and `docs/COACHING.md`. Skim `docs/CHEATSHEET.md` and `docs/GLOSSARY.md` for what's been taught.
2. Build **5 questions**:
   - 2 on today's (or the given) topic
   - 2 from the review queue's due items, oldest and most-missed first
   - 1 tied to a cert exam objective on his path (name the exam and objective)
   Mix the formats: predict-the-output, read-this-error, fix-this-line, name-this-symbol, explain-it-in-Total-Rewards-terms. Use only this project's synthetic data and examples.
3. Ask **one question at a time**. Wait for his answer before showing the next one. Never put the answer in the question. If he asks for something else mid-quiz, do it, then resume at the same question.
4. After each answer: mark ✓ / ½ / ✗ (½ if any part of a multi-part question is missing), then give a 1–3 line explanation. For anything ½ or ✗, show the smallest example that makes it click, tied to Power Query, DAX, R or his payroll and benefits background.
5. At the end, give the score (n/5) as a table and list the missed concepts in one line.
6. Update `docs/REVIEW_QUEUE.md`: move every quizzed concept between boxes per the rules in that file; add new concepts from today's topic at box 1. If `docs/LEARNING_LOG.md` has an entry for today, add the result to its Quiz column (e.g. "/quiz 4/5, missed: range stop"); otherwise hold it for `/wrap`. Don't commit: `/wrap` ships the notes.

Keep it short. No new concepts: a quiz checks what's been taught.
