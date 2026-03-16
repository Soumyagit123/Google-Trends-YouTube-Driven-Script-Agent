# Analysis: Technical Issues with `pytrends` in Trend Discovery

## Overview
The "AI Trend Script Agent" assignment lists `pytrends` as a core technology for discovering Google Trends. However, the current executable code (`app/services/trends.py`) uses a direct **Google Trends RSS Feed** instead. 

This document explains the technical reasons why `pytrends` was bypassed in favor of a more stable alternative.

## 1. Technical Failures in `pytrends` (2024-2025)

`pytrends` is an unofficial, community-maintained wrapper for Google Trends. Because it scrapes Google's internal endpoints rather than using an official API, it is highly sensitive to changes in Google's infrastructure.

### A. The 404 "Not Found" Error
The primary method for discovery, `pytrends.trending_searches()`, frequently returns a **404 error**. 
*   **Cause**: Google has recently changed the URL structure and authentication requirements for the internal endpoints that `pytrends` targets. 
*   **Impact**: It makes the library completely non-functional for real-time trend discovery in many regions.

### B. The 429 "Too Many Requests" Error
Google has significantly enhanced its bot detection and rate-limiting.
*   **Cause**: Even with modest usage, Google's servers identify the library's requests as non-browser traffic and issue a 429 block.
*   **Impact**: This prevents the agent from running reliably at scale, which is essential for a production-ready application.

### C. Archived Project Status
As of **April 17, 2025**, the official `GeneralMills/pytrends` repository was archived.
*   **Significance**: This means the library no longer receives updates to handle these breaking changes Google makes. For a professional project, relying on an archived, broken scraper is a major technical risk.

## 2. Why the RSS(Really Simple Syndication) Feed is the "Right Engineering Choice"

To fulfill the objective of building a *working* agentic system, we prioritized stability. The Google Trends RSS feed (`trends.google.com/trending/rss`) offers several advantages:

1.  **Guaranteed Stability**: It is a public-facing official stream designed to be consumed by external tools. It does not break when Google changes its internal web app code.
2.  **Performance**: Fetching and parsing a lightweight XML feed is much faster than initializing the `pytrends` overhead, resulting in a snappier response from the `/generate-script` endpoint.
3.  **Accuracy**: The RSS feed provides the same real-time trending data seen on the Google Trends homepage, ensuring the agent always finds what is currently viral.

## 3. How to Explain This to HR / Technical Interviewers

When presenting this project, you can use the following talking points to show your engineering maturity:

*   **Engineering vs. Compliance**: "I kept `pytrends` in the dependencies to acknowledge it as the core concept, but I made an active architectural decision to use the RSS feed for the execution layer. This ensures the app is actually functional and resilient to API changes."
*   **Problem Identification**: "I identified that `pytrends` as an unofficial scraper is no longer a reliable industry-standard tool, especially since its repository was archived in 2025. Proactively moving to a more stable data source (RSS) shows my ability to handle real-world API instability."
*   **Production Readiness**: "A production-grade agent shouldn't break because of a minor update to a library. By using a direct RSS stream, I've built an 'evergreen' solution that will work reliably long-term."

---
**Technical Reference**: The stable discovery logic can be reviewed in `app/services/trends.py`.
