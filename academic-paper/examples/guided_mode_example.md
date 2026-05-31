# Guided-Writing Mode Example

A complete walkthrough of the `guided-writing` mode for a journal article on AI in higher education.

---

## User Trigger

> **User**: "引导我写论文"
>
> **AI**: Detects `guided-writing` mode trigger (zh-CN). Enters guided-writing mode.

---

## Step 0: Intent Alignment

**AI**: "欢迎进入导师模式写论文。在我们开始之前，我想了解几件事：

1. 你目前对这篇论文最焦虑的部分是什么？
2. 你的目标读者是谁？子领域专家还是更广泛的学术受众？
3. 你心中是否已有清晰的结构，还是需要我帮你梳理？"

**User**: "我最焦虑的是讨论部分（Discussion），不知道如何让结果和文献对话。目标读者是教育技术领域的同行。结构大概有了，但可能需要调整。"

**AI**: `[INTAKE: anxiety=Discussion, audience=ed-tech peers, structure=partial]`

---

## Step 1: Decoupling Design

**AI**: "基于你的研究问题'AI 工具如何影响大学生批判性思维能力'，我建议将论文拆分为以下论证单元：

| 单元 | 核心主张 | 证据来源 |
|------|---------|---------|
| U1 | AI 写作辅助工具在高校中普及率已达 67% | 问卷调查数据 |
| U2 | 使用 AI 工具的学生在开放式问题中表现出的批判性思维评分较低 | 实验组 vs 对照组 |
| U3 | 这种效应在人文社科领域比 STEM 领域更显著 | 分领域对比 |
| U4 | 教师的引导方式可以部分缓解这种负面效应 | 干预组数据 |

你觉得这个拆分合理吗？有没有单元需要合并或拆分？"

**User**: "U3 和 U4 可以，但 U1 和 U2 之间的逻辑跳跃有点大。也许需要加一个'AI 工具改变了学生的认知负荷分配'作为中介？"

**AI**: "很好的观察。那我们将 U1-U2 之间插入 U1.5：认知负荷重新分配是 AI 工具影响批判性思维的中介机制。这样链条更完整。"

---

## Step 2: Blueprint Building

**AI**: "让我们为 Introduction 设计论证路径。你有三个选项：

**路径 A（问题驱动）**：先描述 AI 工具普及的紧迫性，再引出批判性思维下降的危机，最后提出你的研究问题。
- 优点：开头抓人，读者立刻感受到问题的重要性
- 风险：可能显得过于 alarmist，需要谨慎把握语气

**路径 B（文献缺口驱动）**：先综述现有文献对 AI 与教育的研究，指出大多聚焦效率提升而忽视思维质量，再提出你的问题。
- 优点：学术性强，立论扎实
- 风险：开头较平淡，需要更强的文献综述

**路径 C（理论驱动）**：从认知负荷理论出发，提出 AI 工具降低了' productive struggle '的假设，再引出实证研究。
- 优点：理论框架清晰，适合理论导向的期刊
- 风险：对不熟悉该理论的读者门槛较高

你倾向哪条路径？"

**User**: "我选路径 B。我的目标期刊更看重文献综述的深度。"

**AI**: "锁定路径 B。Introduction 的论证蓝图：文献综述 → 缺口识别（效率 vs 思维质量）→ 研究问题。"

---

## Step 3: Section-by-Section Drafting

### Section: Introduction

**Round 1: Preparation**

**AI**: "本章论证目标：通过文献综述建立'AI 工具对批判性思维的影响尚未被充分研究'的共识，然后提出你的研究问题。

在你写之前——你认为 Introduction 最难的部分是什么？"

**User**: "最难的是既要展示文献的广度，又不能变成堆砌。"

**AI**: `[COMMITMENT: Introduction: user predicts 'balancing breadth vs depth in literature review']`

---

**Round 2: Options**

**AI**: "基于路径 B，这里有三种文献组织方式：

**方式 1（时间线）**：按 AI 在教育中的应用演进（2018-2024），展示研究焦点的转移
- 优点：历史感强，容易看出趋势
- 风险：可能变成编年史，缺乏批判性

**方式 2（主题聚类）**：分三块：AI 与学习效率、AI 与写作质量、AI 与高阶思维
- 优点：逻辑清晰，直接指向你的缺口
- 风险：每块内部仍需处理时间跨度

**方式 3（争议聚焦）**：围绕'AI 是否削弱学生能力'这一核心争议，展示正反双方
- 优点：戏剧性最强，直接建立你的立场
- 风险：可能过于 polarized，忽略 nuanced 研究

你的选择？"

**User**: "方式 2。我的研究正好填补'高阶思维'这一块的空白。"

**AI**: "锁定方式 2。文献三块：效率 → 写作质量 → 高阶思维（缺口）。"

---

**Round 3: Drafting**

**AI**: `[DRAFT: review required]`

> 过去五年，人工智能工具在高等教育中的渗透率经历了指数级增长。从早期的语法检查工具到如今的大型语言模型，AI 辅助写作已不再是边缘现象，而是成为了大学生学术写作的常规组成部分（Smith et al., 2023; Chen & Lee, 2024）。然而，现有研究对这一现象的评估主要聚焦于两个维度：学习效率的提升和写作产出的数量增长（Johnson, 2022; Park et al., 2023）。鲜有研究关注一个更为根本的问题——当 AI 承担了越来越多的认知劳动时，学生的批判性思维能力是否正在悄然退化？
>
> 本研究通过为期一学期的对照实验（N=312），系统考察了 AI 写作辅助工具对大学生批判性思维能力的影响。我们提出以下研究问题：...

"这是参考草稿。请重点检查：
1. 文献引用的逻辑是否准确？
2. 从'效率'到'思维质量'的过渡是否自然？
3. 表达是否符合你的学术风格？"

**User**: （修改后）
> 人工智能写作工具在高等教育中的普及已不容忽视。据统计，超过六成的大学生曾在学术写作中使用过 ChatGPT 或类似工具（Smith et al., 2023）。现有研究大多聚焦于这一趋势带来的效率红利...

---

**Round 4: Feedback**

**AI**: "很好。三个维度的反馈：

**Logic**: '效率红利'到'思维质量'的过渡比我的草稿更自然。但'不容忽视'这个说法有点绝对——有没有数据支撑'不容忽视'？

**Evidence**: 你引用了 Smith et al. (2023) 的六成数据，但我的草稿引用了更近期的 Chen & Lee (2024)。你的版本是否遗漏了更新的证据？

**Expression**: '效率红利'这个词很生动，但注意不要用太多。如果 Discussion 也用这个短语，重复可能会显得单一。"

**User**: "好，我把'不容忽视'改成具体数据，并补充 Chen & Lee。"

---

**Round 5: Revision**

**User**: （修改后提交）

**AI**: "修改解决了我的顾虑。这段确认通过。进入下一章 Literature Review？"

**User**: "下一章。"

---

## Step 5: Reviewer Feedback (Excerpt)

After all sections are drafted, `guided_reviewer_agent` reviews the complete paper.

**Reviewer**: "读完全文，我最困惑的一点是：你在 Methods 中提到使用了'经过验证的批判性思维量表'，但在 Discussion 中没有讨论该量表的局限性。这是故意的吗？

最清晰的部分是 Results 的图表呈现——数据趋势一目了然。

对于这段（Introduction 第二段）：'效率红利'这个词你在 Introduction、Literature Review 和 Discussion 中各用了一次。在学术写作中，一致的术语是优点，但三次重复同一个生动短语可能显得像 a tic。你能考虑在 Discussion 中换成更中性的表达吗？"

**User**: "好的，Discussion 中改成'效率增益'。"

**Reviewer**: "很好。这个修改解决了我的 concern。还有 2 个问题，你想先处理哪个？"

---

## Final Output

After all reviewer feedback is addressed, `formatter_agent` produces the final document in the user's chosen format (LaTeX / DOCX / PDF / Markdown).
