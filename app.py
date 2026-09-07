import streamlit as st
import requests
import base64
import json
import os
import mimetypes
from datetime import datetime
import streamlit.components.v1 as components

# =========================================================
# TECH MITHRA AI - COMPLETE ONE FILE APP
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# FILES
# =========================================================

HISTORY_FILE = "tech_mithra_history.json"
SETTINGS_FILE = "tech_mithra_settings.json"


# =========================================================
# DEFAULT SETTINGS
# =========================================================

DEFAULT_SETTINGS = {
    "api_key": "",
    "model": "gemini-3.6-flash",
    "language": "English",
    "voice": True
}


# =========================================================
# LOAD SETTINGS
# =========================================================

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key, value in DEFAULT_SETTINGS.items():
                if key not in data:
                    data[key] = value

            return data

        except:
            return DEFAULT_SETTINGS.copy()

    return DEFAULT_SETTINGS.copy()


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# =========================================================
# LOAD HISTORY
# =========================================================

def load_history():

    if os.path.exists(HISTORY_FILE):

        try:

            with open(HISTORY_FILE, "r", encoding="utf-8") as f:

                return json.load(f)

        except:

            return []

    return []


# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(history):

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# CLEAR HISTORY
# =========================================================

def clear_history():

    if os.path.exists(HISTORY_FILE):

        os.remove(HISTORY_FILE)

    st.session_state.history = []


# =========================================================
# SESSION STATE
# =========================================================

if "settings" not in st.session_state:

    st.session_state.settings = load_settings()


if "history" not in st.session_state:

    st.session_state.history = load_history()


if "current_answer" not in st.session_state:

    st.session_state.current_answer = ""


if "page" not in st.session_state:

    st.session_state.page = "Ask AI"


# =========================================================
# CSS
# =========================================================

st.markdown("""

<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 45px;
    font-weight: 800;
    margin-bottom: 0px;
}

.sub-title {
    color: gray;
    font-size: 18px;
    margin-bottom: 25px;
}

.answer-box {
    padding: 20px;
    border-radius: 15px;
    background-color: rgba(100,100,100,0.08);
    margin-top: 15px;
}

.history-question {
    font-weight: bold;
}

.stButton button {
    border-radius: 10px;
}

</style>

""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">💬 Tech Mithra AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Ask anything • Upload Photo • Camera • Files • Exam Helper'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.divider()

    if st.button(
        "💬 Ask AI",
        use_container_width=True
    ):
        st.session_state.page = "Ask AI"


    if st.button(
        "🎓 Exam Helper",
        use_container_width=True
    ):
        st.session_state.page = "Exam Helper"


    if st.button(
        "📚 GATE Preparation",
        use_container_width=True
    ):
        st.session_state.page = "GATE Preparation"


    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):
        st.session_state.page = "Settings"


    st.divider()

    st.caption("Tech Mithra AI")


# =========================================================
# FILE TO BASE64
# =========================================================

def file_to_base64(uploaded_file):

    try:

        file_bytes = uploaded_file.getvalue()

        encoded = base64.b64encode(
            file_bytes
        ).decode("utf-8")

        return encoded

    except:

        return None


# =========================================================
# GEMINI API
# =========================================================

def ask_gemini(
    question,
    files=None,
    mode="normal"
):

    settings = st.session_state.settings

    api_key = settings.get(
        "api_key",
        ""
    ).strip()

    model = settings.get(
        "model",
        "gemini-3.6-flash"
    ).strip()


    # -----------------------------------------------------
    # API KEY CHECK
    # -----------------------------------------------------

    if not api_key:

        return (
            "⚠️ API Key not set.\n\n"
            "Go to ⚙️ Settings → API Key "
            "and enter your Gemini API Key."
        )


    # -----------------------------------------------------
    # URL
    # -----------------------------------------------------

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        + model
        + ":generateContent?key="
        + api_key
    )


    # -----------------------------------------------------
    # LANGUAGE
    # -----------------------------------------------------

    language = settings.get(
        "language",
        "English"
    )


    # -----------------------------------------------------
    # MODE PROMPTS
    # -----------------------------------------------------

    if mode == "exam":

        system_prompt = f"""

You are Tech Mithra AI Exam Helper.

Answer in {language}.

Help students prepare for examinations.

If the question is an MCQ:

1. Give the correct answer.
2. Clearly mention the option.
3. Give a short explanation.

If it is a theory question:

1. Give a clear answer.
2. Use headings.
3. Use simple language.
4. Give important points.
5. Make it useful for exam writing.

Do not give unnecessarily complicated answers.

"""

    elif mode == "gate":

        system_prompt = f"""

You are Tech Mithra AI GATE Preparation Assistant.

Answer in {language}.

Help students with:

• GATE concepts
• Numerical problems
• Engineering subjects
• Important formulas
• Shortcuts
• MCQs
• Previous question concepts

Explain step by step.

For numerical problems:

1. Given data
2. Formula
3. Calculation
4. Final answer

Keep answers student-friendly.

"""

    else:

        system_prompt = f"""

You are Tech Mithra AI.

Answer in {language}.

Give accurate, clear and helpful answers.

For study questions:

• Explain simply.
• Use headings.
• Use bullet points.
• Give examples when needed.

If the user asks an MCQ:

Clearly mention:

Correct Answer:
Option:

Then explain briefly.

"""


    # -----------------------------------------------------
    # CONTENT
    # -----------------------------------------------------

    contents = []

    contents.append({
        "text": system_prompt
    })


    contents.append({
        "text": question
    })


    # -----------------------------------------------------
    # ADD FILES
    # -----------------------------------------------------

    if files:

        for uploaded_file in files:

            if uploaded_file is None:

                continue


            try:

                file_data = (
                    uploaded_file.getvalue()
                )

                encoded_file = (
                    base64.b64encode(
                        file_data
                    )
                    .decode("utf-8")
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


                contents.append({

                    "inline_data": {

                        "mime_type": mime_type,

                        "data": encoded_file

                    }

                })

            except:

                pass


    # -----------------------------------------------------
    # REQUEST BODY
    # -----------------------------------------------------

    data = {

        "contents": [

            {

                "parts": contents

            }

        ],

        "generationConfig": {

            "temperature": 0.7,

            "maxOutputTokens": 4096

        }

    }


    # -----------------------------------------------------
    # API REQUEST
    # -----------------------------------------------------

    try:

        response = requests.post(

            url,

            headers={
                "Content-Type":
                "application/json"
            },

            json=data,

            timeout=60

        )


        # -------------------------------------------------
        # ERROR
        # -------------------------------------------------

        if response.status_code != 200:

            try:

                error_data = response.json()

                error_message = (
                    error_data
                    .get("error", {})
                    .get(
                        "message",
                        "Unknown API error"
                    )
                )

            except:

                error_message = response.text


            return (

                f"❌ AI Error ({response.status_code})\n\n"

                f"{error_message}\n\n"

                "Check:\n"

                "1. API Key\n"
                "2. Model Name\n"
                "3. Internet Connection\n"

            )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        result = response.json()


        try:

            answer = (

                result["candidates"][0]
                ["content"]["parts"][0]
                ["text"]

            )

            return answer


        except:

            return (

                "❌ AI returned an unexpected response.\n\n"

                + str(result)

            )


    except requests.exceptions.Timeout:

        return (

            "⚠️ Request timed out.\n\n"

            "Please try again."

        )


    except requests.exceptions.ConnectionError:

        return (

            "⚠️ Internet connection problem.\n\n"

            "Please check your internet."

        )


    except Exception as e:

        return (

            "❌ Error:\n\n"

            + str(e)

        )


# =========================================================
# SAVE QUESTION TO HISTORY
# =========================================================

def add_to_history(
    question,
    answer,
    page
):

    item = {

        "question": question,

        "answer": answer,

        "page": page,

        "time": datetime.now()
        .strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    }


    st.session_state.history.insert(
        0,
        item
    )


    save_history(
        st.session_state.history
    )


# =========================================================
# VOICE PLAYER
# PAUSE + RESUME ONLY
# =========================================================

def voice_player(text):

    clean_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )


    html_code = f"""

    <div style="
        margin-top:10px;
        margin-bottom:10px;
    ">

        <button
            onclick="pauseSpeech()"
            style="
                padding:10px 20px;
                margin-right:10px;
                border-radius:8px;
                border:none;
                cursor:pointer;
                font-size:16px;
            "
        >
            ⏸️ Pause
        </button>


        <button
            onclick="resumeSpeech()"
            style="
                padding:10px 20px;
                border-radius:8px;
                border:none;
                cursor:pointer;
                font-size:16px;
            "
        >
            ▶️ Resume
        </button>

    </div>


    <script>

    const textToSpeak = `{clean_text}`;

    let speechStarted = false;


    function startSpeech() {{

        if (
            !speechStarted
        ) {{

            const speech = new SpeechSynthesisUtterance(
                textToSpeak
            );

            speech.lang = "en-US";

            speech.rate = 1;

            speech.pitch = 1;

            window.speechSynthesis.speak(
                speech
            );

            speechStarted = true;

        }}

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
            !speechStarted
        ) {{

            startSpeech();

        }}

        else {{

            window.speechSynthesis.resume();

        }}

    }}

    </script>

    """


    components.html(
        html_code,
        height=80
    )


# =========================================================
# ASK AI PAGE
# =========================================================

if st.session_state.page == "Ask AI":

    st.subheader(
        "💬 Ask AI"
    )


    # -----------------------------------------------------
    # QUESTION
    # -----------------------------------------------------

    question = st.text_area(

        "Ask your question",

        placeholder=
        "Ask anything...",

        height=100,

        label_visibility="collapsed"

    )


    # -----------------------------------------------------
    # PLUS OPTIONS
    # -----------------------------------------------------

    with st.expander(
        "➕ Upload Options"
    ):


        col1, col2, col3 = st.columns(3)


        with col1:

            uploaded_photo = (
                st.file_uploader(

                    "🖼️ Upload Photo",

                    type=[
                        "jpg",
                        "jpeg",
                        "png",
                        "webp"
                    ],

                    key="photo_upload"

                )
            )


        with col2:

            camera_photo = (
                st.camera_input(

                    "📷 Camera"

                )
            )


        with col3:

            uploaded_file = (
                st.file_uploader(

                    "📁 Upload File",

                    type=[
                        "pdf",
                        "txt",
                        "doc",
                        "docx",
                        "jpg",
                        "jpeg",
                        "png"
                    ],

                    key="file_upload"

                )
            )


    # -----------------------------------------------------
    # ASK BUTTON
    # -----------------------------------------------------

    ask_button = st.button(

        "🚀 Ask Tech Mithra AI",

        use_container_width=True

    )


    # -----------------------------------------------------
    # PROCESS
    # -----------------------------------------------------

    if ask_button:


        if not question.strip():

            st.warning(
                "Please enter a question."
            )


        else:


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


            with st.spinner(
                "🤖 Tech Mithra AI is thinking..."
            ):


                answer = ask_gemini(

                    question,

                    files,

                    "normal"

                )


            st.session_state.current_answer = (
                answer
            )


            add_to_history(

                question,

                answer,

                "Ask AI"

            )


    # -----------------------------------------------------
    # DISPLAY ANSWER
    # -----------------------------------------------------

    if st.session_state.current_answer:


        st.markdown(
            "### 🤖 Tech Mithra AI"
        )


        st.markdown(

            st.session_state.current_answer

        )


        if (
            st.session_state.settings
            .get("voice", True)
        ):

            voice_player(

                st.session_state.current_answer

            )


# =========================================================
# EXAM HELPER
# =========================================================

elif st.session_state.page == "Exam Helper":

    st.subheader(
        "🎓 Exam Helper"
    )


    exam_option = st.radio(

        "Select Answer Type",

        [

            "📝 Normal Answer",

            "❓ MCQ Answer",

            "📚 Important Questions"

        ],

        horizontal=True

    )


    # -----------------------------------------------------
    # NORMAL
    # -----------------------------------------------------

    if exam_option == "📝 Normal Answer":

        exam_question = st.text_area(

            "Enter your question",

            placeholder=
            "Example: Explain the levels of management"

        )


    # -----------------------------------------------------
    # MCQ
    # -----------------------------------------------------

    elif exam_option == "❓ MCQ Answer":

        exam_question = st.text_area(

            "Enter MCQ",

            placeholder=

"""Example:

What is IoT?

A) Internet of Things
B) Internet of Technology
C) Internal Object Technology
D) None

"""

        )


    # -----------------------------------------------------
    # IMPORTANT QUESTIONS
    # -----------------------------------------------------

    else:

        exam_question = st.text_area(

            "Enter Subject",

            placeholder=

            "Example: Electrical Engineering"

        )


    if st.button(

        "📖 Get Exam Answer",

        use_container_width=True

    ):


        if not exam_question.strip():

            st.warning(
                "Please enter a question."
            )


        else:


            if exam_option == (
                "📚 Important Questions"
            ):

                exam_question = (

                    "Give important examination "
                    "questions for the subject: "

                    + exam_question

                )


            with st.spinner(
                "Preparing answer..."
            ):


                answer = ask_gemini(

                    exam_question,

                    None,

                    "exam"

                )


            st.session_state.current_answer = (
                answer
            )


            add_to_history(

                exam_question,

                answer,

                "Exam Helper"

            )


    if st.session_state.current_answer:


        st.divider()


        st.markdown(
            "### 📚 Answer"
        )


        st.markdown(

            st.session_state.current_answer

        )


        if (
            st.session_state.settings
            .get("voice", True)
        ):

            voice_player(

                st.session_state.current_answer

            )


# =========================================================
# GATE PREPARATION
# =========================================================

elif st.session_state.page == "GATE Preparation":

    st.subheader(
        "📚 GATE Preparation"
    )


    gate_option = st.selectbox(

        "Select Option",

        [

            "📖 Explain Concept",

            "🔢 Numerical Problem",

            "❓ GATE MCQ",

            "📐 Formula",

            "⭐ Important Topics"

        ]

    )


    gate_question = st.text_area(

        "Enter your question",

        placeholder=
        "Ask a GATE preparation question..."

    )


    if st.button(

        "🚀 Get GATE Answer",

        use_container_width=True

    ):


        if not gate_question.strip():

            st.warning(
                "Please enter a question."
            )


        else:


            final_question = (

                "GATE Mode: "

                + gate_option

                + "\n\n"

                + gate_question

            )


            with st.spinner(
                "Preparing GATE answer..."
            ):


                answer = ask_gemini(

                    final_question,

                    None,

                    "gate"

                )


            st.session_state.current_answer = (
                answer
            )


            add_to_history(

                final_question,

                answer,

                "GATE Preparation"

            )


    if st.session_state.current_answer:


        st.divider()


        st.markdown(
            "### 🎓 GATE Answer"
        )


        st.markdown(

            st.session_state.current_answer

        )


        if (
            st.session_state.settings
            .get("voice", True)
        ):

            voice_player(

                st.session_state.current_answer

            )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":

    st.subheader(
        "⚙️ Settings"
    )


    # -----------------------------------------------------
    # AI SETTINGS
    # -----------------------------------------------------

    st.markdown(
        "## 🤖 AI Settings"
    )


    api_key = st.text_input(

        "Gemini API Key",

        value=
        st.session_state.settings
        .get(
            "api_key",
            ""
        ),

        type="password",

        help=
        "Enter your Gemini API Key"

    )


    model_name = st.text_input(

        "AI Model",

        value=
        st.session_state.settings
        .get(
            "model",
            "gemini-3.6-flash"
        )

    )


    language = st.selectbox(

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

            st.session_state.settings
            .get(
                "language",
                "English"
            )

            if
            st.session_state.settings
            .get(
                "language",
                "English"
            )

            in [

                "English",

                "Telugu",

                "Hindi"

            ]

            else

            "English"

        )

    )


    voice_enabled = st.checkbox(

        "🔊 Enable AI Voice",

        value=
        st.session_state.settings
        .get(
            "voice",
            True
        )

    )


    if st.button(

        "💾 Save AI Settings",

        use_container_width=True

    ):


        st.session_state.settings[
            "api_key"
        ] = api_key


        st.session_state.settings[
            "model"
        ] = model_name


        st.session_state.settings[
            "language"
        ] = language


        st.session_state.settings[
            "voice"
        ] = voice_enabled


        save_settings(
            st.session_state.settings
        )


        st.success(
            "Settings saved successfully!"
        )


    st.divider()


    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    st.markdown(
        "## 📜 History"
    )


    st.caption(

        "Your questions and answers "
        "are saved until you clear them."

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


            with st.expander(

                "💬 "
                + item.get(
                    "question",
                    "Question"
                )[:80]

            ):


                st.caption(

                    "Section: "

                    + item.get(
                        "page",
                        ""
                    )

                )


                st.caption(

                    "Time: "

                    + item.get(
                        "time",
                        ""
                    )

                )


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


    if st.button(

        "🗑️ Clear All History",

        use_container_width=True

    ):

        clear_history()

        st.success(
            "History cleared successfully."
        )

        st.rerun()


    st.divider()


    # -----------------------------------------------------
    # ABOUT
    # -----------------------------------------------------

    st.markdown(
        "## ℹ️ App Settings"
    )


    st.info(

        """

Tech Mithra AI

Features:

• AI Question Answering
• Photo Analysis
• Camera Upload
• File Upload
• Exam Helper
• MCQ Answers
• GATE Preparation
• Persistent History
• AI Voice
• Pause
• Resume

"""

    )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(

    "🤖 Tech Mithra AI | "
    "Your AI Study Assistant"

)
