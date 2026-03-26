import feedparser
import os
import requests
import random
from datetime import datetime

# Configuration
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
]
LOG_FILE = "problem_log.md"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
# === MISSION ===
Extract actionable problems from news articles.

# === OBJECTIVE ===
- Identify real-world friction, inefficiencies, or unmet needs
- Focus on problems that can be solved with software or AI

# === INPUT ===
News article text

# === OUTPUT FORMAT ===

## 📰 News Summary
(2-3 lines)

## 🎯 Core Problem
(what is actually broken)

## 👤 Affected Users
(who is suffering)

## 💥 Pain Point
(why it matters)

## 🔍 Hidden Opportunity
(not obvious insight)

## 💡 Solution Direction
(practical idea)

## 💰 Monetization Idea
(how to make money)

## ⚡ Urgency Score
(1-10)

---

# === RULES ===

- Avoid surface-level summaries
- Focus on underlying structural problems
- Must include monetization
- Prefer problems that can be automated
"""

def fetch_news():
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary if hasattr(entry, 'summary') else ""
            })
    return articles

def generate_problem_report(article):
    """
    Calls OpenAI API to analyze the article and extract the problem.
    If no API key is found, returns a template for manual entry.
    """
    if not OPENAI_API_KEY:
        return f"""
## 📰 News Summary
(Source: {article['title']})
{article['summary'][:200]}...

> ⚠️ [Action Required] Set OPENAI_API_KEY to automate this extraction.

## 🎯 Core Problem
[Manual Entry Required]

## 👤 Affected Users
[Manual Entry Required]

## 💥 Pain Point
[Manual Entry Required]

## 🔍 Hidden Opportunity
[Manual Entry Required]

## 💡 Solution Direction
[Manual Entry Required]

## 💰 Monetization Idea
[Manual Entry Required]

## ⚡ Urgency Score
(Scale 1-10)

---
"""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-4o",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Title: {article['title']}\nSummary: {article['summary']}"}
                ]
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"\n> ❌ Error processing {article['title']}: {str(e)}\n"

def main():
    print(f"[{datetime.now()}] Starting automated extraction...")
    articles = fetch_news()

    # Shuffle for variety across different sources
    random.shuffle(articles)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("# 🚀 Actionable Problem Log\n\n")

    with open(LOG_FILE, "a") as f:
        f.write(f"\n# Log Entry: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        # We process the top 3 most recent articles
        for article in articles[:3]:
            print(f"Processing: {article['title']}")
            report = generate_problem_report(article)
            f.write(report + "\n")

    print(f"[{datetime.now()}] Log updated in {LOG_FILE}")

if __name__ == "__main__":
    main()
