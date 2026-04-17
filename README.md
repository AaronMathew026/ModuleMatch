# ModuleMatch: AI-Powered Course Recommendation Engine

## Overview

ModuleMatch is an intelligent course recommendation system designed for University of Manchester Computer Science students. It helps you discover the perfect modules to match your interests, career goals, and skill level.

Instead of manually reading through 50+ course descriptions, ModuleMatch uses **semantic search** and **large language model judgment** to intelligently recommend modules that align with your learning objectives.

## Problem It Solves

- 📚 **Too many choices:** 50+ CS modules available; hard to find what's right for you
- 🎯 **Unclear prerequisites:** Difficult to understand which modules build on each other
- 🔍 **Hidden connections:** Relevant modules scattered across year groups with no clear linking
- ⏱️ **Time-consuming:** Manual course selection takes hours of reading

## Solution

**Search once. Find everything.** Enter a topic, skill, or interest (e.g., "machine learning", "system design", "game development") and ModuleMatch returns:

1. **Ranked recommendations** — Top modules sorted by relevance
2. **Clear descriptions** — What you'll learn in each module
3. **Prerequisites** — What to study before tackling this module
4. **Difficulty assessment** — Estimated challenge level
5. **Career alignment** — How this module helps your career goals

## Key Features

✨ **Semantic Search** — Understands meaning, not just keywords  
🤖 **LLM-Powered Ranking** — Uses GPT to intelligently rank recommendations  
🎓 **Course Database** — Complete Manchester CS curriculum (60+ modules)  
⚡ **Real-time Recommendations** — Instant results as you type  
📊 **Streamlit Interface** — Clean, intuitive web UI  

## Tech Stack

**Backend:**
- FastAPI (REST API)
- BeautifulSoup (course scraping)
- Ollama Cloud / OpenAI (embeddings & LLM judgment)
- PostgreSQL (course database)

**Frontend:**
- Streamlit (interactive UI)
- Python (data processing)

**Deployment:**
- Railway (backend API)
- Streamlit Cloud (frontend)

## Example Usage

```
User: "I want to learn about artificial intelligence and machine learning"

ModuleMatch returns:
1. COMP34412 - Machine Learning (Year 3, 10 credits) — 98% match
2. COMP34312 - Neural Networks (Year 3, 10 credits) — 95% match
3. COMP24112 - AI & Advanced Topics (Year 2, 10 credits) — 92% match
4. COMP27112 - Intelligent Systems (Year 3, 10 credits) — 89% match

Prerequisites: COMP15111 (Fundamentals of Computation)
Best time to take: Year 3, after completing data science & algorithms
```




## Why This Matters

As a Year 1 CS student, choosing the right modules is **critical** for internship competitiveness. ModuleMatch helps you:

- 🎯 Build a **coherent specialization** (AI, Systems, Web, etc.)
- 📈 **Show intentionality** on your portfolio (strategic module selection)
- ⏱️ **Save hours** on course research
- 🚀 **Launch faster** into specialized internship prep

## License

MIT License — Open source for the university community.

## Author

Aaron Mathew | University of Manchester, Computer Science Year 1
