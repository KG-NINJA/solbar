# 🤖 Actionable Problem Automation

This tool extracts real-world friction and software-solvable problems from daily news articles.

## 📋 Features
- Fetches latest tech and business news from RSS feeds (TechCrunch, Wired, NYT Tech).
- Formats problems according to the specified objective-driven layout.
- Maintains a persistent `problem_log.md` with daily entries.
- (Optional) AI integration via OpenAI GPT-4o for fully automated extraction.

## 🛠️ Setup (GitHub Actions - 100% Automated)
To have this run every day automatically for free, you can use a GitHub Action:

1. Create a file in your repository: `.github/workflows/daily_log.yml`
2. Paste the following content:

```yaml
name: Daily Problem Log Update
on:
  schedule:
    - cron: '0 0 * * *' # Runs every day at midnight UTC
  workflow_dispatch: # Allows manual trigger

jobs:
  update_log:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install feedparser requests beautifulsoup4
      - name: Run extractor
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python automate_problem_extraction.py
      - name: Commit and Push
        run: |
          git config --global user.name "LogBot"
          git config --global user.email "bot@example.com"
          git add problem_log.md
          git commit -m "Update Daily Problem Log: $(date)"
          git push
```

3. **Important:** Add your `OPENAI_API_KEY` to your repository's **Settings > Secrets and variables > Actions**.

## 🚀 Manual Run
To run the extractor manually:
```bash
export OPENAI_API_KEY="your-key-here"
python automate_problem_extraction.py
```

If no API key is provided, the script will still generate placeholders in the log for manual completion.
