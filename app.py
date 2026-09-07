import streamlit as st
from google import genai
from PIL import Image
import os
import io
import base64
import json
from datetime import datetime


# =========================================================
# TECH MITHRA AI
# =========================================================

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 5rem;
    max-width: 1100px;
}

[data-testid="stSidebar"] {
    background-color: #161b22;
}

.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #8b949e;
    font-size: 17px;
    margin-bottom: 30px;
}

.chat-user {
    background: #1f6feb;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
}

.chat-ai {
    background: #21262d;
    padding: 15px;
    border-radius: 15px;
    margin: 10px 0;
}

.option-card {
    background: #161b22;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""


# =========================================================
# API KEY
# =========================================================

API_KEY = None

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY")


# =========================================================
# GEMINI AI FUNCTION
# =========================================================

def ask_ai(prompt, image=None):

    if not API_KEY:

        return (
            "❌ **Gemini API Key not found.**\n\n"
            "Please add your API key in Streamlit Secrets:\n\n"
            "`GEMINI_API_KEY = \"YOUR_API_KEY\"`"
        )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        # ---------------------------------------------
        # LANGUAGE INSTRUCTION
        # ---------------------------------------------

        language_instruction = f"""

You are Tech Mithra AI.

Answer the user clearly and accurately.

Selected Language:
{st.session_state.language}

If the language is Telugu:
Answer in Telugu.

If the language is English:
Answer in English.

If Telugu + English:
Use easy Telugu and English.

Use proper headings.

Make answers easy for students.

"""

        full_prompt = language_instruction + "\n\nUser Question:\n" + prompt


        # ---------------------------------------------
        # IMAGE + TEXT
        # ---------------------------------------------

        if image is not None:

            response = client.models.generate_content(

                model="gemini-3.8-flash",

                contents=[
                    full_prompt,
                    image
                ]

            )

        # ---------------------------------------------
        # TEXT ONLY
        # ---------------------------------------------

        else:

            response = client.models.generate_content(

                model="gemini-3.8-flash",

                contents=full_prompt

            )


        if response and response.text:

            return response.text

        else:

            return "⚠️ AI did not generate a response. Please try again."


    except Exception as e:

        error = str(e)

        return f"""

❌ **AI Error**

{error}

### Possible Solution

1. Check your Gemini API Key.
2. Check your Internet Connection.
3. Make sure `google-genai` is installed.
4. Make sure your Streamlit Secrets are correct.
5. Restart your Streamlit application.

"""


# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(question, answer):

    item = {
        "time": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "question": question,
        "answer": answer
    }

    st.session_state.history.append(item)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🤖 Tech Mithra AI")

    st.caption("Your AI Study Assistant")

    st.divider()


    option = st.radio(

        "Navigation",

        [

            "💬 AI Chat",

            "📅 Event Planner",

            "📚 Exam Helper",

            "🔬 Project & Lab Guide",

            "🎓 GATE Preparation",

            "⚙️ Settings"

        ]

    )

    st.divider()

    st.caption("Powered by Gemini AI")


# =========================================================
# TITLE
# =========================================================

st.markdown(

    """
    <div class="main-title">
    🤖 Tech Mithra AI
    </div>

    <div class="subtitle">
    Ask Anything • Upload Photo • Camera • Files
    </div>
    """,

    unsafe_allow_html=True

)


# =========================================================
# AI CHAT
# =========================================================

if option == "💬 AI Chat":

    st.subheader("💬 AI Chat")


    # -----------------------------------------------------
    # SHOW CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


    # -----------------------------------------------------
    # PLUS OPTIONS
    # -----------------------------------------------------

    with st.expander("➕ Upload Options"):

        upload_type = st.radio(

            "Choose Input",

            [

                "📷 Upload Photo",

                "📸 Camera",

                "📁 Upload File"

            ],

            horizontal=True

        )


        uploaded_image = None

        uploaded_file = None


        # -------------------------------------------------
        # PHOTO
        # -------------------------------------------------

        if upload_type == "📷 Upload Photo":

            uploaded_image = st.file_uploader(

                "Upload an Image",

                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp"
                ]

            )


        # -------------------------------------------------
        # CAMERA
        # -------------------------------------------------

        elif upload_type == "📸 Camera":

            uploaded_image = st.camera_input(

                "Take a Photo"

            )


        # -------------------------------------------------
        # FILE
        # -------------------------------------------------

        elif upload_type == "📁 Upload File":

            uploaded_file = st.file_uploader(

                "Upload File",

                type=[
                    "txt",
                    "pdf",
                    "docx"
                ]

            )


    # -----------------------------------------------------
    # FILE INFORMATION
    # -----------------------------------------------------

    file_text = ""

    if uploaded_file is not None:

        try:

            if uploaded_file.type == "text/plain":

                file_text = uploaded_file.read().decode("utf-8")


            else:

                file_text = (
                    f"User uploaded file: "
                    f"{uploaded_file.name}"
                )

        except Exception:

            file_text = (
                f"Uploaded File: "
                f"{uploaded_file.name}"
            )


    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    user_input = st.chat_input(

        "Ask anything..."

    )


    if user_input:


        # ---------------------------------------------
        # USER MESSAGE
        # ---------------------------------------------

        st.session_state.messages.append({

            "role": "user",

            "content": user_input

        })


        with st.chat_message("user"):

            st.markdown(user_input)


        # ---------------------------------------------
        # IMAGE PROCESSING
        # ---------------------------------------------

        image = None


        if uploaded_image is not None:

            try:

                image = Image.open(uploaded_image)

            except Exception:

                image = None


        # ---------------------------------------------
        # FINAL PROMPT
        # ---------------------------------------------

        final_prompt = user_input


        if file_text:

            final_prompt += (

                "\n\nUploaded File Information:\n"

                + file_text

            )


        # ---------------------------------------------
        # AI RESPONSE
        # ---------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(

                "🤖 Tech Mithra AI is thinking..."

            ):

                answer = ask_ai(

                    final_prompt,

                    image

                )


                st.markdown(answer)


        # ---------------------------------------------
        # SAVE MESSAGE
        # ---------------------------------------------

        st.session_state.messages.append({

            "role": "assistant",

            "content": answer

        })


        st.session_state.last_answer = answer


        # ---------------------------------------------
        # SAVE HISTORY
        # ---------------------------------------------

        save_history(

            user_input,

            answer

        )


# =========================================================
# EVENT PLANNER
# =========================================================

elif option == "📅 Event Planner":

    st.header("📅 Event Planner")

    st.write(

        "Plan your complete event from beginning to ending."

    )


    event_name = st.text_input(

        "🎉 Event Name"

    )


    event_type = st.selectbox(

        "📌 Event Type",

        [

            "College Event",

            "Technical Workshop",

            "Seminar",

            "Cultural Event",

            "Birthday",

            "Wedding",

            "Festival",

            "Other"

        ]

    )


    event_date = st.date_input(

        "📅 Event Date"

    )


    budget = st.number_input(

        "💰 Total Budget",

        min_value=0,

        value=10000

    )


    guests = st.number_input(

        "👥 Number of Guests",

        min_value=1,

        value=50

    )


    location = st.text_input(

        "📍 Event Location"

    )


    if st.button(

        "🚀 Create Complete Event Plan",

        use_container_width=True

    ):


        prompt = f"""

Create a COMPLETE professional event plan.

Event Name:
{event_name}

Event Type:
{event_type}

Event Date:
{event_date}

Budget:
₹{budget}

Number of Guests:
{guests}

Location:
{location}

Give a complete plan from STARTING to ENDING.

Include:

1. Event Introduction

2. Event Objective

3. Complete Budget Breakdown

4. Venue Planning

5. Decoration Planning

6. Stage Setup

7. Sound System

8. Lighting

9. Food Planning

10. Guest Management

11. Invitation Plan

12. Staff Requirements

13. Volunteer Requirements

14. Materials Required

15. Transportation Plan

16. Event Promotion

17. Social Media Promotion

18. Event Timeline

19. One Month Before Plan

20. One Week Before Plan

21. One Day Before Plan

22. Event Day Plan

23. Opening Ceremony

24. Main Event Activities

25. Closing Ceremony

26. Emergency Plan

27. Risk Management

28. Final Budget Summary

29. Final Checklist

30. After Event Activities

Make the answer practical and easy to understand.

"""


        with st.spinner(

            "📅 Creating Complete Event Plan..."

        ):

            answer = ask_ai(prompt)


        st.markdown(answer)


        save_history(

            f"Event Plan: {event_name}",

            answer

        )


# =========================================================
# EXAM HELPER
# =========================================================

elif option == "📚 Exam Helper":

    st.header("📚 Exam Helper")

    st.write(

        "Get answers, MCQs and important questions."

    )


    exam_type = st.selectbox(

        "Select Answer Type",

        [

            "Long Answer",

            "Short Answer",

            "5 Marks Answer",

            "10 Marks Answer",

            "Important Questions",

            "MCQ Questions",

            "MCQ With Answers",

            "Explain Topic"

        ]

    )


    subject = st.text_input(

        "📖 Subject Name"

    )


    topic = st.text_area(

        "✍️ Enter Topic or Question"

    )


    if st.button(

        "✨ Generate Answer",

        use_container_width=True

    ):


        prompt = f"""

You are an expert educational AI.

Subject:
{subject}

Topic:
{topic}

Answer Type:
{exam_type}

Generate an accurate student-friendly answer.

"""


        if exam_type == "Long Answer":

            prompt += """

Give a detailed long answer with:

Introduction
Definition
Explanation
Important Points
Examples
Advantages
Applications
Conclusion

"""


        elif exam_type == "Short Answer":

            prompt += """

Give a short and clear answer.

"""


        elif exam_type == "5 Marks Answer":

            prompt += """

Give a proper 5 marks examination answer.

Use headings and important points.

"""


        elif exam_type == "10 Marks Answer":

            prompt += """

Give a detailed 10 marks answer.

Use introduction, explanation,
diagram description if necessary,
advantages and conclusion.

"""


        elif exam_type == "Important Questions":

            prompt += """

Generate 15 important examination questions.

"""


        elif exam_type == "MCQ Questions":

            prompt += """

Generate 10 Multiple Choice Questions.

Format:

Question

A)
B)
C)
D)

Do NOT give answers.

"""


        elif exam_type == "MCQ With Answers":

            prompt += """

Generate 10 Multiple Choice Questions.

Format:

Question 1:

A)
B)
C)
D)

Correct Answer:

Explanation:

Give correct answers and
short explanations.

"""


        elif exam_type == "Explain Topic":

            prompt += """

Explain the topic from basics.

Use easy language and examples.

"""


        with st.spinner(

            "📚 Generating Answer..."

        ):

            answer = ask_ai(prompt)


        st.markdown(answer)


        save_history(

            f"Exam Helper: {topic}",

            answer

        )


# =========================================================
# PROJECT & LAB GUIDE
# =========================================================

elif option == "🔬 Project & Lab Guide":

    st.header("🔬 Project & Lab Guide")

    st.write(

        "Generate complete project and laboratory guidance."

    )


    project_type = st.selectbox(

        "Select",

        [

            "Mini Project",

            "Major Project",

            "Lab Experiment",

            "Arduino Project",

            "IoT Project",

            "Electrical Project",

            "Electronics Project",

            "Software Project"

        ]

    )


    project_topic = st.text_area(

        "Enter Project Topic"

    )


    if st.button(

        "🔬 Generate Complete Guide",

        use_container_width=True

    ):


        prompt = f"""

Create a complete student project guide.

Project Type:
{project_type}

Project Topic:
{project_topic}

Include:

1. Project Title

2. Abstract

3. Introduction

4. Objective

5. Problem Statement

6. Components Required

7. Hardware Requirements

8. Software Requirements

9. Working Principle

10. Block Diagram Explanation

11. Circuit Explanation

12. Step-by-Step Implementation

13. Algorithm

14. Applications

15. Advantages

16. Limitations

17. Future Scope

18. Result

19. Conclusion

20. Viva Questions

21. Important Interview Questions

Make the answer suitable for
college students.

"""


        with st.spinner(

            "🔬 Creating Project Guide..."

        ):

            answer = ask_ai(prompt)


        st.markdown(answer)


        save_history(

            f"Project: {project_topic}",

            answer

        )


# =========================================================
# GATE PREPARATION
# =========================================================

elif option == "🎓 GATE Preparation":

    st.header("🎓 GATE Preparation")

    st.write(

        "Prepare for GATE with concepts, formulas and MCQs."

    )


    branch = st.selectbox(

        "Select Engineering Branch",

        [

            "EEE",

            "ECE",

            "CSE",

            "Mechanical Engineering",

            "Civil Engineering",

            "Other"

        ]

    )


    gate_subject = st.text_input(

        "Subject Name"

    )


    gate_topic = st.text_area(

        "Enter Topic"

    )


    preparation_type = st.selectbox(

        "Preparation Type",

        [

            "Complete Topic Study",

            "Important Concepts",

            "Important Formulas",

            "MCQs With Answers",

            "Practice Questions",

            "Study Plan"

        ]

    )


    if st.button(

        "🎓 Generate GATE Preparation",

        use_container_width=True

    ):


        prompt = f"""

Create GATE preparation material.

Engineering Branch:
{branch}

Subject:
{gate_subject}

Topic:
{gate_topic}

Preparation Type:
{preparation_type}

Include:

1. Topic Introduction

2. Important Concepts

3. Important Definitions

4. Important Formulas

5. Formula Explanation

6. Important Shortcuts

7. Common Mistakes

8. Practice Questions

9. MCQ Questions

10. Correct Answers

11. Answer Explanations

12. Important GATE Tips

13. Revision Strategy

Make the content accurate,
clear and student-friendly.

"""


        with st.spinner(

            "🎓 Preparing GATE Material..."

        ):

            answer = ask_ai(prompt)


        st.markdown(answer)


        save_history(

            f"GATE: {gate_topic}",

            answer

        )


# =========================================================
# SETTINGS
# =========================================================

elif option == "⚙️ Settings":

    st.header("⚙️ Settings")


    # -----------------------------------------------------
    # AI SETTINGS
    # -----------------------------------------------------

    st.subheader("🤖 AI Settings")


    language = st.selectbox(

        "🌐 AI Response Language",

        [

            "English",

            "Telugu",

            "Telugu + English"

        ],

        index=[

            "English",

            "Telugu",

            "Telugu + English"

        ].index(

            st.session_state.language

        )

    )


    st.session_state.language = language


    st.success(

        f"Language: {language}"

    )


    st.divider()


    # -----------------------------------------------------
    # AI VOICE
    # -----------------------------------------------------

    st.subheader("🔊 AI Voice")


    if st.session_state.last_answer:


        safe_text = json.dumps(

            st.session_state.last_answer

        )


        st.markdown(

            f"""

<script>

function speakText() {{

    window.speechSynthesis.cancel();

    let text = {safe_text};

    let speech = new SpeechSynthesisUtterance(text);

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

<button onclick="speakText()">

▶️ Play

</button>

<button onclick="pauseSpeech()">

⏸️ Pause

</button>

<button onclick="resumeSpeech()">

▶️ Resume

</button>

""",

            unsafe_allow_html=True

        )


    else:

        st.info(

            "Ask AI a question first. "
            "Then the latest AI response can be used for voice."

        )


    st.divider()


    # -----------------------------------------------------
    # MICROPHONE
    # -----------------------------------------------------

    st.subheader("🎤 Voice Input")

    st.info(

        "Microphone input works through your browser. "
        "Allow microphone permission when prompted."

    )


    st.markdown(

        """

<button onclick="startListening()">

🎤 Start Voice Input

</button>


<p id="voiceText"></p>


<script>

function startListening() {

    const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech Recognition is not supported in this browser."
        );

        return;

    }


    const recognition =
    new SpeechRecognition();


    recognition.lang = "en-IN";


    recognition.start();


    recognition.onresult =
    function(event) {

        document.getElementById(
            "voiceText"
        ).innerHTML =
        event.results[0][0].transcript;

    };

}

</script>

""",

        unsafe_allow_html=True

    )


    st.divider()


    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    st.subheader("📜 History")


    if len(st.session_state.history) == 0:

        st.info(

            "No history available."

        )


    else:

        st.write(

            f"Total History: "
            f"{len(st.session_state.history)}"

        )


        for index, item in enumerate(

            reversed(
                st.session_state.history
            ),

            start=1

        ):


            with st.expander(

                f"{index}. {item['question']} "
                f"({item['time']})"

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

        "🗑️ Clear All History",

        use_container_width=True

    ):


        st.session_state.history = []


        st.session_state.messages = []


        st.success(

            "History cleared successfully!"

        )


        st.rerun()


    st.divider()


    # -----------------------------------------------------
    # CHAT SETTINGS
    # -----------------------------------------------------

    st.subheader("💬 Chat Settings")


    if st.button(

        "🧹 Clear Current Chat",

        use_container_width=True

    ):


        st.session_state.messages = []


        st.success(

            "Current chat cleared!"

        )


        st.rerun()


    st.divider()


    # -----------------------------------------------------
    # APP INFORMATION
    # -----------------------------------------------------

    st.subheader("ℹ️ App Information")


    st.write(

        "🤖 **App Name:** Tech Mithra AI"

    )


    st.write(

        "🎓 **Purpose:** AI Assistant for Students"

    )


    st.write(

        "💬 **Features:** AI Chat, Exam Helper, "
        "Event Planner, Project Guide and GATE Preparation"

    )


    st.divider()


    st.success(

        "⚙️ Settings saved for this session!"

    )
