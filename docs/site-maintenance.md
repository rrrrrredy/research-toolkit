# Website discovery and maintenance

This site uses committed HTML in `docs/`, deployed by the existing GitHub Pages build. No framework migration, CMS, analytics service or deployment-setting change is needed. SEO/GEO work here improves discoverability and source traceability; it does not promise indexing, rankings, AI citations, usage or stars.

## Editing and checks

Run from the repository root with Python 3.10+ (standard library only):

```sh
python scripts/build_site.py
python scripts/build_site.py --check
python scripts/check_site.py --self-test
python scripts/check_docs_sync.py
python scripts/check_docs_sync.py --skill SKILL.zh-CN.md --html docs/framework.zh-CN.html
```

- Edit `docs/index.html`, including its existing bilingual `showcase-data` JSON, for homepage content. The builder creates `docs/index.zh-CN.html` with Chinese text, case excerpts, request text and links already in the initial HTML. Do not edit that generated file directly.
- Edit other HTML pages directly. Update `DESCRIPTIONS`, `TITLES` or `PAIRS` in `scripts/build_site.py` when adding or changing a page. The builder refreshes metadata and the sitemap; `--check` detects drift without writing. Preserve evidence files and the embedded SKILL blocks.
- The checker reads initial HTML, validates 28 hand-authored/generated HTML pages, resolves local links/assets and HTML fragments, validates same-repository GitHub links against the checkout, checks reciprocal hreflang and clean sitemap URLs, and checks llms.txt destinations. It does not test every third-party website or Markdown fragment. Live access to a source remains the researcher's responsibility.
- Homepage, method, translated office report and update scenario have real language pairs. The two historical case indexes contain different material; the API-or-browser case has no Chinese translation. They are not falsely paired with other research topics.
- Canonicals use the `https://rrrrrredy.github.io/research-toolkit/` project prefix. Directory indexes use a trailing slash; old `index.html` links still work. The sitemap is a curated list of 13 useful canonical entry pages, not a dump of raw records, intermediate drafts or parameter URLs. Historical evidence remains accessible.
- Language controls are ordinary links usable without JavaScript. Legacy `?lang=en|zh` links navigate to a static alternate when one exists. On a page without a translation, the document keeps its actual language. With JavaScript disabled, an old query URL retains the base document and offers static language links. Static hosting cannot issue query-dependent HTTP redirects.
- Old `theme`, `case` and `detail` preferences are accepted. Theme persists in local storage; case/detail persist per language in session storage. Internal links and the browser address are cleaned after those preferences are read. Canonical metadata is fixed in the initial HTML and never depends on stored preferences.

The existing **Framework checks** workflow runs the build and local checks on push/PR. Its `workflow_run` job runs after a successful **pages build and deployment** on `main`, checks out that deployment's commit, then checks raw HTML and assets against the committed bytes, static metadata, sitemap, language URLs and legacy query URLs. It retries brief propagation delays. It does not deploy, merge, or modify Pages settings. Because this event handler must first be present on the default branch, verify the first merge manually too:

```sh
python scripts/check_site.py --live --attempts 6 --delay 15
```

For a local HTTP preview preserving the project path, use `--live --base-url http://127.0.0.1:PORT/research-toolkit/`. This checks served bytes; it does not prove production deployment. Browser regression checks should cover both languages, legacy URLs, theme, case/detail controls, report navigation and request copying on desktop and mobile.

## Robots and structured data

Only `https://rrrrrredy.github.io/robots.txt` governs crawling for this origin. A file at `/research-toolkit/robots.txt` would not. This repository does not manage the separate domain-root repository. The exact root URL returned HTTP 404 on 15 October 2026; no root robots policy was available at that check. Recheck the root before diagnosing later indexing problems. No root configuration was changed.

No structured data was added: the visible reports and provenance links currently provide the useful facts, without a clear need for a rich-result type. No ratings, user counts or evaluation gains are invented. `llms.txt` is a convenient reading index, not a standardized inclusion or citation guarantee.

## Measurement: permissions and minimal owner steps

At the 15 October 2026 audit, the available GitHub connection could read public repository metadata and create a PR. Its generic fetch endpoint rejected `/traffic/views` as unsupported. This does **not** establish whether the owner has traffic access in GitHub's UI. No Search Console or Bing connection, verification tag, or site analytics integration was found in the inspected repository/tools. Private account configuration remains unknown. No credentials were created, retrieved or broadened.

1. **Google Search Console:** add the URL-prefix property `https://rrrrrredy.github.io/research-toolkit/`. Use the offered HTML-tag verification on `docs/index.html` or place Google's provided verification file in `docs/`, deploy through a reviewed change, then verify. Keep the verification material. Submit `https://rrrrrredy.github.io/research-toolkit/sitemap.xml`; inspect the two homepages, method pages and update case after deployment. A Domain property would require DNS control of the host and is unnecessary here. See [URL-prefix properties](https://support.google.com/webmasters/answer/10432366) and [verification methods](https://support.google.com/webmasters/answer/9008080).
2. **Bing Webmaster Tools:** add the same project URL and use the offered homepage meta-tag verification, then submit the sitemap. Importing Search Console is optional and grants Bing access to that account; it is not required. See [Bing site verification](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b).
3. **Repository traffic:** use the owner's existing access at repository **Insights → Traffic** and export or record observations before the rolling 14-day window expires. This measures repository visits/clones, not Pages visits. The API currently requires repository Administration read permission for fine-grained tokens; do not expand this PR's token or Actions permissions to obtain it. See [traffic UI](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository) and [traffic API permissions](https://docs.github.com/en/rest/metrics/traffic).
4. **Website clicks:** Search Console/Bing clicks are search-result clicks. They do not measure on-site “use toolkit” or “Star on GitHub” actions. No website event collector is configured; those events remain unmeasured. Choose a lawful existing analytics service and collection scope separately if needed; none is installed here.
5. **Future API collection:** configure approved credentials through GitHub Actions secrets or another secure credential store, never in chat, source code, logs or reports. Start with manual exports; API automation should be added only once the available accounts and approved read scopes are known.

Keep the following series separate. Unknown is not zero. Preserve each export or observation's timestamp, time zone, covered interval, source and definition. Do not add overlapping cumulative windows.

| Series | Record | Interpretation |
| --- | --- | --- |
| Ordinary search | Engine, property, interval, page/query, impressions, clicks, CTR, position, export reference | Engine-specific search performance; no claim that all AI visibility is included or separable. |
| AI citation observation | Product/model, date, exact prompt, locale/session conditions, cited URL and saved answer/evidence | A reproducible observation, not a market share or comprehensive citation count. |
| Website clicks | Collector, event definition, interval and consent/coverage limits | Unmeasured until an actual site event collector is configured. Search clicks are a separate series. |
| Stars | UTC observation time, public repository total, difference between snapshots | Net change only. Stars can be removed; no precise attribution to SEO, AI, the site or this PR. |
| Repository traffic | UTC date/window, visits/unique visitors/clones/referrers and export reference | GitHub repository activity, not GitHub Pages analytics. |

After successful deployments, the existing workflow saves a public star-total snapshot as an Actions artifact with a timestamp and source URL. It uses the existing Actions token with unchanged read permissions and no new secret. Local runs can read anonymously; the audit's anonymous request hit GitHub's rate limit, while the existing connector returned a public baseline of 232 stars at 2026-10-15 06:34:06 UTC. Collection failures are explicit and do not mean zero stars. This is a deployment-time sample, not a continuous growth series. Download artifacts before retention expires if a longer history is wanted. No empty or fabricated search/AI/click measurements are generated.

## Rollback

Before merge, close the PR and leave production unchanged. After merge, revert the merge commit through a new PR and let the existing Pages deployment run. This restores the previous pages and workflow; the original research evidence was not changed. Avoid restoring unrelated files or resetting another task's workspace.

Reference decisions follow [Google multilingual guidance](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites), [localized alternates](https://developers.google.com/search/docs/specialty/international/localized-versions), [canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) and [robots.txt location rules](https://developers.google.com/search/docs/crawling-indexing/robots/intro).
