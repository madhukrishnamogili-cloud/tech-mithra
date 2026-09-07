import streamlit as st
import json
import os
from datetime import datetime
from PIL import Image
from google import genai

# ============================================================
# TECH MITHRA AI PRO
# ============================================================

st.set_page_config(
    page_title="Tech Mithra AI Pro",
    page_icon="🚀",
    layout="wide"
)

APP_NAME = "Tech Mithra AI Pro"
HISTORY_FILE = "history.json"

# ============================================================
# GEMINI MODEL
# ============================================================

# Change the model name in Streamlit Secrets if needed.
# Example:
# GEMINI_MODEL = "your-working-gemini-model"

DEFAULT_MODEL = "gemini-3.5-flash-lite"


# ============================================================
# LOAD HISTORY
# ============================================================

def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list):
                    return data

    except Exception:
        return []

    return []


# ============================================================
# SAVE HISTORY
# ============================================================

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


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    st.session_state.history = []

    try:

        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)

    except Exception:
        pass


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = load_history()


if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


if "show_attachments" not in st.session_state:
    st.session_state.show_attachments = False


if "mcq_data" not in st.session_state:
    st.session_state.mcq_data = []


if "mcq_answers" not in st.session_state:
    st.session_state.mcq_answers = {}


if "mcq_submitted" not in st.session_state:
    st.session_state.mcq_submitted = False


if "mcq_score" not in st.session_state:
    st.session_state.mcq_score = 0


if "answer_language" not in st.session_state:
    st.session_state.answer_language = "English"


if "answer_style" not in st.session_state:
    st.session_state.answer_style = "Detailed"


if "default_marks" not in st.session_state:
    st.session_state.default_marks = "5 Marks"


# ============================================================
# GET GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_client():

    api_key = st.secrets["GEMINI_API_KEY"]

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# GET MODEL
# ============================================================

def get_model():

    try:

        if "GEMINI_MODEL" in st.secrets:

            return st.secrets["GEMINI_MODEL"]

    except Exception:
        pass

    return DEFAULT_MODEL


# ============================================================
# ADD HISTORY
# ============================================================

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

    # Keep maximum 100 history items
    st.session_state.history = (
        st.session_state.history[:100]
    )

    save_history()


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt, extra_content=None):

    try:

        client = get_client()

        model = get_model()

        contents = [prompt]

        if extra_content:

            for item in extra_content:

                contents.append(item)

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

        error_message = str(e)

        return (
            "❌ AI Error:\n\n"
            f"{error_message}\n\n"
            "Please check your GEMINI_API_KEY "
            "and GEMINI_MODEL in Streamlit Secrets."
        )


# ============================================================
# GET ANSWER SETTINGS
# ============================================================

def get_answer_instruction():

    return f"""

Answer Language:
{st.session_state.answer_language}

Answer Style:
{st.session_state.answer_style}

Follow the selected language and style.

"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 Tech Mithra AI")

    st.caption(
        "AI Study & Career Assistant"
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

    st.info(
        "🎓 Tech Mithra AI Pro\n\n"
        "Your AI-powered study assistant."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🚀 Tech Mithra AI Pro")


# ============================================================
# AI CHAT
# ============================================================

if selected == "💬 AI Chat":

    st.subheader("💬 AI Chat")

    st.caption(
        "Ask anything • Upload Photo • Camera • Files"
    )

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.chat_messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # ATTACHMENT BUTTON
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 12]
    )

    with col1:

        if st.button(
            "➕",
            help=(
                "Upload Photo, "
                "Camera or Files"
            )
        ):

            st.session_state.show_attachments = (
                not st.session_state.show_attachments
            )


    # --------------------------------------------------------
    # ATTACHMENT AREA
    # --------------------------------------------------------

    uploaded_files = []

    camera_image = None


    if st.session_state.show_attachments:

        st.markdown(
            "### 📎 Attachments"
        )


        uploaded_files = st.file_uploader(

            "📁 Upload Photo or Files",

            type=[

                "png",

                "jpg",

                "jpeg",

                "webp",

                "txt",

                "py",

                "java",

                "c",

                "cpp",

                "html",

                "css",

                "js",

                "json",

                "csv",

                "md",

                "pdf"

            ],

            accept_multiple_files=True

        )


        camera_image = st.camera_input(
            "📷 Camera"
        )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_prompt = st.chat_input(
        "Ask anything..."
    )


    if user_prompt:


        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        st.session_state.chat_messages.append(

            {

                "role": "user",

                "content": user_prompt

            }

        )


        with st.chat_message("user"):

            st.markdown(
                user_prompt
            )


        extra_content = []


        # ----------------------------------------------------
        # PROCESS UPLOADED FILES
        # ----------------------------------------------------

        if uploaded_files:

            for uploaded_file in uploaded_files:

                try:

                    file_name = (
                        uploaded_file.name.lower()
                    )


                    # IMAGE
                    if file_name.endswith(

                        (

                            ".png",

                            ".jpg",

                            ".jpeg",

                            ".webp"

                        )

                    ):

                        image = Image.open(
                            uploaded_file
                        )

                        extra_content.append(
                            image
                        )


                    # TEXT FILES
                    elif file_name.endswith(

                        (

                            ".txt",

                            ".py",

                            ".java",

                            ".c",

                            ".cpp",

                            ".html",

                            ".css",

                            ".js",

                            ".json",

                            ".csv",

                            ".md"

                        )

                    ):

                        text_data = (
                            uploaded_file.read()
                            .decode(
                                "utf-8",
                                errors="ignore"
                            )
                        )


                        extra_content.append(

                            f"""

FILE NAME:
{uploaded_file.name}

FILE CONTENT:

{text_data}

"""

                        )


                    # OTHER FILE
                    else:

                        extra_content.append(

                            f"""

User uploaded file:

{uploaded_file.name}

"""

                        )


                except Exception:

                    pass


        # ----------------------------------------------------
        # CAMERA IMAGE
        # ----------------------------------------------------

        if camera_image:

            try:

                image = Image.open(
                    camera_image
                )

                extra_content.append(
                    image
                )

            except Exception:

                pass


        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "🤖 Thinking..."
            ):

                prompt = f"""

You are Tech Mithra AI Pro.

You are a helpful AI assistant
for students.

User Question:

{user_prompt}

{get_answer_instruction()}

Rules:

- Give accurate answers.
- Use simple language.
- Use headings when useful.
- Use bullet points when useful.
- Explain clearly.
- Give examples when needed.

"""

                answer = ask_ai(

                    prompt,

                    extra_content

                )


            st.markdown(
                answer
            )


        # ----------------------------------------------------
        # SAVE CHAT MESSAGE
        # ----------------------------------------------------

        st.session_state.chat_messages.append(

            {

                "role": "assistant",

                "content": answer

            }

        )


        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        add_history(

            "AI Chat",

            user_prompt,

            answer

        )


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif selected == "🔬 Project & Lab Guide":


    st.subheader(
        "🔬 Project & Lab Guide"
    )


    topic = st.text_input(

        "Project / Lab Topic",

        placeholder=(
            "Example: Automatic Solar "
            "Street Light"
        )

    )


    project_image = st.file_uploader(

        "📷 Upload Project Photo (Optional)",

        type=[

            "png",

            "jpg",

            "jpeg",

            "webp"

        ]

    )


    if st.button(

        "🚀 Generate Project Guide",

        use_container_width=True

    ):


        if not topic:

            st.warning(
                "⚠️ Please enter a project topic."
            )


        else:


            extra = []


            if project_image:

                try:

                    image = Image.open(
                        project_image
                    )

                    extra.append(
                        image
                    )

                except Exception:

                    pass


            prompt = f"""

You are an expert engineering
project guide.

PROJECT TOPIC:

{topic}

{get_answer_instruction()}

Create a complete guide.

Include:

1. Project Title

2. Aim

3. Introduction

4. Objectives

5. Components Required

6. Block Diagram

7. Working Principle

8. Circuit / System Explanation

9. Step-by-Step Procedure

10. Algorithm

11. Advantages

12. Disadvantages

13. Applications

14. Safety Precautions

15. Result

16. Viva Questions and Answers

17. Future Scope

Make it suitable for
college students.

"""


            with st.spinner(

                "🔬 Preparing project guide..."

            ):

                answer = ask_ai(

                    prompt,

                    extra

                )


            st.markdown(
                answer
            )


            add_history(

                "Project & Lab Guide",

                topic,

                answer

            )


# ============================================================
# EVENT PLANNER
# ============================================================

elif selected == "🎉 Event Planner":


    st.subheader(
        "🎉 Event Planner"
    )


    event_name = st.text_input(
        "Event Name"
    )


    event_type = st.selectbox(

        "Event Type",

        [

            "Technical Event",

            "College Fest",

            "Workshop",

            "Seminar",

            "Cultural Event",

            "Sports Event",

            "Farewell",

            "Freshers Event",

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

You are a professional
college event planner.

Event Name:

{event_name}

Event Type:

{event_type}

Target Audience:

{audience}

{get_answer_instruction()}

Create a complete event plan.

Include:

1. Event Objective

2. Theme Ideas

3. Event Schedule

4. Registration Plan

5. Volunteer Responsibilities

6. Stage Arrangement

7. Required Materials

8. Technical Requirements

9. Budget Categories

10. Promotion Ideas

11. Social Media Promotion

12. Prize Ideas

13. Guest Coordination

14. Food and Refreshments

15. Safety Arrangements

16. Certificate Plan

17. Closing Ceremony

18. Final Checklist

Make it practical and
suitable for a college.

"""


            with st.spinner(

                "🎉 Creating event plan..."

            ):

                answer = ask_ai(
                    prompt
                )


            st.markdown(
                answer
            )


            add_history(

                "Event Planner",

                event_name,

                answer

            )


# ============================================================
# EXAM HACKER
# ============================================================

elif selected == "📚 Exam Hacker":


    st.subheader(
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


        st.markdown(
            "### ✍️ Exam Answer Generator"
        )


        question = st.text_area(

            "Enter your question",

            height=150,

            placeholder=(
                "Example: Explain the "
                "evolution of management."
            )

        )


        marks = st.selectbox(

            "Marks",

            [

                "2 Marks",

                "5 Marks",

                "10 Marks",

                "15 Marks"

            ],

            index=[

                "2 Marks",

                "5 Marks",

                "10 Marks",

                "15 Marks"

            ].index(
                st.session_state.default_marks
            )

        )


        if st.button(

            "📝 Generate Answer",

            use_container_width=True

        ):


            if not question:

                st.warning(
                    "⚠️ Please enter a question."
                )


            else:


                prompt = f"""

You are an expert
college exam answer writer.

Question:

{question}

Marks:

{marks}

{get_answer_instruction()}

Generate an exam-ready answer.

Requirements:

- Simple language
- Clear headings
- Important points
- Definitions where required
- Examples where useful
- Suitable length for {marks}
- Easy to memorize
- Proper exam format
- Use bullet points where needed

"""


                with st.spinner(

                    "✍️ Writing answer..."

                ):

                    answer = ask_ai(
                        prompt
                    )


                st.markdown(
                    answer
                )


                add_history(

                    "Exam Answer",

                    question,

                    answer

                )


    # ========================================================
    # MCQ QUIZ
    # ========================================================

    with tab2:


        st.markdown(
            "### 🧠 MCQ Quiz"
        )


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
                    "⚠️ Please enter a topic."
                )


            else:


                prompt = f"""

Create exactly {mcq_count}
multiple choice questions.

Topic:

{mcq_topic}

Return ONLY valid JSON.

Use this format:

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
        "explanation": "Explanation"
    }}
]

Rules:

- Exactly {mcq_count} questions.
- Four options.
- One correct answer.
- Answer must be A, B, C or D.
- Do not use markdown.
- Return only JSON.

"""


                with st.spinner(

                    "🧠 Generating MCQs..."

                ):

                    raw = ask_ai(
                        prompt
                    )


                try:


                    clean = raw.strip()


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


                    data = json.loads(
                        clean
                    )


                    st.session_state.mcq_data = (
                        data
                    )


                    st.session_state.mcq_answers = (
                        {}
                    )


                    st.session_state.mcq_submitted = (
                        False
                    )


                    st.session_state.mcq_score = 0


                    st.success(

                        f"✅ {len(data)} MCQs generated!"

                    )


                except Exception:


                    st.error(
                        "❌ Unable to generate MCQs. "
                        "Please try again."
                    )


        # ----------------------------------------------------
        # DISPLAY MCQS
        # ----------------------------------------------------

        if st.session_state.mcq_data:


            st.divider()


            st.markdown(
                "## 📝 Answer the Questions"
            )


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


                available_options = [

                    key

                    for key in [

                        "A",

                        "B",

                        "C",

                        "D"

                    ]

                    if key in options

                ]


                selected_answer = st.radio(

                    "Select your answer:",

                    available_options,

                    format_func=lambda x:
                    f"{x}. "
                    f"{options.get(x, '')}",

                    key=f"mcq_{index}"

                )


                st.session_state.mcq_answers[
                    index
                ] = selected_answer


            st.divider()


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

                    ).upper().strip()


                    selected_answer = str(

                        st.session_state.mcq_answers.get(

                            index,

                            ""

                        )

                    ).upper().strip()


                    if (
                        selected_answer == correct
                    ):

                        score += 1


                st.session_state.mcq_score = (
                    score
                )


                st.session_state.mcq_submitted = (
                    True
                )


                total = len(

                    st.session_state.mcq_data

                )


                percentage = (

                    score / total * 100

                    if total > 0

                    else 0

                )


                result = (

                    f"Score: {score}/{total}\n"

                    f"Percentage: "
                    f"{percentage:.1f}%"

                )


                add_history(

                    "MCQ Quiz",

                    mcq_topic,

                    result

                )


            # ------------------------------------------------
            # SHOW RESULT
            # ------------------------------------------------

            if st.session_state.mcq_submitted:


                total = len(

                    st.session_state.mcq_data

                )


                score = (
                    st.session_state.mcq_score
                )


                percentage = (

                    score / total * 100

                    if total > 0

                    else 0

                )


                st.divider()


                st.markdown(
                    "## 🏆 Quiz Result"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Score",
                        f"{score}/{total}"
                    )


                with col2:

                    st.metric(
                        "Percentage",
                        f"{percentage:.1f}%"
                    )


                with col3:


                    if percentage >= 80:

                        performance = "🔥 Excellent"


                    elif percentage >= 60:

                        performance = "👍 Good"


                    elif percentage >= 40:

                        performance = "📈 Average"


                    else:

                        performance = (
                            "💪 Need Practice"
                        )


                    st.metric(
                        "Performance",
                        performance
                    )


                st.divider()


                st.markdown(
                    "## 📖 Correct Answers"
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

                            "Not Answered"

                        )

                    ).upper()


                    st.markdown(
                        f"### Q{index + 1}"
                    )


                    if (
                        selected_answer == correct
                    ):

                        st.success(

                            f"✅ Your Answer: "
                            f"{selected_answer}"

                        )


                    else:

                        st.error(

                            f"❌ Your Answer: "
                            f"{selected_answer}"

                        )


                    st.info(

                        f"🎯 Correct Answer: "
                        f"{correct}"

                    )


                    st.write(

                        "💡 Explanation: "

                        +

                        mcq.get(

                            "explanation",

                            "No explanation available."

                        )

                    )


                if st.button(

                    "🔄 New Quiz",

                    use_container_width=True

                ):


                    st.session_state.mcq_data = []


                    st.session_state.mcq_answers = {}


                    st.session_state.mcq_submitted = (
                        False
                    )


                    st.session_state.mcq_score = 0


                    st.rerun()


# ============================================================
# GATE PREPARATION
# ============================================================

elif selected == "🎓 GATE Preparation":


    st.subheader(
        "🎓 GATE Preparation"
    )


    st.caption(
        "Prepare for GATE examination "
        "with AI."
    )


    gate_branch = st.selectbox(

        "Select Branch",

        [

            "Electrical Engineering (EE)",

            "Electronics and Communication (EC)",

            "Computer Science (CSE)",

            "Mechanical Engineering (ME)",

            "Civil Engineering (CE)",

            "Instrumentation Engineering (IN)",

            "Artificial Intelligence and Data Science",

            "Other"

        ]

    )


    gate_mode = st.selectbox(

        "What do you want?",

        [

            "Study Plan",

            "Topic Explanation",

            "Important Questions",

            "MCQ Practice",

            "Previous Year Question Practice",

            "Formula Sheet",

            "Revision Notes",

            "Mock Test"

        ]

    )


    gate_topic = st.text_input(

        "Topic (Optional)",

        placeholder=(
            "Example: Network Theory, "
            "Control Systems, "
            "Power Systems"
        )

    )


    gate_days = st.selectbox(

        "Preparation Duration",

        [

            "7 Days",

            "15 Days",

            "30 Days",

            "60 Days",

            "90 Days",

            "6 Months"

        ]

    )


    if st.button(

        "🎓 Generate GATE Preparation",

        use_container_width=True

    ):


        prompt = f"""

You are an expert GATE examination
mentor.

Student Branch:

{gate_branch}

Preparation Type:

{gate_mode}

Topic:

{gate_topic}

Preparation Duration:

{gate_days}

{get_answer_instruction()}

Create high-quality GATE preparation
content.

If Study Plan:

Create a complete day-wise plan.

If Topic Explanation:

Explain concepts from basics to
GATE level.

If Important Questions:

Give important GATE-level questions
with answers.

If MCQ Practice:

Give multiple MCQs with correct
answers and explanations.

If Previous Year Question Practice:

Give GATE-style practice questions
and explain solutions.

If Formula Sheet:

Provide important formulas with
short explanations.

If Revision Notes:

Give concise revision notes.

If Mock Test:

Create a GATE-style mock test.

Make the content:

- Exam focused
- Conceptually accurate
- Easy to understand
- Useful for engineering students

"""


        with st.spinner(

            "🎓 Preparing GATE content..."

        ):

            answer = ask_ai(
                prompt
            )


        st.markdown(
            answer
        )


        add_history(

            "GATE Preparation",

            f"{gate_branch} - {gate_mode} - "
            f"{gate_topic}",

            answer

        )


# ============================================================
# PLACEMENT PREPARATION
# ============================================================

elif selected == "💼 Placement Prep":


    st.subheader(
        "💼 Placement Preparation"
    )


    role = st.selectbox(

        "Target Role",

        [

            "Software Engineer",

            "Electrical Engineer",

            "Electronics Engineer",

            "Data Analyst",

            "Cloud Engineer",

            "AI / ML Engineer",

            "Embedded Engineer",

            "PLC / Automation Engineer",

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

            "Resume Preparation",

            "Group Discussion",

            "Mock Interview"

        ]

    )


    placement_topic = st.text_input(

        "Topic / Question",

        placeholder=(
            "Example: Transformer "
            "interview questions"
        )

    )


    if st.button(

        "🚀 Start Preparation",

        use_container_width=True

    ):


        prompt = f"""

You are an expert placement
trainer.

Target Role:

{role}

Preparation Type:

{prep_type}

Topic:

{placement_topic}

{get_answer_instruction()}

Create useful placement
preparation material.

Include:

1. Important Concepts

2. Frequently Asked Questions

3. Answers

4. Technical Points

5. Interview Tips

6. Common Mistakes

7. Practice Questions

8. HR Tips if relevant

9. Final Preparation Checklist

Make it suitable for
college students.

"""


        with st.spinner(

            "💼 Preparing..."

        ):

            answer = ask_ai(
                prompt
            )


        st.markdown(
            answer
        )


        add_history(

            "Placement Preparation",

            placement_topic or prep_type,

            answer

        )


# ============================================================
# SETTINGS
# ============================================================

elif selected == "⚙️ Settings":


    st.subheader(
        "⚙️ Settings"
    )


    # ========================================================
    # AI SETTINGS
    # ========================================================

    st.markdown(
        "## 🤖 AI Settings"
    )


    language = st.selectbox(

        "Answer Language",

        [

            "English",

            "Telugu",

            "Telugu + English",

            "Hindi"

        ],

        index=[

            "English",

            "Telugu",

            "Telugu + English",

            "Hindi"

        ].index(
            st.session_state.answer_language
        )

    )


    style = st.selectbox(

        "Answer Style",

        [

            "Short",

            "Detailed",

            "Exam Style",

            "Simple Explanation"

        ],

        index=[

            "Short",

            "Detailed",

            "Exam Style",

            "Simple Explanation"

        ].index(
            st.session_state.answer_style
        )

    )


    default_marks = st.selectbox(

        "Default Exam Marks",

        [

            "2 Marks",

            "5 Marks",

            "10 Marks",

            "15 Marks"

        ],

        index=[

            "2 Marks",

            "5 Marks",

            "10 Marks",

            "15 Marks"

        ].index(
            st.session_state.default_marks
        )

    )


    if st.button(

        "💾 Save Settings",

        use_container_width=True

    ):


        st.session_state.answer_language = (
            language
        )


        st.session_state.answer_style = (
            style
        )


        st.session_state.default_marks = (
            default_marks
        )


        st.success(
            "✅ Settings saved successfully!"
        )


    # ========================================================
    # HISTORY
    # ========================================================

    st.divider()


    st.markdown(
        "## 📜 History"
    )


    st.caption(
        "Your activity history is saved "
        "until you clear it."
    )


    if not st.session_state.history:


        st.info(
            "📭 No history available."
        )


    else:


        st.write(

            f"📊 Total History: "
            f"{len(st.session_state.history)}"

        )


        for i, item in enumerate(

            st.session_state.history

        ):


            title = (

                f"{i + 1}. "

                f"{item.get('mode', 'Activity')} "

                f"• "

                f"{item.get('time', '')}"

            )


            with st.expander(
                title
            ):


                st.markdown(
                    "### 📝 Question / Topic"
                )


                st.write(

                    item.get(
                        "question",
                        ""
                    )

                )


                st.markdown(
                    "### 🤖 Answer / Result"
                )


                st.markdown(

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


        clear_history()


        st.success(
            "✅ History cleared successfully!"
        )


        st.rerun()


    # ========================================================
    # APP INFORMATION
    # ========================================================

    st.divider()


    st.markdown(
        "## ℹ️ App Information"
    )


    st.write(
        "🚀 **App Name:** Tech Mithra AI Pro"
    )


    st.write(
        "🎓 **Purpose:** AI-powered "
        "study and career assistant"
    )


    st.write(
        "📚 **Features:**"
    )


    st.write(
        """
• AI Chat

• Photo Analysis

• Camera Input

• File Upload

• Project & Lab Guide

• Event Planner

• Exam Hacker

• MCQ Quiz

• GATE Preparation

• Placement Preparation

• History

• Settings
"""
    )


    st.divider()


    st.markdown(
        "### 🔐 Privacy"
    )


    st.info(
        "Do not enter passwords, "
        "bank details or other "
        "sensitive personal information."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "🚀 Tech Mithra AI Pro "
    "• AI-Powered Student Assistant"
)
