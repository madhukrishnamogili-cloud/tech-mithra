import os
import time
import json
import random
from datetime import datetime

import streamlit as st

# Optional file/image support
try:
    from PIL import Image
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False

# Gemini new SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
    color: white;
}

.main-title {
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 0px;
}

.sub-title {
    color: #a0a0a0;
    font-size: 17px;
}

.answer-box {
    background-color: #171b24;
    padding: 20px;
    border-radius: 15px;
    border-left: 4px solid #ff9800;
    margin-top: 10px;
}

.stButton button {
    border-radius: 10px;
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

if "selected_option" not in st.session_state:
    st.session_state.selected_option = "AI Chat"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = False


# ============================================================
# API KEY
# ============================================================

def get_api_key():

    # Streamlit Cloud secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # Environment variable
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    return None


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client(api_key):

    if not GENAI_AVAILABLE:
        return None

    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None


# ============================================================
# GET AVAILABLE MODELS
# Automatically discovers models
# ============================================================

@st.cache_data(ttl=3600)
def get_available_models(api_key):

    models = []

    if not GENAI_AVAILABLE:
        return models

    try:

        client = genai.Client(api_key=api_key)

        for model in client.models.list():

            try:

                name = getattr(model, "name", "")

                if not name:
                    continue

                name = name.replace("models/", "")

                # Only Gemini models
                if "gemini" in name.lower():

                    models.append(name)

            except Exception:
                continue

    except Exception:
        pass

    # Preferred order
    preferred_models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash"
    ]

    final_models = []

    # Add preferred models first if available
    for preferred in preferred_models:

        if preferred in models:
            final_models.append(preferred)

    # Add other discovered Gemini models
    for model in models:

        if model not in final_models:

            lower_name = model.lower()

            # Prefer flash models
            if "flash" in lower_name:
                final_models.append(model)

    # Add remaining models
    for model in models:

        if model not in final_models:
            final_models.append(model)

    return final_models


# ============================================================
# FALLBACK MODEL LIST
# ============================================================

def fallback_models():

    return [

        "gemini-2.5-flash",

        "gemini-2.5-flash-lite",

        "gemini-2.0-flash",

        "gemini-2.0-flash-lite"

    ]


# ============================================================
# LANGUAGE INSTRUCTION
# ============================================================

def language_instruction():

    language = st.session_state.language

    if language == "Telugu":
        return """
Respond completely in Telugu.
Use simple Telugu language.
If technical terms are needed, Telugu explanation with English technical words is allowed.
"""

    elif language == "Hindi":
        return """
Respond in simple Hindi.
"""

    else:
        return """
Respond in clear and simple English.
"""


# ============================================================
# SYSTEM PROMPT
# ============================================================

def create_system_prompt(mode):

    common = f"""

You are Tech Mithra AI.

You are a helpful AI assistant for students.

Your answers should be:
- Accurate
- Clear
- Easy to understand
- Well structured
- Student friendly

{language_instruction()}

"""

    if mode == "AI Chat":

        return common + """

You are a general AI assistant.

Answer questions clearly.
Explain concepts step by step when necessary.

"""

    elif mode == "Event Planner":

        return common + """

You are an expert Event Planner.

When a user gives an event idea, provide:

1. Event Overview
2. Event Goal
3. Target Audience
4. Budget Planning
5. Budget Breakdown
6. Venue Suggestions
7. Required Materials
8. Team Requirements
9. Timeline
10. Step-by-step plan from beginning to ending
11. Marketing and Promotion
12. Registration Plan
13. Food and Refreshments
14. Technical Requirements
15. Risk Management
16. Final Event Day Checklist
17. Post Event Activities

Make the plan practical.

"""

    elif mode == "Exam Helper":

        return common + """

You are an Exam Helper.

Help students with:

- Short answers
- Long answers
- 2 mark questions
- 5 mark questions
- 10 mark questions
- Important questions
- MCQs
- MCQ answers
- Explanations
- Revision notes

When asked for MCQs:

Give format:

Question
A)
B)
C)
D)

Correct Answer:
Explanation:

"""

    elif mode == "Project & Lab Guide":

        return common + """

You are a Project and Lab Guide.

Help students with:

- Project ideas
- Project titles
- Abstract
- Objectives
- Components
- Circuit explanation
- Software requirements
- Hardware requirements
- Procedure
- Implementation
- Results
- Conclusion
- Viva questions

Provide practical and student-friendly guidance.

"""

    elif mode == "GATE Preparation":

        return common + """

You are a GATE Preparation Assistant.

Help students with:

- GATE study plans
- Subject-wise preparation
- Important topics
- Daily timetable
- Weekly timetable
- Practice questions
- MCQs
- Previous question concepts
- Revision strategy
- Exam strategy

Give structured preparation plans.

"""

    return common


# ============================================================
# EXTRACT FILE TEXT
# ============================================================

def extract_file_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    try:

        # TXT
        if file_name.endswith(".txt"):

            return uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )


        # JSON
        if file_name.endswith(".json"):

            data = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            return data


        # CSV
        if file_name.endswith(".csv"):

            data = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            return data


        # Markdown
        if file_name.endswith(".md"):

            data = uploaded_file.read().decode(
                "utf-8",
                errors="ignore"
            )

            return data


        # PDF
        if file_name.endswith(".pdf") and PDF_AVAILABLE:

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

    except Exception:
        return ""

    return ""


# ============================================================
# GEMINI RESPONSE
# Retry + Fallback System
# ============================================================

def generate_ai_response(
    user_prompt,
    mode,
    uploaded_image=None,
    uploaded_file=None
):

    api_key = get_api_key()

    if not api_key:

        return (
            "⚠️ Gemini API Key కనుగొనబడలేదు.\n\n"
            "Streamlit Secrets లో:\n\n"
            "GEMINI_API_KEY = \"YOUR_API_KEY\"\n\n"
            "అని add చేయండి."
        )

    if not GENAI_AVAILABLE:

        return (
            "⚠️ Required Gemini package install కాలేదు.\n\n"
            "requirements.txt లో:\n\n"
            "google-genai\n\n"
            "add చేయండి."
        )

    client = get_client(api_key)

    if client is None:

        return (
            "⚠️ AI service ప్రారంభించలేకపోయింది. "
            "API Key మరియు internet connection చెక్ చేయండి."
        )


    # --------------------------------------------------------
    # GET MODELS
    # --------------------------------------------------------

    available_models = get_available_models(api_key)

    if not available_models:

        available_models = fallback_models()


    # Remove duplicates
    clean_models = []

    for model in available_models:

        if model not in clean_models:
            clean_models.append(model)


    # --------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------

    system_prompt = create_system_prompt(mode)


    # --------------------------------------------------------
    # FILE TEXT
    # --------------------------------------------------------

    file_text = ""

    if uploaded_file is not None:

        file_text = extract_file_text(uploaded_file)

        if file_text:

            # Limit huge files
            file_text = file_text[:20000]

            user_prompt += f"""

FILE CONTENT:

{file_text}

Please analyze the uploaded file and answer the user's question.

"""


    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    contents = []

    final_prompt = f"""

{system_prompt}

USER QUESTION:

{user_prompt}

"""


    contents.append(final_prompt)


    # Add image
    if uploaded_image is not None and PIL_AVAILABLE:

        try:

            image = Image.open(uploaded_image)

            contents.append(image)

        except Exception:
            pass


    # --------------------------------------------------------
    # RETRY SETTINGS
    # --------------------------------------------------------

    max_retries_per_model = 3

    successful_errors = []


    # --------------------------------------------------------
    # TRY EACH MODEL
    # --------------------------------------------------------

    for model_name in clean_models:

        for attempt in range(max_retries_per_model):

            try:

                response = client.models.generate_content(

                    model=model_name,

                    contents=contents,

                    config=types.GenerateContentConfig(

                        temperature=0.7,

                        max_output_tokens=2048

                    )

                )


                # Get response text
                answer = getattr(response, "text", None)


                if answer and answer.strip():

                    return answer.strip()


                # Empty response
                successful_errors.append(
                    f"{model_name}: empty response"
                )


            except Exception as e:

                error_text = str(e).lower()

                successful_errors.append(
                    f"{model_name}: {error_text[:100]}"
                )


                # ------------------------------------------------
                # 503 / High demand
                # ------------------------------------------------

                if (
                    "503" in error_text
                    or
                    "unavailable" in error_text
                    or
                    "high demand" in error_text
                    or
                    "overloaded" in error_text
                ):

                    wait_time = min(
                        2 ** attempt,
                        8
                    ) + random.uniform(0, 1)

                    time.sleep(wait_time)

                    continue


                # ------------------------------------------------
                # 429 / Rate limit
                # ------------------------------------------------

                elif (
                    "429" in error_text
                    or
                    "rate limit" in error_text
                    or
                    "quota" in error_text
                ):

                    wait_time = min(
                        3 ** attempt,
                        10
                    )

                    time.sleep(wait_time)

                    continue


                # ------------------------------------------------
                # 404 / Model not found
                # Try next model
                # ------------------------------------------------

                elif (
                    "404" in error_text
                    or
                    "not found" in error_text
                    or
                    "not supported" in error_text
                ):

                    break


                # ------------------------------------------------
                # Other errors
                # ------------------------------------------------

                else:

                    if attempt < max_retries_per_model - 1:

                        time.sleep(2)

                        continue

                    break


    # --------------------------------------------------------
    # FRIENDLY FALLBACK MESSAGE
    # --------------------------------------------------------

    return """

⚠️ **AI ప్రస్తుతం కొద్దిసేపు busy గా ఉంది.**

మీ question తప్పు కాదు మరియు app కూడా crash కాలేదు.

దయచేసి కొన్ని seconds తర్వాత **Try Again** చేయండి.

💡 Tip:
- ఒకేసారి చాలా requests పంపవద్దు
- Internet connection చెక్ చేయండి
- API quota available ఉందో చూడండి

"""


# ============================================================
# SAVE HISTORY
# ============================================================

def save_history(question, answer, mode):

    item = {

        "time": datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        ),

        "mode": mode,

        "question": question,

        "answer": answer

    }

    st.session_state.history.append(item)


# ============================================================
# TEXT TO SPEECH
# Browser Speech API
# ============================================================

def voice_html(text):

    safe_text = json.dumps(text)

    html = f"""

<script>

let speechText = {safe_text};

window.techMithraSpeech = new SpeechSynthesisUtterance(
    speechText
);

window.techMithraSpeech.rate = 1;
window.techMithraSpeech.pitch = 1;

function playSpeech() {{
    window.speechSynthesis.cancel();

    window.techMithraSpeech =
        new SpeechSynthesisUtterance(speechText);

    window.techMithraSpeech.rate = 1;
    window.techMithraSpeech.pitch = 1;

    window.speechSynthesis.speak(
        window.techMithraSpeech
    );
}}

function pauseSpeech() {{
    window.speechSynthesis.pause();
}}

function resumeSpeech() {{
    window.speechSynthesis.resume();
}}

</script>

"""

    return html


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.caption(
        "Student AI Assistant"
    )

    st.divider()


    options = [

        "💬 AI Chat",

        "📅 Event Planner",

        "📝 Exam Helper",

        "🔬 Project & Lab Guide",

        "🎓 GATE Preparation",

        "⚙️ Settings"

    ]


    selected_display = st.radio(

        "Select Option",

        options

    )


    # Remove emoji
    selected_option = selected_display

    if selected_display == "💬 AI Chat":
        selected_option = "AI Chat"

    elif selected_display == "📅 Event Planner":
        selected_option = "Event Planner"

    elif selected_display == "📝 Exam Helper":
        selected_option = "Exam Helper"

    elif selected_display == "🔬 Project & Lab Guide":
        selected_option = "Project & Lab Guide"

    elif selected_display == "🎓 GATE Preparation":
        selected_option = "GATE Preparation"

    elif selected_display == "⚙️ Settings":
        selected_option = "Settings"


    st.session_state.selected_option = selected_option


    st.divider()

    st.caption("Tech Mithra AI v1.0")


# ============================================================
# SETTINGS PAGE
# ============================================================

if st.session_state.selected_option == "Settings":

    st.title("⚙️ Settings")

    st.subheader("🤖 AI Settings")

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
            st.session_state.language
        )

    )

    st.session_state.language = language


    st.divider()


    # ========================================================
    # HISTORY
    # ========================================================

    st.subheader("📜 History")

    st.caption(
        "History ఈ session లో save అవుతుంది."
    )


    if len(st.session_state.history) == 0:

        st.info(
            "ఇంకా History లేదు."
        )

    else:

        for index, item in enumerate(
            reversed(st.session_state.history)
        ):

            with st.expander(

                f"{item['mode']} | {item['time']}"

            ):

                st.markdown(
                    "**Question:**"
                )

                st.write(
                    item["question"]
                )

                st.markdown(
                    "**Answer:**"
                )

                st.write(
                    item["answer"]
                )


    if st.button(
        "🗑️ Clear History"
    ):

        st.session_state.history = []

        st.success(
            "History Cleared Successfully!"
        )

        st.rerun()


    st.divider()


    # ========================================================
    # APP INFORMATION
    # ========================================================

    st.subheader(
        "ℹ️ App Information"
    )

    st.write(
        "Tech Mithra AI is designed to help students "
        "with learning, exams, projects, GATE preparation "
        "and event planning."
    )


    st.stop()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">💬 Tech Mithra AI</div>',
    unsafe_allow_html=True
)


st.markdown(
    f'<div class="sub-title">{st.session_state.selected_option}</div>',
    unsafe_allow_html=True
)


st.divider()


# ============================================================
# MODE INTRODUCTION
# ============================================================

mode = st.session_state.selected_option


if mode == "Event Planner":

    st.info(
        "📅 Event name, budget, number of people and event type ఇవ్వండి. "
        "AI మీకు starting నుండి ending వరకు complete plan ఇస్తుంది."
    )


elif mode == "Exam Helper":

    st.info(
        "📝 Questions, MCQs, short answers, long answers లేదా exam preparation అడగండి."
    )


elif mode == "Project & Lab Guide":

    st.info(
        "🔬 Project idea, abstract, components, procedure లేదా viva questions అడగండి."
    )


elif mode == "GATE Preparation":

    st.info(
        "🎓 మీ branch మరియు available preparation time ఇవ్వండి."
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# PLUS OPTIONS
# ============================================================

with st.expander(
    "➕ Upload Photo • Camera • Files"
):

    upload_tab1, upload_tab2, upload_tab3 = st.tabs(

        [

            "🖼️ Upload Photo",

            "📷 Camera",

            "📁 Files"

        ]

    )


    with upload_tab1:

        uploaded_photo = st.file_uploader(

            "Upload Photo",

            type=[

                "jpg",

                "jpeg",

                "png",

                "webp"

            ],

            key="photo_upload"

        )


    with upload_tab2:

        camera_photo = st.camera_input(

            "Take Photo"

        )


    with upload_tab3:

        uploaded_file = st.file_uploader(

            "Upload File",

            type=[

                "txt",

                "pdf",

                "csv",

                "json",

                "md"

            ],

            key="file_upload"

        )


# ============================================================
# MICROPHONE
# ============================================================

with st.expander(
    "🎤 Microphone"
):

    st.caption(
        "Voice recording upload చేయవచ్చు."
    )

    try:

        audio_data = st.audio_input(
            "Record your voice"
        )

        if audio_data:

            st.audio(audio_data)

            st.info(
                "Voice recording captured successfully. "
                "Please type your question below."
            )

    except Exception:

        st.info(
            "Microphone feature మీ Streamlit version లో available లేదు."
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(

    "Ask anything..."

)


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_question:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role": "user",

        "content": user_question

    })


    with st.chat_message(
        "user"
    ):

        st.markdown(
            user_question
        )


    # --------------------------------------------------------
    # SELECT IMAGE
    # --------------------------------------------------------

    final_image = None


    if "uploaded_photo" in locals():

        if uploaded_photo is not None:

            final_image = uploaded_photo


    if "camera_photo" in locals():

        if camera_photo is not None:

            final_image = camera_photo


    # --------------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "🤖 Tech Mithra AI is thinking..."
        ):

            answer = generate_ai_response(

                user_prompt=user_question,

                mode=mode,

                uploaded_image=final_image,

                uploaded_file=(
                    uploaded_file
                    if "uploaded_file" in locals()
                    else None
                )

            )


        st.markdown(
            answer
        )


    # --------------------------------------------------------
    # SAVE MESSAGE
    # --------------------------------------------------------

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })


    # --------------------------------------------------------
    # SAVE HISTORY
    # --------------------------------------------------------

    save_history(

        user_question,

        answer,

        mode

    )


    # --------------------------------------------------------
    # SAVE LAST ANSWER
    # --------------------------------------------------------

    st.session_state.last_answer = answer


# ============================================================
# VOICE CONTROLS
# ============================================================

if st.session_state.last_answer:

    st.divider()

    st.subheader(
        "🔊 AI Voice"
    )


    st.components.v1.html(

        voice_html(
            st.session_state.last_answer
        ),

        height=0

    )


    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "🔊 Play"
        ):

            st.components.v1.html(

                f"""

<script>

let text =
{json.dumps(st.session_state.last_answer)};

let speech =
new SpeechSynthesisUtterance(text);

window.speechSynthesis.cancel();

window.speechSynthesis.speak(speech);

</script>

""",

                height=0

            )


    with col2:

        if st.button(
            "⏸ Pause"
        ):

            st.components.v1.html(

                """

<script>

window.speechSynthesis.pause();

</script>

""",

                height=0

            )


    with col3:

        if st.button(
            "▶ Resume"
        ):

            st.components.v1.html(

                """

<script>

window.speechSynthesis.resume();

</script>

""",

                height=0

            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 Tech Mithra AI • Student Learning Assistant"
)
