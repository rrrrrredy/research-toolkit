# Located process-language revision

Based on the independent process_language findings. Preserve source versions, cited locations, assumptions, calculations and substantive evidence limits; keep access/reading operations in the original execution records.

Previous SHA256: 818d119dff2f67c6747331df2d1c6b17dcb4151304af2de2307c723d6b586832

Revised SHA256: 5988ea792c50ec4c20b1124b0d5764fe350f849631d4770528c7cb2a1f38b57f

```diff
--- current-before.md
+++ draft-revision-full-02.md
@@ -377,9 +377,9 @@
 
 The report combines three evidence types. Public prices and technical/financial disclosures retain their version or observation date. Published studies retain their experimental setting. Workload acceptance rates, human time, tool allowances, demand and hosting capacity are explicit economic scenarios. Local tokenizer counts and deterministic arithmetic were actually executed; no model inference experiment was performed.
 
-`workload_calculations.py` and `calculation-results.json` contain all route counts, price inputs, cache request rows, agent step rows and sensitivity cases. `tokenizer_count.py` and `tokenizer-results.json` retain the exact paired strings, package version and encoding-file hashes. `reading-ledger.json` records the original paths and actual reading scope; `web-reading-notes.md` separates successfully read web originals from failed local downloads.
-
-Historical OpenAI launch pages were read through the web tool after local 403 responses. The DeepSeek R1 news URL redirected to the current quickstart, so it does not establish a historical R1 price here. Gemini's acquired documentation included authoritative Markdown inside server-delivered HTML; that text was extracted separately while preserving originals. The current GPT-6.1 model page resolves the short/long price boundary. The dated Claude rate card is used for commercial SKU prices, without inventing an underlying weight revision absent from that source.
+`workload_calculations.py` and `calculation-results.json` contain all route counts, price inputs, cache request rows, agent step rows and sensitivity cases. `tokenizer_count.py` and `tokenizer-results.json` retain the exact paired strings, package version and encoding-file hashes.
+
+Historical OpenAI launch pages supply the dated model and price announcements. The DeepSeek R1 news URL redirected to the current quickstart, so it does not establish a historical R1 price here. Gemini rates use the official documentation version listed in the source record. The current GPT-6.1 model page resolves the short/long price boundary. The dated Claude rate card is used for commercial SKU prices, without inventing an underlying weight revision absent from that source.
 
 The Azure quote retains the full public JSON and exact SKU rows. The report does not use post-cutoff Lambda rates. It also does not use the concurrency preprint's inaccessible raw commit or mismatched GPU capacity claim to assign a measured throughput to its independent hosting scenario. No confidential margin, negotiated discount, realized labor saving or language-wide token ratio is inferred.
 
```

## Author acceptance and formal save

Accepted by the registered substantive author `/root/ttc_research` after reading the saved process_language finding and comparing the actual current manuscript with this revision. The textual changes match the recorded diff; numerical results, source versions, page/table references, assumptions and material evidence limits remain intact. This is author acceptance, not independent-review approval.

The coordinator-prepared proposal used CRLF line endings. The accepted file uses LF, with identical text, so its on-disk SHA-256 matches the revised hash above. Original proposal byte SHA-256: `8540fcb3bc46f5f8f253563e39c00dcc38446332809e3423fd8952b29989080c`.
