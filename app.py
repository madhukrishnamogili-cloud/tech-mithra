# ============================================================
# TECH MITHRA AI - COMPLETE STREAMLIT APP
# ============================================================
# Install:
# pip install streamlit google-genai
#
# Run:
# streamlit run app.py
#
# ============================================================

import streamlit as st
import os
import json
import base64
import mimetypes
from datetime import datetime

try:
    from google import genai
except ImportError:
    st.error("Please install required package: pip install google-genai")
    st.stop()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.sub-title {
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 25px;
}

.user-box {
    background: #f3f4f6;
    padding: 16px;
    border-radius: 16px;
    margin: 10px 0;
}

.ai-box {
    background: #fff7ed;
    padding: 18px;
    border-radius: 16px;
    margin: 10px 0 20px 0;
    border-left: 5px solid #f59e0b;
}

.answer-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.small-text {
    color: #6b7280;
    font-size: 14px;
}

div[data-testid="stSidebar"] {
    background-color: #f8fafc;
}

.stButton button {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HISTORY FILE
# ============================================================

HISTORY_FILE = "tech_mithra_history.json"


def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
    except:
        pass

    return []


def save_history(history):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
    except:
        pass


def add_history(question, answer, section="Ask AI"):
    history = load_history()

    history.insert(
        0,
        {
            "question": question,
            "answer": answer,
            "section": section,
            "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        }
    )

    save_history(history)


def clear_history():
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except:
        pass


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "💬 Ask AI"


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():

    # First check session
    if st.session_state.api_key:
        return st.session_state.api_key

    # Check Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except:
        pass

    # Check environment variable
    key = os.getenv("GEMINI_API_KEY")

    if key:
        return key

    return None


# ============================================================
# GEMINI AI FUNCTION
# ============================================================

def ask_ai(prompt, uploaded_files=None):

    api_key = get_api_key()

    if not api_key:
        return (
            "❌ Gemini API Key is not set.\n\n"
            "Please add your API key in `.streamlit/secrets.toml`:\n\n"
            "```toml\n"
            'GEMINI_API_KEY = "YOUR_API_KEY_HERE"\n'
            "```"
        )

    try:

        client = genai.Client(api_key=api_key)

        language = st.session_state.language

        system_instruction = f"""
You are Tech Mithra AI, a helpful educational AI assistant.

Always answer in {language} unless the user specifically requests another language.

Rules:
1. Give accurate and clear answers.
2. For educational questions, explain in simple language.
3. For 2 marks, give short answers.
4. For 5 marks, give medium detailed answers.
5. For long answers, explain with headings and points.
6. For engineering questions, provide examples when useful.
7. For MCQs, clearly mention the correct answer.
8. Do not give unnecessary long answers for simple questions.
9. Be fast and direct.
"""

        final_prompt = system_instruction + "\n\nUSER QUESTION:\n" + prompt

        contents = [final_prompt]

        # Add uploaded files
        if uploaded_files:

            for uploaded_file in uploaded_files:

                try:

                    file_bytes = uploaded_file.getvalue()

                    mime_type = uploaded_file.type

                    if not mime_type:
                        mime_type = mimetypes.guess_type(
                            uploaded_file.name
                        )[0]

                    if not mime_type:
                        mime_type = "application/octet-stream"

                    contents.append(
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64.b64encode(
                                    file_bytes
                                ).decode("utf-8")
                            }
                        }
                    )

                except:
                    pass


        # ====================================================
        # MODEL FALLBACK
        # ====================================================

        models_to_try = [

            "gemini-3.5-flash-lite",
            "gemini-3.5-flash",
            "gemini-2.5-flash",

        ]

        last_error = None

        for model_name in models_to_try:

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )

                if response and response.text:
                    return response.text

            except Exception as e:

                last_error = str(e)
                continue


        return (
            "❌ AI service is temporarily unavailable.\n\n"
            "Please try again after some time.\n\n"
            "Error: " + str(last_error)
        )


    except Exception as e:

        return (
            "❌ AI Error\n\n"
            + str(e)
        )


# ============================================================
# VOICE FUNCTION
# ============================================================

def speak_text(text):

    safe_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    html_code = f"""
    <button onclick="speakAnswer()" style="
        background:#2563eb;
        color:white;
        border:none;
        padding:10px 16px;
        border-radius:10px;
        cursor:pointer;
        font-size:16px;
    ">
        🔊 Listen Answer
    </button>

    <script>

    function speakAnswer() {{

        window.speechSynthesis.cancel();

        let text = `{safe_text}`;

        let speech = new SpeechSynthesisUtterance(text);

        speech.rate = 1;
        speech.pitch = 1;

        window.speechSynthesis.speak(speech);

    }}

    </script>
    """

    st.components.v1.html(
        html_code,
        height=55
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
    💬 Tech Mithra AI
    </div>

    <div class="sub-title">
    Ask anything • Upload Photo • Camera • Files • Voice AI
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.markdown("---")

    if st.button(
        "💬 Ask AI",
        use_container_width=True
    ):
        st.session_state.selected_section = "💬 Ask AI"


    if st.button(
        "📚 Exam Hacker",
        use_container_width=True
    ):
        st.session_state.selected_section = "📚 Exam Hacker"


    if st.button(
        "🎓 GATE Preparation",
        use_container_width=True
    ):
        st.session_state.selected_section = "🎓 GATE Preparation"


    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):
        st.session_state.selected_section = "⚙️ Settings"


    st.markdown("---")

    st.caption("🚀 Tech Mithra AI")


# ============================================================
# ASK AI SECTION
# ============================================================

if st.session_state.selected_section == "💬 Ask AI":

    st.subheader("💬 Ask AI")

    st.caption(
        "Ask any question like ChatGPT"
    )


    # ========================================================
    # SHOW CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user"):
                st.write(message["content"])

        else:

            with st.chat_message("assistant"):

                st.write(message["content"])

                speak_text(message["content"])


    # ========================================================
    # PLUS OPTION
    # ========================================================

    with st.popover("➕"):

        st.write("### Add Attachment")

        upload_photo = st.file_uploader(
            "🖼️ Upload Photo",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ],
            key="upload_photo"
        )

        camera_photo = st.camera_input(
            "📷 Camera"
        )

        upload_file = st.file_uploader(
            "📁 Upload Files",
            type=[
                "pdf",
                "txt",
                "docx",
                "pptx",
                "xlsx"
            ],
            key="upload_file"
        )


    # ========================================================
    # MICROPHONE
    # ========================================================

    audio_file = st.audio_input(
        "🎤 Ask using Microphone"
    )


    # ========================================================
    # TEXT QUESTION
    # ========================================================

    question = st.chat_input(
        "Ask anything..."
    )


    # ========================================================
    # PREPARE FILES
    # ========================================================

    uploaded_items = []

    if upload_photo:
        uploaded_items.append(upload_photo)

    if camera_photo:
        uploaded_items.append(camera_photo)

    if upload_file:
        uploaded_items.append(upload_file)


    # ========================================================
    # TEXT QUESTION PROCESSING
    # ========================================================

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        with st.chat_message("user"):

            st.write(question)


        with st.chat_message("assistant"):

            with st.spinner("🤖 Thinking..."):

                answer = ask_ai(
                    question,
                    uploaded_items
                )

                st.write(answer)

                speak_text(answer)


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        add_history(
            question,
            answer,
            "Ask AI"
        )


    # ========================================================
    # MICROPHONE PROCESSING
    # ========================================================

    if audio_file:

        st.info(
            "🎤 Voice recorded successfully."
        )

        st.audio(audio_file)

        if st.button(
            "🤖 Ask AI using Voice",
            use_container_width=True
        ):

            voice_question = """
The user has uploaded an audio recording.

Please listen to the audio and understand the question.

First identify what the user is asking.

Then answer clearly in the selected language.

Keep the answer accurate and simple.
"""

            with st.spinner(
                "🎤 Understanding your voice..."
            ):

                answer = ask_ai(
                    voice_question,
                    [audio_file]
                )

            st.success("🤖 AI Answer")

            st.write(answer)

            speak_text(answer)

            add_history(
                "🎤 Voice Question",
                answer,
                "Ask AI - Voice"
            )


# ============================================================
# EXAM HACKER
# ============================================================

elif st.session_state.selected_section == "📚 Exam Hacker":

    st.header("📚 Exam Hacker")

    st.caption(
        "Generate exam answers and MCQs"
    )


    exam_type = st.selectbox(

        "Select Answer Type",

        [
            "2 Marks Answer",
            "5 Marks Answer",
            "Long Answer",
            "MCQs"
        ]

    )


    subject_name = st.text_input(
        "📘 Subject Name",
        placeholder="Example: Fundamentals of Management"
    )


    topic_name = st.text_input(
        "📖 Topic / Chapter",
        placeholder="Example: Levels of Management"
    )


    number_of_mcqs = 10

    if exam_type == "MCQs":

        number_of_mcqs = st.slider(
            "Number of MCQs",
            min_value=5,
            max_value=50,
            value=10
        )


    if st.button(
        "✨ Generate",
        use_container_width=True
    ):

        if not subject_name or not topic_name:

            st.warning(
                "⚠️ Please enter Subject Name and Topic."
            )

        else:

            if exam_type == "MCQs":

                prompt = f"""
Subject:
{subject_name}

Topic:
{topic_name}

Generate {number_of_mcqs} multiple choice questions.

Format:

Question 1

A)
B)
C)
D)

Correct Answer: A

Explanation: Simple explanation.

Continue for all questions.
"""

            else:

                prompt = f"""
Subject: {subject_name}

Topic: {topic_name}

Answer Type: {exam_type}

Generate an exam-ready answer.

Use:
- Clear headings
- Important points
- Simple explanation
- Easy language
"""


            with st.spinner(
                "🤖 Generating answer..."
            ):

                answer = ask_ai(prompt)


            st.markdown("---")

            st.markdown(
                "### 🤖 Generated Answer"
            )

            st.write(answer)

            speak_text(answer)


            add_history(
                f"{subject_name} - {topic_name}",
                answer,
                "Exam Hacker"
            )


# ============================================================
# GATE PREPARATION
# ============================================================

elif st.session_state.selected_section == "🎓 GATE Preparation":

    st.header("🎓 GATE Preparation")

    st.caption(
        "Prepare for GATE examination"
    )


    gate_subject = st.text_input(
        "📘 GATE Subject",
        placeholder="Example: Electrical Engineering"
    )


    gate_topic = st.text_input(
        "📖 Topic",
        placeholder="Example: Network Theory"
    )


    gate_option = st.selectbox(

        "Choose Preparation Type",

        [
            "Concept Explanation",
            "Important Questions",
            "Practice MCQs",
            "Formula Sheet",
            "Study Plan"
        ]

    )


    if st.button(
        "🚀 Generate GATE Content",
        use_container_width=True
    ):

        if not gate_subject:

            st.warning(
                "⚠️ Please enter GATE Subject."
            )

        else:

            prompt = f"""
You are a GATE exam preparation assistant.

Subject:
{gate_subject}

Topic:
{gate_topic}

Preparation Type:
{gate_option}

Create high-quality GATE preparation content.

If MCQs are requested:
Give questions with 4 options,
correct answer,
and explanation.

Make the content useful for exam preparation.
"""


            with st.spinner(
                "🎓 Preparing GATE content..."
            ):

                answer = ask_ai(prompt)


            st.markdown("---")

            st.markdown(
                "### 🎓 GATE Preparation"
            )

            st.write(answer)

            speak_text(answer)


            add_history(
                f"GATE - {gate_subject} - {gate_topic}",
                answer,
                "GATE Preparation"
            )


# ============================================================
# SETTINGS
# ============================================================

elif st.session_state.selected_section == "⚙️ Settings":

    st.header("⚙️ Settings")


    # ========================================================
    # AI SETTINGS
    # ========================================================

    with st.expander(
        "🤖 AI Settings",
        expanded=True
    ):

        st.markdown(
            "### 🌐 Language"
        )


        language = st.selectbox(

            "Select AI Language",

            [
                "English",
                "Telugu",
                "Hindi",
                "Tamil"
            ],

            index=[
                "English",
                "Telugu",
                "Hindi",
                "Tamil"
            ].index(
                st.session_state.language
            )

        )


        st.session_state.language = language


        st.success(
            f"Language selected: {language}"
        )


    # ========================================================
    # HISTORY
    # ========================================================

    with st.expander(
        "🕘 History"
    ):

        history = load_history()


        if not history:

            st.info(
                "No history available."
            )

        else:

            st.write(
                f"Total History: {len(history)}"
            )


            for index, item in enumerate(history):

                with st.expander(

                    f"{index + 1}. "
                    f"{item['question'][:60]}"

                ):

                    st.caption(
                        f"📂 {item.get('section', '')}"
                    )

                    st.caption(
                        f"🕒 {item.get('time', '')}"
                    )

                    st.markdown(
                        "### Question"
                    )

                    st.write(
                        item["question"]
                    )

                    st.markdown(
                        "### Answer"
                    )

                    st.write(
                        item["answer"]
                    )


        st.markdown("---")


        if st.button(
            "🗑️ Clear All History",
            type="primary",
            use_container_width=True
        ):

            clear_history()

            st.success(
                "History cleared successfully!"
            )

            st.rerun()


    # ========================================================
    # APP SETTINGS
    # ========================================================

    with st.expander(
        "📱 App Information"
    ):

        st.write(
            "### 🤖 Tech Mithra AI"
        )

        st.write(
            """
Tech Mithra AI is an educational AI assistant.

Features:

• Ask AI Questions  
• Upload Photos  
• Camera Input  
• Upload Files  
• Voice Input  
• Voice Answers  
• Exam Hacker  
• MCQs  
• GATE Preparation  
• History  
• Multiple Languages  
"""
        )


    # ========================================================
    # API STATUS
    # ========================================================

    with st.expander(
        "🔑 API Status"
    ):

        api_key = get_api_key()


        if api_key:

            st.success(
                "✅ Gemini API Key is configured."
            )

        else:

            st.warning(
                "⚠️ Gemini API Key is not configured."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🤖 Tech Mithra AI • Your AI Study Assistant"
)

# ============================================================
# END OF CODE
# ============================================================
