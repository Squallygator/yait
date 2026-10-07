// Mockup behaviour: theme toggle and column sort. Nothing else.
// No business logic here: mockup data is hard-coded in the HTML.

const THEME_KEY = "yait-theme";

function storedTheme() {
  try {
    return localStorage.getItem(THEME_KEY);
  } catch {
    return null; // storage blocked: fall back to the OS preference
  }
}

function applyTheme(theme) {
  if (theme === "light" || theme === "dark") {
    document.documentElement.dataset.theme = theme;
  } else {
    delete document.documentElement.dataset.theme;
  }
}

function currentTheme() {
  const explicit = document.documentElement.dataset.theme;
  if (explicit) return explicit;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function initTheme() {
  applyTheme(storedTheme());
  for (const button of document.querySelectorAll("[data-theme-toggle]")) {
    button.addEventListener("click", () => {
      const next = currentTheme() === "dark" ? "light" : "dark";
      applyTheme(next);
      try {
        localStorage.setItem(THEME_KEY, next);
      } catch {
        // not persisted; the toggle still works for this page
      }
    });
  }
}

function cellValue(row, index) {
  const cell = row.cells[index];
  return cell ? (cell.dataset.value ?? cell.textContent).trim() : "";
}

function sortTable(table, index, direction) {
  const body = table.tBodies[0];
  const rows = Array.from(body.rows);
  const factor = direction === "ascending" ? 1 : -1;
  rows.sort((a, b) =>
    factor * cellValue(a, index).localeCompare(cellValue(b, index), undefined, { numeric: true }),
  );
  body.append(...rows);
}

function initSort() {
  for (const table of document.querySelectorAll("table.grid")) {
    const headers = Array.from(table.tHead.rows[0].cells);
    headers.forEach((th, index) => {
      if (!th.hasAttribute("data-sort")) return;
      th.tabIndex = 0;
      const toggle = () => {
        const next = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        for (const other of headers) other.removeAttribute("aria-sort");
        th.setAttribute("aria-sort", next);
        sortTable(table, index, next);
      };
      th.addEventListener("click", toggle);
      th.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          toggle();
        }
      });
    });
  }
}

initTheme();
initSort();
