# zh-article-analyzer

[![Build & Release Skill](https://github.com/htlin222/zh-article-analyzer-skill/actions/workflows/release.yml/badge.svg)](https://github.com/htlin222/zh-article-analyzer-skill/actions/workflows/release.yml)
[![GitHub Release](https://img.shields.io/github/v/release/htlin222/zh-article-analyzer-skill?include_prereleases&label=skill%20version)](https://github.com/htlin222/zh-article-analyzer-skill/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
[![Skills Protocol](https://img.shields.io/badge/protocol-vercel--labs%2Fskills-blue)](https://github.com/vercel-labs/skills)
[![Compatible Agents](https://img.shields.io/badge/agents-40%2B-green)](https://github.com/vercel-labs/skills#supported-agents)

> 繁體中文文章深度分析技能。對任何中文文章進行多維度科學化剖析，產出精確到行號與段落的分析報告。

## Install

```bash
npx skills add htlin222/zh-article-analyzer-skill
npx skills add -g htlin222/zh-article-analyzer-skill        # global
npx skills add htlin222/zh-article-analyzer-skill --agent claude-code  # specific agent
```

## What it does

對繁體中文文章執行兩階段分析：

1. **量化階段**：執行 Python 腳本（jieba 分詞），產出客觀數據指標（詞彙豐富度、句式節奏、語域特徵、情感弧線），附行號定位
2. **質性階段**：基於量化數據，由 LLM 進行深層修辭、典故、論證結構分析

涵蓋：文體指紋（Stylometrics）、語言節奏、詞彙豐富度、引用與典故圖譜、主題動態、情感弧線、修辭力道、文白比、成語密度等。最終整合為一份「文章指紋報告」。

## Example

Below is a sample analysis report generated from [this Facebook post](https://www.facebook.com/caseychen1996/posts/pfbid0x7n8AM4NA5AtjzF6GtPCbZfafzBck7WF7X8tXyqUZSUmktnUqubNh2wVxZCE5DJMl) — a social commentary article on gender issues in entertainment media.

<details>
<summary>Click to expand full report</summary>

# 文章指紋分析報告

---

## 一、文章概要

| 項目 | 數據 |
|------|------|
| **標題** | 用擦邊未成年、性話題、親密行為來做效果，為什麼以前這樣可以但現在不行？ |
| **總字數** | 2,643 字 |
| **總段落數** | 23 段 |
| **總句數** | 46 句 |
| **推估文類** | 社會評論／媒體素養論說文 |

---

## 二、量化指標摘要

### 2.1 詞彙豐富度

| 指標 | 數值 | 解讀 |
|------|------|------|
| 總詞數（tokens） | 1,544 | — |
| 不重複詞數（types） | 742 | — |
| TTR（Type-Token Ratio） | 0.481 | 中等偏高，詞彙運用有一定多樣性 |
| Hapax Legomena 比率 | 69.5% | 高——近七成詞彙僅出現一次，顯示作者避免重複用語的傾向 |

**高頻實詞 Top 5**：社會（13）、效果（11）、我們（11）、性別（10）、玩笑（9）。這五個詞構成全文的議題骨幹：作者以「社會」為論述場域，以「效果」和「玩笑」為批判對象，以「性別」為核心議題，以「我們」拉近讀者距離。

**功能詞指紋特徵**：「的」使用頻率 77.07‰，遠高於一般口語文體（約 50–60‰），顯示句式偏書面、修飾語較多。「了」14.25‰、「在」13.6‰、「也」9.07‰ 的組合顯示作者頻繁使用遞進與並列句式。

### 2.2 句式節奏特徵

| 指標 | 數值 | 解讀 |
|------|------|------|
| Shannon Entropy | 4.94 | 高——句式長度多變，不單調 |
| 句長變異係數（CV） | 0.545 | 節奏起伏大，長短句交替明顯 |
| 長短句交替分數 | 0.489 | 中等——有意識地交替但並非嚴格韻律 |
| 四字格密度 | 12.1 / 千字 | 偏高——文言四字結構頻繁出現 |
| 氣口平均長度 | 16.6 字（σ=9.6） | 朗讀節奏適中，偶有長氣口（最長 55 字） |

**節奏風格判定**：作者傾向以「長句鋪陳論述 → 短句收束觀點」的節奏推進。

### 2.3 語域特徵

| 指標 | 數值 | 解讀 |
|------|------|------|
| 文白比（文言詞佔比） | 8.78% | 文言色彩偏濃，高於一般網路評論 |
| 成語及四字格密度 | 3.78 / 千字 | 中等，點綴使用 |
| 常用字比例 | 60.7% | — |
| 次常用字比例 | 30.0% | — |
| 罕用字比例 | 9.4% | 低——用字親民，不刻意掉書袋 |

### 2.4 情感弧線

全文情感走向可歸納為 **「波浪式推進」**，整體在正面（分析、期許）與負面（批判、憂慮）之間反覆擺盪。最大轉折點出現在 **段落 4→5**（shift = -1.6）及 **段落 18→19**（shift = -1.667）。

---

## 三、質性分析

### 3.1 引用與典故圖譜

| 段落（行） | 引用內容 | 類型 | 領域 | 時代 |
|------------|---------|------|------|------|
| 段 2（行 3-4） | 黃子佼 #MeToo 事件、統神事件 | 明確引用（時事） | 台灣娛樂圈/網紅文化 | 2023–2024 |
| 段 4（行 8） | 行政院《識讀性別平等與案例分析》報告（2013），第 134 頁 | 明確引用（政府報告） | 性別平等政策 | 2013 |
| 段 7（行 14） | 《人格與社會心理學公刊》Thomas Ford "More Than Just a Joke" | 明確引用（學術論文） | 社會心理學 | 2000s |
| 段 9（行 18） | 「久入鮑肆不聞其臭」 | 化用（古典典故） | 先秦哲學（《孔子家語》） | 先秦 |
| 段 12（行 24） | George Gerbner 涵化理論（Cultivation Theory），1970s | 明確引用（傳播學理論） | 傳播學 | 1970s |
| 段 17（行 34） | 「大陸妹」→「福山萵苣」、「處女蟳」→「幼母蟳」更名運動 | 明確引用（社會運動案例） | 性別語言改革 | 2020s |

**引用跨度**：從先秦（《孔子家語》）到 2024 年時事，橫跨約 2,500 年。

### 3.2 論證結構

**論證角色佔比**：證據 39% ／主張 30% ／讓步 17% ／前提 9% ／總結 4%

結構完整，具備「提問→鋪陳→學理佐證→讓步→收束」的完整迴路。讓步比例達 17%，顯示作者刻意避免單面批判。

### 3.3 修辭手法清單

以「反諷」與「格言式短句」為最突出手法。反諷集中在段 5，是全文情感張力最高點；格言式短句（段 10、16、19、23）則成為全文的記憶錨點。

### 3.4 主題結構與轉折

**主題推進模式**：**問答展開 + 線性推進**。全文以四個小標題為骨架，呈現「提問→原因→機制→立場→行動」的線性邏輯鏈。

---

## 四、文章指紋總結

### 風格標籤

> **社會評論散文 ／ 口語書面交融 ／ 節奏張弛有度 ／ 引用密集-跨領域 ／ 反諷格言型收束**

### 與典型風格的比較定位

| 維度 | 本文定位 | 典型學術論文 | 典型網路評論 |
|------|---------|-------------|-------------|
| 文白比 | 8.8%（偏文） | 5–8% | 2–4% |
| TTR | 0.48 | 0.40–0.50 | 0.35–0.45 |
| 四字格密度 | 12.1‰ | 8–15‰ | 3–8‰ |
| 讓步比例 | 17% | 15–25% | 0–5% |
| 引用密度 | 11 處 / 2643 字 | 高 | 極低 |

</details>

## Skill structure

```
zh-article-analyzer
├── references
│   └── output_schema.md
├── scripts
│   └── zh_analyzer.py
└── SKILL.md
```

## Protocol

This skill follows the [vercel-labs/skills](https://github.com/vercel-labs/skills) protocol.
Each push to `main` triggers a GitHub Action that packages the skill as a `.skill` file
and creates a release tagged with the commit SHA.

## License

MIT License
