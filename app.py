import streamlit as st
import requests
import json
import os
import base64
import time
from datetime import datetime
import streamlit.components.v1 as components


# ============================================================
# TECH MITHRA AI
# Complete Streamlit Application
# ============================================================


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 1.5rem;
}

.tech-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 5px;
}

.tech-subtitle {
    color: #9ca3af;
    font-size: 17px;
    margin-bottom: 25px;
}

.chat-user {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0px;
}

.chat-ai {
    background-color: #111827;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0px;
}

.option-card {
    padding: 15px;
    border-radius: 12px;
    background-color: #161b22;
    border: 1px solid #30363d;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# FILES
# ------------------------------------------------------------

HISTORY_FILE = "techmithra_history.json"
SETTINGS_FILE = "techmithra_settings.json"


# ------------------------------------------------------------
# DEFAULT SETTINGS
# ------------------------------------------------------------

DEFAULT_SETTINGS = {
    "language": "English",
    "auto_save_history": True
}


# ------------------------------------------------------------
# LOAD SETTINGS
# ------------------------------------------------------------

def load_settings():

    if os.path.exists(SETTINGS_FILE):

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except:
            return DEFAULT_SETTINGS.copy()

    return DEFAULT_SETTINGS.copy()


# ------------------------------------------------------------
# SAVE SETTINGS
# ------------------------------------------------------------

def save_settings(settings):

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:

        json.dump(
            settings,
            file,
            ensure_ascii=False,
            indent=4
        )


# ------------------------------------------------------------
# LOAD HISTORY
# ------------------------------------------------------------

def load_history():

    if os.path.exists(HISTORY_FILE):

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except:

            return []

    return []


# ------------------------------------------------------------
# SAVE HISTORY
# ------------------------------------------------------------

def save_history(history):

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4
            )

    except:
        pass


# ------------------------------------------------------------
# INITIALIZE SESSION STATE
# ------------------------------------------------------------

if "settings" not in st.session_state:

    st.session_state.settings = load_settings()


if "history" not in st.session_state:

    st.session_state.history = load_history()


if "messages" not in st.session_state:

    st.session_state.messages = []


if "last_response" not in st.session_state:

    st.session_state.last_response = ""


if "selected_page" not in st.session_state:

    st.session_state.selected_page = "💬 AI Chat"


# ------------------------------------------------------------
# GET GEMINI API KEY
# ------------------------------------------------------------

def get_api_key():

    api_key = None

    try:

        if "GEMINI_API_KEY" in st.secrets:

            api_key = st.secrets["GEMINI_API_KEY"]

    except:
        pass

    if not api_key:

        api_key = os.getenv("GEMINI_API_KEY")

    return api_key


# ------------------------------------------------------------
# GET AVAILABLE GEMINI MODELS AUTOMATICALLY
# No hardcoded old model names
# ------------------------------------------------------------

def get_available_model(api_key):

    try:

        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models"
        )

        response = requests.get(
            url,
            params={
                "key": api_key
            },
            timeout=20
        )

        data = response.json()

        if "models" not in data:

            return None

        models = data["models"]

        preferred_names = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash"
        ]

        available = []

        for model in models:

            name = model.get("name", "")

            methods = model.get(
                "supportedGenerationMethods",
                []
            )

            if "generateContent" in methods:

                clean_name = name.replace(
                    "models/",
                    ""
                )

                available.append(clean_name)

        for preferred in preferred_names:

            if preferred in available:

                return preferred

        if len(available) > 0:

            return available[0]

        return None

    except:

        return None


# ------------------------------------------------------------
# READ TEXT FILE
# ------------------------------------------------------------

def read_uploaded_text(uploaded_file):

    try:

        content = uploaded_file.read()

        try:

            return content.decode("utf-8")

        except:

            return str(content)

    except:

        return ""


# ------------------------------------------------------------
# CREATE GEMINI PART
# ------------------------------------------------------------

def create_file_part(uploaded_file):

    try:

        file_bytes = uploaded_file.getvalue()

        encoded_data = base64.b64encode(
            file_bytes
        ).decode("utf-8")

        mime_type = uploaded_file.type

        if not mime_type:

            mime_type = (
                "application/octet-stream"
            )

        return {

            "inline_data": {

                "mime_type": mime_type,

                "data": encoded_data

            }

        }

    except:

        return None


# ------------------------------------------------------------
# GEMINI AI REQUEST
# Automatic Model Detection + Retry
# ------------------------------------------------------------

def ask_ai(
    prompt,
    uploaded_files=None
):

    api_key = get_api_key()

    if not api_key:

        return (
            "❌ Gemini API Key not found.\n\n"
            "Please add GEMINI_API_KEY in "
            "Streamlit Secrets."
        )

    model = get_available_model(api_key)

    if not model:

        return (
            "❌ Unable to find an available Gemini model.\n\n"
            "Please check:\n"
            "1. Your API Key\n"
            "2. Internet connection\n"
            "3. Gemini API access"
        )

    language = st.session_state.settings.get(
        "language",
        "English"
    )

    system_instruction = f"""

You are Tech Mithra AI.

You are a helpful AI assistant for students.

Answer clearly and accurately.

Selected response language:
{language}

Rules:

- Explain step by step when needed.
- Use simple language.
- Help students with Engineering,
  GATE, exams, projects and labs.
- For MCQs provide the correct answer
  and explanation.
- For planning provide practical
  step-by-step guidance.
- Do not unnecessarily mention
  internal model errors.
"""

    final_prompt = (
        system_instruction
        + "\n\nUSER QUESTION:\n"
        + prompt
    )

    parts = [

        {
            "text": final_prompt
        }

    ]

    if uploaded_files:

        for uploaded_file in uploaded_files:

            if uploaded_file:

                file_part = create_file_part(
                    uploaded_file
                )

                if file_part:

                    parts.append(file_part)

    request_data = {

        "contents": [

            {

                "parts": parts

            }

        ],

        "generationConfig": {

            "temperature": 0.7,

            "maxOutputTokens": 4096

        }

    }

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        + model
        + ":generateContent"
    )

    # Retry for temporary server errors

    for attempt in range(3):

        try:

            response = requests.post(

                url,

                params={
                    "key": api_key
                },

                json=request_data,

                timeout=60

            )

            data = response.json()

            if response.status_code == 200:

                candidates = data.get(
                    "candidates",
                    []
                )

                if candidates:

                    content = candidates[0].get(
                        "content",
                        {}
                    )

                    response_parts = content.get(
                        "parts",
                        []
                    )

                    answer = ""

                    for part in response_parts:

                        if "text" in part:

                            answer += part["text"]

                    if answer.strip():

                        return answer

                return (
                    "⚠️ AI generated an empty response. "
                    "Please try again."
                )

            # Temporary server error

            if response.status_code in [429, 500, 502, 503]:

                if attempt < 2:

                    time.sleep(2 * (attempt + 1))

                    continue

                return (
                    "⚠️ The AI service is temporarily busy.\n\n"
                    "Please wait for a moment and try again."
                )

            error_message = (
                data.get(
                    "error",
                    {}
                ).get(
                    "message",
                    "Unknown API Error"
                )
            )

            return (
                "❌ AI service error:\n\n"
                + error_message
            )

        except requests.exceptions.Timeout:

            if attempt < 2:

                time.sleep(2)

                continue

            return (
                "⚠️ Request timed out.\n\n"
                "Please check your internet connection "
                "and try again."
            )

        except Exception:

            if attempt < 2:

                time.sleep(2)

                continue

            return (
                "⚠️ Unable to connect to the AI service.\n\n"
                "Please try again."
            )

    return (
        "⚠️ Unable to generate a response. "
        "Please try again."
    )


# ------------------------------------------------------------
# SAVE CHAT HISTORY
# ------------------------------------------------------------

def add_to_history(
    question,
    answer,
    category
):

    if not st.session_state.settings.get(
        "auto_save_history",
        True
    ):

        return

    history_item = {

        "time": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        ),

        "category": category,

        "question": question,

        "answer": answer

    }

    st.session_state.history.insert(
        0,
        history_item
    )

    save_history(
        st.session_state.history
    )


# ------------------------------------------------------------
# VOICE PLAYER
# Play Pause Resume Stop
# ------------------------------------------------------------

def voice_player(text):

    safe_text = json.dumps(text)

    components.html(

        f"""

        <div style="
        padding:10px;
        font-family:Arial;
        ">

        <button onclick="playVoice()">
        🔊 Play
        </button>

        <button onclick="pauseVoice()">
        ⏸ Pause
        </button>

        <button onclick="resumeVoice()">
        ▶ Resume
        </button>

        <button onclick="stopVoice()">
        ⏹ Stop
        </button>

        </div>

        <script>

        const message =
        new SpeechSynthesisUtterance(
        {safe_text}
        );

        message.rate = 1;

        function playVoice() {{

            window.speechSynthesis.cancel();

            window.speechSynthesis.speak(
            message
            );

        }}

        function pauseVoice() {{

            window.speechSynthesis.pause();

        }}

        function resumeVoice() {{

            window.speechSynthesis.resume();

        }}

        function stopVoice() {{

            window.speechSynthesis.cancel();

        }}

        </script>

        """,

        height=70

    )


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.caption(
        "Your AI Study Assistant"
    )

    st.divider()

    options = [

        "💬 AI Chat",

        "📅 Event Planner",

        "📚 Exam Helper",

        "🔬 Project & Lab Guide",

        "🎓 GATE Preparation",

        "⚙️ Settings"

    ]

    selected_option = st.radio(

        "Navigation",

        options,

        index=options.index(
            st.session_state.selected_page
        )

        if st.session_state.selected_page
        in options

        else 0

    )

    st.session_state.selected_page = (
        selected_option
    )

    st.divider()

    st.subheader("📎 Upload")

    upload_photo = st.file_uploader(

        "Upload Photo",

        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],

        key="photo_upload"

    )

    camera_photo = st.camera_input(

        "Camera",

        key="camera_upload"

    )

    upload_file = st.file_uploader(

        "Upload File",

        type=[
            "pdf",
            "txt",
            "docx",
            "jpg",
            "jpeg",
            "png"
        ],

        key="file_upload"

    )

    st.divider()

    st.subheader("🎤 Voice Input")

    try:

        voice_input = st.audio_input(
            "Record your voice"
        )

    except:

        voice_input = None

        st.caption(
            "Voice recording requires "
            "a newer Streamlit version."
        )


# ------------------------------------------------------------
# APP HEADER
# ------------------------------------------------------------

st.markdown(
    '<div class="tech-title">💬 Tech Mithra AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tech-subtitle">'
    'Ask Anything • Upload Photo • Camera • Files'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# AI CHAT
# ============================================================

if selected_option == "💬 AI Chat":

    st.subheader("💬 AI Chat")

    # Show messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # Upload files list

    attachments = []

    if upload_photo:

        attachments.append(
            upload_photo
        )

    if camera_photo:

        attachments.append(
            camera_photo
        )

    if upload_file:

        attachments.append(
            upload_file
        )

    # Chat Input

    user_prompt = st.chat_input(
        "Ask anything..."
    )

    if user_prompt:

        st.session_state.messages.append(

            {

                "role": "user",

                "content": user_prompt

            }

        )

        with st.chat_message("user"):

            st.markdown(
                user_prompt
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "Tech Mithra AI is thinking..."
            ):

                answer = ask_ai(

                    user_prompt,

                    attachments

                )

            st.markdown(answer)

        st.session_state.messages.append(

            {

                "role": "assistant",

                "content": answer

            }

        )

        st.session_state.last_response = (
            answer
        )

        add_to_history(

            user_prompt,

            answer,

            "AI Chat"

        )

    # Voice Input

    if voice_input:

        st.info(
            "🎤 Voice recording received. "
            "You can ask AI to analyze the audio."
        )

        if st.button(
            "🤖 Analyze Voice",
            key="analyze_voice"
        ):

            with st.spinner(
                "Analyzing voice..."
            ):

                answer = ask_ai(

                    "Please listen to this audio "
                    "and answer the user's question.",

                    [voice_input]

                )

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "Voice Question",

                answer,

                "AI Voice"

            )

    # Voice response

    if st.session_state.last_response:

        st.divider()

        st.subheader(
            "🔊 AI Voice"
        )

        voice_player(
            st.session_state.last_response
        )


# ============================================================
# EVENT PLANNER
# Complete Event Organization
# Starting to Ending
# ============================================================

elif selected_option == "📅 Event Planner":

    st.header(
        "📅 Complete Event Planner"
    )

    st.write(
        """
Plan your event from the beginning
to the final completion.
"""
    )

    event_name = st.text_input(
        "Event Name",
        placeholder=
        "Example: College Technical Fest"
    )

    event_type = st.selectbox(

        "Event Type",

        [

            "College Event",

            "Technical Event",

            "Cultural Event",

            "Workshop",

            "Seminar",

            "Conference",

            "Fest",

            "Birthday",

            "Wedding",

            "Sports Event",

            "Other"

        ]

    )

    event_goal = st.text_area(

        "Event Goal / Purpose",

        placeholder=
        "What is the main purpose of this event?"

    )

    event_date = st.text_input(
        "Event Date / Duration"
    )

    expected_people = st.text_input(
        "Expected Participants / Guests"
    )

    venue = st.text_input(
        "Venue / Location"
    )

    organizers = st.text_input(
        "Number of Organizers / Team Members"
    )

    special_requirements = st.text_area(

        "Special Requirements",

        placeholder=
        "Guests, certificates, stage, food, "
        "registration, sponsors, etc."

    )

    if st.button(

        "📋 Generate Complete Event Plan",

        use_container_width=True

    ):

        if not event_name:

            st.warning(
                "Please enter Event Name."
            )

        else:

            event_prompt = f"""

Create a COMPLETE EVENT ORGANIZATION PLAN.

Event Details:

Event Name:
{event_name}

Event Type:
{event_type}

Purpose:
{event_goal}

Date / Duration:
{event_date}

Expected Participants:
{expected_people}

Venue:
{venue}

Organizing Team:
{organizers}

Special Requirements:
{special_requirements}


IMPORTANT:

Do not give only a budget.

Create a COMPLETE EVENT PLAN
from STARTING to ENDING.

Use the following structure:


1. EVENT OVERVIEW

2. EVENT OBJECTIVES

3. PRE-EVENT PLANNING

4. ORGANIZING TEAM STRUCTURE

Include roles such as:

- Event Head
- Coordinator
- Registration Team
- Technical Team
- Stage Team
- Hospitality Team
- Marketing Team
- Photography Team
- Volunteer Team


5. STEP-BY-STEP TIMELINE

Include:

- One Month Before
- Two Weeks Before
- One Week Before
- Three Days Before
- One Day Before


6. REGISTRATION PLAN

7. PROMOTION AND MARKETING PLAN

8. VENUE ARRANGEMENT

9. EQUIPMENT REQUIREMENTS

10. GUEST MANAGEMENT

11. PARTICIPANT MANAGEMENT

12. EVENT DAY COMPLETE SCHEDULE

Give a detailed timeline from:

- Organizers arrival
- Registration
- Welcome
- Event opening
- Main activities
- Breaks
- Guest sessions
- Prize distribution
- Closing ceremony


13. TEAM RESPONSIBILITIES

14. COMMUNICATION PLAN

15. RISK MANAGEMENT

16. BACKUP PLAN

17. POST-EVENT ACTIVITIES

Include:

- Feedback
- Certificates
- Photos and videos
- Reports
- Social media posts
- Thank you messages


18. COMPLETE CHECKLIST

19. OPTIONAL BUDGET ESTIMATE

Budget should be optional.

The main focus must be COMPLETE
EVENT ORGANIZATION FROM START TO FINISH.

Make the answer practical,
clear and easy to follow.

"""

            with st.spinner(
                "Creating complete event plan..."
            ):

                answer = ask_ai(
                    event_prompt
                )

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "Event Plan: "
                + event_name,

                answer,

                "Event Planner"

            )

            st.subheader(
                "🔊 Listen to Event Plan"
            )

            voice_player(answer)


# ============================================================
# EXAM HELPER
# ============================================================

elif selected_option == "📚 Exam Helper":

    st.header("📚 Exam Helper")

    exam_tab1, exam_tab2, exam_tab3 = st.tabs(

        [

            "✍️ Answer Generator",

            "❓ MCQ Generator",

            "📝 Answer Explanation"

        ]

    )


    # --------------------------------------------------------
    # ANSWER GENERATOR
    # --------------------------------------------------------

    with exam_tab1:

        st.subheader(
            "✍️ Generate Exam Answer"
        )

        subject = st.text_input(
            "Subject Name",
            key="exam_subject"
        )

        question = st.text_area(
            "Enter Question",
            key="exam_question"
        )

        marks = st.selectbox(

            "Answer Type",

            [

                "2 Marks",

                "5 Marks",

                "10 Marks",

                "Long Answer"

            ]

        )

        if st.button(
            "Generate Answer",
            key="generate_exam_answer"
        ):

            if question:

                prompt = f"""

Subject:
{subject}

Question:
{question}

Answer Type:
{marks}

Write an accurate student-friendly answer.

Use:

- Definition
- Explanation
- Important Points
- Examples where required
- Conclusion if needed

Make the answer suitable
for examination writing.

"""

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = ask_ai(prompt)

                st.markdown(answer)

                st.session_state.last_response = (
                    answer
                )

                add_to_history(

                    question,

                    answer,

                    "Exam Helper"

                )

                voice_player(answer)

            else:

                st.warning(
                    "Please enter a question."
                )


    # --------------------------------------------------------
    # MCQ GENERATOR
    # --------------------------------------------------------

    with exam_tab2:

        st.subheader(
            "❓ MCQ Generator"
        )

        mcq_subject = st.text_input(
            "Subject",
            key="mcq_subject"
        )

        mcq_topic = st.text_input(
            "Topic",
            key="mcq_topic"
        )

        mcq_count = st.slider(

            "Number of MCQs",

            5,

            20,

            10

        )

        if st.button(
            "Generate MCQs",
            key="generate_mcqs"
        ):

            prompt = f"""

Create {mcq_count} multiple choice
questions.

Subject:
{mcq_subject}

Topic:
{mcq_topic}

For every question provide:

Question

A)

B)

C)

D)

Correct Answer

Explanation

Make questions useful for exams.

"""

            with st.spinner(
                "Generating MCQs..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "MCQs: "
                + mcq_topic,

                answer,

                "Exam Helper MCQs"

            )


    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    with exam_tab3:

        st.subheader(
            "📝 Explain Answer"
        )

        answer_text = st.text_area(
            "Paste Question or Answer"
        )

        if st.button(
            "Explain Clearly"
        ):

            prompt = f"""

Explain the following clearly
in simple student-friendly language.

Content:

{answer_text}

Give:

1. Simple Explanation
2. Important Points
3. Example
4. Exam Tips

"""

            with st.spinner(
                "Explaining..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            voice_player(answer)


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif selected_option == "🔬 Project & Lab Guide":

    st.header(
        "🔬 Project & Lab Guide"
    )

    project_tab1, project_tab2 = st.tabs(

        [

            "💡 Project Guide",

            "🧪 Lab Guide"

        ]

    )


    # --------------------------------------------------------
    # PROJECT GUIDE
    # --------------------------------------------------------

    with project_tab1:

        branch = st.selectbox(

            "Select Branch",

            [

                "EEE",

                "ECE",

                "CSE",

                "IT",

                "Mechanical",

                "Civil",

                "Other"

            ]

        )

        project_topic = st.text_input(
            "Project Topic / Idea"
        )

        project_level = st.selectbox(

            "Project Level",

            [

                "Mini Project",

                "Major Project",

                "Final Year Project"

            ]

        )

        if st.button(
            "Generate Project Guide"
        ):

            prompt = f"""

Create a complete engineering
project guide.

Branch:
{branch}

Project Topic:
{project_topic}

Project Level:
{project_level}

Include:

1. Project Title
2. Abstract
3. Objective
4. Problem Statement
5. Components Required
6. Software Required
7. Hardware Required
8. Working Principle
9. Block Diagram Explanation
10. Methodology
11. Implementation Steps
12. Expected Output
13. Applications
14. Advantages
15. Future Scope
16. Viva Questions

Make it practical for students.

"""

            with st.spinner(
                "Creating project guide..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "Project: "
                + project_topic,

                answer,

                "Project Guide"

            )


    # --------------------------------------------------------
    # LAB GUIDE
    # --------------------------------------------------------

    with project_tab2:

        lab_subject = st.text_input(
            "Lab Subject"
        )

        experiment = st.text_input(
            "Experiment Name"
        )

        if st.button(
            "Generate Lab Guide"
        ):

            prompt = f"""

Create a complete laboratory
experiment guide.

Subject:
{lab_subject}

Experiment:
{experiment}

Include:

1. Aim
2. Apparatus Required
3. Theory
4. Circuit / Setup Description
5. Procedure
6. Observations
7. Calculations
8. Result
9. Precautions
10. Viva Questions
11. Important Notes

Make it suitable for
engineering students.

"""

            with st.spinner(
                "Creating lab guide..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "Lab: "
                + experiment,

                answer,

                "Lab Guide"

            )


# ============================================================
# GATE PREPARATION
# ============================================================

elif selected_option == "🎓 GATE Preparation":

    st.header(
        "🎓 GATE Preparation"
    )

    st.write(
        "Complete GATE preparation assistant."
    )

    gate_tab1, gate_tab2, gate_tab3, gate_tab4, gate_tab5 = st.tabs(

        [

            "📅 Student Planning",

            "⭐ Important Questions",

            "❓ MCQs",

            "📜 Previous Papers",

            "📖 Topic Explanation"

        ]

    )


    # --------------------------------------------------------
    # GATE STUDENT PLANNING
    # --------------------------------------------------------

    with gate_tab1:

        st.subheader(
            "📅 Personalized GATE Study Plan"
        )

        gate_branch = st.selectbox(

            "GATE Branch",

            [

                "Electrical Engineering",

                "Electronics & Communication",

                "Computer Science",

                "Mechanical Engineering",

                "Civil Engineering",

                "Other"

            ],

            key="gate_branch"

        )

        preparation_time = st.selectbox(

            "Available Preparation Time",

            [

                "1 Month",

                "3 Months",

                "6 Months",

                "1 Year"

            ]

        )

        study_hours = st.selectbox(

            "Daily Study Time",

            [

                "1 Hour",

                "2 Hours",

                "3 Hours",

                "4 Hours",

                "5+ Hours"

            ]

        )

        current_level = st.selectbox(

            "Current Preparation Level",

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ]

        )

        weak_subjects = st.text_area(

            "Weak Subjects / Topics",

            placeholder=
            "Example: Network Theory, "
            "Electrical Machines"

        )

        if st.button(

            "📅 Create My GATE Plan",

            key="create_gate_plan",

            use_container_width=True

        ):

            prompt = f"""

Create a personalized GATE
preparation plan.

Branch:
{gate_branch}

Preparation Time:
{preparation_time}

Daily Study Hours:
{study_hours}

Current Level:
{current_level}

Weak Subjects:
{weak_subjects}


Create a complete student plan.

Include:

1. Preparation Strategy

2. Subject Priority

3. Complete Study Schedule

4. Daily Routine

5. Weekly Routine

6. Monthly Targets

7. Topic Learning Strategy

8. Revision Strategy

9. Formula Revision Plan

10. Previous Paper Strategy

11. MCQ Practice Strategy

12. Mock Test Strategy

13. Weak Subject Improvement Plan

14. Time Management

15. Final Month Strategy

16. Final Week Strategy

17. Exam Day Tips

Make the plan realistic and
student-friendly.

"""

            with st.spinner(
                "Creating your GATE plan..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "GATE Student Plan",

                answer,

                "GATE Preparation"

            )

            voice_player(answer)


    # --------------------------------------------------------
    # IMPORTANT QUESTIONS
    # --------------------------------------------------------

    with gate_tab2:

        st.subheader(
            "⭐ Important GATE Questions"
        )

        important_subject = st.text_input(
            "Enter Subject"
        )

        important_topic = st.text_input(
            "Enter Topic (Optional)"
        )

        question_number = st.slider(

            "Number of Questions",

            5,

            30,

            10

        )

        if st.button(
            "Generate Important Questions"
        ):

            prompt = f"""

Generate {question_number}
important GATE preparation questions.

Branch:
{gate_branch}

Subject:
{important_subject}

Topic:
{important_topic}

Include:

- Conceptual Questions
- Numerical Questions
- Important Formula Questions
- Frequently Asked Concepts

For every question provide:

Question

Answer

Explanation

Important Formula if applicable.

Make it useful for GATE preparation.

"""

            with st.spinner(
                "Generating important questions..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "GATE Important Questions: "
                + important_subject,

                answer,

                "GATE Important Questions"

            )


    # --------------------------------------------------------
    # GATE MCQs
    # --------------------------------------------------------

    with gate_tab3:

        st.subheader(
            "❓ GATE MCQ Practice"
        )

        gate_mcq_subject = st.text_input(
            "Subject",
            key="gate_mcq_subject"
        )

        gate_mcq_topic = st.text_input(
            "Topic",
            key="gate_mcq_topic"
        )

        gate_mcq_count = st.slider(

            "Number of MCQs",

            5,

            30,

            10,

            key="gate_mcq_count"

        )

        difficulty = st.selectbox(

            "Difficulty Level",

            [

                "Easy",

                "Medium",

                "Hard",

                "Mixed"

            ]

        )

        if st.button(
            "Generate GATE MCQs"
        ):

            prompt = f"""

Create {gate_mcq_count}
GATE style MCQs.

Branch:
{gate_branch}

Subject:
{gate_mcq_subject}

Topic:
{gate_mcq_topic}

Difficulty:
{difficulty}


For every question provide:

Question

A) Option

B) Option

C) Option

D) Option

Correct Answer

Detailed Explanation

Formula if required.

Make the questions similar
to competitive examination style.

"""

            with st.spinner(
                "Generating GATE MCQs..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "GATE MCQs: "
                + gate_mcq_topic,

                answer,

                "GATE MCQs"

            )


    # --------------------------------------------------------
    # PREVIOUS PAPERS
    # --------------------------------------------------------

    with gate_tab4:

        st.subheader(
            "📜 Previous Paper Analysis"
        )

        previous_subject = st.text_input(
            "Subject for Previous Paper Analysis"
        )

        previous_topic = st.text_input(
            "Topic (Optional)"
        )

        if st.button(
            "Analyze Previous Paper Pattern"
        ):

            prompt = f"""

Provide GATE previous year
question paper preparation guidance.

Branch:
{gate_branch}

Subject:
{previous_subject}

Topic:
{previous_topic}

Explain:

1. Important recurring topics

2. Frequently tested concepts

3. Question pattern

4. Numerical question areas

5. Conceptual question areas

6. Difficulty pattern

7. How to practice previous questions

8. Step-by-step previous paper strategy

9. Revision after solving papers

10. Common mistakes students make


Do NOT claim exact previous-year
questions unless you are certain.

Provide useful preparation guidance.

"""

            with st.spinner(
                "Analyzing preparation pattern..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "GATE Previous Paper: "
                + previous_subject,

                answer,

                "GATE Previous Papers"

            )


    # --------------------------------------------------------
    # TOPIC EXPLANATION
    # --------------------------------------------------------

    with gate_tab5:

        st.subheader(
            "📖 GATE Topic Explanation"
        )

        explain_subject = st.text_input(
            "Subject",
            key="explain_subject"
        )

        explain_topic = st.text_input(
            "Topic",
            key="explain_topic"
        )

        explanation_level = st.selectbox(

            "Explanation Level",

            [

                "Beginner",

                "Intermediate",

                "Advanced",

                "GATE Exam Level"

            ]

        )

        if st.button(
            "Explain Topic"
        ):

            prompt = f"""

Explain the following topic
for GATE preparation.

Subject:
{explain_subject}

Topic:
{explain_topic}

Level:
{explanation_level}


Explain using:

1. Basic Introduction

2. Definition

3. Core Concepts

4. Important Theory

5. Important Formulas

6. Step-by-Step Explanation

7. Example

8. Numerical Example if applicable

9. Important GATE Points

10. Common Mistakes

11. Quick Revision Notes

Make it clear and easy
for students.

"""

            with st.spinner(
                "Explaining topic..."
            ):

                answer = ask_ai(prompt)

            st.markdown(answer)

            st.session_state.last_response = (
                answer
            )

            add_to_history(

                "GATE Topic: "
                + explain_topic,

                answer,

                "GATE Topic Explanation"

            )

            st.subheader(
                "🔊 Listen to Explanation"
            )

            voice_player(answer)


# ============================================================
# SETTINGS
# ============================================================

elif selected_option == "⚙️ Settings":

    st.header("⚙️ Settings")

    setting_tab1, setting_tab2 = st.tabs(

        [

            "🤖 AI Settings",

            "🕘 History"

        ]

    )


    # --------------------------------------------------------
    # AI SETTINGS
    # --------------------------------------------------------

    with setting_tab1:

        st.subheader(
            "🤖 AI Settings"
        )

        language = st.selectbox(

            "Language",

            [

                "English",

                "Telugu",

                "Hindi"

            ],

            index=[

                "English",

                "Telugu",

                "Hindi"

            ].index(

                st.session_state.settings.get(
                    "language",
                    "English"
                )

            )

        )

        auto_save = st.checkbox(

            "Automatically Save History",

            value=st.session_state.settings.get(
                "auto_save_history",
                True
            )

        )

        if st.button(
            "💾 Save Settings"
        ):

            st.session_state.settings[
                "language"
            ] = language

            st.session_state.settings[
                "auto_save_history"
            ] = auto_save

            save_settings(
                st.session_state.settings
            )

            st.success(
                "Settings Saved Successfully!"
            )

        st.info(
            "🎤 Voice Input: Record your voice "
            "using the microphone.\n\n"
            "🔊 AI Voice: Use Play, Pause, "
            "Resume and Stop buttons after "
            "receiving an AI response."
        )


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    with setting_tab2:

        st.subheader(
            "🕘 Chat History"
        )

        if len(
            st.session_state.history
        ) == 0:

            st.info(
                "No history available."
            )

        else:

            for index, item in enumerate(

                st.session_state.history

            ):

                title = (

                    item.get(
                        "category",
                        "History"
                    )

                    + " - "

                    + item.get(
                        "time",
                        ""
                    )

                )

                with st.expander(title):

                    st.markdown(
                        "### Question"
                    )

                    st.write(
                        item.get(
                            "question",
                            ""
                        )
                    )

                    st.markdown(
                        "### Answer"
                    )

                    st.write(
                        item.get(
                            "answer",
                            ""
                        )
                    )

        st.divider()

        if st.button(

            "🗑️ Clear All History",

            use_container_width=True

        ):

            st.session_state.history = []

            save_history([])

            st.success(
                "History Cleared Successfully!"
            )

            time.sleep(1)

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 Tech Mithra AI • AI Study Assistant"
)
