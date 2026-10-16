# Website discovery and maintenance

This site uses committed HTML in `docs/`, deployed by the existing GitHub Pages build. No framework migration, CMS, analytics service or deployment-setting change is needed. Website work here improves discoverability and source traceability; it does not promise indexing, rankings, AI citations, usage or stars.

The optional `docs/materials/` reading pages are exported from `agent-trajectory-data/corpora/ai-industry` using that repository's `scripts/export_ai_industry_site.cjs`. Edit the source Markdown there, export, then run the normal site builder. `materials/pages.json` extends the existing metadata manifest; no additional website runtime is needed. Catalogs and guides have bilingual entries; article bodies keep their original language. The original Markdown and all historical versions remain linked from each page.

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

At the 15 October 2026 audit, the GitHub connector's generic fetch endpoint rejected `/traffic/views` as unsupported. A subsequent read using the owner's existing local GitHub credential succeeded for views, clones, popular paths and referrers. Those snapshots were saved locally, outside the public repository; the Actions token and its permissions remain unchanged. No API credentials were created or broadened. No site event collector is configured.

The homepage contains the current owner's public Google verification meta tag. It is an ownership marker, not an API credential, and must remain after successful verification. Keep verification tags outside the generated `discovery` block in `docs/index.html`; `build_site.py` preserves them and copies them to the Chinese homepage. A tag in the source does not establish that account-side verification or sitemap submission has succeeded; confirm those statuses in the provider's dashboard.

The owner's Bing verification file is preserved as `docs/BingSiteAuth.xml`, served at `https://rrrrrredy.github.io/research-toolkit/BingSiteAuth.xml`. Keep this file after verification too. Both services' basic website verification, sitemap submission and search reports are free; advertising purchases and API credentials are unnecessary for this setup. These tools are optional diagnostics, not a requirement for appearing in search results.

1. **Google Search Console:** use the URL-prefix property `https://rrrrrredy.github.io/research-toolkit/`. Choose HTML-tag verification, deploy the exact tag supplied to the owner through a reviewed change, then click Verify. The current owner's tag is already in the homepage source; a different account requires its own verification or an explicitly approved invitation. Keep the verification material. Submit `https://rrrrrredy.github.io/research-toolkit/sitemap.xml` under Sitemaps; inspect the two homepages, method pages and update case after deployment. A Domain property would require DNS control of the host and is unnecessary here. See [URL-prefix properties](https://support.google.com/webmasters/answer/10432366) and [verification methods](https://support.google.com/webmasters/answer/9008080).
2. **Bing Webmaster Tools:** sign in with an existing account, add the same project website URL (not the `github.com` repository URL), and choose XML-file verification. The current owner's file is already in `docs/`; confirm it is deployed at the exact URL Bing requests, then click Verify. Submit the same sitemap under Sitemaps. Homepage meta-tag verification is another supported option. Importing Search Console is optional and grants Bing access to that account; it is not required. See [Bing site verification](https://www.bing.com/webmasters/help/add-and-verify-site-12184f8b) and [Bing's free setup guide](https://blogs.bing.com/webmaster/2025/6/Start-Using-Bing-Webmaster-Tools-to-Improve-Your-Site-Visibility/).
3. **Repository traffic:** use the owner's existing access at repository **Insights → Traffic** and export or record observations before the rolling 14-day window expires. This measures repository visits/clones, not Pages visits. The API currently requires repository Administration read permission for fine-grained tokens; do not expand this PR's token or Actions permissions to obtain it. See [traffic UI](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository) and [traffic API permissions](https://docs.github.com/en/rest/metrics/traffic).
4. **Website clicks:** Search Console/Bing clicks are search-result clicks. They do not measure on-site “use toolkit” or “Star on GitHub” actions. No website event collector is configured; those events remain unmeasured. Choose a lawful existing analytics service and collection scope separately if needed; none is installed here.
5. **Future API collection:** configure approved credentials through GitHub Actions secrets or another secure credential store, never in chat, source code, logs or reports. Start with manual exports; API automation should be added only once the available accounts and approved read scopes are known.

Keep the following series separate. Unknown is not zero. Preserve each export or observation's timestamp, time zone, covered interval, source and definition. Do not add overlapping cumulative windows.

| Series | Record | Interpretation |
| --- | --- | --- |
| Ordinary search | Engine, property, interval, page/query, impressions, clicks, CTR, position, export reference | Engine-specific search performance; no claim that all AI visibility is included or separable. |
| AI citation observation | Product/model, date, exact prompt, locale/session conditions, cited URL and saved answer/evidence | A reproducible observation, not a market share or comprehensive citation count. |
| Website clicks | Collector, event definition, interval and consent/coverage limits | Unmeasured until an actual site event collector is configured. Search clicks are a separate series. |
| Stars | UTC observation time, public repository total, difference between snapshots | Net change only. Stars can be removed; no precise attribution to search, AI, the site or this PR. |
| Repository traffic | UTC date/window, visits/unique visitors/clones/referrers and export reference | GitHub repository activity, not GitHub Pages analytics. |

After successful deployments, the existing workflow saves a public star-total snapshot as an Actions artifact with a timestamp and source URL. It uses the existing Actions token with unchanged read permissions and no new secret. Local runs can read anonymously; the audit's anonymous request hit GitHub's rate limit, while the existing connector returned a public baseline of 232 stars at 2026-10-15 06:34:06 UTC. Collection failures are explicit and do not mean zero stars. This is a deployment-time sample, not a continuous growth series. Download artifacts before retention expires if a longer history is wanted. No empty or fabricated search/AI/click measurements are generated.

## Rollback

Before merge, close the PR and leave production unchanged. After merge, revert the merge commit through a new PR and let the existing Pages deployment run. This restores the previous pages and workflow; the original research evidence was not changed. Avoid restoring unrelated files or resetting another task's workspace.

Reference decisions follow [Google multilingual guidance](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites), [localized alternates](https://developers.google.com/search/docs/specialty/international/localized-versions), [canonical consolidation](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) and [robots.txt location rules](https://developers.google.com/search/docs/crawling-indexing/robots/intro).
