from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

with open("data/courses.json") as f:
    course_data = json.load(f)

progress_file = "data/progress.json"

if not os.path.exists(progress_file):
    with open(progress_file, "w") as f:
        json.dump({}, f)


def load_progress():
    with open(progress_file) as f:
        return json.load(f)


def save_progress(data):
    with open(progress_file, "w") as f:
        json.dump(data, f)


# ---------- DASHBOARD ----------
@app.route("/")
def index():
    progress = load_progress()
    return render_template("dashboard.html", progress=progress)


@app.route("/dashboard")
def dashboard():
    progress = load_progress()
    return render_template("dashboard.html", progress=progress)


# ---------- GENERATE PAGE ----------
@app.route("/generate-page")
def generate_page():
    goals = list(course_data.keys())
    return render_template("generate.html", goals=goals)


# ---------- PATH + AI RECOMMENDER ----------
@app.route("/generate", methods=["POST"])
def generate():
    user_skills = [s.strip() for s in request.form["skills"].split(",")]
    goal = request.form["goal"]

    required_skills = course_data[goal]["skills"]
    courses = course_data[goal]["courses"]

    # Skill gap detection
    gap_skills = [s for s in required_skills if s not in user_skills]

    # AI course recommendation
    recommendations = [courses[s]["name"] for s in gap_skills]

    # Time prediction
    total_hours = sum(courses[s]["hours"] for s in gap_skills)

    progress = load_progress()
    progress["path"] = gap_skills
    progress["completed"] = []
    progress["hours"] = {s: courses[s]["hours"] for s in gap_skills}
    progress["links"] = {s: courses[s]["link"] for s in gap_skills}
    progress["total_hours"] = total_hours
    progress["recommendations"] = recommendations
    save_progress(progress)

    return render_template(
        "analysis.html",
        goal=goal,
        user_skills=user_skills,
        gap_skills=gap_skills,
        recommendations=recommendations
    )


# ---------- COMPLETE SKILL ----------
@app.route("/complete/<skill>")
def complete(skill):
    progress = load_progress()

    if skill not in progress.get("completed", []):
        progress.setdefault("completed", []).append(skill)

    save_progress(progress)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
