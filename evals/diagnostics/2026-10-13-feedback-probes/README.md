# Prospective feedback probes — 13 October 2026

[English](README.md) | [简体中文](README.zh-CN.md)

These are real executed tests on independent tasks distinguished by their research questions. Development use does not invalidate that identity. This narrative was corrected on 2026-10-13; original requests, reports, reviews and scores are unchanged.

Eight first replies parsed under the new explicit JSON contract, but only **3/8 met the requested report length**. Serious source/decision errors remain. This closes the bounded implementation-and-validation batch, **not** the question of whether Toolkit improves research quality. No failed sample was repaired or rerun to obtain a favorable result.

## Changes and frozen scope

The [October 12 evidence](../../studies/2026-10-12-lite-four-models/README.md) and [LongCat format probes](../2026-10-12-longcat-format/README.md) identified prompt/schema mismatch, process disclosures, excessive structure, incorrect constraint application and provenance drift. This batch:

1. Injects the actual Lite stage guide instead of the Full workflow reference in new instruction-only evaluations.
2. Specifies JSON `report`/`notes` strings and escaping; preserves the already strict parser. A common final envelope reminder in both conditions puts production disclosures in notes and retains the brief's length/citation requirements.
3. Updates bilingual Lite/writing guidance: compact short notes, current hard constraints before preferences, forecasts separate from present eligibility, and measurements kept with their population, date and treatment state. The plugin carries the same guidance.

[Plan](plan.json), [commitment](commitment.json), source archives and [manifest](manifest.json) were frozen before calls. The base commit is `7e80b91cea2903673f0b433319c62192b1ce87d2`; **uncommitted working-tree changes were included**, so base commit alone does not identify the executed instructions. Exact injected method text/hashes and harness bytes are retained. The public driver archive replaces one local Git executable path with `<GIT_EXECUTABLE>`; original/public archive and decoded-source hashes are separately recorded in the [public manifest](public-manifest.json). It is not byte-identical to the private execution driver.

Two new implementation-authored fictional tasks cover an English constrained storage choice and a Chinese water-use comparison. Each ran with/without Toolkit on `deepseek-flash` and `LongCat-2.0`, in a predeclared counterbalanced order. Eight calls total, no judges, retries or post-result additions; both arms use identical settings except the Toolkit method text. Thinking disabled, 4,096 completion / 32,768 total tokens, 180 seconds, text response mode, `json_object_v1`, whole-output JSON fence allowed. API total-token/time checks occur after return, not guaranteed billing caps.

These two exposed development tasks are not held-out observations. Task/model/input changes prevent a controlled before/after effect estimate or attribution to one edit. Implementation-assistant source checking is condition-aware, not independent validation. Earlier missing pairs and scores remain unchanged.

## Results and residual defects

| Author / task | Without Toolkit length | With Toolkit length | Required range |
| --- | ---: | ---: | --- |
| DeepSeek / storage | 144 ✓ | 118 ✗ | 120–170 whitespace words |
| LongCat / storage | 150 ✓ | 198 ✗ | 120–170 whitespace words |
| DeepSeek / water | 244 ✓ | 283 ✗ | 180–260 non-whitespace Unicode characters |
| LongCat / water | 711 ✗ | 626 ✗ | 180–260 non-whitespace Unicode characters |

Counts cover the whole report, including headings, markup and citations. All eight parsed; a fixed literal scan found no process-disclosure terms. This does not establish reliable formatting, successful blinding or semantic quality. In particular, **all four Toolkit reports failed length** in this small diagnostic.

[Source adjudication](adjudication.json) preserves the main counterexamples. DeepSeek's Toolkit storage report recommends A, rejects it and then says no option is feasible while claiming 14 TB is less than the required 12 TB; C actually meets current constraints. Several water reports still assert a changed soil mix although July's mix was unrecorded. A length-compliant baseline water note also contains that error. Parser success and measured length cannot certify the recommendation or source interpretation.

[Analysis](analysis.json) retains provider-level reported tokens and local elapsed sums. Notes and raw outputs are in `attempts/`; no output was substituted. [Two editorial controls](editorial-controls.json), 126 English words and 250 Chinese characters, were written **after** the results by the implementation assistant. They illustrate source-faithful compact answers and exercise a software gate; they are not new model generations, predeclared controls or replacement scores.

## Product verification and disposition

`python scripts/check_feedback_probes.py --self-test` reconstructs the evidence read-only and runs **two test methods covering seven artifact cases** in temporary tool-backed tasks. All five real length failures are rejected even when a synthetic checklist falsely claims completion; neither a Lite receipt nor completed status is granted. Both editorial controls pass the existing length gate. These tests establish tested software behavior only; the research agent still must register the agreed constraint and resolve semantic defects.

Adopt the concrete prompt/schema and guidance corrections. **Do not recommend prompt-only self-checks as a completion guarantee, claim that LongCat is generally reliable, or claim a research-quality gain.** No further paid sample was appended to this fixed queue. Continue concrete repairs on existing tasks with Astra review; outside task collection and additional reviewer panels are not prerequisites.
