# ============================================================
# TECH MITHRA AI - COMPLETE STREAMLIT APP
# Save this file as: app.py
#
# Install:
# pip install streamlit google-genai streamlit-mic-recorder
#
# Run:
# streamlit run app.py
#
# Add your Gemini API Key in Streamlit Secrets:
# GEMINI_API_KEY = "YOUR_API_KEY"
# ============================================================

import streamlit as st
import json
import os
from datetime import datetime

try:
    from google import genai
except ImportError:
    genai = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="֎🇦🇮",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "Tech Mithra AI"
HISTORY_FILE = "tech_mithra_history.json"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
}

.sub-title {
    color: gray;
    font-size: 17px;
    margin-bottom: 20px;
}

.stButton button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "💬 AI Chat"

if "history" not in st.session_state:
    st.session_state.history = []

if "history_loaded" not in st.session_state:
    st.session_state.history_loaded = False

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""


# ============================================================
# HISTORY FUNCTIONS
# ============================================================

def load_history():

    if os.path.exists(HISTORY_FILE):

        try:

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

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
                indent=2
            )

    except Exception:
        pass


def add_history(mode, question, answer):

    item = {

        "time": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        ),

        "mode": mode,

        "question": str(question),

        "answer": str(answer)

    }

    st.session_state.history.insert(
        0,
        item
    )

    st.session_state.history = (
        st.session_state.history[:100]
    )

    save_history()


def clear_history():

    st.session_state.history = []

    try:

        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    except Exception:
        pass


if not st.session_state.history_loaded:

    st.session_state.history = load_history()

    st.session_state.history_loaded = True


# ============================================================
# GET GEMINI API KEY
# ============================================================

def get_api_key():

    api_key = None

    try:

        api_key = st.secrets.get(
            "GEMINI_API_KEY"
        )

    except Exception:
        pass

    if not api_key:

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

    return api_key


# ============================================================
# GET GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client():

    if genai is None:
        return None

    api_key = get_api_key()

    if not api_key:
        return None

    try:

        client = genai.Client(
            api_key=api_key
        )

        return client

    except Exception:
        return None


# ============================================================
# LANGUAGE INSTRUCTION
# ============================================================

def get_language_instruction():

    language = st.session_state.language

    if language == "Telugu":

        return """

Answer completely in Telugu.

Use simple and clear Telugu.

"""

    elif language == "Telugu + English":

        return """

Answer using Telugu and English.

Use Telugu for explanation
and English technical terms where needed.

"""

    else:

        return """

Answer in clear English.

"""


# ============================================================
# ASK AI FUNCTION
# ============================================================

def ask_ai(question, files=None, mode="General"):

    client = get_client()

    if client is None:

        return """

❌ Gemini API Key is not configured.

Please add your API key.

Streamlit Cloud:

App Settings → Secrets

Add:

GEMINI_API_KEY = "YOUR_API_KEY"

"""


    language_instruction = (
        get_language_instruction()
    )


    mode_instruction = ""


    if mode == "Exam Helper":

        mode_instruction = """

You are an expert Exam Preparation Assistant.

Give exam-ready answers.

Use:

• Definition
• Explanation
• Important points
• Examples
• Conclusion

If it is an MCQ:

Clearly mention:

Correct Answer:
Correct Option:
Explanation:

"""


    elif mode == "GATE Preparation":

        mode_instruction = """

You are a GATE preparation expert.

Give accurate engineering answers.

For numerical problems:

1. Given Data
2. Formula
3. Calculation
4. Final Answer

Include shortcuts and important concepts.

"""


    elif mode == "Project & Lab Guide":

        mode_instruction = """

You are an Engineering Project and Lab Guide.

Give detailed practical guidance.

Include:

• Title
• Aim
• Objective
• Components
• Working Principle
• Procedure
• Result
• Applications
• Viva Questions

"""


    elif mode == "Event Planner":

        mode_instruction = """

You are an Event Planning Assistant.

Create practical and organized event plans.

Include:

• Event Objective
• Schedule
• Team
• Materials
• Budget
• Promotion
• Checklist

"""


    else:

        mode_instruction = """

You are a helpful AI assistant.

Give accurate and useful answers.

For study questions:

• Use simple explanations
• Use headings
• Use bullet points
• Give examples when useful

"""


    prompt = f"""

You are {APP_NAME}.

{language_instruction}

{mode_instruction}

User Question:

{question}

Important:

Give a direct answer.

Do not add unnecessary information.

"""


    try:

        contents = [prompt]


        if files:

            for file in files:

                if file is not None:

                    try:

                        contents.append(
                            file
                        )

                    except Exception:
                        pass


        # Try Gemini model names
        models_to_try = [

            "gemini-2.5-flash",

            "gemini-2.0-flash",

            "gemini-2.0-flash-lite"

        ]


        last_error = ""


        for model_name in models_to_try:

            try:

                response = (
                    client.models.generate_content(

                        model=model_name,

                        contents=contents

                    )
                )


                if response:

                    if response.text:

                        return response.text


            except Exception as e:

                last_error = str(e)


        return (
            "❌ AI Error:\n\n"
            + last_error
        )


    except Exception as e:

        return (
            "❌ Error:\n\n"
            + str(e)
        )


# ============================================================
# VOICE CONTROLS
# PAUSE + RESUME
# ============================================================

def voice_controls(text):

    if not st.session_state.voice_enabled:
        return


    clean_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "'")
        .replace("${", "")
        .replace("</script>", "")
        .replace("\n", " ")
    )


    html = f"""

<div>

<button onclick="speakText()"
style="
padding:8px 14px;
border-radius:8px;
border:1px solid #888;
cursor:pointer;
margin-right:8px;
">

🔊 Speak

</button>


<button onclick="pauseSpeech()"
style="
padding:8px 14px;
border-radius:8px;
border:1px solid #888;
cursor:pointer;
margin-right:8px;
">

⏸️ Pause

</button>


<button onclick="resumeSpeech()"
style="
padding:8px 14px;
border-radius:8px;
border:1px solid #888;
cursor:pointer;
">

▶️ Resume

</button>


<script>

let techMithraUtterance;

function speakText() {{

    window.speechSynthesis.cancel();

    techMithraUtterance =
        new SpeechSynthesisUtterance();

    techMithraUtterance.text =
        `{clean_text}`;

    techMithraUtterance.rate = 1;

    techMithraUtterance.pitch = 1;

    window.speechSynthesis.speak(
        techMithraUtterance
    );

}}


function pauseSpeech() {{

    if (
        window.speechSynthesis.speaking
    ) {{

        window.speechSynthesis.pause();

    }}

}}


function resumeSpeech() {{

    if (
        window.speechSynthesis.paused
    ) {{

        window.speechSynthesis.resume();

    }}

}}

</script>

</div>

"""


    st.components.v1.html(
        html,
        height=60
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.caption(
        "Your AI Student Assistant"
    )

    st.divider()


    options = [

        "💬 AI Chat",

        "🎉 Event Planner",

        "🎓 Exam Helper",

        "🔬 Project & Lab Guide",

        "📚 GATE Preparation",

        "⚙️ Settings"

    ]


    selected_page = st.radio(

        "Menu",

        options,

        index=options.index(
            st.session_state.page
        )
        if st.session_state.page in options
        else 0

    )


    st.session_state.page = selected_page


    st.divider()

    st.caption(
        "🚀 Tech Mithra AI"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 Tech Mithra AI'
    '</div>',

    unsafe_allow_html=True
)


# ============================================================
# AI CHAT
# ============================================================

if st.session_state.page == "💬 AI Chat":

    st.markdown(
        '<div class="sub-title">'
        'Ask anything like ChatGPT'
        '</div>',

        unsafe_allow_html=True
    )


    # DISPLAY OLD MESSAGES

    for message in (
        st.session_state.chat_messages
    ):


        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # PLUS OPTIONS
    # ========================================================

    with st.expander(
        "➕ Attachments"
    ):


        col1, col2, col3 = st.columns(3)


        with col1:

            uploaded_photo = st.file_uploader(

                "🖼️ Upload Photo",

                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp"
                ],

                key="chat_photo"

            )


        with col2:

            camera_photo = st.camera_input(

                "📷 Camera"

            )


        with col3:

            uploaded_file = st.file_uploader(

                "📁 Upload File",

                type=[
                    "txt",
                    "pdf",
                    "csv",
                    "json",
                    "py",
                    "java",
                    "c",
                    "cpp"
                ],

                key="chat_file"

            )


    # ========================================================
    # VOICE INPUT
    # ========================================================

    st.markdown("### 🎤 Voice Input")


    audio_file = st.audio_input(

        "Record your question"

    )


    if audio_file:

        st.audio(audio_file)


        if st.button(

            "🎤 Ask AI",

            key="voice_ask"

        ):


            with st.spinner(
                "Understanding your voice..."
            ):


                answer = ask_ai(

                    """

Listen to the uploaded audio.

Understand the user's question.

Answer clearly.

""",

                    files=[audio_file],

                    mode="General"

                )


            st.session_state.chat_messages.append({

                "role": "user",

                "content": "🎤 Voice Question"

            })


            st.session_state.chat_messages.append({

                "role": "assistant",

                "content": answer

            })


            add_history(

                "AI Chat Voice",

                "Voice Question",

                answer

            )


            st.rerun()


    # ========================================================
    # CHAT INPUT
    # ========================================================

    question = st.chat_input(

        "Message Tech Mithra AI..."

    )


    if question:


        files = []


        if uploaded_photo:

            files.append(
                uploaded_photo
            )


        if camera_photo:

            files.append(
                camera_photo
            )


        if uploaded_file:

            files.append(
                uploaded_file
            )


        st.session_state.chat_messages.append({

            "role": "user",

            "content": question

        })


        with st.chat_message("user"):

            st.markdown(question)


        with st.chat_message("assistant"):


            with st.spinner(
                "🤖 Thinking..."
            ):


                answer = ask_ai(

                    question,

                    files=files,

                    mode="General"

                )


            st.markdown(answer)

            voice_controls(answer)


        st.session_state.chat_messages.append({

            "role": "assistant",

            "content": answer

        })


        st.session_state.last_answer = answer


        add_history(

            "AI Chat",

            question,

            answer

        )


# ============================================================
# EVENT PLANNER
# ============================================================

elif st.session_state.page == "🎉 Event Planner":

    st.header(
        "🎉 Event Planner"
    )


    event_name = st.text_input(

        "Event Name",

        placeholder=
        "Example: Technical Workshop"

    )


    event_type = st.selectbox(

        "Event Type",

        [

            "Technical Event",

            "Workshop",

            "Seminar",

            "College Fest",

            "Cultural Event",

            "Sports Event",

            "Hackathon",

            "Other"

        ]

    )


    participants = st.text_input(

        "Expected Participants",

        placeholder="Example: 100 Students"

    )


    event_details = st.text_area(

        "Additional Details",

        placeholder=
        "Write your event requirements..."

    )


    if st.button(

        "🎉 Create Event Plan",

        use_container_width=True

    ):


        if not event_name:

            st.warning(
                "Please enter event name."
            )


        else:


            question = f"""

Create a complete event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Expected Participants:
{participants}

Additional Details:
{event_details}

"""


            with st.spinner(
                "Creating event plan..."
            ):


                answer = ask_ai(

                    question,

                    mode="Event Planner"

                )


            st.markdown(answer)

            voice_controls(answer)


            st.session_state.last_answer = answer


            add_history(

                "Event Planner",

                event_name,

                answer

            )


# ============================================================
# EXAM HELPER
# ============================================================

elif st.session_state.page == "🎓 Exam Helper":

    st.header(
        "🎓 Exam Helper"
    )


    exam_option = st.radio(

        "Choose Option",

        [

            "📝 Answer Generator",

            "🧠 MCQ Answer",

            "📚 Important Questions"

        ],

        horizontal=True

    )


    # ========================================================
    # ANSWER GENERATOR
    # ========================================================

    if exam_option == "📝 Answer Generator":


        question = st.text_area(

            "Enter your Question",

            placeholder=
            "Example: Explain the evolution of management"

        )


        marks = st.selectbox(

            "Answer Length",

            [

                "2 Marks",

                "5 Marks",

                "10 Marks",

                "15 Marks"

            ]

        )


        if st.button(

            "📝 Generate Answer",

            use_container_width=True

        ):


            if not question:

                st.warning(
                    "Please enter a question."
                )


            else:


                prompt = f"""

Question:

{question}

Write an exam answer for:

{marks}

"""

                with st.spinner(
                    "Writing answer..."
                ):


                    answer = ask_ai(

                        prompt,

                        mode="Exam Helper"

                    )


                st.markdown(answer)

                voice_controls(answer)


                add_history(

                    "Exam Answer",

                    question,

                    answer

                )


    # ========================================================
    # MCQ ANSWER
    # ========================================================

    elif exam_option == "🧠 MCQ Answer":


        mcq_question = st.text_area(

            "Enter MCQ",

            placeholder="""
Example:

What is the capital of India?

A) Mumbai
B) Delhi
C) Chennai
D) Hyderabad
"""

        )


        if st.button(

            "🧠 Get Correct Answer",

            use_container_width=True

        ):


            if not mcq_question:

                st.warning(
                    "Please enter MCQ."
                )


            else:


                prompt = f"""

Solve this MCQ.

{mcq_question}

Give exactly:

Correct Answer:
Correct Option:
Explanation:

"""

                with st.spinner(
                    "Finding correct answer..."
                ):


                    answer = ask_ai(

                        prompt,

                        mode="Exam Helper"

                    )


                st.markdown(answer)

                voice_controls(answer)


                add_history(

                    "MCQ Answer",

                    mcq_question,

                    answer

                )


    # ========================================================
    # IMPORTANT QUESTIONS
    # ========================================================

    else:


        subject = st.text_input(

            "Enter Subject",

            placeholder=
            "Example: Management"

        )


        topic = st.text_input(

            "Topic (Optional)",

            placeholder=
            "Example: Evolution of Management"

        )


        if st.button(

            "📚 Generate Important Questions",

            use_container_width=True

        ):


            if not subject:

                st.warning(
                    "Please enter subject."
                )


            else:


                prompt = f"""

Give important exam questions.

Subject:

{subject}

Topic:

{topic}

Include:

• 2 Marks Questions
• 5 Marks Questions
• 10 Marks Questions

"""

                with st.spinner(
                    "Generating questions..."
                ):


                    answer = ask_ai(

                        prompt,

                        mode="Exam Helper"

                    )


                st.markdown(answer)

                voice_controls(answer)


                add_history(

                    "Important Questions",

                    subject,

                    answer

                )


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif st.session_state.page == "🔬 Project & Lab Guide":

    st.header(
        "🔬 Project & Lab Guide"
    )


    project_type = st.selectbox(

        "Select Type",

        [

            "Engineering Project",

            "Mini Project",

            "Major Project",

            "Lab Experiment",

            "Circuit Project"

        ]

    )


    project_topic = st.text_input(

        "Project / Experiment Topic",

        placeholder=
        "Example: Automatic Solar Street Light"

    )


    branch = st.selectbox(

        "Branch",

        [

            "Electrical Engineering",

            "Electronics Engineering",

            "Computer Science",

            "Mechanical Engineering",

            "Civil Engineering",

            "Other"

        ]

    )


    if st.button(

        "🔬 Generate Complete Guide",

        use_container_width=True

    ):


        if not project_topic:

            st.warning(
                "Please enter project topic."
            )


        else:


            prompt = f"""

Create a complete guide.

Type:

{project_type}

Topic:

{project_topic}

Branch:

{branch}

Include:

1. Title
2. Aim
3. Introduction
4. Objectives
5. Components Required
6. Block Diagram Description
7. Working Principle
8. Procedure
9. Advantages
10. Disadvantages
11. Applications
12. Result
13. Viva Questions
14. Future Scope

"""


            with st.spinner(
                "Creating complete guide..."
            ):


                answer = ask_ai(

                    prompt,

                    mode="Project & Lab Guide"

                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "Project & Lab Guide",

                project_topic,

                answer

            )


# ============================================================
# GATE PREPARATION
# ============================================================

elif st.session_state.page == "📚 GATE Preparation":

    st.header(
        "📚 GATE Preparation"
    )


    branch = st.selectbox(

        "Select Branch",

        [

            "Electrical Engineering",

            "Electronics Engineering",

            "Computer Science",

            "Mechanical Engineering",

            "Civil Engineering",

            "Instrumentation Engineering",

            "Other"

        ]

    )


    preparation_type = st.selectbox(

        "Select Preparation Type",

        [

            "📖 Explain Concept",

            "🔢 Numerical Problem",

            "🧠 GATE MCQ",

            "📐 Formula",

            "⭐ Important Topics",

            "📅 Study Plan",

            "📝 Practice Questions"

        ]

    )


    gate_question = st.text_area(

        "Enter Topic / Question",

        placeholder=
        "Example: Transformer efficiency"

    )


    if st.button(

        "🚀 Generate GATE Answer",

        use_container_width=True

    ):


        if not gate_question:

            st.warning(
                "Please enter topic or question."
            )


        else:


            prompt = f"""

GATE Branch:

{branch}

Preparation Type:

{preparation_type}

Topic:

{gate_question}

"""

            with st.spinner(
                "Preparing GATE content..."
            ):


                answer = ask_ai(

                    prompt,

                    mode="GATE Preparation"

                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "GATE Preparation",

                gate_question,

                answer

            )


# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.page == "⚙️ Settings":

    st.header(
        "⚙️ Settings"
    )


    # ========================================================
    # LANGUAGE
    # ========================================================

    st.subheader(
        "🌐 Language"
    )


    languages = [

        "English",

        "Telugu",

        "Telugu + English",

        "Hindi"

    ]


    current_language = (
        st.session_state.language
    )


    if current_language not in languages:

        current_language = "English"


    language = st.selectbox(

        "Select AI Answer Language",

        languages,

        index=languages.index(
            current_language
        )

    )


    if st.button(

        "💾 Save Language"

    ):


        st.session_state.language = language


        st.success(
            "Language saved successfully!"
        )


    st.divider()


    # ========================================================
    # AI VOICE
    # ========================================================

    st.subheader(
        "🔊 AI Voice"
    )


    voice = st.toggle(

        "Enable AI Voice",

        value=st.session_state.voice_enabled

    )


    if voice != st.session_state.voice_enabled:

        st.session_state.voice_enabled = voice


    st.caption(
        "Voice controls: Pause and Resume"
    )


    st.divider()


    # ========================================================
    # HISTORY
    # ========================================================

    st.subheader(
        "🕘 History"
    )


    if not st.session_state.history:

        st.info(
            "No history available."
        )


    else:


        st.caption(
            "History remains saved until you clear it."
        )


        for index, item in enumerate(

            st.session_state.history

        ):


            title = (

                f"{index + 1}. "

                f"{item.get('mode', '')} "

                f"• "

                f"{item.get('time', '')}"

            )


            with st.expander(title):


                st.markdown(
                    "### 📝 Question"
                )


                st.write(

                    item.get(
                        "question",
                        ""
                    )

                )


                st.markdown(
                    "### 🤖 Answer"
                )


                st.markdown(

                    item.get(
                        "answer",
                        ""
                    )

                )


    if st.button(

        "🗑️ Clear All History",

        use_container_width=True

    ):


        clear_history()


        st.success(
            "History cleared successfully!"
        )


        st.rerun()


    st.divider()


    # ========================================================
    # APP INFORMATION
    # ========================================================

    st.subheader(
        "📱 App Information"
    )


    st.info("""

🤖 Tech Mithra AI

Features:

💬 AI Chat
🎉 Event Planner
🎓 Exam Helper
🔬 Project & Lab Guide
📚 GATE Preparation
📎 File Upload
📷 Camera
🖼️ Photo Upload
🎤 Voice Input
🔊 AI Voice
⏸️ Pause
▶️ Resume
🕘 History

""")


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🤖 Tech Mithra AI • Your AI Student Assistant"
)
