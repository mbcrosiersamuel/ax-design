// WebMCP: register read-only tools on every page, for browsers and agents that support
// document.modelContext (W3C webmachinelearning/webmcp). Older builds used navigator.modelContext.
// The page works the same without it.

type ToolResult = { content: { type: 'text'; text: string }[] };
type ModelContext = {
  registerTool: (tool: {
    name: string;
    description: string;
    inputSchema: Record<string, unknown>;
    annotations?: Record<string, unknown>;
    execute: (input: Record<string, unknown>) => Promise<ToolResult>;
  }) => unknown;
};

const mc: ModelContext | undefined =
  (document as unknown as { modelContext?: ModelContext }).modelContext ??
  (navigator as unknown as { modelContext?: ModelContext }).modelContext;

if (mc?.registerTool) {
  const text = (data: unknown): ToolResult => ({ content: [{ type: 'text', text: JSON.stringify(data) }] });
  const cache = new Map<string, Promise<any>>();
  const load = (path: string) => {
    if (!cache.has(path)) cache.set(path, fetch(path).then((r) => r.json()));
    return cache.get(path)!;
  };
  const readOnly = { readOnlyHint: true, destructiveHint: false, openWorldHint: false };

  mc.registerTool({
    name: 'list_patterns',
    description:
      'Agent Experience patterns: what stops AI agents on websites and what lets them through. Each has a title, a one-sentence summary, the evidence, and the fix.',
    inputSchema: { type: 'object', properties: {} },
    annotations: readOnly,
    execute: async () => {
      const d = await load('/patterns.json');
      return text(d.patterns.map(({ body, ...p }: any) => p));
    },
  });

  mc.registerTool({
    name: 'get_site_report',
    description:
      'Real posts from X and Reddit about AI agents on one website (for example delta.com): how often agents got through, and the quotes with links.',
    inputSchema: {
      type: 'object',
      properties: { domain: { type: 'string', description: 'A bare domain, such as amazon.com' } },
      required: ['domain'],
    },
    annotations: readOnly,
    execute: async ({ domain }) => {
      const d = await load('/wall.json');
      const site = String(domain).toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0];
      const posts = d.posts.filter((p: any) => p.sites.includes(site));
      if (!posts.length) return text({ site, posts: 0, note: 'No posts about this site yet.' });
      const outcome = (p: any) => p.siteOutcomes?.[site] ?? p.outcome;
      const n = (o: string) => posts.filter((p: any) => outcome(p) === o).length;
      return text({
        site,
        posts: posts.length,
        worked: n('worked'),
        stuck: n('stuck'),
        mixed: n('mixed'),
        url: `${location.origin}/wall?days=0&site=${encodeURIComponent(site)}`,
        recent: posts.slice(0, 15).map((p: any) => ({
          date: p.created,
          outcome: outcome(p),
          assistant: p.agents.join(', '),
          stuckOn: p.antiPatterns,
          workedWith: p.patterns,
          quote: p.quote,
          url: p.url,
        })),
      });
    },
  });

  mc.registerTool({
    name: 'subscribe',
    description:
      'Subscribe a person to the agentexperience.design newsletter (new examples and patterns, a few times a month). Ask the person before you call this. It sends their name and email address to the site.',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'The name of the person' },
        email: { type: 'string', format: 'email', description: 'The email address of the person' },
      },
      required: ['name', 'email'],
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false, consequentialHint: true },
    execute: async ({ name, email }) => {
      const body = new URLSearchParams({ 'form-name': 'subscribe', name: String(name), email: String(email) });
      const r = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
      return text(r.ok ? { subscribed: true, email } : { subscribed: false, status: r.status, note: 'The form did not accept the request.' });
    },
  });

  mc.registerTool({
    name: 'search',
    description: 'Search this site: patterns, gallery examples, and the wall of posts about agents on websites.',
    inputSchema: {
      type: 'object',
      properties: { query: { type: 'string', description: 'Words to look for, such as captcha, 2FA, or a company name' } },
      required: ['query'],
    },
    annotations: readOnly,
    execute: async ({ query }) => {
      const q = String(query).toLowerCase();
      const hit = (s: unknown) => String(s ?? '').toLowerCase().includes(q);
      const [c, w] = await Promise.all([load('/patterns.json'), load('/wall.json')]);
      return text({
        patterns: c.patterns.filter((p: any) => hit(p.title) || hit(p.summary) || hit(p.body)).map(({ body, ...p }: any) => p),
        examples: c.examples.filter((p: any) => hit(p.title) || hit(p.summary) || p.companies.some(hit)),
        posts: w.posts
          .filter((p: any) => hit(p.quote) || p.sites.some(hit) || p.agents.some(hit) || p.antiPatterns.some(hit) || p.patterns.some(hit))
          .slice(0, 20)
          .map((p: any) => ({ sites: p.sites, outcome: p.outcome, quote: p.quote, url: p.url, date: p.created })),
      });
    },
  });
}
