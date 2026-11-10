# bytedance_advertising_zh

[Complete report](final.md) · [Original task](task.json) · [Original review results](reviews/) · [Analyses and first manuscripts](analysis/) · [Source index](sources/source_registry.csv)

The accepted report is the exact registered `reports/current.md` output. Its delivery result is retained under `delivery/`. Original author manuscripts, substantive units, calculations and subsequent changes remain separate files in `analysis/`; original independent findings and revision confirmations remain in `reviews/`. The execution files identify their actual agent context or API run.

Public-source URLs, reading locations and capture hashes are supplied in the source index and the corresponding `evals/source_packs/` package. Complete third-party source captures and full assignment inputs remain in the local execution archive; they are not republished as project-owned documents. Local paths in unchanged execution originals identify that archive.

This is one report assignment in the 13-question, 15-report baseline. Revisions and another-language output do not count as another independent question. It is not a fixed-model version comparison. See the study README for the actual findings and API-to-native continuation.

Report SHA-256: `2ceafdcf61f2b80e0900078f67b95bbc6887d8a1780be302b217c398f9505d97`.

## Download URL redaction / 下载链接脱敏

On 2026-11-10, the public copy of `analysis/sources.json` removed the query string from `BDA-A02.local_retrieval.final_url`. Companies House had redirected the public financial filing to an AWS-signed download URL, valid for 60 seconds and expired at 2026-11-09 12:16:45 UTC. The original URL now returns HTTP 403, `Request has expired`. The source's stable public URL, document hash, reading notes, report and review records are unchanged. `final_url` retains the destination without its temporary authorization; use the source's `url` to retrieve the filing. The local execution original is retained. `artifact-hashes.json` describes this redacted public copy.

2026-11-10，公开副本仅移除了 `analysis/sources.json` 中 `BDA-A02.local_retrieval.final_url` 的查询参数。这是英国 Companies House 公开财报下载时跳转的 AWS 临时签名链接，有效期 60 秒，已于北京时间 2026-11-09 20:16:45 到期；原链接实际返回 HTTP 403、`Request has expired`。正式来源链接、材料哈希、阅读记录、报告与审阅记录均未修改。`final_url` 只保留去除临时授权后的目标地址；重新下载请使用该来源的 `url`。本地执行原件保留，`artifact-hashes.json` 对应脱敏后的公开副本。

- Original source-record file SHA-256 / 原来源记录文件哈希: `dc601447474a23f61582b77524787a478cf1442281646bc9d93037dcb59bbb36`
- Redacted public file SHA-256 / 脱敏公开文件哈希: `7dd35fcaf4624ba76818faf11a7407eb6092b799db4adc64bd1840b9c38b711c`
