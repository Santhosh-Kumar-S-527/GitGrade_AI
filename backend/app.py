from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔐 GitHub API headers (REMOVE token before pushing to GitHub)
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "GitGrade-AI-Hackathon",
    #"Authorization": "token GITHUB_TOKEN_HERE"  //runs without token until rate limit
}

# ---------- Safe GitHub Fetch ----------
def safe_get_json(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


# ---------- Repository Analysis ----------
def analyze_repo(owner, repo):
    score = 0
    roadmap = []

    contents = safe_get_json(f"https://api.github.com/repos/{owner}/{repo}/contents")
    commits = safe_get_json(f"https://api.github.com/repos/{owner}/{repo}/commits")
    languages = safe_get_json(f"https://api.github.com/repos/{owner}/{repo}/languages")

    # Ensure correct data types
    if not isinstance(contents, list):
        contents = []
    if not isinstance(commits, list):
        commits = []
    if not isinstance(languages, dict):
        languages = {}

    # README check
    readme = any(
        isinstance(file, dict) and file.get("name", "").lower() == "readme.md"
        for file in contents
    )
    if readme:
        score += 20
    else:
        roadmap.append("Add a README.md with project overview and setup instructions")

    # Commit consistency
    if len(commits) >= 10:
        score += 20
    else:
        roadmap.append("Commit code more frequently with meaningful commit messages")

    # Language usage
    if len(languages) >= 1:
        score += 15

    # Folder structure
    folders = [
        f.get("name") for f in contents
        if isinstance(f, dict) and f.get("type") == "dir"
    ]
    if "src" in folders or "backend" in folders:
        score += 15
    else:
        roadmap.append("Organize code into proper folders (src, backend, etc.)")

    # Testing
    if "test" in " ".join(folders).lower():
        score += 20
    else:
        roadmap.append("Add unit or integration tests to improve reliability")

    # Summary
    if score > 80:
        summary = "Excellent project structure and clean code. Minor improvements can enhance maintainability."
    elif score > 50:
        summary = "Good project foundation but lacks testing and documentation in some areas."
    else:
        summary = "Basic project setup with major scope for improvement in structure and consistency."

    # 🪞 Recruiter Lens (Unique Feature)
    if score > 80:
        recruiter_view = (
            "A recruiter would view this repository as industry-ready. "
            "Strong structure, consistent commits, and clean practices positively impact the candidate’s profile."
        )
    elif score > 50:
        recruiter_view = (
            "A recruiter would see potential, but missing tests or incomplete documentation may raise concerns."
        )
    else:
        recruiter_view = (
            "From a recruiter’s perspective, this repository may not yet meet industry expectations."
        )

    # Ensure roadmap always exists
    if not roadmap:
        roadmap = [
            "Add CI/CD pipelines using GitHub Actions",
            "Improve inline code documentation",
            "Optimize code for readability and performance",
            "Add contribution guidelines and issue templates"
        ]

    return score, summary, roadmap, recruiter_view


# ---------- API Route ----------
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data or "repo" not in data:
        return jsonify({"error": "GitHub repository URL is required."}), 400

    repo_url = data.get("repo")
    if not repo_url.startswith("https://github.com/"):
        return jsonify({"error": "Invalid GitHub repository URL."}), 400

    try:
        owner, repo = repo_url.replace("https://github.com/", "").split("/")[:2]

        repo_check = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers=HEADERS
        )

        if repo_check.status_code == 403:
            return jsonify({
                "error": "GitHub API rate limit exceeded. Please try again later."
            }), 403

        if repo_check.status_code != 200:
            return jsonify({
                "error": "Repository not found, private, or unavailable."
            }), 404

        score, summary, roadmap, recruiter_view = analyze_repo(owner, repo)

        return jsonify({
            "score": score,
            "summary": summary,
            "recruiter_view": recruiter_view,
            "roadmap": roadmap
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "error": "Failed to analyze repository. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
