---
description: Quick quiz on recent concepts (spaced review + today's topic + one cert question)
---
Run a short quiz for Thomas as his lead analytics engineer. Teaching rules from CLAUDE.md section 5 apply.

Topic: $ARGUMENTS (if empty, pick from the sources below).

1. Read the last 3 entries of `docs/LEARNING_LOG.md`. Note every quiz item marked ✗ or ½ and every "Spaced review" item in the Next column. Skim `docs/CHEATSHEET.md` for the concepts covered so far.
2. Build **5 questions**:
   - 2 on today's (or the given) topic
   - 2 spaced-review questions on concepts from 1–7 days ago, favoring ones he missed
   - 1 tied to a cert exam objective on his path (name the exam and objective)
   Mix the formats: predict-the-output, read-this-error, fix-this-line, explain-it-in-Total-Rewards-terms. Use only this project's synthetic data and examples.
3. Ask **one question at a time**. Wait for his answer before showing the next one. Never put the answer in the question.
4. After each answer: mark ✓ / ½ / ✗, then give a 1–3 line explanation. For anything ½ or ✗, show the smallest example that makes it click, tied to Power Query, DAX, R or his payroll and benefits background.
5. At the end, give the score (n/5) and list the missed concepts in one line.
6. If `docs/LEARNING_LOG.md` already has an entry for today, add the result to its Quiz column (e.g. "/quiz 4/5, missed: range stop"). Otherwise, hold the result and add it at `/wrap`. Add missed concepts to the next entry's spaced-review list. Don't commit: `/wrap` ships the notes.

Keep it to about 10 minutes. No new concepts: a quiz checks what's been taught.
