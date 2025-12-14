# GitGrade AI
### Intelligent GitHub Repository Analyzer with a Recruiter’s Perspective

---

## Problem Statement

In today’s tech hiring landscape, a GitHub repository represents a developer’s real-world skills.
However, many students are unsure how their repositories appear to recruiters and mentors.

GitGrade AI addresses this gap by analyzing a public GitHub repository and converting it into a
score, meaningful feedback, and a personalized improvement roadmap, helping developers become
more industry-ready.

---

## Solution Overview

GitGrade AI accepts a public GitHub repository URL and automatically evaluates it across multiple
dimensions such as structure, commit consistency, documentation, and testing practices.

The system then generates:
- A quantitative repository score
- A concise AI-style summary
- A Recruiter Lens showing how hiring managers perceive the repository
- A Confidence Meter indicating developer readiness
- A personalized roadmap with actionable improvement steps

This approach acts as a “repository mirror,” reflecting strengths, gaps, and next steps clearly.

---

## Key Features

- Repository Scoring (0–100)
- AI-style project summary
- Recruiter Lens – industry-facing evaluation
- Confidence Meter for developer readiness
- Personalized improvement roadmap
- Defensive handling of GitHub API limits and failures

---

## How It Works

1. User enters a public GitHub repository URL
2. Backend fetches repository data using GitHub REST APIs
3. Repository is evaluated using rule-based and heuristic analysis
4. Score, summary, recruiter insights, and roadmap are generated
5. Results are displayed through an interactive frontend

---

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Flask
- Flask-CORS

APIs:
- GitHub REST API

---

## How to Run Locally

### Prerequisites
- Python 3.x
- Git

### Steps

bash
-pip install flask flask-cors requests
-python backend/app.py

- Open `index.html` in your browser
- Enter a public GitHub repository URL
- Click Analyze


###  Demo Video

Demo Recording:
https://drive.google.com/file/d/1qspRUjuRnXUZxv2bzF8FiPo5TagNALJW/view?usp=drive_link

---

## AI & Intelligence Approach

GitGrade AI follows a hybrid intelligence model combining deterministic rule-based repository
analysis with AI-inspired mentor-style feedback generation. This approach ensures accuracy,
explainability, and reliability without overdependence on external AI APIs.

---

## Conclusion

GitGrade AI transforms raw GitHub repository data into clear, actionable insights that help students
understand their standing from a recruiter’s perspective and take focused steps toward industry
readiness.
