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
