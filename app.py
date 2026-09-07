# ============================================================
# TECH MITHRA AI PRO - COMPLETE APP
# ============================================================
# INSTALL:
# pip install streamlit google-genai
#
# RUN:
# streamlit run app.py
#
# SECRETS:
# GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
# ============================================================

import streamlit as st
import json
import os
import base64
import mimetypes
from datetime import datetime
from google import genai


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

APP_NAME = "Tech Mithra AI Pro"
HISTORY_FILE = "history.json"

# Change this only if your Gemini model is different
DEFAULT_MODEL = "gemini-2.5-flash"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "mcq_data" not in st.session_state:
    st.session_state.mcq_data = []

if "mcq_answers" not in st.session_state:
    st.session_state.mcq_answers = {}

if "mcq_submitted" not in st.session_state:
    st.session_state.mcq_submitted = False

if "mcq_score" not in st.session_state:
    st.session_state.mcq_score = 0


# ============================================================
# HISTORY FUNCTIONS
# ============================================================

def load_history():

    try:

        if os.path.exists(HISTORY_FILE):

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

    except Exception:
        pass

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

    # Maximum 100 items
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


# Load history only once
if "history_loaded" not in st.session_state:

    st.session_state.history = load_history()

    st.session_state.history_loaded = True


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client():

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


    if not api_key:

        return None


    return genai.Client(
        api_key=api_key
    )


# ============================================================
# GET MODEL
# ============================================================

def get_model():

    try:

        if "GEMINI_MODEL" in st.secrets:

            return st.secrets[
                "GEMINI_MODEL"
            ]

    except Exception:
        pass


    return DEFAULT_MODEL


# ============================================================
# LANGUAGE INSTRUCTION
# ============================================================

def language_instruction():

    return f"""

IMPORTANT LANGUAGE:

Answer in:
{st.session_state.language}

If Telugu is selected,
use clear Telugu.

If Telugu + English is selected,
use both languages naturally.

Keep answers clear,
accurate and useful.

"""


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt, files=None):

    client = get_client()

    if client is None:

        return (
            "❌ GEMINI API KEY NOT FOUND.\n\n"
            "Please add GEMINI_API_KEY "
            "in Streamlit Secrets."
        )


    model = get_model()


    final_prompt = f"""

You are Tech Mithra AI Pro.

You are an intelligent,
friendly AI assistant
for students.

{language_instruction()}

USER REQUEST:

{prompt}

Rules:

1. Answer accurately.

2. Use simple language.

3. Use headings when useful.

4. Use bullet points.

5. For simple questions,
keep answers short.

6. For exam questions,
give proper exam format.

7. Do not add unnecessary text.

"""


    try:

        contents = [final_prompt]


        # Add uploaded files
        if files:

            for uploaded_file in files:

                if uploaded_file is None:
                    continue

                try:

                    file_bytes = (
                        uploaded_file.getvalue()
                    )

                    mime_type = (
                        uploaded_file.type
                    )

                    if not mime_type:

                        mime_type = (
                            mimetypes.guess_type(
                                uploaded_file.name
                            )[0]
                        )

                    if not mime_type:

                        mime_type = (
                            "application/octet-stream"
                        )


                    encoded_data = (
                        base64.b64encode(
                            file_bytes
                        ).decode("utf-8")
                    )


                    contents.append({

                        "inline_data": {

                            "mime_type": mime_type,

                            "data": encoded_data

                        }

                    })


                except Exception:
                    pass


        response = client.models.generate_content(

            model=model,

            contents=contents

        )


        if response and response.text:

            return response.text


        return (
            "❌ AI did not return an answer. "
            "Please try again."
        )


    except Exception as e:

        return (
            "❌ AI Error:\n\n"
            + str(e)
        )


# ============================================================
# VOICE OUTPUT
# PLAY / PAUSE / RESUME / STOP
# ============================================================

def voice_controls(text):

    safe_text = (
        str(text)
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
        .replace("</script>", "")
    )


    html = f"""

    <div style="
        display:flex;
        gap:8px;
        flex-wrap:wrap;
        margin-top:10px;
    ">

        <button onclick="playVoice()"
        style="
            padding:8px 14px;
            border-radius:8px;
            border:none;
            cursor:pointer;
        ">
            🔊 Play
        </button>


        <button onclick="pauseVoice()"
        style="
            padding:8px 14px;
            border-radius:8px;
            border:none;
            cursor:pointer;
        ">
            ⏸️ Pause
        </button>


        <button onclick="resumeVoice()"
        style="
            padding:8px 14px;
            border-radius:8px;
            border:none;
            cursor:pointer;
        ">
            ▶️ Resume
        </button>


        <button onclick="stopVoice()"
        style="
            padding:8px 14px;
            border-radius:8px;
            border:none;
            cursor:pointer;
        ">
            ⏹️ Stop
        </button>

    </div>


    <script>

    var techMithraSpeech = null;


    function playVoice() {{

        window.speechSynthesis.cancel();

        techMithraSpeech =
        new SpeechSynthesisUtterance(
            `{safe_text}`
        );

        techMithraSpeech.rate = 1;

        techMithraSpeech.pitch = 1;

        window.speechSynthesis.speak(
            techMithraSpeech
        );

    }}


    function pauseVoice() {{

        if (
            window.speechSynthesis.speaking
        ) {{

            window.speechSynthesis.pause();

        }}

    }}


    function resumeVoice() {{

        if (
            window.speechSynthesis.paused
        ) {{

            window.speechSynthesis.resume();

        }}

    }}


    function stopVoice() {{

        window.speechSynthesis.cancel();

    }}

    </script>

    """


    st.components.v1.html(
        html,
        height=65
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI")

    st.caption(
        "AI-Powered Student Assistant"
    )

    st.divider()


    menu_items = [

        "💬 AI Chat",

        "🔬 Project & Lab Guide",

        "🎉 Event Planner",

        "📚 Exam Hacker",

        "🎓 GATE Preparation",

        "💼 Placement Prep",

        "⚙️ Settings"

    ]


    selected = st.radio(

        "Choose Feature",

        menu_items

    )


    st.divider()

    st.caption(
        "🚀 Tech Mithra AI Pro"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🚀 Tech Mithra AI Pro'
    '</div>',

    unsafe_allow_html=True
)


# ============================================================
# AI CHAT
# ============================================================

if selected == "💬 AI Chat":

    st.markdown(
        '<div class="subtitle">'
        'Ask anything like ChatGPT'
        '</div>',

        unsafe_allow_html=True
    )


    # ========================================================
    # DISPLAY CHAT
    # ========================================================

    for message in st.session_state.chat_messages:


        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


            if message["role"] == "assistant":

                voice_controls(
                    message["content"]
                )


    # ========================================================
    # ATTACHMENTS
    # ========================================================

    uploaded_items = []


    with st.expander(
        "➕ Attachments"
    ):


        upload_photo = st.file_uploader(

            "🖼️ Upload Photo",

            type=[

                "png",

                "jpg",

                "jpeg",

                "webp"

            ],

            key="chat_photo"

        )


        camera_photo = st.camera_input(
            "📷 Take Photo"
        )


        upload_file = st.file_uploader(

            "📁 Upload File",

            type=[

                "txt",

                "pdf",

                "csv",

                "json",

                "py",

                "java",

                "c",

                "cpp",

                "html",

                "css",

                "js",

                "md"

            ],

            key="chat_file"

        )


        if upload_photo:

            uploaded_items.append(
                upload_photo
            )


        if camera_photo:

            uploaded_items.append(
                camera_photo
            )


        if upload_file:

            uploaded_items.append(
                upload_file
            )


    # ========================================================
    # MICROPHONE
    # ========================================================

    st.markdown("### 🎤 Voice Question")


    audio_file = st.audio_input(
        "Speak your question"
    )


    if audio_file:

        st.audio(audio_file)


        if st.button(
            "🎤 Ask AI Using Voice",
            use_container_width=True
        ):


            voice_prompt = """

The user uploaded an audio recording.

Listen to the audio carefully.

Understand the question.

Answer the question clearly.

"""


            with st.spinner(
                "🎤 Understanding your voice..."
            ):

                answer = ask_ai(

                    voice_prompt,

                    [audio_file]

                )


            st.session_state.chat_messages.append({

                "role": "user",

                "content":
                "🎤 Voice Question"

            })


            st.session_state.chat_messages.append({

                "role": "assistant",

                "content": answer

            })


            add_history(

                "Voice AI Chat",

                "🎤 Voice Question",

                answer

            )


            st.rerun()


    # ========================================================
    # CHAT INPUT
    # ========================================================

    user_prompt = st.chat_input(
        "Ask anything..."
    )


    if user_prompt:


        # USER MESSAGE

        st.session_state.chat_messages.append({

            "role": "user",

            "content": user_prompt

        })


        with st.chat_message("user"):

            st.markdown(
                user_prompt
            )


        # AI MESSAGE

        with st.chat_message("assistant"):


            with st.spinner(
                "🤖 Thinking..."
            ):

                answer = ask_ai(

                    user_prompt,

                    uploaded_items

                )


            st.markdown(
                answer
            )


            voice_controls(
                answer
            )


        st.session_state.chat_messages.append({

            "role": "assistant",

            "content": answer

        })


        add_history(

            "AI Chat",

            user_prompt,

            answer

        )


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif selected == "🔬 Project & Lab Guide":


    st.header(
        "🔬 Project & Lab Guide"
    )


    topic = st.text_input(

        "Project / Lab Topic",

        placeholder=
        "Example: Automatic Solar Street Light"

    )


    if st.button(

        "🚀 Generate Complete Guide",

        use_container_width=True

    ):


        if not topic:

            st.warning(
                "⚠️ Please enter a topic."
            )


        else:


            prompt = f"""

Create a complete
engineering project guide.

TOPIC:

{topic}

Include:

1. Title

2. Aim

3. Introduction

4. Objectives

5. Components Required

6. Block Diagram

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
                "🔬 Creating guide..."
            ):

                answer = ask_ai(
                    prompt
                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "Project & Lab Guide",

                topic,

                answer

            )


# ============================================================
# EVENT PLANNER
# ============================================================

elif selected == "🎉 Event Planner":


    st.header(
        "🎉 Event Planner"
    )


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


    audience = st.text_input(
        "Target Audience"
    )


    if st.button(

        "🎯 Generate Event Plan",

        use_container_width=True

    ):


        if not event_name:

            st.warning(
                "⚠️ Please enter event name."
            )


        else:


            prompt = f"""

Create a complete event plan.

Event Name:

{event_name}

Event Type:

{event_type}

Audience:

{audience}

Include:

1. Objective

2. Theme

3. Schedule

4. Registration

5. Volunteers

6. Stage Setup

7. Materials

8. Budget

9. Promotion

10. Social Media

11. Prizes

12. Certificates

13. Safety

14. Final Checklist

"""


            with st.spinner(
                "🎉 Creating event plan..."
            ):

                answer = ask_ai(
                    prompt
                )


            st.markdown(answer)

            voice_controls(answer)


            add_history(

                "Event Planner",

                event_name,

                answer

            )


# ============================================================
# EXAM HACKER
# ============================================================

elif selected == "📚 Exam Hacker":


    st.header(
        "📚 Exam Hacker"
    )


    tab1, tab2 = st.tabs(

        [

            "✍️ Answer Generator",

            "🧠 MCQ Quiz"

        ]

    )


    # ========================================================
    # ANSWER GENERATOR
    # ========================================================

    with tab1:


        question = st.text_area(
            "Enter your Question"
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

Marks:

{marks}

Generate an exam-ready answer.

Use:

- Clear headings

- Important points

- Simple language

- Proper exam format

"""


                with st.spinner(
                    "✍️ Writing answer..."
                ):

                    answer = ask_ai(
                        prompt
                    )


                st.markdown(answer)

                voice_controls(answer)


                add_history(

                    "Exam Answer",

                    question,

                    answer

                )


    # ========================================================
    # MCQ QUIZ
    # ========================================================

    with tab2:


        mcq_topic = st.text_input(
            "MCQ Topic"
        )


        mcq_count = st.selectbox(

            "Number of Questions",

            [

                5,

                10,

                15,

                20

            ]

        )


        if st.button(
            "🎯 Generate MCQs",
            use_container_width=True
        ):


            if not mcq_topic:

                st.warning(
                    "Enter MCQ topic."
                )


            else:


                prompt = f"""

Create exactly
{mcq_count}
MCQs.

Topic:

{mcq_topic}

Return ONLY JSON.

Format:

[
    {{
        "question": "Question",

        "options": {{
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
        }},

        "answer": "A",

        "explanation":
        "Explanation"
    }}
]

"""


                with st.spinner(
                    "🧠 Generating MCQs..."
                ):

                    raw_answer = ask_ai(
                        prompt
                    )


                try:


                    clean = raw_answer.strip()

                    clean = clean.replace(
                        "```json",
                        ""
                    )

                    clean = clean.replace(
                        "```",
                        ""
                    )


                    start = clean.find("[")
                    end = clean.rfind("]")


                    if (
                        start != -1
                        and end != -1
                    ):

                        clean = clean[
                            start:end + 1
                        ]


                    st.session_state.mcq_data = (
                        json.loads(clean)
                    )


                    st.session_state.mcq_answers = {}


                    st.session_state.mcq_submitted = False


                    st.success(
                        "✅ MCQs Generated!"
                    )


                except Exception:

                    st.error(
                        "❌ MCQ generation failed. "
                        "Please try again."
                    )


        # DISPLAY MCQS

        if st.session_state.mcq_data:


            st.divider()


            for index, mcq in enumerate(

                st.session_state.mcq_data

            ):


                st.markdown(

                    f"### Q{index + 1}. "
                    f"{mcq.get('question', '')}"

                )


                options = mcq.get(
                    "options",
                    {}
                )


                selected_answer = st.radio(

                    "Select Answer",

                    ["A", "B", "C", "D"],

                    format_func=lambda x:

                    f"{x}. "
                    f"{options.get(x, '')}",

                    key=f"mcq_{index}"

                )


                st.session_state.mcq_answers[
                    index
                ] = selected_answer


            if st.button(
                "✅ Submit Quiz",
                use_container_width=True
            ):


                score = 0


                for index, mcq in enumerate(

                    st.session_state.mcq_data

                ):


                    correct = str(

                        mcq.get(
                            "answer",
                            ""
                        )

                    ).upper()


                    selected_answer = str(

                        st.session_state.mcq_answers.get(

                            index,
                            ""

                        )

                    ).upper()


                    if selected_answer == correct:

                        score += 1


                st.session_state.mcq_score = score

                st.session_state.mcq_submitted = True


        # RESULTS

        if st.session_state.mcq_submitted:


            total = len(
                st.session_state.mcq_data
            )


            score = (
                st.session_state.mcq_score
            )


            st.divider()


            st.success(

                f"🏆 Your Score: "
                f"{score}/{total}"

            )


            for index, mcq in enumerate(

                st.session_state.mcq_data

            ):


                correct = str(

                    mcq.get(
                        "answer",
                        ""
                    )

                ).upper()


                selected_answer = str(

                    st.session_state.mcq_answers.get(

                        index,
                        ""

                    )

                ).upper()


                st.markdown(
                    f"### Q{index + 1}"
                )


                if selected_answer == correct:

                    st.success(
                        f"✅ Correct: {correct}"
                    )

                else:

                    st.error(
                        f"❌ Correct Answer: "
                        f"{correct}"
                    )


                st.info(

                    "💡 "
                    + mcq.get(
                        "explanation",
                        ""
                    )

                )


# ============================================================
# GATE PREPARATION
# ============================================================

elif selected == "🎓 GATE Preparation":


    st.header(
        "🎓 GATE Preparation"
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


    gate_type = st.selectbox(

        "Preparation Type",

        [

            "Study Plan",

            "Topic Explanation",

            "Important Questions",

            "MCQ Practice",

            "Formula Sheet",

            "Revision Notes",

            "Mock Test"

        ]

    )


    topic = st.text_input(
        "Topic"
    )


    if st.button(

        "🎓 Generate GATE Content",

        use_container_width=True

    ):


        prompt = f"""

You are a GATE expert.

Branch:

{branch}

Preparation Type:

{gate_type}

Topic:

{topic}

Create high-quality
GATE preparation content.

Make it:

- Exam focused

- Accurate

- Easy to understand

- Useful for students

"""


        with st.spinner(
            "🎓 Preparing..."
        ):

            answer = ask_ai(
                prompt
            )


        st.markdown(answer)

        voice_controls(answer)


        add_history(

            "GATE Preparation",

            f"{branch} - {topic}",

            answer

        )


# ============================================================
# PLACEMENT PREP
# ============================================================

elif selected == "💼 Placement Prep":


    st.header(
        "💼 Placement Preparation"
    )


    role = st.selectbox(

        "Target Role",

        [

            "Software Engineer",

            "Electrical Engineer",

            "Electronics Engineer",

            "Data Analyst",

            "AI / ML Engineer",

            "Embedded Engineer",

            "PLC Engineer",

            "Other"

        ]

    )


    prep_type = st.selectbox(

        "Preparation Type",

        [

            "Interview Questions",

            "Technical Questions",

            "HR Questions",

            "Aptitude",

            "Resume Help",

            "Mock Interview"

        ]

    )


    topic = st.text_input(
        "Topic / Question"
    )


    if st.button(

        "🚀 Start Preparation",

        use_container_width=True

    ):


        prompt = f"""

You are a placement trainer.

Target Role:

{role}

Preparation Type:

{prep_type}

Topic:

{topic}

Create placement preparation content.

Include:

1. Important concepts

2. Questions

3. Answers

4. Interview tips

5. Common mistakes

6. Practice questions

"""


        with st.spinner(
            "💼 Preparing..."
        ):

            answer = ask_ai(
                prompt
            )


        st.markdown(answer)

        voice_controls(answer)


        add_history(

            "Placement Preparation",

            topic,

            answer

        )


# ============================================================
# SETTINGS
# ============================================================

elif selected == "⚙️ Settings":


    st.header(
        "⚙️ Settings"
    )


    # ========================================================
    # LANGUAGE SETTINGS ONLY
    # ========================================================

    with st.expander(

        "🌐 Language",

        expanded=True

    ):


        languages = [

            "English",

            "Telugu",

            "Telugu + English",

            "Hindi"

        ]


        current_index = 0


        if (
            st.session_state.language
            in languages
        ):

            current_index = languages.index(

                st.session_state.language

            )


        selected_language = st.selectbox(

            "Select Answer Language",

            languages,

            index=current_index

        )


        if st.button(
            "💾 Save Language",
            use_container_width=True
        ):


            st.session_state.language = (
                selected_language
            )


            st.success(
                "✅ Language saved successfully!"
            )


    # ========================================================
    # HISTORY
    # ========================================================

    st.divider()


    st.subheader(
        "🕘 History"
    )


    if not st.session_state.history:


        st.info(
            "📭 No history available."
        )


    else:


        st.caption(
            "History will remain saved "
            "until you clear it."
        )


        for i, item in enumerate(

            st.session_state.history

        ):


            title = (

                f"{i + 1}. "

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
            "✅ History cleared successfully!"
        )


        st.rerun()


    # ========================================================
    # APP INFORMATION
    # ========================================================

    st.divider()


    with st.expander(
        "📱 App Information"
    ):


        st.write(
            "### 🚀 Tech Mithra AI Pro"
        )


        st.write(
            """
Features:

💬 AI Chat

📎 Upload Photo

📷 Camera

📁 File Upload

🎤 Voice Input

🔊 Voice Output

⏸️ Pause Voice

▶️ Resume Voice

⏹️ Stop Voice

🔬 Project & Lab Guide

🎉 Event Planner

📚 Exam Hacker

🧠 MCQ Quiz

🎓 GATE Preparation

💼 Placement Preparation

🌐 Language

🕘 History
"""
        )


    st.divider()


    st.info(
        "🔒 Do not enter passwords, "
        "bank details or sensitive "
        "personal information."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🚀 Tech Mithra AI Pro • "
    "AI-Powered Student Assistant"
)
