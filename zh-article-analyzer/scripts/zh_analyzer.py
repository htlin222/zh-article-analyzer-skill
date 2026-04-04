#!/usr/bin/env python3
"""
繁體中文文章量化分析器
=======================
對繁體中文文章執行多維度量化分析，輸出 JSON 格式結果。
所有指標附帶行號或段落編號定位。

用法：python3 zh_analyzer.py <文章檔案路徑> [--output json|summary]
"""

import sys
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

try:
    import jieba
    jieba.setLogLevel(20)  # suppress debug logs
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False
    print("警告：jieba 未安裝，將使用基礎分詞。建議執行 pip install jieba --break-system-packages", file=sys.stderr)


# ============================================================
# 常數與詞表
# ============================================================

# 功能詞（虛詞）清單
FUNCTION_WORDS = set("的了在是有不人我他她它們這那個就都也要會可以上到說為和與及"
                     "而且但卻又還已將把被從對於讓給跟所如果雖然因為所以"
                     "然而因此而且並且或者既然即使儘管無論不過只是之其")

# 文言特徵詞
CLASSICAL_MARKERS = set("之乎者也矣焉哉兮夫其若乃則遂既遽豈曷胡奚何"
                        "故且況況且然而然則是以以是於是乃至以至以及"
                        "蓋嘗嘗試須臾俄而俄頃既而已而亦復猶尚且"
                        "莫勿毋弗非未無不若如似猶奈何如何何以所以")

# 基礎情感詞典（正面/負面）
POSITIVE_WORDS = set("好美妙佳優善良愛喜歡快樂幸福希望光明溫暖感動成功勝利"
                     "精彩出色卓越進步成長豐富充實滿足感恩珍惜美好甜蜜"
                     "自由和平安寧寧靜祥和歡欣雀躍振奮鼓舞讚嘆欣賞")

NEGATIVE_WORDS = set("壞醜惡劣差恨厭煩痛苦悲傷絕望黑暗寒冷失敗挫折"
                     "困難危機恐懼擔憂焦慮憤怒悲哀哀傷淒涼孤獨寂寞"
                     "殘酷無情冷漠疲憊崩潰崩壞毀滅災難悲慘")


# ============================================================
# 工具函式
# ============================================================

def read_article(filepath):
    """讀取文章，回傳 (全文, 行列表, 段落列表)"""
    path = Path(filepath)
    for enc in ['utf-8', 'utf-8-sig', 'big5', 'gb18030']:
        try:
            text = path.read_text(encoding=enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        raise ValueError(f"無法讀取檔案 {filepath}，請確認編碼格式")

    lines = text.split('\n')
    # 段落以空行分隔
    paragraphs = []
    current_para = []
    current_start_line = 1
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            if current_para:
                paragraphs.append({
                    'text': '\n'.join(current_para),
                    'start_line': current_start_line,
                    'end_line': i - 1
                })
                current_para = []
            current_start_line = i + 1
        else:
            if not current_para:
                current_start_line = i
            current_para.append(line)
    if current_para:
        paragraphs.append({
            'text': '\n'.join(current_para),
            'start_line': current_start_line,
            'end_line': len(lines)
        })

    return text, lines, paragraphs


def segment(text):
    """分詞"""
    # 移除標點和空白
    clean = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf]', '', text)
    if HAS_JIEBA:
        return list(jieba.cut(clean))
    else:
        # fallback: 逐字切分
        return list(clean)


def extract_sentences(text):
    """以句號、問號、驚嘆號、分號切句"""
    sents = re.split(r'[。！？；\n]+', text)
    return [s.strip() for s in sents if s.strip()]


def count_chars(text):
    """計算中文字元數"""
    return len(re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text))


def shannon_entropy(sequence):
    """計算序列的 Shannon Entropy"""
    if not sequence:
        return 0.0
    counter = Counter(sequence)
    total = len(sequence)
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)
    return round(entropy, 4)


def coefficient_of_variation(values):
    """變異係數 = 標準差 / 平均值"""
    if not values or len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return round(math.sqrt(variance) / mean, 4)


# ============================================================
# 分析模組
# ============================================================

def module_a_basic_stats(text, lines, paragraphs, sentences):
    """模組 A：基礎統計"""
    total_chars = count_chars(text)
    total_paras = len(paragraphs)
    total_sents = len(sentences)

    para_lengths = [count_chars(p['text']) for p in paragraphs]
    sent_lengths = [count_chars(s) for s in sentences]

    # 標點統計
    punctuation_counts = Counter()
    for ch in text:
        if ch in '，。！？、；：「」『』（）—…──""''《》〈〉【】':
            punctuation_counts[ch] += 1
    punct_total = sum(punctuation_counts.values())

    return {
        'total_chars': total_chars,
        'total_paragraphs': total_paras,
        'total_sentences': total_sents,
        'total_lines': len(lines),
        'paragraph_lengths': {
            'mean': round(sum(para_lengths) / max(len(para_lengths), 1), 1),
            'std': round((sum((x - sum(para_lengths)/max(len(para_lengths),1))**2 for x in para_lengths) / max(len(para_lengths)-1, 1))**0.5, 1) if len(para_lengths) > 1 else 0,
            'min': min(para_lengths) if para_lengths else 0,
            'max': max(para_lengths) if para_lengths else 0,
            'per_paragraph': [{'para': i+1, 'chars': l, 'lines': f"{paragraphs[i]['start_line']}-{paragraphs[i]['end_line']}"} for i, l in enumerate(para_lengths)]
        },
        'sentence_lengths': {
            'mean': round(sum(sent_lengths) / max(len(sent_lengths), 1), 1),
            'std': round((sum((x - sum(sent_lengths)/max(len(sent_lengths),1))**2 for x in sent_lengths) / max(len(sent_lengths)-1, 1))**0.5, 1) if len(sent_lengths) > 1 else 0,
            'cv': coefficient_of_variation(sent_lengths),
        },
        'punctuation': {
            'total': punct_total,
            'density_per_100_chars': round(punct_total / max(total_chars, 1) * 100, 2),
            'distribution': dict(punctuation_counts.most_common(15))
        }
    }


def module_b_lexical_richness(text, paragraphs):
    """模組 B：詞彙豐富度"""
    words = segment(text)
    if not words:
        return {'error': '無法分詞，文章可能不含中文字元'}

    total_tokens = len(words)
    types = set(words)
    total_types = len(types)
    ttr = round(total_types / max(total_tokens, 1), 4)

    word_freq = Counter(words)
    hapax = sum(1 for w, c in word_freq.items() if c == 1)
    hapax_ratio = round(hapax / max(total_types, 1), 4)

    # 前 30 高頻詞，標記功能詞/實詞
    top30 = []
    for word, count in word_freq.most_common(30):
        top30.append({
            'word': word,
            'count': count,
            'type': '功能詞' if word in FUNCTION_WORDS or len(word) == 1 and word in FUNCTION_WORDS else '實詞',
            'frequency': round(count / total_tokens, 4)
        })

    # 功能詞指紋向量
    func_fingerprint = {}
    target_func_words = list("的了在是有不就都也要會可以把被而且但卻又還")
    for fw in target_func_words:
        func_fingerprint[fw] = round(word_freq.get(fw, 0) / max(total_tokens, 1) * 1000, 2)  # per 1000 tokens

    return {
        'total_tokens': total_tokens,
        'total_types': total_types,
        'type_token_ratio': ttr,
        'hapax_legomena_count': hapax,
        'hapax_ratio': hapax_ratio,
        'top_30_words': top30,
        'function_word_fingerprint': func_fingerprint
    }


def module_c_rhythm(text, sentences, paragraphs):
    """模組 C：句式節奏分析"""
    sent_lengths = [count_chars(s) for s in sentences]

    # Shannon Entropy of sentence lengths
    entropy = shannon_entropy(sent_lengths)
    cv = coefficient_of_variation(sent_lengths)

    # 四字格偵測（含位置）
    four_char_patterns = []
    for pi, para in enumerate(paragraphs):
        clean = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf]', '', para['text'])
        # 掃描所有可能的四字組合，基於標點分隔的片段
        segments = re.split(r'[，。！？、；：「」『』（）\u2014…\u2500\u2500\u201c\u201d\u2018\u2019《》〈〉【】\s]+', para['text'])
        for seg in segments:
            seg_clean = re.sub(r'[^\u4e00-\u9fff\u3400-\u4dbf]', '', seg)
            if len(seg_clean) == 4:
                four_char_patterns.append({
                    'text': seg_clean,
                    'paragraph': pi + 1,
                    'lines': f"{para['start_line']}-{para['end_line']}"
                })
            elif len(seg_clean) > 4:
                # 檢查是否由多個四字格組成（如八字對偶）
                if len(seg_clean) == 8:
                    four_char_patterns.append({
                        'text': seg_clean[:4],
                        'paragraph': pi + 1,
                        'lines': f"{para['start_line']}-{para['end_line']}"
                    })
                    four_char_patterns.append({
                        'text': seg_clean[4:],
                        'paragraph': pi + 1,
                        'lines': f"{para['start_line']}-{para['end_line']}"
                    })

    total_chars = count_chars(text)
    four_char_density = round(len(four_char_patterns) / max(total_chars, 1) * 1000, 2)

    # 氣口分析（標點間的字數分佈）
    breath_units = []
    for seg in re.split(r'[，。！？、；：\n]+', text):
        c = count_chars(seg)
        if c > 0:
            breath_units.append(c)

    breath_stats = {
        'mean': round(sum(breath_units) / max(len(breath_units), 1), 1),
        'std': round((sum((x - sum(breath_units)/max(len(breath_units),1))**2 for x in breath_units) / max(len(breath_units)-1, 1))**0.5, 1) if len(breath_units) > 1 else 0,
        'min': min(breath_units) if breath_units else 0,
        'max': max(breath_units) if breath_units else 0,
    }

    # 長短句交替偵測
    alternation_score = 0
    if len(sent_lengths) > 1:
        mean_len = sum(sent_lengths) / len(sent_lengths)
        pattern = ['L' if l > mean_len else 'S' for l in sent_lengths]
        transitions = sum(1 for i in range(len(pattern)-1) if pattern[i] != pattern[i+1])
        alternation_score = round(transitions / max(len(pattern)-1, 1), 4)

    return {
        'sentence_length_entropy': entropy,
        'sentence_length_cv': cv,
        'four_char_patterns': {
            'count': len(four_char_patterns),
            'density_per_1000_chars': four_char_density,
            'items': four_char_patterns[:50]  # 最多列出 50 個
        },
        'breath_unit_stats': breath_stats,
        'long_short_alternation_score': alternation_score,
        'interpretation': {
            'entropy': '高（句式多變）' if entropy > 3.5 else '中等' if entropy > 2.5 else '低（句式規律）',
            'cv': '節奏起伏大' if cv > 0.5 else '節奏起伏中等' if cv > 0.3 else '節奏平穩',
            'alternation': '長短句交替頻繁' if alternation_score > 0.6 else '交替中等' if alternation_score > 0.4 else '句長趨同'
        }
    }


def module_d_register(text, paragraphs):
    """模組 D：語域特徵"""
    words = segment(text)
    chars = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]', text)

    # 文言特徵詞偵測
    classical_count = 0
    classical_hits = []
    for pi, para in enumerate(paragraphs):
        para_chars = list(para['text'])
        for ch in para_chars:
            if ch in CLASSICAL_MARKERS:
                classical_count += 1
                classical_hits.append({
                    'char': ch,
                    'paragraph': pi + 1
                })

    total_chars = len(chars)
    classical_ratio = round(classical_count / max(total_chars, 1), 4)

    # 成語偵測（四字格中可能是成語的）— 這裡做粗估
    # 真正的成語偵測需要成語詞典，這裡統計四字詞頻
    four_char_words = [w for w in words if len(w) == 4]
    idiom_density = round(len(four_char_words) / max(total_chars, 1) * 1000, 2)

    # 字頻層級（基於 Unicode 碼位的粗估）
    # 常用字大致在 \u4e00-\u6fff，次常用字 \u7000-\u8fff，罕用字 \u9000+
    common = sum(1 for c in chars if '\u4e00' <= c <= '\u6fff')
    mid = sum(1 for c in chars if '\u7000' <= c <= '\u8fff')
    rare = sum(1 for c in chars if '\u9000' <= c <= '\u9fff')
    ext = sum(1 for c in chars if '\u3400' <= c <= '\u4dbf')

    # 合併統計
    classical_by_para = defaultdict(int)
    for hit in classical_hits:
        classical_by_para[hit['paragraph']] += 1

    return {
        'classical_ratio': {
            'overall': classical_ratio,
            'count': classical_count,
            'interpretation': '文言色彩濃厚' if classical_ratio > 0.03 else '略帶文言' if classical_ratio > 0.015 else '白話為主',
            'by_paragraph': [{'para': p, 'count': c} for p, c in sorted(classical_by_para.items())]
        },
        'four_char_word_density': {
            'count': len(four_char_words),
            'density_per_1000_chars': idiom_density
        },
        'char_frequency_tiers': {
            'common_ratio': round(common / max(total_chars, 1), 4),
            'mid_ratio': round(mid / max(total_chars, 1), 4),
            'rare_ratio': round(rare / max(total_chars, 1), 4),
            'extended_ratio': round(ext / max(total_chars, 1), 4),
            'interpretation': '用字平易' if common / max(total_chars, 1) > 0.7 else '用字中等' if common / max(total_chars, 1) > 0.5 else '用字艱深'
        }
    }


def module_e_sentiment(text, paragraphs):
    """模組 E：段落層級情感弧線"""
    para_sentiments = []

    for pi, para in enumerate(paragraphs):
        pos_count = sum(1 for w in POSITIVE_WORDS if w in para['text'])
        neg_count = sum(1 for w in NEGATIVE_WORDS if w in para['text'])
        total = pos_count + neg_count
        if total == 0:
            score = 0.0
        else:
            score = round((pos_count - neg_count) / total, 3)

        para_sentiments.append({
            'paragraph': pi + 1,
            'lines': f"{para['start_line']}-{para['end_line']}",
            'positive_hits': pos_count,
            'negative_hits': neg_count,
            'sentiment_score': score,  # -1 to 1
            'label': '正面' if score > 0.3 else '負面' if score < -0.3 else '中性'
        })

    # 偵測情感轉折點
    turning_points = []
    scores = [p['sentiment_score'] for p in para_sentiments]
    for i in range(1, len(scores)):
        if abs(scores[i] - scores[i-1]) > 0.4:
            turning_points.append({
                'from_paragraph': i,
                'to_paragraph': i + 1,
                'shift': round(scores[i] - scores[i-1], 3),
                'direction': '正→負' if scores[i] < scores[i-1] else '負→正'
            })

    return {
        'paragraph_sentiments': para_sentiments,
        'turning_points': turning_points,
        'overall_trend': _describe_trend(scores)
    }


def _describe_trend(scores):
    """描述情感趨勢"""
    if not scores:
        return '無資料'
    if len(scores) < 3:
        return '段落過少，無法判斷趨勢'

    first_third = sum(scores[:len(scores)//3]) / max(len(scores)//3, 1)
    last_third = sum(scores[-(len(scores)//3):]) / max(len(scores)//3, 1)

    if last_third > first_third + 0.2:
        return '前低後高（漸趨正面）'
    elif last_third < first_third - 0.2:
        return '前高後低（漸趨負面）'
    else:
        return '整體平穩'


# ============================================================
# 主程式
# ============================================================

def analyze(filepath):
    """執行完整分析"""
    text, lines, paragraphs = read_article(filepath)
    sentences = extract_sentences(text)

    results = {
        'file': str(filepath),
        'module_a_basic_stats': module_a_basic_stats(text, lines, paragraphs, sentences),
        'module_b_lexical_richness': module_b_lexical_richness(text, paragraphs),
        'module_c_rhythm': module_c_rhythm(text, sentences, paragraphs),
        'module_d_register': module_d_register(text, paragraphs),
        'module_e_sentiment': module_e_sentiment(text, paragraphs),
    }

    return results


def main():
    if len(sys.argv) < 2:
        print("用法：python3 zh_analyzer.py <文章檔案路徑>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"錯誤：檔案不存在 {filepath}", file=sys.stderr)
        sys.exit(1)

    results = analyze(filepath)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
