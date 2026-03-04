from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

_HIGH_IMPACT = {
    "zero-day","zero day","ransomware","critical","nation-state","data breach",
    "exploit","attack","vulnerability","breach","malware","apt","trojan","backdoor",
    "infrastructure","emergency","leaked","compromised","stolen","hacked",
}
_MED_IMPACT = {
    "patch","update","advisory","warning","threat","risk","exposure","disclosure",
    "regulation","compliance","sanctions","ban","policy","fine","lawsuit",
}


def score_sentiment(text: str) -> float:
    if not text:
        return 0.0
    return round(_analyzer.polarity_scores(text)["compound"], 4)


def score_impact(title: str, text: str = "", tags: list[str] | None = None) -> float:
    combined = (title + " " + (text or "") + " " + " ".join(tags or [])).lower()
    score = 0.0
    for kw in _HIGH_IMPACT:
        if kw in combined:
            score += 2.5
    for kw in _MED_IMPACT:
        if kw in combined:
            score += 1.0
    return round(min(score, 10.0), 2)
