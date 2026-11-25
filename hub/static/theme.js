// Runs in <head>, before the page is drawn, so a saved dark choice never
// flashes light first. Light is the default; the choice lives in this browser.
const savedTheme = localStorage.getItem("hub-theme");
document.documentElement.dataset.theme = savedTheme === "dark" ? "dark" : "light";
