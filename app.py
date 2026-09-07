import streamlit as st
import os
import json
from datetime import datetime
from google import genai

# =========================================================
# TECH MITHRA AI
# COMPLETE APP - PERMANENT GEMINI MODEL FALLBACK
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #1f2937;
}

.sub-title {
    font-size: 17px;
    color: #6b7280;
}

.answer-box {
    background-color: #f5f7fb;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
}

.option-card {
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "AI Chat"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# =========================================================
# HISTORY FILE
# =========================================================

HISTORY_FILE = "tech_mithra_history.json"


def load_history():

    if os.path.exists(HISTORY_FILE):

        try:

            with open(HISTORY_FILE, "r", encoding="utf-8") as file:

                return json.load(file)

        except:

            return []

    return []


def save_history(history):

    try:

        with open(HISTORY_FILE, "w", encoding="utf-8") as file:

            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4
            )

    except:

        pass


if len(st.session_state.history) == 0:

    st.session_state.history = load_history()


# =========================================================
# GET API KEY
# =========================================================

def get_api_key():

    if st.session_state.api_key:

        return st.session_state.api_key

    try:

        if "GEMINI_API_KEY" in st.secrets:

            return st.secrets["GEMINI_API_KEY"]

    except:

        pass

    try:

        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key:

            return api_key

    except:

        pass

    return ""


# =========================================================
# AUTOMATIC MODEL DETECTION
# PERMANENT SOLUTION
# =========================================================

def get_available_model(client):

    preferred_models = [

        "gemini-3.6-flash",

        "gemini-2.5-flash",

        "gemini-2.5-flash-lite",

        "gemini-2.0-flash",

        "gemini-1.5-flash"

    ]

    # First try preferred models

    for model_name in preferred_models:

        try:

            response = client.models.generate_content(

                model=model_name,

                contents="Hello"

            )

            if response:

                return model_name

        except:

            continue


    # If preferred models fail,
    # automatically find an available model

    try:

        models = client.models.list()

        for model in models:

            try:

                model_name = model.name

                if model_name:

                    clean_name = model_name.replace(
                        "models/",
                        ""
                    )

                    if "gemini" in clean_name.lower():

                        return clean_name

            except:

                continue

    except:

        pass


    return None


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt):

    api_key = get_api_key()

    if not api_key:

        return (
            "❌ Gemini API Key కనబడలేదు.\n\n"
            "Settings లో API Key add చేయండి "
            "లేదా Streamlit Secrets లో GEMINI_API_KEY set చేయండి."
        )


    try:

        client = genai.Client(
            api_key=api_key
        )

    except Exception as error:

        return f"❌ AI Client Error:\n\n{str(error)}"


    model_name = None


    # =====================================================
    # TRY MODELS ONE BY ONE
    # =====================================================

    preferred_models = [

        "gemini-3.6-flash",

        "gemini-2.5-flash",

        "gemini-2.5-flash-lite",

        "gemini-2.0-flash",

        "gemini-1.5-flash"

    ]


    last_error = ""


    for model_name in preferred_models:

        try:

            response = client.models.generate_content(

                model=model_name,

                contents=prompt

            )


            if response:

                if hasattr(response, "text"):

                    if response.text:

                        return response.text


        except Exception as error:

            last_error = str(error)

            continue


    # =====================================================
    # AUTOMATICALLY FIND AVAILABLE MODEL
    # =====================================================

    try:

        models = client.models.list()


        for model in models:

            try:

                name = model.name

                if not name:

                    continue


                clean_name = name.replace(
                    "models/",
                    ""
                )


                if "gemini" not in clean_name.lower():

                    continue


                try:

                    response = client.models.generate_content(

                        model=clean_name,

                        contents=prompt

                    )


                    if response:

                        if hasattr(response, "text"):

                            if response.text:

                                return response.text


                except:

                    continue


            except:

                continue


    except Exception as error:

        last_error = str(error)


    return (
        "❌ AI ప్రస్తుతం response ఇవ్వలేకపోయింది.\n\n"
        "Possible reason:\n"
        "• API Key సమస్య\n"
        "• Gemini API quota సమస్య\n"
        "• Available model లేకపోవడం\n"
        "• Internet connection సమస్య\n\n"
        f"Last Error:\n{last_error}"
    )


# =========================================================
# ADD HISTORY
# =========================================================

def add_history(question, answer, category):

    item = {

        "question": question,

        "answer": answer,

        "category": category,

        "time": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
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
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.divider()


    if st.button(
        "💬 AI Chat",
        use_container_width=True
    ):

        st.session_state.selected_page = "AI Chat"


    if st.button(
        "📅 Event Planner",
        use_container_width=True
    ):

        st.session_state.selected_page = "Event Planner"


    if st.button(
        "📝 Exam Helper",
        use_container_width=True
    ):

        st.session_state.selected_page = "Exam Helper"


    if st.button(
        "🔬 Project & Lab Guide",
        use_container_width=True
    ):

        st.session_state.selected_page = "Project & Lab Guide"


    if st.button(
        "🎯 GATE Preparation",
        use_container_width=True
    ):

        st.session_state.selected_page = "GATE Preparation"


    if st.button(
        "⚙️ Settings",
        use_container_width=True
    ):

        st.session_state.selected_page = "Settings"


    st.divider()

    st.caption(
        "Tech Mithra AI"
    )


# =========================================================
# MAIN PAGE
# =========================================================

page = st.session_state.selected_page


# =========================================================
# AI CHAT
# =========================================================

if page == "AI Chat":

    st.markdown(
        '<div class="main-title">💬 Tech Mithra AI</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-title">'
        'Ask anything • Upload Photo • Camera • Files'
        '</div>',
        unsafe_allow_html=True
    )


    st.write("")


    # =====================================================
    # SHOW CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # =====================================================
    # PLUS OPTIONS
    # =====================================================

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
                ]

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
                    "docx"
                ]

            )


    # =====================================================
    # CHAT INPUT
    # =====================================================

    prompt = st.chat_input(
        "Ask anything..."
    )


    if prompt:


        st.session_state.messages.append({

            "role": "user",

            "content": prompt

        })


        with st.chat_message("user"):

            st.markdown(prompt)


        with st.chat_message("assistant"):


            with st.spinner(
                "🤖 Tech Mithra AI is thinking..."
            ):


                final_prompt = f"""

You are Tech Mithra AI.

Answer in a clear and helpful way.

Selected Language:
{st.session_state.language}

User Question:

{prompt}

"""


                answer = ask_ai(
                    final_prompt
                )


            st.markdown(answer)


        st.session_state.messages.append({

            "role": "assistant",

            "content": answer

        })


        add_history(

            prompt,

            answer,

            "AI Chat"

        )


# =========================================================
# EVENT PLANNER
# =========================================================

elif page == "Event Planner":

    st.title("📅 Event Planner")

    st.write(
        "Plan your event with AI."
    )


    event_name = st.text_input(
        "Event Name"
    )


    event_date = st.date_input(
        "Event Date"
    )


    event_people = st.number_input(

        "Number of People",

        min_value=1,

        value=10

    )


    event_budget = st.text_input(
        "Budget"
    )


    if st.button(
        "✨ Create Event Plan",
        use_container_width=True
    ):


        if event_name:


            prompt = f"""

Create a complete event plan.

Event Name:
{event_name}

Date:
{event_date}

Number of People:
{event_people}

Budget:
{event_budget}

Give:

1. Event Introduction

2. Preparation Steps

3. Budget Plan

4. Required Materials

5. Schedule

6. Team Responsibilities

7. Final Checklist

"""


            with st.spinner(
                "Creating your event plan..."
            ):

                answer = ask_ai(prompt)


            st.markdown(answer)


            add_history(

                event_name,

                answer,

                "Event Planner"

            )


        else:

            st.warning(
                "Please enter Event Name."
            )


# =========================================================
# EXAM HELPER
# =========================================================

elif page == "Exam Helper":

    st.title("📝 Exam Helper")


    exam_type = st.selectbox(

        "Select Answer Type",

        [

            "Long Answer",

            "Short Answer",

            "5 Marks Answer",

            "10 Marks Answer",

            "MCQ Questions & Answers"

        ]

    )


    subject = st.text_input(
        "Subject Name"
    )


    question = st.text_area(
        "Enter your Question / Topic"
    )


    if st.button(
        "🚀 Generate Answer",
        use_container_width=True
    ):


        if question:


            prompt = f"""

You are an educational AI assistant.

Subject:
{subject}

Answer Type:
{exam_type}

Question:
{question}

Give a clear and student-friendly answer.

"""


            if exam_type == "MCQ Questions & Answers":

                prompt += """

Create multiple-choice questions.

For every question provide:

Question

A)

B)

C)

D)

Correct Answer

Explanation

"""


            with st.spinner(
                "Preparing your answer..."
            ):

                answer = ask_ai(prompt)


            st.markdown(answer)


            add_history(

                question,

                answer,

                "Exam Helper"

            )


        else:

            st.warning(
                "Please enter a question."
            )


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

elif page == "Project & Lab Guide":

    st.title("🔬 Project & Lab Guide")


    project_type = st.selectbox(

        "Select",

        [

            "Mini Project",

            "Major Project",

            "Lab Experiment",

            "Engineering Project",

            "Science Project"

        ]

    )


    project_topic = st.text_area(
        "Enter Project Topic"
    )


    if st.button(
        "💡 Generate Guide",
        use_container_width=True
    ):


        if project_topic:


            prompt = f"""

Create a complete guide.

Type:
{project_type}

Topic:
{project_topic}

Include:

1. Title

2. Abstract

3. Objective

4. Required Components

5. Software Requirements

6. Hardware Requirements

7. Working Principle

8. Step-by-Step Procedure

9. Circuit / System Explanation

10. Expected Output

11. Applications

12. Advantages

13. Future Scope

14. Conclusion

"""


            with st.spinner(
                "Creating project guide..."
            ):

                answer = ask_ai(prompt)


            st.markdown(answer)


            add_history(

                project_topic,

                answer,

                "Project & Lab Guide"

            )


        else:

            st.warning(
                "Please enter a project topic."
            )


# =========================================================
# GATE PREPARATION
# =========================================================

elif page == "GATE Preparation":

    st.title("🎯 GATE Preparation")


    gate_subject = st.text_input(
        "Enter Subject"
    )


    gate_topic = st.text_area(
        "Enter Topic"
    )


    gate_option = st.selectbox(

        "Choose Preparation Type",

        [

            "Topic Explanation",

            "Important Questions",

            "MCQ Practice",

            "Previous Year Style Questions",

            "Study Plan"

        ]

    )


    if st.button(
        "🚀 Start GATE Preparation",
        use_container_width=True
    ):


        if gate_topic:


            prompt = f"""

You are a GATE exam preparation expert.

Subject:
{gate_subject}

Topic:
{gate_topic}

Preparation Type:
{gate_option}

Give a detailed and easy-to-understand answer.

If MCQs are requested, include:

Question

A)

B)

C)

D)

Correct Answer

Explanation

"""


            with st.spinner(
                "Preparing GATE content..."
            ):

                answer = ask_ai(prompt)


            st.markdown(answer)


            add_history(

                gate_topic,

                answer,

                "GATE Preparation"

            )


        else:

            st.warning(
                "Please enter a topic."
            )


# =========================================================
# SETTINGS
# =========================================================

elif page == "Settings":

    st.title("⚙️ Settings")


    tab1, tab2, tab3 = st.tabs([

        "🤖 AI Settings",

        "🕘 History",

        "ℹ️ About"

    ])


    # =====================================================
    # AI SETTINGS
    # =====================================================

    with tab1:


        st.subheader(
            "AI Settings"
        )


        language = st.selectbox(

            "🌐 AI Language",

            [

                "English",

                "Telugu",

                "Hindi",

                "Auto"

            ],

            index=[

                "English",

                "Telugu",

                "Hindi",

                "Auto"

            ].index(
                st.session_state.language
            )

        )


        st.session_state.language = language


        st.divider()


        st.subheader(
            "🔑 Gemini API Key"
        )


        api_key_input = st.text_input(

            "Enter API Key",

            value=st.session_state.api_key,

            type="password"

        )


        if st.button(
            "💾 Save API Key"
        ):

            st.session_state.api_key = (
                api_key_input
            )

            st.success(
                "API Key saved for this session."
            )


        st.info(
            "For permanent Streamlit Cloud usage, "
            "store GEMINI_API_KEY in Streamlit Secrets."
        )


        st.divider()


        st.subheader(
            "🔊 AI Voice"
        )


        st.write(
            "Voice controls depend on your browser."
        )


        st.button(
            "▶️ Play"
        )


        st.button(
            "⏸️ Pause"
        )


        st.button(
            "▶️ Resume"
        )


    # =====================================================
    # HISTORY
    # =====================================================

    with tab2:


        st.subheader(
            "🕘 Question History"
        )


        st.write(
            "Your history remains saved until you clear it."
        )


        if len(st.session_state.history) == 0:

            st.info(
                "No history available."
            )


        else:


            for index, item in enumerate(
                st.session_state.history
            ):


                with st.expander(

                    f"{item['category']} - "
                    f"{item['question'][:50]}"

                ):


                    st.caption(
                        item["time"]
                    )


                    st.write(
                        "### Question"
                    )


                    st.write(
                        item["question"]
                    )


                    st.write(
                        "### Answer"
                    )


                    st.markdown(
                        item["answer"]
                    )


        st.divider()


        if st.button(
            "🗑️ Clear Complete History",
            use_container_width=True
        ):


            st.session_state.history = []


            save_history([])


            st.success(
                "History cleared successfully."
            )


            st.rerun()


    # =====================================================
    # ABOUT
    # =====================================================

    with tab3:


        st.subheader(
            "🤖 Tech Mithra AI"
        )


        st.write(
            "An AI-powered student assistant."
        )


        st.write(
            """
Features:

• AI Chat

• Event Planner

• Exam Helper

• MCQ Questions & Answers

• Project & Lab Guide

• GATE Preparation

• Upload Photo

• Camera

• File Upload

• Saved History

• AI Settings

• Automatic Gemini Model Fallback
"""
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "🤖 Tech Mithra AI • Powered by Gemini AI"
)
