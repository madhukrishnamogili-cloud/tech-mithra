# ============================================================
# TECH MITHRA AI - COMPLETE APP
# Save as: app.py
#
# INSTALL:
# pip install streamlit google-genai
#
# RUN:
# streamlit run app.py
#
# STREAMLIT SECRETS:
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
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
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

HISTORY_FILE = "tech_mithra_history.json"


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
}

.sub-title {
    color: gray;
    font-size: 17px;
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

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""


# ============================================================
# HISTORY
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
# GEMINI API KEY
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
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client():

    if genai is None:
        return None

    api_key = get_api_key()

    if not api_key:
        return None

    try:
        return genai.Client(
            api_key=api_key
        )

    except Exception:
        return None


# ============================================================
# LANGUAGE
# ============================================================

def language_instruction():

    if st.session_state.language == "Telugu":

        return """
Answer in Telugu.
Use simple and clear Telugu.
"""

    elif st.session_state.language == "Telugu + English":

        return """
Answer using Telugu and English.
Use English technical terms where necessary.
"""

    elif st.session_state.language == "Hindi":

        return """
Answer in Hindi.
"""

    return """
Answer in clear English.
"""


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(question, mode="General", files=None):

    client = get_client()

    if client is None:

        return """
❌ Gemini API Key not configured.

Add your API Key in Streamlit Secrets:

GEMINI_API_KEY = "YOUR_API_KEY"
"""


    mode_instruction = ""


    if mode == "Exam Helper":

        mode_instruction = """
You are an expert exam preparation assistant.

Give exam-ready answers.

For MCQs clearly provide:

Correct Answer:
Correct Option:
Explanation:
"""


    elif mode == "GATE Preparation":

        mode_instruction = """
You are an expert GATE preparation assistant.

For numerical problems use:

1. Given Data
2. Formula
3. Calculation
4. Final Answer

Give accurate engineering explanations.
"""


    elif mode == "Project & Lab Guide":

        mode_instruction = """
You are an Engineering Project and Lab Guide.

Provide practical and detailed guidance.

Include where relevant:

Title
Aim
Objective
Components
Working Principle
Procedure
Result
Applications
Viva Questions
"""


    elif mode == "Event Planner":

        mode_instruction = """
You are an Event Planning Assistant.

Create organized and practical event plans.

Include:

Event Objective
Schedule
Team
Materials
Budget
Promotion
Checklist
"""


    else:

        mode_instruction = """
You are a helpful AI assistant.

Give accurate answers.

Use simple explanations.
Use headings and bullet points when useful.
"""


    prompt = f"""
You are Tech Mithra AI.

{language_instruction()}

{mode_instruction}

User Question:

{question}

Give a direct and useful answer.
"""


    try:

        contents = [prompt]


        if files:

            for file in files:

                if file is not None:
                    contents.append(file)


        models = [

            "gemini-2.5-flash",
            "gemini-2.0-flash"

        ]


        last_error = ""


        for model_name in models:

            try:

                response = (
                    client.models.generate_content(
                        model=model_name,
                        contents=contents
                    )
                )


                if response and response.text:
                    return response.text


            except Exception as e:
                last_error = str(e)


        return "❌ AI Error:\n\n" + last_error


    except Exception as e:

        return "❌ Error:\n\n" + str(e)


# ============================================================
# AUDIO TO TEXT
# ============================================================

def audio_to_text(audio_file):

    client = get_client()

    if client is None:

        return (
            "❌ Gemini API Key not configured."
        )


    try:

        prompt = """
Listen carefully to the uploaded audio.

Convert the spoken words into text.

IMPORTANT:

Return ONLY the spoken text.

Do not answer the question.

Do not explain anything.

Do not add extra words.
"""


        models = [

            "gemini-2.5-flash",
            "gemini-2.0-flash"

        ]


        last_error = ""


        for model_name in models:

            try:

                response = (
                    client.models.generate_content(

                        model=model_name,

                        contents=[
                            prompt,
                            audio_file
                        ]

                    )
                )


                if response and response.text:

                    return response.text


            except Exception as e:

                last_error = str(e)


        return (
            "❌ Audio conversion failed:\n\n"
            + last_error
        )


    except Exception as e:

        return (
            "❌ Audio Error:\n\n"
            + str(e)
        )


# ============================================================
# VOICE OUTPUT
# PAUSE + RESUME
# ============================================================

def voice_controls(text):

    if not st.session_state.voice_enabled:
        return


    safe_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "'")
        .replace("${", "")
        .replace("</script>", "")
        .replace("\n", " ")
    )


    html = f"""
<div>

<button onclick="startSpeech()"
style="
padding:8px 15px;
border-radius:8px;
cursor:pointer;
margin-right:8px;
">
🔊 Speak
</button>

<button onclick="pauseSpeech()"
style="
padding:8px 15px;
border-radius:8px;
cursor:pointer;
margin-right:8px;
">
⏸️ Pause
</button>

<button onclick="resumeSpeech()"
style="
padding:8px 15px;
border-radius:8px;
cursor:pointer;
">
▶️ Resume
</button>

<script>

let speechStarted = false;

function startSpeech() {{

    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance();

    speech.text =
        `{safe_text}`;

    speech.rate = 1;

    speech.pitch = 1;

    window.speechSynthesis.speak(
        speech
    );

    speechStarted = true;
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
        height=65
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.caption(
        "AI Student Assistant"
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

    )


    st.session_state.page = selected_page


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


    # DISPLAY CHAT

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ========================================================
    # ATTACHMENTS
    # ========================================================

    with st.expander(
        "➕ Upload Options"
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
    # AUDIO INPUT
    # ========================================================

    st.markdown("### 🎤 Voice Input")


    audio_file = st.audio_input(
        "Record your question"
    )


    if audio_file:

        st.audio(audio_file)


        if st.button(

            "🔄 Convert Voice to Text",

            use_container_width=True

        ):


            with st.spinner(
                "🎤 Converting voice to text..."
            ):


                converted_text = audio_to_text(
                    audio_file
                )


            if not converted_text.startswith("❌"):

                st.session_state.voice_text = (
                    converted_text
                )


                st.success(
                    "✅ Voice converted to text!"
                )

            else:

                st.error(
                    converted_text
                )


    # SHOW CONVERTED TEXT

    if st.session_state.voice_text:


        st.markdown(
            "### 📝 Your Voice Text"
        )


        voice_question = st.text_area(

            "Edit your question if needed",

            value=st.session_state.voice_text,

            height=100,

            key="voice_question_text"

        )


        if st.button(

            "🤖 Ask AI from Voice Text",

            use_container_width=True

        ):


            if voice_question.strip():


                with st.spinner(
                    "🤖 Thinking..."
                ):


                    answer = ask_ai(
                        voice_question,
                        mode="General"
                    )


                st.session_state.chat_messages.append({

                    "role": "user",

                    "content": voice_question

                })


                st.session_state.chat_messages.append({

                    "role": "assistant",

                    "content": answer

                })


                add_history(

                    "AI Chat Voice",

                    voice_question,

                    answer

                )


                st.session_state.voice_text = ""


                st.rerun()


    # ========================================================
    # TEXT CHAT
    # ========================================================

    question = st.chat_input(
        "Message Tech Mithra AI..."
    )


    if question:


        files = []


        if uploaded_photo:
            files.append(uploaded_photo)

        if camera_photo:
            files.append(camera_photo)

        if uploaded_file:
            files.append(uploaded_file)


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

                    mode="General",

                    files=files

                )


            st.markdown(answer)

            voice_controls(answer)


        st.session_state.chat_messages.append({

            "role": "assistant",

            "content": answer

        })


        add_history(

            "AI Chat",

            question,

            answer

        )


# ============================================================
# EVENT PLANNER
# ============================================================

elif st.session_state.page == "🎉 Event Planner":

    st.header("🎉 Event Planner")


    event_name = st.text_input(
        "Event Name"
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
        "Expected Participants"
    )


    details = st.text_area(
        "Additional Details"
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


            prompt = f"""

Event Name:
{event_name}

Event Type:
{event_type}

Participants:
{participants}

Details:
{details}

Create a complete event plan.

"""


            with st.spinner(
                "Creating event plan..."
            ):


                answer = ask_ai(

                    prompt,

                    mode="Event Planner"

                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "Event Planner",

                event_name,

                answer

            )


# ============================================================
# EXAM HELPER
# ============================================================

elif st.session_state.page == "🎓 Exam Helper":

    st.header("🎓 Exam Helper")


    exam_option = st.radio(

        "Choose Option",

        [

            "📝 Answer Generator",

            "🧠 MCQ Answer",

            "📚 Important Questions"

        ],

        horizontal=True

    )


    # ANSWER GENERATOR

    if exam_option == "📝 Answer Generator":


        question = st.text_area(
            "Enter Question"
        )


        marks = st.selectbox(

            "Marks",

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
                    "Please enter question."
                )


            else:


                prompt = f"""

Question:

{question}

Answer Length:

{marks}

Write an exam-ready answer.

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


    # MCQ ANSWER

    elif exam_option == "🧠 MCQ Answer":


        mcq = st.text_area(
            "Enter MCQ"
        )


        if st.button(

            "🧠 Get Correct Answer",

            use_container_width=True

        ):


            if not mcq:

                st.warning(
                    "Please enter MCQ."
                )


            else:


                prompt = f"""

Solve this MCQ:

{mcq}

Give:

Correct Answer:
Correct Option:
Explanation:

"""


                with st.spinner(
                    "Finding answer..."
                ):


                    answer = ask_ai(

                        prompt,

                        mode="Exam Helper"

                    )


                st.markdown(answer)

                voice_controls(answer)


                add_history(

                    "MCQ Answer",

                    mcq,

                    answer

                )


    # IMPORTANT QUESTIONS

    else:


        subject = st.text_input(
            "Subject"
        )


        topic = st.text_input(
            "Topic (Optional)"
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

2 Marks Questions
5 Marks Questions
10 Marks Questions

"""


                with st.spinner(
                    "Generating..."
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

        "Project Type",

        [

            "Engineering Project",

            "Mini Project",

            "Major Project",

            "Lab Experiment",

            "Circuit Project"

        ]

    )


    topic = st.text_input(
        "Project / Lab Topic"
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


        if not topic:

            st.warning(
                "Please enter topic."
            )


        else:


            prompt = f"""

Project Type:

{project_type}

Topic:

{topic}

Branch:

{branch}

Create a complete guide.

"""


            with st.spinner(
                "Creating guide..."
            ):


                answer = ask_ai(

                    prompt,

                    mode="Project & Lab Guide"

                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "Project & Lab Guide",

                topic,

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

        "Branch",

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

        "Preparation Type",

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
        "Topic / Question"
    )


    if st.button(

        "🚀 Generate GATE Answer",

        use_container_width=True

    ):


        if not gate_question:

            st.warning(
                "Please enter topic."
            )


        else:


            prompt = f"""

Branch:

{branch}

Preparation Type:

{preparation_type}

Question:

{gate_question}

"""


            with st.spinner(
                "Preparing..."
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

    st.header("⚙️ Settings")


    # LANGUAGE

    st.subheader("🌐 Language")


    languages = [

        "English",

        "Telugu",

        "Telugu + English",

        "Hindi"

    ]


    current = (
        st.session_state.language
    )


    if current not in languages:
        current = "English"


    language = st.selectbox(

        "Select Language",

        languages,

        index=languages.index(current)

    )


    if st.button(
        "💾 Save Language"
    ):

        st.session_state.language = language

        st.success(
            "Language saved!"
        )


    st.divider()


    # VOICE

    st.subheader("🔊 AI Voice")


    voice_enabled = st.toggle(

        "Enable AI Voice",

        value=
        st.session_state.voice_enabled

    )


    st.session_state.voice_enabled = (
        voice_enabled
    )


    st.caption(
        "Controls: ⏸️ Pause and ▶️ Resume"
    )


    st.divider()


    # HISTORY

    st.subheader("🕘 History")


    if not st.session_state.history:

        st.info(
            "No history available."
        )


    else:


        st.caption(
            "History stays saved until you clear it."
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
            "History cleared!"
        )

        st.rerun()


    st.divider()


    # APP INFORMATION

    st.subheader(
        "📱 App Information"
    )


    st.info("""

🤖 Tech Mithra AI

Available Features:

💬 AI Chat
🎉 Event Planner
🎓 Exam Helper
🔬 Project & Lab Guide
📚 GATE Preparation
⚙️ Settings

AI Chat Features:

🖼️ Photo Upload
📷 Camera
📁 File Upload
🎤 Voice Input
📝 Voice to Text
🔊 AI Voice
⏸️ Pause
▶️ Resume

📜 History

""")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 Tech Mithra AI • Your AI Student Assistant"
)
