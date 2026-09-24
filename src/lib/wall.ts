// Shared by the server render and the client re-render of /wall. Pure functions only.

export type Outcome = 'worked' | 'stuck' | 'mixed';

export interface WallItem {
  id: string;
  platform: 'x' | 'reddit';
  url: string;
  postId: string | null;
  author: string;
  community: string;
  created: string;
  engagement: number;
  sites: string[];
  agents: string[];
  outcome: Outcome;
  siteOutcomes: Record<string, Outcome>;
  antiPatterns: string[];
  patterns: string[];
  quote: string;
  unavailable?: boolean; // the source post was deleted; show the quote only
}

export interface WallState {
  days: number; // 0 = all time
  agent: string;
  pattern: string; // "anti:Bot block" | "good:MCP server" | ""
}

export const DEFAULT_STATE: WallState = { days: 30, agent: '', pattern: '' };

const esc = (s: string) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

const MARK: Record<Outcome, string> = { worked: '✓', stuck: '✕', mixed: '–' };
const ORDER: Record<Outcome, number> = { worked: 0, mixed: 1, stuck: 2 };

export function cutoff(days: number, today: string): string {
  if (!days) return '';
  const d = new Date(today + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - days);
  return d.toISOString().slice(0, 10);
}

export function filterItems(items: WallItem[], state: WallState, today: string): WallItem[] {
  const from = cutoff(state.days, today);
  const [kind, tag] = state.pattern ? [state.pattern.slice(0, 4), state.pattern.slice(5)] : ['', ''];
  return items.filter(
    (i) =>
      (!from || i.created >= from) &&
      (!state.agent || i.agents.includes(state.agent)) &&
      (!tag || (kind === 'anti' ? i.antiPatterns : i.patterns).includes(tag)),
  );
}

function counted(values: string[]): [string, number][] {
  const c = new Map<string, number>();
  for (const v of values) c.set(v, (c.get(v) ?? 0) + 1);
  return [...c.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

// Options for the two selects, counted inside the current window and the other select's choice.
export function options(items: WallItem[], state: WallState, today: string) {
  const forAgents = filterItems(items, { ...state, agent: '' }, today);
  const forPatterns = filterItems(items, { ...state, pattern: '' }, today);
  return {
    agents: counted(forAgents.flatMap((i) => i.agents)),
    anti: counted(forPatterns.flatMap((i) => i.antiPatterns)),
    good: counted(forPatterns.flatMap((i) => i.patterns)),
  };
}

const opt = (value: string, label: string, n: number, selected: string) =>
  `<option value="${esc(value)}"${value === selected ? ' selected' : ''}>${esc(label)} (${n})</option>`;

export function renderAgentOptions(o: ReturnType<typeof options>, state: WallState): string {
  return `<option value="">Any assistant</option>` + o.agents.map(([n, c]) => opt(n, n, c, state.agent)).join('');
}

export function renderPatternOptions(o: ReturnType<typeof options>, state: WallState): string {
  return `<option value="">Any pattern</option>` +
    `<optgroup label="Stuck on">${o.anti.map(([n, c]) => opt('anti:' + n, n, c, state.pattern)).join('')}</optgroup>` +
    `<optgroup label="Worked with">${o.good.map(([n, c]) => opt('good:' + n, n, c, state.pattern)).join('')}</optgroup>`;
}

// Posts in the window that show one pattern label. Used by the pattern pages.
export function countPattern(items: WallItem[], kind: 'anti' | 'good', tag: string, today: string): number {
  return filterItems(items, { ...DEFAULT_STATE, pattern: `${kind}:${tag}` }, today).length;
}

export interface SiteRow {
  site: string;
  posts: WallItem[]; // newest first
  outcomes: Outcome[]; // one per post, sorted worked, mixed, stuck
  worked: number;
  stuck: number;
}

// Sites with one post are noise in the full view. In a filtered view the user asked for them.
export const minRowPosts = (state: WallState) => (state.agent || state.pattern ? 1 : 2);

export function groupBySite(items: WallItem[], minPosts = 2): SiteRow[] {
  const map = new Map<string, SiteRow>();
  for (const i of items) {
    for (const site of i.sites) {
      const row = map.get(site) ?? { site, posts: [], outcomes: [], worked: 0, stuck: 0 };
      const o = i.siteOutcomes[site] ?? i.outcome;
      row.posts.push(i);
      row.outcomes.push(o);
      if (o === 'worked') row.worked++;
      if (o === 'stuck') row.stuck++;
      map.set(site, row);
    }
  }
  const rows = [...map.values()].filter((r) => r.posts.length >= minPosts);
  for (const r of rows) {
    r.posts.sort((a, b) => (b.created > a.created ? 1 : b.created < a.created ? -1 : b.engagement - a.engagement));
    r.outcomes.sort((a, b) => ORDER[a] - ORDER[b]);
  }
  return rows.sort((a, b) => b.posts.length - a.posts.length || a.site.localeCompare(b.site));
}

// The summary counts only the posts that are in a row, so the numbers add up on the page.
export function summary(_items: WallItem[], rows: SiteRow[]) {
  const posts = [...new Set(rows.flatMap((r) => r.posts))];
  const worked = posts.filter((i) => i.outcome === 'worked').length;
  const stuck = posts.filter((i) => i.outcome === 'stuck').length;
  const pct = worked + stuck ? Math.round((100 * worked) / (worked + stuck)) : null;
  const agents = new Set(posts.flatMap((i) => i.agents)).size;
  return { pct, posts: posts.length, sites: rows.length, agents };
}

export function age(created: string, today: string): string {
  const days = Math.round((Date.parse(today) - Date.parse(created)) / 86400000);
  if (days < 1) return 'today';
  if (days < 30) return `${days}d`;
  if (days < 365) return `${Math.round(days / 30)}mo`;
  return `${Math.floor(days / 365)}y`;
}

export function renderRows(rows: SiteRow[], today: string): string {
  return rows
    .map((r) => {
      const latest = r.posts[0];
      const who = latest.platform === 'x' ? `@${latest.author}` : `u/${latest.author}`;
      const meta = [who, latest.agents[0], age(latest.created, today)].filter(Boolean).join(' · ');
      const strip = r.outcomes.map((o) => `<i class="sq sq--${o}"></i>`).join('');
      return `<tr class="row" data-site="${esc(r.site)}">
  <th scope="row"><button type="button" class="row__open" aria-expanded="false">${esc(r.site)}</button></th>
  <td class="row__strip"><span class="strip" aria-hidden="true">${strip}</span><span class="tally"><b class="t-ok">${MARK.worked}${r.worked}</b> <b class="t-no">${MARK.stuck}${r.stuck}</b></span><span class="sr-only">${r.worked} worked, ${r.stuck} stuck, ${r.posts.length} posts</span></td>
  <td class="row__q">${esc(latest.quote)}<small>${esc(meta)}</small></td>
</tr>
<tr class="detail" hidden><td colspan="3"><div class="embeds">${r.posts.map((p) => renderPost(p, r.site, today)).join('')}</div></td></tr>`;
    })
    .join('\n');
}

export function renderPost(p: WallItem, site: string, today: string): string {
  const o = p.siteOutcomes[site] ?? p.outcome;
  const who = p.platform === 'x' ? `@${p.author} on X` : `u/${p.author} in r/${p.community}`;
  const kind = p.id.startsWith('reddit:t3') ? 'thread' : 'single';
  const tags = [...p.antiPatterns.map((t) => `<li class="tag tag--anti">${MARK.stuck} ${esc(t)}</li>`), ...p.patterns.map((t) => `<li class="tag tag--good">${MARK.worked} ${esc(t)}</li>`)];
  return `<article class="post${p.unavailable ? ' is-loading' : ''}" data-platform="${p.platform}" data-kind="${kind}" data-url="${esc(p.url)}" data-post-id="${p.postId ?? ''}">
  <span class="m m--${o}" title="${o}">${MARK[o]}</span>
  <div class="post__embed" data-slot></div>
  <blockquote class="post__quote" cite="${esc(p.url)}"><p>${esc(p.quote)}</p><footer><a href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">${esc(who)}</a> <span>${age(p.created, today)}</span></footer></blockquote>
  ${tags.length ? `<ul class="post__tags">${tags.join('')}</ul>` : ''}
</article>`;
}
