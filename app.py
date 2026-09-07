# ============================================================
# TECH MITHRA AI - COMPLETE STREAMLIT APPLICATION
# ============================================================
#
# INSTALL COMMAND:
#
# pip install streamlit google-genai
#
# OPTIONAL:
# pip install pillow
#
# RUN COMMAND:
#
# streamlit run app.py
#
# ============================================================


import streamlit as st
import os
import json
import time
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    color: #777;
    font-size: 18px;
    margin-bottom: 25px;
}

.option-card {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.user-message {
    padding: 15px;
    border-radius: 15px;
    margin: 8px 0px;
}

.assistant-message {
    padding: 15px;
    border-radius: 15px;
    margin: 8px 0px;
}

.small-text {
    font-size: 14px;
    color: gray;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "current_option" not in st.session_state:
    st.session_state.current_option = "💬 AI Chat"

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = None


# ============================================================
# HISTORY FILE
# ============================================================

HISTORY_FILE = "tech_mithra_history.json"


def load_history():

    try:

        if os.path.exists(HISTORY_FILE):

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

    except Exception:

        return []

    return []


def save_history():

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                st.session_state.history,
                file,
                ensure_ascii=False,
                indent=4
            )

    except Exception:

        pass


# Load history only once
if "history_loaded" not in st.session_state:

    st.session_state.history = load_history()

    st.session_state.history_loaded = True


# ============================================================
# GEMINI INITIALIZATION
# ============================================================

def get_api_key():

    # Streamlit Secrets
    try:

        if "GEMINI_API_KEY" in st.secrets:

            return st.secrets["GEMINI_API_KEY"]

    except Exception:

        pass

    # Environment Variable
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:

        return api_key

    return None


def get_gemini_client():

    if st.session_state.gemini_client is not None:

        return st.session_state.gemini_client


    api_key = get_api_key()

    if not api_key:

        return None


    try:

        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        st.session_state.gemini_client = client

        return client


    except Exception:

        return None


# ============================================================
# FIND AVAILABLE MODEL
# ============================================================

def find_working_model():

    client = get_gemini_client()

    if client is None:

        return None


    # If model already selected
    if st.session_state.selected_model:

        return st.session_state.selected_model


    try:

        available_models = []

        for model in client.models.list():

            model_name = getattr(model, "name", "")

            if model_name:

                available_models.append(model_name)


        # Preferred models
        preferred_models = [

            "models/gemini-3.6-flash",
            "models/gemini-3-flash",
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "gemini-3.6-flash",
            "gemini-3-flash",
            "gemini-2.5-flash",
            "gemini-2.0-flash"

        ]


        # Check preferred model
        for preferred in preferred_models:

            if preferred in available_models:

                st.session_state.selected_model = preferred

                return preferred


        # Find any Gemini model
        for model_name in available_models:

            name = model_name.lower()

            if "gemini" in name and "flash" in name:

                st.session_state.selected_model = model_name

                return model_name


        # Any Gemini model
        for model_name in available_models:

            if "gemini" in model_name.lower():

                st.session_state.selected_model = model_name

                return model_name


    except Exception:

        pass


    return None


# ============================================================
# OFFLINE FALLBACK AI
# ============================================================

def offline_response(question):

    question_lower = question.lower()


    # --------------------------------------------------------
    # MANAGEMENT
    # --------------------------------------------------------

    if "management" in question_lower:

        return """

## Management

Management is the process of planning, organizing, staffing, directing and controlling organizational resources to achieve organizational goals effectively and efficiently.

### Main Functions of Management

1. **Planning**
   - Deciding what to do in the future.

2. **Organizing**
   - Arranging resources and responsibilities.

3. **Staffing**
   - Selecting and managing employees.

4. **Directing**
   - Guiding and motivating employees.

5. **Controlling**
   - Checking whether goals are achieved.

"""


    # --------------------------------------------------------
    # CLOUD COMPUTING
    # --------------------------------------------------------

    if "cloud" in question_lower:

        return """

## Cloud Computing

Cloud computing is the delivery of computing services such as servers, storage, databases, networking and software through the Internet.

### Main Types

- Public Cloud
- Private Cloud
- Hybrid Cloud

### Service Models

- IaaS
- PaaS
- SaaS

"""


    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    if "artificial intelligence" in question_lower or question_lower == "ai":

        return """

## Artificial Intelligence

Artificial Intelligence (AI) is a branch of computer science that enables machines to perform tasks that normally require human intelligence.

### Examples

- Chatbots
- Voice Assistants
- Image Recognition
- Self Driving Cars
- Recommendation Systems

"""


    # --------------------------------------------------------
    # DEFAULT RESPONSE
    # --------------------------------------------------------

    return f"""

## Answer

### Your Question

**{question}**

I am currently running in fallback mode.

Please check:

1. Internet connection.
2. Gemini API key.
3. Streamlit Secrets configuration.
4. Gemini API availability.

You can still use the application options such as:

- Exam Helper
- Event Planner
- Project & Lab Guide
- GATE Preparation

"""


# ============================================================
# AI RESPONSE
# ============================================================

def generate_ai_response(prompt):

    client = get_gemini_client()


    # No API key
    if client is None:

        return offline_response(prompt)


    model_name = find_working_model()


    if model_name is None:

        return offline_response(prompt)


    # Retry API
    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model=model_name,

                contents=prompt

            )


            if response:

                text = getattr(
                    response,
                    "text",
                    None
                )

                if text:

                    return text


        except Exception:

            # Wait and retry
            time.sleep(2)


    # Never show technical API error
    return offline_response(prompt)


# ============================================================
# ADD CHAT HISTORY
# ============================================================

def add_to_history(role, content):

    item = {

        "role": role,

        "content": content,

        "time": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

    }


    st.session_state.messages.append(item)

    st.session_state.history.append(item)

    save_history()


# ============================================================
# AI CHAT FUNCTION
# ============================================================

def normal_ai_chat(question):

    language = st.session_state.language


    prompt = f"""

You are Tech Mithra AI.

Answer the user's question clearly and accurately.

Selected language:
{language}

User Question:
{question}

Instructions:

- Give a clear answer.
- Use headings.
- Use bullet points when useful.
- For study questions give easy explanations.
- For technical questions give examples.
- Do not give unnecessary information.

"""


    return generate_ai_response(prompt)


# ============================================================
# EVENT PLANNER
# ============================================================

def event_planner(
    event_name,
    budget,
    guests,
    location
):

    prompt = f"""

You are an expert Event Planner.

Create a COMPLETE EVENT PLAN.

Event Name:
{event_name}

Budget:
{budget}

Expected Guests:
{guests}

Location:
{location}

Give the complete plan from START TO END.

Include:

1. Event Overview
2. Objectives
3. Budget Planning
4. Budget Breakdown
5. Timeline
6. Planning Before Event
7. Venue Selection
8. Decorations
9. Food and Catering
10. Invitations
11. Guest Management
12. Transportation
13. Sound and Lighting
14. Photography
15. Event Schedule
16. Team Responsibilities
17. Risk Management
18. Backup Plan
19. Event Day Checklist
20. Closing Activities
21. Post Event Activities

Make the answer practical.

Use tables when useful.

"""


    return generate_ai_response(prompt)


# ============================================================
# EXAM HELPER
# ============================================================

def exam_helper(question, answer_type):

    prompt = f"""

You are an expert teacher and exam preparation assistant.

Student Question:

{question}

Answer Type:

{answer_type}

Follow the requested answer type exactly.

"""


    # --------------------------------------------------------
    # SHORT ANSWER
    # --------------------------------------------------------

    if answer_type == "Short Answer":

        prompt += """

Give:

- Definition
- Main points
- Simple explanation

Suitable for 2 to 5 marks.

"""


    # --------------------------------------------------------
    # LONG ANSWER
    # --------------------------------------------------------

    elif answer_type == "Long Answer":

        prompt += """

Give a detailed exam answer.

Include:

- Introduction
- Definition
- Explanation
- Important Points
- Examples
- Diagram explanation if applicable
- Conclusion

Suitable for 10 marks.

"""


    # --------------------------------------------------------
    # MCQ
    # --------------------------------------------------------

    elif answer_type == "MCQs":

        prompt += """

Generate 10 Multiple Choice Questions.

For every question provide:

Question

A)
B)
C)
D)

Correct Answer:
Explanation:

Make the answers educational.

"""


    # --------------------------------------------------------
    # MCQ WITH ANSWERS
    # --------------------------------------------------------

    elif answer_type == "MCQs With Answers":

        prompt += """

Generate 15 Multiple Choice Questions.

For every question provide:

Question

A)
B)
C)
D)

Correct Answer:
Explanation:

Make the correct answer clearly visible.

"""


    return generate_ai_response(prompt)


# ============================================================
# PROJECT GUIDE
# ============================================================

def project_lab_guide(question):

    prompt = f"""

You are an engineering Project and Laboratory Guide.

Student Request:

{question}

Give a complete practical answer.

Include when applicable:

1. Project Title
2. Abstract
3. Objective
4. Required Components
5. Software Requirements
6. Hardware Requirements
7. Block Diagram Explanation
8. Working Principle
9. Circuit or System Explanation
10. Procedure
11. Implementation Steps
12. Expected Output
13. Advantages
14. Applications
15. Limitations
16. Future Scope
17. Conclusion
18. Viva Questions
19. Viva Answers

Make the explanation easy for students.

"""


    return generate_ai_response(prompt)


# ============================================================
# GATE PREPARATION
# ============================================================

def gate_preparation(
    branch,
    topic,
    days
):

    prompt = f"""

You are an expert GATE preparation mentor.

Student Branch:
{branch}

Topic or Subject:
{topic}

Preparation Duration:
{days} days

Create a complete GATE preparation plan.

Include:

1. Subject Priority
2. Important Topics
3. Daily Study Plan
4. Weekly Plan
5. Concept Learning
6. Numerical Practice
7. Previous Year Questions
8. Mock Tests
9. Revision Plan
10. Important Formulas
11. Time Management
12. Common Mistakes
13. Final Week Strategy

Also generate 5 practice MCQs with answers.

Make the plan practical and realistic.

"""


    return generate_ai_response(prompt)


# ============================================================
# SPEAK TEXT
# ============================================================

def speak_text(text):

    clean_text = text.replace(
        "\n",
        " "
    )

    clean_text = clean_text.replace(
        "`",
        ""
    )

    clean_text = clean_text.replace(
        "#",
        ""
    )


    html = f"""

<script>

function speakText() {{

    window.speechSynthesis.cancel();

    let text =
    `{clean_text}`;

    let speech =
    new SpeechSynthesisUtterance(text);

    speech.rate = 1;

    speech.pitch = 1;

    window.speechSynthesis.speak(speech);

}}

function pauseSpeech() {{

    window.speechSynthesis.pause();

}}

function resumeSpeech() {{

    window.speechSynthesis.resume();

}}

</script>

"""


    st.components.v1.html(
        html,
        height=0
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🤖 Tech Mithra AI"
    )

    st.caption(
        "Your Smart AI Assistant"
    )


    st.divider()


    # --------------------------------------------------------
    # OPTIONS
    # --------------------------------------------------------

    options = [

        "💬 AI Chat",

        "📅 Event Planner",

        "📝 Exam Helper",

        "🔬 Project & Lab Guide",

        "🎓 GATE Preparation",

        "⚙️ Settings"

    ]


    selected_option = st.radio(

        "Choose an Option",

        options,

        index=options.index(
            st.session_state.current_option
        )

    )


    st.session_state.current_option = (
        selected_option
    )


    st.divider()


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    with st.expander("🕘 Recent History"):

        if st.session_state.history:

            recent_history = (
                st.session_state.history[-10:]
            )

            for item in reversed(recent_history):

                if item["role"] == "user":

                    text = item["content"]

                    if len(text) > 40:

                        text = text[:40] + "..."

                    st.caption(
                        "💬 " + text
                    )

        else:

            st.caption(
                "No history yet."
            )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Tech Mithra AI</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">Ask anything • Upload Photo • Camera • Files • Voice</div>',
    unsafe_allow_html=True
)


# ============================================================
# AI CHAT
# ============================================================

if selected_option == "💬 AI Chat":


    st.subheader(
        "💬 AI Chat"
    )


    # --------------------------------------------------------
    # SHOW MESSAGES
    # --------------------------------------------------------

    for message in st.session_state.messages:


        if message["role"] == "user":

            with st.chat_message("user"):

                st.write(
                    message["content"]
                )


        elif message["role"] == "assistant":

            with st.chat_message("assistant"):

                st.markdown(
                    message["content"]
                )


    # --------------------------------------------------------
    # UPLOAD OPTIONS
    # --------------------------------------------------------

    with st.expander(
        "➕ Upload Options"
    ):

        col1, col2 = st.columns(2)


        with col1:

            uploaded_file = st.file_uploader(

                "📁 Upload File",

                type=[

                    "txt",
                    "pdf",
                    "docx",
                    "jpg",
                    "jpeg",
                    "png"

                ]

            )


        with col2:

            camera_photo = st.camera_input(

                "📸 Take a Photo"

            )


        # ----------------------------------------------------
        # AUDIO
        # ----------------------------------------------------

        try:

            audio_input = st.audio_input(
                "🎤 Microphone"
            )

        except Exception:

            audio_input = None

            st.caption(
                "🎤 Microphone feature depends on your Streamlit version."
            )


        if uploaded_file:

            st.success(
                "File uploaded successfully."
            )


        if camera_photo:

            st.success(
                "Photo captured successfully."
            )


        if audio_input:

            st.success(
                "Audio recorded successfully."
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_question = st.chat_input(

        "Message Tech Mithra AI..."

    )


    if user_question:


        # USER MESSAGE
        with st.chat_message("user"):

            st.write(
                user_question
            )


        add_to_history(

            "user",

            user_question

        )


        # ASSISTANT
        with st.chat_message("assistant"):


            with st.spinner(
                "Tech Mithra AI is thinking..."
            ):


                answer = normal_ai_chat(
                    user_question
                )


                st.markdown(
                    answer
                )


        add_to_history(

            "assistant",

            answer

        )


        # ----------------------------------------------------
        # VOICE CONTROLS
        # ----------------------------------------------------

        if st.session_state.voice_enabled:


            st.divider()


            st.markdown(
                "### 🔊 AI Voice"
            )


            voice_col1, voice_col2, voice_col3 = (
                st.columns(3)
            )


            with voice_col1:

                if st.button(
                    "🔊 Play",
                    key="play_voice"
                ):

                    speak_text(answer)

                    st.success(
                        "Voice started."
                    )


            with voice_col2:

                if st.button(
                    "⏸ Pause",
                    key="pause_voice"
                ):

                    st.components.v1.html(

                        """

<script>

window.parent.speechSynthesis.pause();

</script>

                        """,

                        height=0

                    )

                    st.info(
                        "Voice paused."
                    )


            with voice_col3:

                if st.button(
                    "▶ Resume",
                    key="resume_voice"
                ):

                    st.components.v1.html(

                        """

<script>

window.parent.speechSynthesis.resume();

</script>

                        """,

                        height=0

                    )

                    st.success(
                        "Voice resumed."
                    )


# ============================================================
# EVENT PLANNER
# ============================================================

elif selected_option == "📅 Event Planner":


    st.header(
        "📅 Event Planner"
    )


    st.write(
        "Plan your complete event from beginning to ending."
    )


    event_name = st.text_input(

        "🎉 Event Name",

        placeholder=
        "Example: College Farewell Party"

    )


    col1, col2 = st.columns(2)


    with col1:

        budget = st.text_input(

            "💰 Budget",

            placeholder=
            "Example: ₹50,000"

        )


    with col2:

        guests = st.number_input(

            "👥 Expected Guests",

            min_value=1,

            value=100

        )


    location = st.text_input(

        "📍 Event Location",

        placeholder=
        "Example: College Auditorium"

    )


    if st.button(
        "✨ Create Complete Event Plan",
        type="primary"
    ):


        if event_name:


            with st.spinner(
                "Creating your complete event plan..."
            ):


                answer = event_planner(

                    event_name,

                    budget,

                    guests,

                    location

                )


                st.markdown(
                    answer
                )


                add_to_history(

                    "user",

                    "Event Planner: "
                    + event_name

                )


                add_to_history(

                    "assistant",

                    answer

                )


        else:

            st.warning(
                "Please enter the Event Name."
            )


# ============================================================
# EXAM HELPER
# ============================================================

elif selected_option == "📝 Exam Helper":


    st.header(
        "📝 Exam Helper"
    )


    st.write(
        "Get exam answers, long answers and MCQs."
    )


    answer_type = st.selectbox(

        "Select Answer Type",

        [

            "Short Answer",

            "Long Answer",

            "MCQs",

            "MCQs With Answers"

        ]

    )


    question = st.text_area(

        "Enter Your Question or Topic",

        placeholder=
        "Example: Explain the evolution of management"

    )


    if st.button(

        "📚 Generate Answer",

        type="primary"

    ):


        if question:


            with st.spinner(
                "Preparing your exam answer..."
            ):


                answer = exam_helper(

                    question,

                    answer_type

                )


                st.markdown(
                    answer
                )


                add_to_history(

                    "user",

                    "Exam Helper: "
                    + question

                )


                add_to_history(

                    "assistant",

                    answer

                )


        else:

            st.warning(
                "Please enter a question."
            )


# ============================================================
# PROJECT AND LAB GUIDE
# ============================================================

elif selected_option == "🔬 Project & Lab Guide":


    st.header(
        "🔬 Project & Lab Guide"
    )


    st.write(
        "Get complete project guidance and laboratory assistance."
    )


    project_question = st.text_area(

        "Enter Project or Lab Question",

        placeholder=
        "Example: Give an IoT based smart irrigation project"

    )


    if st.button(

        "🔬 Generate Project Guide",

        type="primary"

    ):


        if project_question:


            with st.spinner(
                "Creating your project guide..."
            ):


                answer = project_lab_guide(
                    project_question
                )


                st.markdown(
                    answer
                )


                add_to_history(

                    "user",

                    "Project Guide: "
                    + project_question

                )


                add_to_history(

                    "assistant",

                    answer

                )


        else:

            st.warning(
                "Please enter your project topic."
            )


# ============================================================
# GATE PREPARATION
# ============================================================

elif selected_option == "🎓 GATE Preparation":


    st.header(
        "🎓 GATE Preparation"
    )


    st.write(
        "Create your personalized GATE preparation plan."
    )


    gate_branch = st.selectbox(

        "Select Your Branch",

        [

            "Computer Science",

            "Electrical Engineering",

            "Electronics and Communication",

            "Mechanical Engineering",

            "Civil Engineering",

            "Other"

        ]

    )


    gate_topic = st.text_input(

        "Subject or Topic",

        placeholder=
        "Example: Network Theory"

    )


    preparation_days = st.number_input(

        "Preparation Duration (Days)",

        min_value=1,

        value=90

    )


    if st.button(

        "🎯 Create GATE Study Plan",

        type="primary"

    ):


        with st.spinner(
            "Creating your GATE preparation plan..."
        ):


            answer = gate_preparation(

                gate_branch,

                gate_topic,

                preparation_days

            )


            st.markdown(
                answer
            )


            add_to_history(

                "user",

                "GATE Preparation: "
                + gate_topic

            )


            add_to_history(

                "assistant",

                answer

            )


# ============================================================
# SETTINGS
# ============================================================

elif selected_option == "⚙️ Settings":


    st.header(
        "⚙️ Settings"
    )


    # --------------------------------------------------------
    # AI SETTINGS
    # --------------------------------------------------------

    st.subheader(
        "🤖 AI Settings"
    )


    st.session_state.language = st.selectbox(

        "🌐 Language",

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
            st.session_state.language
        )

    )


    # --------------------------------------------------------
    # VOICE SETTINGS
    # --------------------------------------------------------

    st.subheader(
        "🔊 Voice Settings"
    )


    st.session_state.voice_enabled = st.toggle(

        "Enable AI Voice",

        value=
        st.session_state.voice_enabled

    )


    if st.session_state.voice_enabled:

        st.success(
            "AI Voice is Enabled."
        )

    else:

        st.warning(
            "AI Voice is Disabled."
        )


    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    st.divider()


    st.subheader(
        "🕘 Chat History"
    )


    st.write(
        f"Total History Messages: "
        f"{len(st.session_state.history)}"
    )


    if st.session_state.history:


        with st.expander(
            "📜 View History"
        ):


            for item in reversed(
                st.session_state.history[-50:]
            ):


                if item["role"] == "user":

                    st.markdown(
                        f"**👤 You:** "
                        f"{item['content']}"
                    )


                else:

                    st.markdown(
                        f"**🤖 Tech Mithra AI:** "
                        f"{item['content'][:300]}"
                    )


                st.caption(
                    item["time"]
                )


                st.divider()


    else:

        st.info(
            "No history available."
        )


    # --------------------------------------------------------
    # CLEAR HISTORY
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear All History",
        type="secondary"
    ):


        st.session_state.history = []

        st.session_state.messages = []


        try:

            if os.path.exists(
                HISTORY_FILE
            ):

                os.remove(
                    HISTORY_FILE
                )

        except Exception:

            pass


        st.success(
            "History cleared successfully."
        )


        st.rerun()


    # --------------------------------------------------------
    # APPLICATION INFO
    # --------------------------------------------------------

    st.divider()


    st.subheader(
        "ℹ️ Application Information"
    )


    st.write(

        """

**Application Name:** Tech Mithra AI

**Features:**

- AI Chat
- Event Planner
- Exam Helper
- MCQs with Answers
- Project & Lab Guide
- GATE Preparation
- Photo Upload
- Camera
- File Upload
- Microphone Support
- AI Voice
- Chat History

"""

    )


    # --------------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------------

    st.divider()


    st.subheader(
        "🤖 AI Connection"
    )


    if get_api_key():

        st.success(
            "Gemini API Key Found."
        )


        model = find_working_model()


        if model:

            st.info(
                f"Selected Model: {model}"
            )

        else:

            st.warning(
                "AI model will be detected automatically when available."
            )


    else:

        st.warning(
            "Gemini API Key not found. "
            "The application will use fallback mode."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🤖 Tech Mithra AI • Smart Learning Assistant"
)
