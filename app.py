import streamlit as st
import json
from datetime import datetime
from utils.hf_handler import get_ai_feedback, get_solution
import re

def extract_scores(feedback):
    logic = re.search(r'logic.*?(\d+)/10', feedback.lower())
    clarity = re.search(r'clarity.*?(\d+)/10', feedback.lower())
    understanding = re.search(r'understanding.*?(\d+)/10', feedback.lower())

    return {
        "logic": int(logic.group(1)) if logic else None,
        "clarity": int(clarity.group(1)) if clarity else None,
        "understanding": int(understanding.group(1)) if understanding else None
    }
if "history" not in st.session_state:
    st.session_state.history = []

# Load prompt template


# Page settings
st.set_page_config(page_title="AI Reasoning Study Companion")

# Title
st.title("🧠 AI Reasoning Study Companion")
st.write("Improve your thinking, not just answers!")

st.divider()

# Subject selector
subject = st.selectbox(
    "Select Subject",
    ["Math", "Physics", "Programming", "General"]
)

# Input fields
problem = st.text_area("📘 Enter the problem")
reasoning = st.text_area("🧩 Explain your reasoning step-by-step")

# Button
col1, col2 = st.columns(2)

analyze_clicked = col1.button("🔍 Analyze My Thinking")
solution_clicked = col2.button("📘 Show Full Solution")
if analyze_clicked:

    if problem and reasoning:

        with st.spinner("Analyzing your reasoning..."):

            # Create prompt
            prompt = template.format(
                problem=f"[{subject}] {problem}",
                reasoning=reasoning
            )

            # Get AI response
            result = get_ai_feedback(problem,reasoning)
            st.session_state.history.append({
               "problem": problem,
               "reasoning": reasoning,
               "feedback": result
            })
            # 🔥 NEW: Save to history.json permanently
            try:
                import json
                from datetime import datetime

                with open("history.json", "r") as f:
                   data = json.load(f)
            except:
                 data = []

            scores = extract_scores(result)

            data.append({
            
                      "problem": problem,
                      "reasoning": reasoning,
                      "feedback": result,
                      "logic": scores["logic"],
                      "clarity": scores["clarity"],
                      "understanding": scores["understanding"],
                      "time": str(datetime.now())
        })

            with open("history.json", "w") as f:
                    json.dump(data, f, indent=4)

            # Show output
            st.subheader("📊 AI Feedback")
            st.text_area("Result", result, height=300)

    else:
        st.warning("Please fill both fields!")




if solution_clicked:

    if problem:
        with st.spinner("Generating full solution..."):

            solution_prompt = solution_template.format(problem=problem)
            solution = get_solution(problem)

            st.subheader("📘 Step-by-Step Solution")
            st.text_area("Solution", solution, height=300)

    else:
        st.warning("Please enter the problem!")

st.divider()
st.subheader("📜 Recent Attempts")

import json

try:
    with open("history.json", "r") as f:
        data = json.load(f)
except:
    data = []

for item in reversed(data[-5:]):
    st.write("**Problem:**", item["problem"])
    st.write("**Your reasoning:**", item["reasoning"])
    st.write("**AI Feedback:**")
    st.write(item["feedback"])
    st.divider()


# =============================
# 📊 Learning Insights Section
# =============================

st.subheader("📊 Learning Insights")

import json

# Load history safely
try:
    with open("history.json", "r") as f:
        data = json.load(f)
except:
    data = []

total = len(data)
mistake_count = 0
correct_count = 0
concept_errors = 0
logic_errors = 0
calculation_errors = 0

for entry in data:
    feedback = entry["feedback"].lower()

    if "no mistake detected" in feedback or "excellent work" in feedback or "great job" in feedback:
        correct_count += 1

    else:
        mistake_count += 1

        if "concept" in feedback or "understanding" in feedback:
            concept_errors += 1

        if "logic" in feedback:
            logic_errors += 1

        if "calculation" in feedback or "arithmetic" in feedback:
            calculation_errors += 1
if total > 0:
    st.write(f"Total attempts: {total}")
    st.write(f"Mistakes detected: {mistake_count}")
    st.write(f"Correct attempts: {correct_count}")

    # 👇 ADD IT RIGHT HERE
    st.subheader("📌 Mistake Type Analysis")
    st.write(f"Concept mistakes: {concept_errors}")
    st.write(f"Logic mistakes: {logic_errors}")
    st.write(f"Calculation mistakes: {calculation_errors}")

st.subheader("📈 Logic Score Progress")

logic_scores = [item["logic"] for item in data if item.get("logic") is not None]

if len(logic_scores) > 1:
    st.line_chart(logic_scores)
else:
    st.write("Solve more problems to see progress graph.")

