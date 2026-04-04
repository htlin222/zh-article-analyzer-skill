# 量化分析輸出 Schema

## JSON 結構概覽

```json
{
  "file": "article.txt",

  "module_a_basic_stats": {
    "total_chars": 3200,
    "total_paragraphs": 12,
    "total_sentences": 85,
    "total_lines": 48,
    "paragraph_lengths": {
      "mean": 266.7,
      "std": 89.3,
      "min": 45,
      "max": 520,
      "per_paragraph": [
        {"para": 1, "chars": 180, "lines": "1-3"},
        {"para": 2, "chars": 320, "lines": "5-9"}
      ]
    },
    "sentence_lengths": {
      "mean": 37.6,
      "std": 15.2,
      "cv": 0.4042
    },
    "punctuation": {
      "total": 245,
      "density_per_100_chars": 7.66,
      "distribution": {"，": 98, "。": 72, "、": 35}
    }
  },

  "module_b_lexical_richness": {
    "total_tokens": 1850,
    "total_types": 920,
    "type_token_ratio": 0.4973,
    "hapax_legomena_count": 580,
    "hapax_ratio": 0.6304,
    "top_30_words": [
      {"word": "的", "count": 95, "type": "功能詞", "frequency": 0.0514}
    ],
    "function_word_fingerprint": {
      "的": 51.35, "了": 12.43, "在": 8.11, "是": 15.68
    }
  },

  "module_c_rhythm": {
    "sentence_length_entropy": 3.82,
    "sentence_length_cv": 0.4042,
    "four_char_patterns": {
      "count": 23,
      "density_per_1000_chars": 7.19,
      "items": [
        {"text": "風和日麗", "paragraph": 2, "lines": "5-9"}
      ]
    },
    "breath_unit_stats": {
      "mean": 6.8, "std": 3.2, "min": 2, "max": 18
    },
    "long_short_alternation_score": 0.58,
    "interpretation": {
      "entropy": "高（句式多變）",
      "cv": "節奏起伏中等",
      "alternation": "長短句交替中等"
    }
  },

  "module_d_register": {
    "classical_ratio": {
      "overall": 0.0185,
      "count": 59,
      "interpretation": "略帶文言",
      "by_paragraph": [{"para": 3, "count": 12}]
    },
    "four_char_word_density": {
      "count": 15,
      "density_per_1000_chars": 4.69
    },
    "char_frequency_tiers": {
      "common_ratio": 0.72,
      "mid_ratio": 0.22,
      "rare_ratio": 0.05,
      "extended_ratio": 0.01,
      "interpretation": "用字平易"
    }
  },

  "module_e_sentiment": {
    "paragraph_sentiments": [
      {
        "paragraph": 1,
        "lines": "1-3",
        "positive_hits": 3,
        "negative_hits": 0,
        "sentiment_score": 1.0,
        "label": "正面"
      }
    ],
    "turning_points": [
      {
        "from_paragraph": 4,
        "to_paragraph": 5,
        "shift": -0.667,
        "direction": "正→負"
      }
    ],
    "overall_trend": "前高後低（漸趨負面）"
  }
}
```

## 關鍵指標解讀參考

| 指標 | 低 | 中 | 高 | 意義 |
|------|-----|-----|-----|------|
| TTR | < 0.3 | 0.3-0.5 | > 0.5 | 詞彙越豐富越高 |
| Hapax Ratio | < 0.4 | 0.4-0.6 | > 0.6 | 越高表示用詞越獨特 |
| Sentence Entropy | < 2.5 | 2.5-3.5 | > 3.5 | 越高句式越多變 |
| CV | < 0.3 | 0.3-0.5 | > 0.5 | 越高節奏起伏越大 |
| Alternation Score | < 0.4 | 0.4-0.6 | > 0.6 | 越高長短句交替越頻繁 |
| Classical Ratio | < 0.015 | 0.015-0.03 | > 0.03 | 越高文言色彩越濃 |
| 4-char Density | < 3 | 3-7 | > 7 | 四字格使用頻率 |
