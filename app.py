import streamlit as st
import os
import time

# =========================================================
# TECH MITHRA AI
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# GEMINI SETUP
# =========================================================

try:
    from google import genai
except ImportError:
    st.error("google-genai package is not installed.")
    st.stop()


# =========================================================
# API KEY
# =========================================================

API_KEY = None

try:
    API_KEY = st.secrets.get("GEMINI_API_KEY")
except:
    pass

if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt):

    if not API_KEY:
        return (
            "❌ API Key not found.\n\n"
            "Please add GEMINI_API_KEY in Streamlit Secrets."
        )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        # Current Gemini model
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text

        return "⚠️ AI returned an empty response. Please try again."

    except Exception as e:

        error_text = str(e)

        # Retry with another supported model
        try:

            client = genai.Client(
                api_key=API_KEY
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if response and response.text:
                return response.text

        except Exception as second_error:
            error_text = str(second_error)

        # Friendly error messages

        if "503" in error_text:
            return (
                "⚠️ AI service is temporarily busy.\n\n"
                "Please wait a few seconds and try again."
            )

        if "429" in error_text:
            return (
                "⚠️ Too many requests.\n\n"
                "Please wait for a moment and try again."
            )

        if "401" in error_text or "403" in error_text:
            return (
                "❌ API Key error.\n\n"
                "Please check your GEMINI_API_KEY."
            )

        if "404" in error_text:
            return (
                "❌ Model error.\n\n"
                "Please update the google-genai package."
            )

        return (
            "❌ AI Service Error\n\n"
            f"Details: {error_text}"
        )


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HISTORY FUNCTION
# =========================================================

def save_history(question, answer, section):

    item = {
        "section": section,
        "question": question,
        "answer": answer
    }

    st.session_state.history.append(item)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🤖 Tech Mithra AI")

st.sidebar.markdown("---")

option = st.sidebar.radio(

    "Choose an option",

    [
        "💬 AI Chat",
        "📅 Event Planner",
        "🎓 Exam Helper",
        "🧪 Project & Lab Guide",
        "📚 GATE Preparation",
        "⚙️ Settings"
    ]

)

st.sidebar.markdown("---")

st.sidebar.caption("Tech Mithra AI")


# =========================================================
# TITLE
# =========================================================

st.title("🤖 Tech Mithra AI")

st.caption(
    "Ask Anything • Upload Photo • Camera • Files"
)


# =========================================================
# AI CHAT
# =========================================================

if option == "💬 AI Chat":

    st.subheader("💬 AI Chat")

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # Chat input

    prompt = st.chat_input(
        "Ask anything..."
    )


    # PLUS OPTIONS

    with st.expander("➕ Upload Options"):

        uploaded_photo = st.file_uploader(
            "📷 Upload Photo",
            type=["png", "jpg", "jpeg"]
        )

        camera_photo = st.camera_input(
            "📸 Camera"
        )

        uploaded_file = st.file_uploader(
            "📁 Upload File",
            type=["pdf", "txt", "docx"],
            key="chat_file"
        )


    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )


        with st.chat_message("user"):

            st.markdown(prompt)


        with st.chat_message("assistant"):

            with st.spinner("Tech Mithra AI is thinking..."):

                full_prompt = f"""

You are Tech Mithra AI.

Answer the user's question clearly.

User Question:

{prompt}

Give a useful, simple and detailed answer.

"""

                answer = ask_ai(full_prompt)

                st.markdown(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        save_history(
            prompt,
            answer,
            "AI Chat"
        )


# =========================================================
# EVENT PLANNER
# =========================================================

elif option == "📅 Event Planner":

    st.subheader("📅 Complete Event Planner")

    st.write(
        "Plan your event from starting to ending."
    )


    event_name = st.text_input(
        "Event Name"
    )

    event_type = st.selectbox(

        "Event Type",

        [
            "College Event",
            "Technical Event",
            "Workshop",
            "Seminar",
            "Cultural Event",
            "Birthday Event",
            "Wedding Event",
            "Other"
        ]

    )

    participants = st.number_input(

        "Expected Participants",

        min_value=1,
        value=50

    )

    event_date = st.date_input(
        "Event Date"
    )

    event_place = st.text_input(
        "Event Location"
    )


    if st.button(
        "🚀 Generate Complete Event Plan"
    ):

        if not event_name:

            st.warning(
                "Please enter Event Name."
            )

        else:

            with st.spinner(
                "Creating complete event organization plan..."
            ):

                prompt = f"""

You are a professional Event Organizer.

Create a COMPLETE EVENT PLAN.

Event Name:
{event_name}

Event Type:
{event_type}

Expected Participants:
{participants}

Event Date:
{event_date}

Event Location:
{event_place}

Create the complete plan from STARTING to ENDING.

Include:

1. Event Objective

2. Pre Event Planning

3. Team Formation

4. Roles and Responsibilities

5. Permission Process

6. Event Timeline

7. Venue Planning

8. Equipment Requirements

9. Registration Process

10. Participant Management

11. Guest Management

12. Stage Arrangement

13. Technical Requirements

14. Sound System

15. Projector

16. Internet Requirements

17. Volunteer Management

18. Promotion Plan

19. Social Media Promotion

20. Poster Plan

21. Event Schedule

22. Opening Ceremony

23. Main Activities

24. Break Management

25. Closing Ceremony

26. Feedback Collection

27. Post Event Report

28. Event Checklist

29. Problems that may occur

30. Solutions

Give the answer step by step.

"""

                answer = ask_ai(prompt)

                st.markdown("## 📋 Complete Event Plan")

                st.markdown(answer)

                save_history(
                    event_name,
                    answer,
                    "Event Planner"
                )


# =========================================================
# EXAM HELPER
# =========================================================

elif option == "🎓 Exam Helper":

    st.subheader("🎓 Exam Helper")

    exam_type = st.selectbox(

        "Select Help Type",

        [
            "Question Answer",
            "MCQs",
            "Important Questions",
            "Short Answers",
            "Long Answers",
            "Topic Explanation"
        ]

    )

    subject = st.text_input(
        "Subject Name"
    )

    topic = st.text_input(
        "Topic Name"
    )

    question = st.text_area(
        "Enter your Question or Topic"
    )


    if st.button(
        "🚀 Generate Exam Help"
    ):

        if not question and not topic:

            st.warning(
                "Please enter a Question or Topic."
            )

        else:

            prompt = f"""

You are an expert educational assistant.

Help the student with:

Help Type:
{exam_type}

Subject:
{subject}

Topic:
{topic}

Question:
{question}

Give accurate and easy-to-understand answers.

If MCQs are requested:

Give:

Question
A)
B)
C)
D)

Correct Answer:
Explanation:

"""

            with st.spinner(
                "Preparing your answer..."
            ):

                answer = ask_ai(prompt)

                st.markdown(answer)

                save_history(
                    question or topic,
                    answer,
                    "Exam Helper"
                )


# =========================================================
# PROJECT AND LAB GUIDE
# =========================================================

elif option == "🧪 Project & Lab Guide":

    st.subheader("🧪 Project & Lab Guide")

    guide_type = st.selectbox(

        "Select Type",

        [
            "Project Idea",
            "Mini Project",
            "Major Project",
            "Lab Experiment",
            "Project Documentation",
            "Project Explanation"
        ]

    )

    branch = st.selectbox(

        "Select Branch",

        [
            "CSE",
            "ECE",
            "EEE",
            "MECH",
            "CIVIL",
            "AI & ML",
            "Data Science",
            "Other"
        ]

    )

    project_topic = st.text_input(
        "Enter Project / Lab Topic"
    )


    if st.button(
        "🚀 Generate Guide"
    ):

        if not project_topic:

            st.warning(
                "Please enter a topic."
            )

        else:

            prompt = f"""

You are a professional Engineering Project Guide.

Guide Type:
{guide_type}

Branch:
{branch}

Topic:
{project_topic}

Give a complete guide.

Include:

1. Introduction

2. Objective

3. Required Components

4. Software Requirements

5. Hardware Requirements

6. Working Principle

7. Step by Step Procedure

8. Implementation

9. Block Diagram Explanation

10. Advantages

11. Applications

12. Future Improvements

13. Viva Questions

14. Conclusion

Explain in simple language.

"""

            with st.spinner(
                "Creating project guide..."
            ):

                answer = ask_ai(prompt)

                st.markdown(answer)

                save_history(
                    project_topic,
                    answer,
                    "Project & Lab Guide"
                )


# =========================================================
# GATE PREPARATION
# =========================================================

elif option == "📚 GATE Preparation":

    st.subheader("📚 GATE Preparation")

    st.write(
        "Select Branch → Subject → Topic → Preparation Type"
    )


    # -----------------------------------------------------
    # BRANCH
    # -----------------------------------------------------

    gate_branch = st.selectbox(

        "🎓 Select Branch",

        [
            "CSE",
            "ECE",
            "EEE",
            "ME",
            "CE",
            "AI & Data Science"
        ]

    )


    # -----------------------------------------------------
    # SUBJECT
    # -----------------------------------------------------

    subjects = {

        "CSE": [

            "Engineering Mathematics",
            "Programming and Data Structures",
            "Algorithms",
            "Database Management Systems",
            "Operating Systems",
            "Computer Networks",
            "Theory of Computation",
            "Digital Logic",
            "Computer Organization"
        ],

        "ECE": [

            "Engineering Mathematics",
            "Network Theory",
            "Signals and Systems",
            "Electronic Devices",
            "Analog Circuits",
            "Digital Circuits",
            "Control Systems",
            "Communications",
            "Electromagnetics"
        ],

        "EEE": [

            "Engineering Mathematics",
            "Electric Circuits",
            "Electromagnetic Fields",
            "Signals and Systems",
            "Electrical Machines",
            "Power Systems",
            "Control Systems",
            "Electrical Measurements",
            "Power Electronics"
        ],

        "ME": [

            "Engineering Mathematics",
            "Engineering Mechanics",
            "Strength of Materials",
            "Theory of Machines",
            "Thermodynamics",
            "Fluid Mechanics",
            "Heat Transfer",
            "Manufacturing Engineering"
        ],

        "CE": [

            "Engineering Mathematics",
            "Engineering Mechanics",
            "Strength of Materials",
            "Structural Analysis",
            "Geotechnical Engineering",
            "Fluid Mechanics",
            "Transportation Engineering",
            "Environmental Engineering"
        ],

        "AI & Data Science": [

            "Engineering Mathematics",
            "Programming",
            "Data Structures",
            "Machine Learning",
            "Artificial Intelligence",
            "Probability",
            "Statistics",
            "Database Systems"
        ]

    }


    gate_subject = st.selectbox(

        "📖 Select Subject",

        subjects[gate_branch]

    )


    # -----------------------------------------------------
    # TOPIC
    # -----------------------------------------------------

    gate_topic = st.text_input(
        "📝 Enter Topic"
    )


    # -----------------------------------------------------
    # PREPARATION TYPE
    # -----------------------------------------------------

    preparation_type = st.selectbox(

        "🎯 Preparation Type",

        [
            "📅 Study Plan",
            "❓ Important Questions",
            "📝 MCQs",
            "📄 Previous Papers",
            "📚 Topic Explanation"
        ]

    )


    # -----------------------------------------------------
    # STUDY PLAN
    # -----------------------------------------------------

    if preparation_type == "📅 Study Plan":

        study_days = st.selectbox(

            "Select Study Duration",

            [
                "7 Days",
                "15 Days",
                "30 Days",
                "60 Days",
                "90 Days"
            ]

        )


    # -----------------------------------------------------
    # MCQ COUNT
    # -----------------------------------------------------

    if preparation_type == "📝 MCQs":

        mcq_count = st.selectbox(

            "Number of MCQs",

            [
                5,
                10,
                15,
                20
            ]

        )


    if st.button(
        "🚀 Generate GATE Preparation"
    ):

        if not gate_topic:

            st.warning(
                "Please enter a Topic."
            )

        else:

            # =============================================
            # STUDY PLAN
            # =============================================

            if preparation_type == "📅 Study Plan":

                prompt = f"""

You are an expert GATE preparation mentor.

Branch:
{gate_branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Create a {study_days} GATE preparation study plan.

Include:

1. Daily Schedule

2. Concepts to Study

3. Important Formulas

4. Practice Questions

5. Revision Plan

6. Mock Test Plan

7. Time Management Tips

8. Important Topics

Give a clear day-wise plan.

"""


            # =============================================
            # IMPORTANT QUESTIONS
            # =============================================

            elif preparation_type == "❓ Important Questions":

                prompt = f"""

You are a GATE examination expert.

Branch:
{gate_branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Generate important GATE questions.

Include:

1. Conceptual Questions

2. Numerical Questions

3. Frequently Asked Questions

4. High Priority Questions

Give answers and explanations.

"""


            # =============================================
            # MCQS
            # =============================================

            elif preparation_type == "📝 MCQs":

                prompt = f"""

You are a GATE examination expert.

Branch:
{gate_branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Generate {mcq_count} GATE style MCQs.

For every question use this format:

Question:

A)

B)

C)

D)

Correct Answer:

Explanation:

Make the questions educational and relevant.

"""


            # =============================================
            # PREVIOUS PAPERS
            # =============================================

            elif preparation_type == "📄 Previous Papers":

                prompt = f"""

You are a GATE preparation mentor.

Branch:
{gate_branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Give a previous-paper-oriented preparation guide.

Include:

1. Common question patterns

2. Frequently tested concepts

3. Important numerical problem types

4. Previous exam style questions

5. Difficulty level

6. Solutions and explanations

Clearly mention that practice questions are representative
unless exact official previous questions are provided by the user.

"""


            # =============================================
            # TOPIC EXPLANATION
            # =============================================

            elif preparation_type == "📚 Topic Explanation":

                prompt = f"""

You are an expert GATE teacher.

Branch:
{gate_branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Explain the topic completely.

Include:

1. Introduction

2. Basic Concepts

3. Important Definitions

4. Formulas

5. Step by Step Explanation

6. Examples

7. Numerical Examples

8. Important Points

9. Common Mistakes

10. GATE Exam Tips

Explain in simple student-friendly language.

"""


            # =============================================
            # GENERATE
            # =============================================

            with st.spinner(
                "Creating GATE preparation content..."
            ):

                answer = ask_ai(prompt)

                st.markdown(
                    f"## {preparation_type}"
                )

                st.markdown(answer)

                save_history(

                    f"{gate_branch} | {gate_subject} | {gate_topic}",

                    answer,

                    "GATE Preparation"

                )


# =========================================================
# SETTINGS
# =========================================================

elif option == "⚙️ Settings":

    st.subheader("⚙️ Settings")


    # =====================================================
    # AI SETTINGS
    # =====================================================

    st.markdown("## 🤖 AI Settings")

    language = st.selectbox(

        "🌐 Response Language",

        [
            "English",
            "Telugu",
            "Telugu + English"
        ]

    )

    st.success(
        f"Selected Language: {language}"
    )


    # =====================================================
    # HISTORY
    # =====================================================

    st.markdown("---")

    st.markdown("## 📜 History")

    if len(st.session_state.history) == 0:

        st.info(
            "No history available."
        )

    else:

        for index, item in enumerate(
            reversed(st.session_state.history)
        ):

            with st.expander(

                f"{item['section']} — {item['question'][:60]}"

            ):

                st.markdown(
                    f"### Question\n{item['question']}"
                )

                st.markdown(
                    f"### Answer\n{item['answer']}"
                )


    if st.button(
        "🗑️ Clear History"
    ):

        st.session_state.history = []

        st.success(
            "History cleared successfully."
        )

        time.sleep(1)

        st.rerun()


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    st.markdown("---")

    st.markdown("## 💬 Chat Settings")

    if st.button(
        "🗑️ Clear AI Chat"
    ):

        st.session_state.messages = []

        st.success(
            "Chat cleared successfully."
        )


    # =====================================================
    # APP INFORMATION
    # =====================================================

    st.markdown("---")

    st.markdown("## ℹ️ App Information")

    st.write(
        "🤖 App Name: Tech Mithra AI"
    )

    st.write(
        "📚 Features:"
    )

    st.write(
        """
• AI Chat

• Event Planner

• Exam Helper

• Project & Lab Guide

• GATE Preparation

• History

• Settings
"""
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🤖 Tech Mithra AI • Your AI Learning Assistant"
)
