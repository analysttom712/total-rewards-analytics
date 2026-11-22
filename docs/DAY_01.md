# Day 1 checklist

## Part A: Thomas does these before the first session (about 30 min, phone or PC)
- [ ] **GitHub Education student verification** (github.com/education). While you're a verified student, the GH-900 GitHub Foundations exam fee is waived. Do it before you graduate in December.
- [ ] **Create the repo** at github.com/new: name `total-rewards-analytics`, **Public**, check "Add a README", no template.
- [ ] **Put the starter kit in the repo.** Pick one:
  - PC browser: unzip `total-rewards-starter-kit.zip`, then on the repo page choose **Add file → Upload files** and drag in everything *inside* the `total-rewards-analytics` folder, including the `.claude` folder. Commit to `main`. Replace the README when asked.
  - Or ask Claude (in the chat where the kit was made) to push it for you.
- [ ] **Connect GitHub to Claude.** Open the Claude app → **Code** tab (or claude.ai/code) and authorize the Claude GitHub App for `total-rewards-analytics`.
- [ ] **Block the time.** Put a recurring 2-hour "Total Rewards build" block on your calendar, at the same time daily if you can.

## Part B: First session (tutor-led, about 2 hours)
Start a cloud session on the repo and type `/standup`. The tutor sees an empty LEARNING_LOG and runs this Day 1 plan instead of a normal standup.

1. **Welcome + map (10 min):** the tutor walks the curriculum phases, how a session runs, the hint ladder, the incident drills (and when they start), and the cert path.
2. **Lesson: Git and GitHub basics (20 min):** repository, commit, branch, remote, pull request, issue. Each one is compared to something Thomas already knows (a commit is like a saved version with a note; a PR is like sending a reconciliation for review before posting).
3. **Ticket #1: "Project skeleton"** (the tutor creates it with `gh issue create`). Thomas does each step:
   - `git config user.name "Thomas Baynum"` and set his email (use GitHub's private no-reply address, since the repo is public)
   - `git switch -c 1-project-skeleton`
   - Create the folders: `generator/`, `models/staging/`, `models/intermediate/`, `models/marts/`, `seeds/`, `tests/`, `sql/practice/`, `api/`, `aws/`, `powerbi/`
   - Create `requirements.txt` (faker, pandas, pyarrow, duckdb, pytest, ruff) and install it
   - **First Python:** `generator/hello_employee.py` prints one fake Northwind Mutual employee (employee_id, name, hire date, job, salary) using Faker with a fixed seed. Thomas writes it with the hint ladder; it's his first Python script.
   - Run it twice to show the seed gives the same output.
4. **Ship (15 min):** commit → push → `gh pr create` ("Closes #1") → tutor reviews like a teammate → Thomas merges. His first PR.
5. **Log (10 min):** first LEARNING_LOG entry; first SKILLS_MATRIX update.
6. **Blog Day 1 (15 min):** `/blog`. Topic: *why I'm building a Total Rewards data platform in public* (career direction, the curriculum, what he'll post daily). No employer names, no internal details. The tutor also drafts a **LinkedIn launch post** for Thomas to edit and post himself.
7. **Queue tomorrow:** the tutor creates tickets #2–#4 (Python basics through the generator: lists/dicts, functions, a DataFrame of 25 employees).

## Part C: Thomas after the session (10 min)
- [ ] Edit and post the LinkedIn launch post, with a link to the repo.
- [ ] Add the repo to your portfolio and LinkedIn **Featured** section.
- [ ] Start Microsoft Learn's **GitHub Foundations** learning path (GH-900 prep), 15 minutes.
