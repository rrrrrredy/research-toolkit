# 完整稿修订 01：预算口径与第二轮耗时

以 native-full-prepared.json 指向的实际报告 `C:\Users\luosong03\Documents\ChatGPT\Others\work\toolkit-long-research-20261109\evals\runs\2026-11-09-long-research\tasks\test_time_compute_zh\reports\current.md` 为基准，原稿 SHA256 为 `eef296bd90c6ef8a34e04a7ce533e84034adc24c77417030b9fef057ab6b1eac`；保留此前有限探针与停止可学习性的修订。

本次只处理两个已定位问题，修改行号（前后相同）为 141, 143, 157, 166：

- 第 141、143、157 行：将 0.10 美元明确为单题期望费用预算，表头明确期望工具费用和期望总费用；补充 7 个强生成候选合计 2 次工具重试时费用为 0.10020 美元的反例。硬上限需按实际余额与在途费用预留限制新调用和重试，固定候选数及其成功率不构成硬上限保证。
- 第 166 行：对应 EV-TTCZH-01，披露原代码已有的第二轮前置处理 2.7 秒假设，说明每链 52.1 秒、两波 104.2 秒。保留原始算术、数值及方案排序。

已阅读 native-full-current-reviews/evidence/response.json 与 process_language/response.json；后者为 pass，findings 为空，无额外必要修订。核对预算代码、既有 budget_output.json 和 budget_stdout.txt，未执行预算代码、未重跑算例或任何测试，未修改工具状态或报告发布位置。除上述四行外，其余分析、引文逐字保留，原始作者稿与先前修订均保留。

输出 draft-revision-full-01.md，SHA256 `259846b7cc7271e0ca20b3a25a5d1fb992c1d7aac6722232f6ea35e704661ef4`，53637 bytes。作者修订供独立复核，不替代验收。
