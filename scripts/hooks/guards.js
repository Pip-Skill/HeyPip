#!/usr/bin/env node
/**
 * Tool guards from everything-claude-code, ported to the current hook format
 * (matcher = tool name; conditions are checked here on the hook's JSON input).
 *
 *   node guards.js pre   -> PreToolUse  (Bash, Edit, Write)
 *   node guards.js post  -> PostToolUse (Bash, Edit)
 *   node guards.js stop  -> Stop
 *
 * Messages go to stderr. Exit 0 = continue. Nothing here blocks a tool call; see
 * docs/ecc/hooks.original.json for the original rules and README "Hooks" for what changed.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const mode = process.argv[2];
let raw = '';
process.stdin.on('data', c => (raw += c));
process.stdin.on('end', () => {
  let i = {};
  try { i = JSON.parse(raw || '{}'); } catch { process.exit(0); }
  const tool = i.tool_name || '';
  const inp = i.tool_input || {};
  const say = m => console.error('[Hook] ' + m);
  const hasLocal = (bin, from) => {
    let dir = from;
    while (dir && dir !== path.dirname(dir)) {
      if (fs.existsSync(path.join(dir, 'node_modules', '.bin', bin))) return dir;
      dir = path.dirname(dir);
    }
    return null;
  };
  try {
    if (mode === 'pre' && tool === 'Bash') {
      const cmd = inp.command || '';
      if (/(npm run dev|pnpm( run)? dev|yarn dev|bun run dev)/.test(cmd) && !process.env.TMUX) {
        say('Dev server outside tmux: logs will be hard to reach. Prefer: tmux new-session -d -s dev "npm run dev"');
      } else if (/(npm (install|test)|pnpm (install|test)|yarn (install|test)|bun (install|test)|cargo build|\bmake\b|docker|pytest|vitest|playwright)/.test(cmd) && !process.env.TMUX) {
        say('Long-running command: consider tmux for session persistence (tmux new -s dev)');
      }
      if (/git push/.test(cmd)) say('Review changes before push.');
    }
    if (mode === 'post' && tool === 'Bash') {
      const cmd = inp.command || '';
      const out = (i.tool_response && (i.tool_response.stdout || i.tool_response.output)) || '';
      if (/gh pr create/.test(cmd)) {
        const m = String(out).match(/https:\/\/github.com\/([^/]+\/[^/]+)\/pull\/(\d+)/);
        if (m) say(`PR created: ${m[0]} — review: gh pr review ${m[2]} --repo ${m[1]}`);
      }
    }
    if (mode === 'post' && (tool === 'Edit' || tool === 'Write' || tool === 'MultiEdit')) {
      const p = inp.file_path;
      if (p && fs.existsSync(p) && /\.(ts|tsx|js|jsx)$/.test(p)) {
        const dir = path.dirname(p);
        const pr = hasLocal('prettier', dir);              // only a project-local prettier, never an npx download
        if (pr) { try { execSync(`"${path.join(pr, 'node_modules/.bin/prettier')}" --write "${p}"`, { stdio: 'pipe' }); } catch {} }
        if (/\.(ts|tsx)$/.test(p)) {
          const ts = hasLocal('tsc', dir);
          if (ts && fs.existsSync(path.join(ts, 'tsconfig.json'))) {
            try { execSync(`"${path.join(ts, 'node_modules/.bin/tsc')}" --noEmit --pretty false`, { cwd: ts, stdio: 'pipe', encoding: 'utf8' }); }
            catch (e) { const l = String(e.stdout || '').split('\n').filter(x => x.includes(path.basename(p))).slice(0, 10); if (l.length) console.error(l.join('\n')); }
          }
        }
        const lines = fs.readFileSync(p, 'utf8').split('\n');
        const hits = lines.map((l, n) => (/console\.log/.test(l) ? `${n + 1}: ${l.trim()}` : null)).filter(Boolean);
        if (hits.length) { say('console.log found in ' + p); hits.slice(0, 5).forEach(h => console.error(h)); }
      }
    }
    if (mode === 'stop') {
      try { execSync('git rev-parse --git-dir', { stdio: 'pipe' }); } catch { process.exit(0); }
      const files = execSync('git diff --name-only HEAD', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] })
        .split('\n').filter(f => /\.(ts|tsx|js|jsx)$/.test(f) && fs.existsSync(f));
      const bad = files.filter(f => fs.readFileSync(f, 'utf8').includes('console.log'));
      if (bad.length) say('console.log in modified files: ' + bad.join(', ') + ' — remove before committing');
    }
  } catch {}
  process.exit(0);
});
