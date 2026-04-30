(function () {
  if (document.getElementById("terminalBackdrop")) return;
  const body = document.body;
  const overlay = document.createElement("div");
  overlay.className = "terminal-backdrop";
  overlay.id = "terminalBackdrop";
  overlay.setAttribute("aria-hidden", "true");
  overlay.innerHTML = `
    <section class="terminal" role="dialog" aria-modal="true" aria-label="Project Creator terminal easter egg">
      <div class="terminal-head">
        <div>Project Creator Terminal</div>
        <button class="terminal-close" id="terminalClose" type="button" aria-label="Close terminal">Close</button>
      </div>
      <div class="terminal-body">
        <div class="terminal-log" id="terminalLog"></div>
        <label class="terminal-line" for="terminalInput">
          <span class="terminal-prompt">project-creator&gt;</span>
          <input class="terminal-input" id="terminalInput" type="text" autocomplete="off" spellcheck="false" aria-label="Terminal command">
        </label>
      </div>
    </section>
  `;
  body.appendChild(overlay);
  const terminalBackdrop = overlay;
  const terminalClose = document.getElementById("terminalClose");
  const terminalLog = document.getElementById("terminalLog");
  const terminalInput = document.getElementById("terminalInput");
  const path = window.location.pathname.replace(/\/+/g, "/");
  const baseRoot = path.replace(/\/(?:docs|contributing|documentation)\/?$/, "/");
  const siteRoot = baseRoot === "/" ? "/" : baseRoot.replace(/\/$/, "");
  const rootHref = siteRoot === "/" ? "/" : `${siteRoot}/`;
  const urls = {
    home: rootHref,
    docs: `${rootHref}docs/`,
    contributing: `${rootHref}contributing/`,
  };
  const commands = {
    help: ["Available commands:", "  ls", "  cd docs", "  cd contributing", "  cd home", "  pwd", "  clear", "  exit"],
    ls: ["docs/", "contributing/", "home/"],
    pwd: [rootHref],
    clear: [],
  };
  function addLine(text) { const line = document.createElement("div"); line.textContent = text; terminalLog.appendChild(line); terminalLog.scrollTop = terminalLog.scrollHeight; }
  function addBlock(lines) { lines.forEach(addLine); }
  function openTerminal() { terminalBackdrop.classList.add("open"); terminalBackdrop.setAttribute("aria-hidden", "false"); if (!terminalLog.dataset.booted) { terminalLog.innerHTML = ""; addBlock(["Project Creator shell", "Type `help` to see commands."]); terminalLog.dataset.booted = "true"; } terminalInput.value = ""; terminalInput.focus(); }
  function closeTerminal() { terminalBackdrop.classList.remove("open"); terminalBackdrop.setAttribute("aria-hidden", "true"); }
  function go(target) { if (window.location.pathname === target) { addLine("already here."); return; } window.location.href = target; }
  function runCommand(raw) {
    const input = raw.trim(); if (!input) return; addLine(`project-creator> ${input}`); const lower = input.toLowerCase();
    if (lower === "exit") { addLine("closing terminal..."); setTimeout(closeTerminal, 120); return; }
    if (lower === "clear") { terminalLog.innerHTML = ""; return; }
    if (lower === "pwd") { addBlock(commands.pwd); return; }
    if (lower === "ls") { addBlock(commands.ls); return; }
    if (lower === "help") { addBlock(commands.help); return; }
    const cdMatch = lower.match(/^cd\s+(.+)$/);
    if (cdMatch) {
      const target = cdMatch[1].replace(/^\.\//, "").replace(/^\/+/, "").replace(/\/+$/, "");
      if (target === "" || target === "." || target === "home" || target === "..") { addLine("already at home."); return; }
      if (target === "docs") { addLine("opening docs..."); setTimeout(() => go(urls.docs), 120); return; }
      if (target === "contributing") { addLine("opening contributing guide..."); setTimeout(() => go(urls.contributing), 120); return; }
      addLine(`no such directory: ${cdMatch[1]}`); return;
    }
    addLine(`command not found: ${input}`);
  }
  terminalInput.addEventListener("keydown", (event) => { if (event.key === "Enter") { event.preventDefault(); runCommand(terminalInput.value); terminalInput.value = ""; } });
  terminalClose.addEventListener("click", closeTerminal);
  terminalBackdrop.addEventListener("click", (event) => { if (event.target === terminalBackdrop) closeTerminal(); });
  document.addEventListener("keydown", (event) => {
    const target = event.target;
    const typing = target instanceof HTMLElement && ["INPUT", "TEXTAREA"].includes(target.tagName);
    if (typing) return;
    if (event.key.toLowerCase() === "p" && !event.metaKey && !event.ctrlKey && !event.altKey) { event.preventDefault(); openTerminal(); }
    if (event.key === "Escape" && terminalBackdrop.classList.contains("open")) closeTerminal();
  });
})();
