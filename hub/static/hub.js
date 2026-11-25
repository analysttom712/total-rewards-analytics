// Learning hub: sends answers and self-marks to the local server.
// Takes in: clicks and typing on a lesson page.
// Puts out: POST requests to /api/answer and /api/mark (same site only).

const MARK_SYMBOLS = { correct: "✓", partial: "½", missed: "✗" };

async function post(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok || !result.ok) {
    throw new Error(result.error || `The save failed (${response.status}).`);
  }
  return result.entry;
}

for (const check of document.querySelectorAll(".check")) {
  const form = check.querySelector(".answer-form");
  const textarea = form.querySelector("textarea");
  const status = form.querySelector(".status");
  const showButton = check.querySelector(".show-answer");
  const answerKey = check.querySelector(".answer-key");
  const markLine = check.querySelector(".mark-line");
  const markButtons = check.querySelectorAll(".mark");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.textContent = "Saving…";
    try {
      const entry = await post("/api/answer", {
        item_id: check.dataset.item,
        lesson: check.dataset.lesson,
        answer: textarea.value,
      });
      status.textContent = `Saved ${entry.answered_at}`;
      showButton.disabled = false;
      if (!entry.self_mark) {
        markLine.textContent = "";
        for (const button of markButtons) button.removeAttribute("aria-pressed");
      }
    } catch (error) {
      status.textContent = `Not saved: ${error.message}`;
    }
  });

  showButton.addEventListener("click", () => {
    answerKey.hidden = false;
    showButton.disabled = true;
  });

  for (const button of markButtons) {
    button.addEventListener("click", async () => {
      try {
        const entry = await post("/api/mark", {
          item_id: check.dataset.item,
          mark: button.dataset.mark,
        });
        for (const other of markButtons) other.removeAttribute("aria-pressed");
        button.setAttribute("aria-pressed", "true");
        markLine.textContent =
          `Your mark: ${MARK_SYMBOLS[entry.self_mark]} (provisional until /standup)`;
      } catch (error) {
        markLine.textContent = `Not saved: ${error.message}`;
      }
    });
  }
}

// --- drop-down sections: open the one a link points at; open/close all ------

function openTarget() {
  const id = decodeURIComponent(location.hash.slice(1));
  const target = id && document.getElementById(id);
  if (!target) return;
  for (let node = target; node; node = node.parentElement) {
    if (node.tagName === "DETAILS") node.open = true;
  }
  target.scrollIntoView();
}
window.addEventListener("hashchange", openTarget);
openTarget();

for (const button of document.querySelectorAll(".fold-all")) {
  button.addEventListener("click", () => {
    const open = button.dataset.open === "true";
    for (const fold of document.querySelectorAll("details.fold")) fold.open = open;
  });
}

// --- copying: a Copy button on every code block; click inline code to copy --

async function copyText(text, element, restore) {
  try {
    await navigator.clipboard.writeText(text);
    element.dataset.copied = "true";
    if (restore !== undefined) element.textContent = "Copied";
  } catch {
    if (restore !== undefined) element.textContent = "Copy failed";
  }
  setTimeout(() => {
    delete element.dataset.copied;
    if (restore !== undefined) element.textContent = restore;
  }, 1200);
}

for (const block of document.querySelectorAll("pre")) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "copy";
  button.textContent = "Copy";
  button.addEventListener("click", () => copyText(block.querySelector("code")?.textContent ?? block.textContent, button, "Copy"));
  block.prepend(button);
}

for (const code of document.querySelectorAll(".copyable code")) {
  if (code.closest("pre")) continue;
  code.classList.add("click-copy");
  code.title = "Click to copy";
  code.tabIndex = 0;
  code.setAttribute("role", "button");
  const copy = () => copyText(code.textContent, code);
  code.addEventListener("click", copy);
  code.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") { event.preventDefault(); copy(); }
  });
}

// --- task list: a tick saves at once; reload so the counts and bar update ---

for (const box of document.querySelectorAll("input.task")) {
  box.addEventListener("change", async () => {
    try {
      await post("/api/task", {
        lesson: box.dataset.lesson,
        task: box.dataset.task,
        done: box.checked,
      });
      location.reload();
    } catch (error) {
      box.checked = !box.checked;
      alert(`Not saved: ${error.message}`);
    }
  });
}

// --- light / dark switch: the button names the mode it will switch to -------

const themeButton = document.querySelector(".theme-toggle");
function showTheme() {
  const dark = document.documentElement.dataset.theme === "dark";
  themeButton.textContent = dark ? "☀ Light mode" : "☾ Dark mode";
  themeButton.setAttribute("aria-pressed", String(dark));
}
if (themeButton) {
  showTheme();
  themeButton.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("hub-theme", next);
    showTheme();
  });
}
