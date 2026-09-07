# ============================================================
# TECH MITHRA AI
# COMPLETE STREAMLIT APPLICATION
# ============================================================

import streamlit as st
import os
import json
import base64
import tempfile
from datetime import datetime

# Optional file readers
try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except:
    DOCX_AVAILABLE = False

# Google Gemini AI
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except:
    GEMINI_AVAILABLE = False


# ============================================================
# PAGE CONFIGURATION
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

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
    }

    .main {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1100px;
    }

    /* TITLE */

    .app-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .app-subtitle {
        color: #9CA3AF;
        font-size: 17px;
        margin-bottom: 25px;
    }

    /* CHAT MESSAGE */

    .chat-user {
        background-color: #1F2937;
        padding: 15px;
        border-radius: 14px;
        margin: 10px 0px;
    }

    .chat-ai {
        background-color: #111827;
        padding: 15px;
        border-radius: 14px;
        margin: 10px 0px;
        border: 1px solid #1F2937;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* BUTTON */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* INPUT */

    .stTextInput input {
        border-radius: 10px;
    }

    .stTextArea textarea {
        border-radius: 10px;
    }

    /* EXPANDER */

    .streamlit-expanderHeader {
        font-size: 17px;
        font-weight: 600;
    }

    /* MOBILE */

    @media (max-width: 768px) {

        .app-title {
            font-size: 30px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# APP CONSTANTS
# ============================================================

APP_NAME = "Tech Mithra AI"

HISTORY_FILE = "tech_mithra_history.json"

MODEL_CANDIDATES = [

    "gemini-2.5-flash",

    "gemini-2.0-flash",

    "gemini-1.5-flash"

]


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "history" not in st.session_state:

    st.session_state.history = []


if "page" not in st.session_state:

    st.session_state.page = "AI Chat"


if "language" not in st.session_state:

    st.session_state.language = "English"


if "api_key" not in st.session_state:

    st.session_state.api_key = ""


if "uploaded_items" not in st.session_state:

    st.session_state.uploaded_items = []


if "last_answer" not in st.session_state:

    st.session_state.last_answer = ""


if "voice_text" not in st.session_state:

    st.session_state.voice_text = ""


# ============================================================
# LOAD HISTORY
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

                return data

    except:

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

                indent=4

            )

    except Exception as error:

        print("History Save Error:", error)


# ============================================================
# INITIAL HISTORY LOAD
# ============================================================

if len(st.session_state.history) == 0:

    saved_history = load_history()

    if saved_history:

        st.session_state.history = saved_history


# ============================================================
# ADD HISTORY
# ============================================================

def add_history(
    title,
    question,
    answer,
    category
):

    history_item = {

        "id": datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        ),

        "title": title,

        "question": question,

        "answer": answer,

        "category": category,

        "time": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

    }


    st.session_state.history.insert(

        0,

        history_item

    )


    save_history()


# ============================================================
# CLEAR HISTORY
# ============================================================

def clear_history():

    st.session_state.history = []

    save_history()


# ============================================================
# GET API KEY
# ============================================================

def get_api_key():

    # Session API Key

    if st.session_state.api_key:

        return st.session_state.api_key


    # Streamlit Secrets

    try:

        if "GEMINI_API_KEY" in st.secrets:

            return st.secrets["GEMINI_API_KEY"]

    except:

        pass


    # Environment Variable

    env_key = os.getenv(
        "GEMINI_API_KEY"
    )


    if env_key:

        return env_key


    return None


# ============================================================
# LANGUAGE INSTRUCTION
# ============================================================

def language_instruction():

    language = st.session_state.language


    if language == "Telugu":

        return """

Respond completely in Telugu.

Use simple Telugu language.

Technical words can be written
in English when necessary.

"""


    elif language == "Hindi":

        return """

Respond in Hindi.

Use simple and easy language.

"""


    else:

        return """

Respond in clear English.

Use simple language.

"""


# ============================================================
# CREATE AI CLIENT
# ============================================================

def get_ai_client():

    api_key = get_api_key()


    if not api_key:

        return None


    if not GEMINI_AVAILABLE:

        return None


    try:

        client = genai.Client(

            api_key=api_key

        )

        return client


    except:

        return None


# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(
    prompt,
    files=None
):

    api_key = get_api_key()


    if not api_key:

        return """

❌ Gemini API Key is not set.

Go to:

⚙️ Settings → Gemini API Key

Enter your API Key and save it.

"""


    if not GEMINI_AVAILABLE:

        return """

❌ Gemini AI library is not installed.

Run:

pip install google-genai

"""


    client = get_ai_client()


    if client is None:

        return """

❌ Unable to initialize AI.

Please check your Gemini API Key.

"""


    full_prompt = f"""

You are Tech Mithra AI.

You are a helpful AI assistant
for students.

You help with:

• Education
• Engineering
• Management
• Programming
• Projects
• Exams
• GATE Preparation
• Event Planning
• Lab Experiments
• General Questions

{language_instruction()}

USER QUESTION:

{prompt}

Give an accurate,
clear,
well-structured
and useful answer.

"""


    contents = [

        full_prompt

    ]


    # ========================================================
    # ADD FILES TO AI
    # ========================================================

    if files:

        for file in files:

            try:

                file_bytes = file.getvalue()


                mime_type = file.type


                if mime_type:

                    part = types.Part.from_bytes(

                        data=file_bytes,

                        mime_type=mime_type

                    )


                    contents.append(

                        part

                    )

            except:

                pass


    # ========================================================
    # MODEL FALLBACK SYSTEM
    # ========================================================

    last_error = ""


    for model_name in MODEL_CANDIDATES:

        try:

            response = client.models.generate_content(

                model=model_name,

                contents=contents

            )


            if response:

                if response.text:

                    return response.text


        except Exception as error:

            last_error = str(error)


    return f"""

❌ AI Error

Unable to generate a response.

Model Error:

{last_error}

Possible Solution:

1. Check your API Key
2. Check your Internet Connection
3. Make sure Gemini API is enabled
4. Update the google-genai package

Run:

pip install --upgrade google-genai

"""


# ============================================================
# READ TEXT FILE
# ============================================================

def read_uploaded_file(file):

    try:

        file_name = file.name.lower()


        # TXT FILE

        if file_name.endswith(".txt"):

            content = file.getvalue()

            return content.decode(
                "utf-8",
                errors="ignore"
            )


        # PDF FILE

        if file_name.endswith(".pdf"):

            if PDF_AVAILABLE:

                pdf = PdfReader(file)

                text = ""

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:

                        text += page_text + "\n"


                return text


            else:

                return "PDF reader is not installed."


        # DOCX FILE

        if file_name.endswith(".docx"):

            if DOCX_AVAILABLE:

                document = Document(file)

                text = ""

                for paragraph in document.paragraphs:

                    text += paragraph.text + "\n"


                return text


            else:

                return "DOCX reader is not installed."


    except Exception as error:

        return f"File reading error: {error}"


    return ""


# ============================================================
# TEXT TO SPEECH
# ============================================================

def text_to_speech_html(text):

    clean_text = text.replace(

        "`",

        ""

    )


    encoded_text = json.dumps(
        clean_text
    )


    html = f"""

<script>

const speechText = {encoded_text};

let speechInstance = null;

function playSpeech() {{

    window.speechSynthesis.cancel();

    speechInstance =
        new SpeechSynthesisUtterance(
            speechText
        );

    speechInstance.rate = 1;

    speechInstance.pitch = 1;

    window.speechSynthesis.speak(
        speechInstance
    );

}}

function pauseSpeech() {{

    window.speechSynthesis.pause();

}}

function resumeSpeech() {{

    window.speechSynthesis.resume();

}}

</script>

<button onclick="playSpeech()">

🔊 Play

</button>

<button onclick="pauseSpeech()">

⏸ Pause

</button>

<button onclick="resumeSpeech()">

▶ Resume

</button>

"""

    return html


# ============================================================
# DISPLAY VOICE BUTTONS
# ============================================================

def show_voice_buttons(text):

    if not text:

        return


    encoded_text = json.dumps(
        text
    )


    st.components.v1.html(

        f"""

<!DOCTYPE html>

<html>

<head>

<style>

body {{
    background: transparent;
    font-family: Arial;
}}

button {{

    background: #262730;

    color: white;

    border: 1px solid #555;

    padding: 10px 18px;

    border-radius: 8px;

    margin-right: 8px;

    cursor: pointer;

    font-size: 14px;

}}

button:hover {{

    background: #444;

}}

</style>

</head>

<body>

<button onclick="playText()">

🔊 Play

</button>

<button onclick="pauseText()">

⏸ Pause

</button>

<button onclick="resumeText()">

▶ Resume

</button>

<script>

let text =
{encoded_text};

let speech =
new SpeechSynthesisUtterance(text);


function playText() {{

    window.speechSynthesis.cancel();

    speech =
    new SpeechSynthesisUtterance(text);

    speech.rate = 1;

    window.speechSynthesis.speak(speech);

}}


function pauseText() {{

    window.speechSynthesis.pause();

}}


function resumeText() {{

    window.speechSynthesis.resume();

}}

</script>

</body>

</html>

""",

        height=65

    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:


    st.title(
        "🤖 Tech Mithra AI"
    )


    st.caption(
        "Your AI Study Assistant"
    )


    st.divider()


    # ========================================================
    # AI CHAT
    # ========================================================

    if st.button(

        "💬 AI Chat",

        use_container_width=True

    ):

        st.session_state.page = "AI Chat"


    # ========================================================
    # EVENT PLANNER
    # ========================================================

    if st.button(

        "📅 Event Planner",

        use_container_width=True

    ):

        st.session_state.page = "Event Planner"


    # ========================================================
    # EXAM HELPER
    # ========================================================

    if st.button(

        "📝 Exam Helper",

        use_container_width=True

    ):

        st.session_state.page = "Exam Helper"


    # ========================================================
    # PROJECT & LAB GUIDE
    # ========================================================

    if st.button(

        "🔬 Project & Lab Guide",

        use_container_width=True

    ):

        st.session_state.page = "Project & Lab Guide"


    # ========================================================
    # GATE PREPARATION
    # ========================================================

    if st.button(

        "🎯 GATE Preparation",

        use_container_width=True

    ):

        st.session_state.page = "GATE Preparation"


    # ========================================================
    # SETTINGS
    # ========================================================

    if st.button(

        "⚙️ Settings",

        use_container_width=True

    ):

        st.session_state.page = "Settings"


    st.divider()


    st.caption(
        "Tech Mithra AI • Student Assistant"
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.page


# ============================================================
# AI CHAT PAGE
# ============================================================

if page == "AI Chat":


    st.markdown(

        '<div class="app-title">🤖 Tech Mithra AI</div>',

        unsafe_allow_html=True

    )


    st.markdown(

        '<div class="app-subtitle">Ask anything • Upload Photo • Camera • Files • Audio</div>',

        unsafe_allow_html=True

    )


    # ========================================================
    # DISPLAY CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:


        with st.chat_message(

            message["role"]

        ):


            st.markdown(

                message["content"]

            )


            # Voice only for AI messages

            if message["role"] == "assistant":

                show_voice_buttons(

                    message["content"]

                )


    # ========================================================
    # PLUS OPTIONS
    # ========================================================

    with st.popover(

        "➕"

    ):


        st.subheader(
            "Add Attachment"
        )


        # PHOTO

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


        # CAMERA

        camera_photo = st.camera_input(

            "📷 Camera"

        )


        # FILE

        uploaded_files = st.file_uploader(

            "📁 Upload Files",

            type=[

                "pdf",

                "docx",

                "txt"

            ],

            accept_multiple_files=True,

            key="chat_files"

        )


        # AUDIO

        try:

            audio_input = st.audio_input(

                "🎤 Record Audio"

            )

        except:

            audio_input = None


        if uploaded_photo:

            if st.button(

                "Add Uploaded Photo"

            ):

                st.session_state.uploaded_items.append(

                    uploaded_photo

                )

                st.success(
                    "Photo Added!"
                )


        if camera_photo:

            if st.button(

                "Add Camera Photo"

            ):

                st.session_state.uploaded_items.append(

                    camera_photo

                )

                st.success(
                    "Camera Photo Added!"
                )


        if uploaded_files:

            if st.button(

                "Add Files"

            ):

                for file in uploaded_files:

                    st.session_state.uploaded_items.append(

                        file

                    )


                st.success(
                    "Files Added!"
                )


        if audio_input:

            if st.button(

                "Add Audio"

            ):

                st.session_state.uploaded_items.append(

                    audio_input

                )


                st.success(
                    "Audio Added!"
                )


    # ========================================================
    # SHOW ATTACHMENTS
    # ========================================================

    if st.session_state.uploaded_items:


        with st.expander(

            f"📎 Attachments ({len(st.session_state.uploaded_items)})"

        ):


            for index, item in enumerate(

                st.session_state.uploaded_items

            ):


                st.write(

                    f"{index + 1}. {item.name}"

                )


            if st.button(

                "🗑️ Remove All Attachments"

            ):

                st.session_state.uploaded_items = []

                st.rerun()


    # ========================================================
    # CHATGPT STYLE INPUT
    # ========================================================

    user_question = st.chat_input(

        "Ask anything..."

    )


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    if user_question:


        st.session_state.messages.append(

            {

                "role": "user",

                "content": user_question

            }

        )


        with st.chat_message(

            "user"

        ):

            st.markdown(
                user_question
            )


        with st.chat_message(

            "assistant"

        ):


            with st.spinner(

                "🤖 Thinking..."

            ):


                # File text

                file_text = ""


                for item in st.session_state.uploaded_items:


                    try:

                        if item.name.lower().endswith(

                            (

                                ".pdf",

                                ".docx",

                                ".txt"

                            )

                        ):


                            file_text += (

                                "\n\nFILE: "

                                + item.name

                                + "\n"

                                + read_uploaded_file(item)

                            )

                    except:

                        pass


                final_question = user_question


                if file_text:


                    final_question += f"""

Analyze the following file content:

{file_text}

"""


                answer = ask_ai(

                    final_question,

                    st.session_state.uploaded_items

                )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


        st.session_state.last_answer = answer


        st.session_state.messages.append(

            {

                "role": "assistant",

                "content": answer

            }

        )


        add_history(

            "AI Chat",

            user_question,

            answer,

            "AI Chat"

        )


        # Clear attachments after response

        st.session_state.uploaded_items = []


# ============================================================
# EVENT PLANNER
# ============================================================

elif page == "Event Planner":


    st.title(
        "📅 AI Event Planner"
    )


    st.write(

        """
Plan your complete event from
starting to ending with budget planning.
"""

    )


    st.divider()


    # ========================================================
    # EVENT DETAILS
    # ========================================================

    st.subheader(
        "📝 Event Details"
    )


    event_name = st.text_input(

        "Event Name",

        placeholder="Example: Tech Fest 2026"

    )


    event_type = st.selectbox(

        "Event Type",

        [

            "College Event",

            "Technical Event",

            "Cultural Event",

            "Workshop",

            "Seminar",

            "Conference",

            "Sports Event",

            "Birthday Event",

            "Wedding Event",

            "Festival",

            "Farewell Party",

            "Freshers Party",

            "Other"

        ]

    )


    event_date = st.date_input(

        "Event Date"

    )


    event_duration = st.selectbox(

        "Event Duration",

        [

            "1 Day",

            "2 Days",

            "3 Days",

            "More than 3 Days"

        ]

    )


    st.divider()


    # ========================================================
    # LOCATION
    # ========================================================

    st.subheader(
        "📍 Location"
    )


    event_location = st.text_input(

        "Event Location / City",

        placeholder="Example: Hyderabad"

    )


    venue_type = st.selectbox(

        "Venue Type",

        [

            "College Campus",

            "Auditorium",

            "Function Hall",

            "Open Ground",

            "Hotel",

            "Conference Hall",

            "Online Event",

            "Other"

        ]

    )


    st.divider()


    # ========================================================
    # PARTICIPANTS
    # ========================================================

    st.subheader(
        "👥 Participants"
    )


    event_people = st.number_input(

        "Expected Participants",

        min_value=1,

        value=100

    )


    special_guests = st.number_input(

        "Number of Special Guests",

        min_value=0,

        value=0

    )


    st.divider()


    # ========================================================
    # BUDGET
    # ========================================================

    st.subheader(
        "💰 Budget"
    )


    event_budget = st.number_input(

        "Total Available Budget",

        min_value=0,

        value=10000,

        step=1000

    )


    currency = st.selectbox(

        "Currency",

        [

            "INR ₹",

            "USD $"

        ]

    )


    st.divider()


    # ========================================================
    # REQUIREMENTS
    # ========================================================

    st.subheader(
        "🎯 Special Requirements"
    )


    requirements = st.text_area(

        "Enter your requirements",

        placeholder="""
Example:

DJ
Stage
Sound System
Food
Photography
Certificates
Decorations
Transportation

"""

    )


    # ========================================================
    # GENERATE EVENT PLAN
    # ========================================================

    if st.button(

        "🚀 Generate Complete Event Plan",

        use_container_width=True

    ):


        if not event_name:


            st.warning(

                "⚠️ Please enter Event Name."

            )


        else:


            event_prompt = f"""

You are a professional Event Planner.

Create a COMPLETE EVENT PLAN
from the beginning until the event
is completely finished.

EVENT DETAILS:

Event Name:
{event_name}

Event Type:
{event_type}

Event Date:
{event_date}

Duration:
{event_duration}

Location:
{event_location}

Venue:
{venue_type}

Participants:
{event_people}

Special Guests:
{special_guests}

Total Budget:
{currency} {event_budget}

Special Requirements:

{requirements}


Create a professional
step-by-step plan.

Include:

1. Event Overview

2. Event Objectives

3. Planning Team

4. Team Responsibilities

5. Complete Timeline

6. 30 Days Before Event

7. 20 Days Before Event

8. 15 Days Before Event

9. 10 Days Before Event

10. 7 Days Before Event

11. 3 Days Before Event

12. 1 Day Before Event

13. Venue Planning

14. Seating Arrangement

15. Stage Planning

16. Registration Plan

17. Participant Management

18. Guest Management

19. Budget Breakdown

20. Create a detailed budget table.

Divide the budget into:

• Venue
• Stage
• Decoration
• Sound
• Lighting
• Food
• Photography
• Videography
• Certificates
• Printing
• Marketing
• Transportation
• Emergency Fund

Make the budget realistic and
close to the available budget.

22. Marketing Plan

23. Social Media Promotion

24. WhatsApp Promotion

25. Instagram Promotion

26. Required Materials Checklist

27. Technical Setup

28. Sound System

29. Microphones

30. Projector

31. Internet

32. Power Backup

33. Food Planning

34. Event Day Schedule

35. Team Arrival

36. Venue Setup

37. Registration

38. Guest Arrival

39. Event Opening

40. Main Program

41. Break

42. Lunch

43. Final Session

44. Vote of Thanks

45. Event Closing

46. Photography

47. Cleanup

48. Emergency Plan

Include solutions for:

• Power Failure
• Internet Failure
• Sound Failure
• Rain
• Medical Emergency
• Guest Delay
• Food Shortage

49. Post Event Activities

50. Feedback Collection

51. Financial Report

52. Final Event Report

53. Final Checklist

54. Day 1 to Event End Summary

Make the answer practical,
detailed,
professional
and easy to understand.

"""


            with st.spinner(

                "🤖 Creating Complete Event Plan..."

            ):


                answer = ask_ai(

                    event_prompt

                )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


            st.session_state.last_answer = answer


            add_history(

                event_name,

                event_prompt,

                answer,

                "Event Planner"

            )


# ============================================================
# EXAM HELPER
# ============================================================

elif page == "Exam Helper":


    st.title(
        "📝 AI Exam Helper"
    )


    st.write(

        "Get answers, explanations and MCQ solutions."

    )


    exam_option = st.selectbox(

        "Select Option",

        [

            "Write Answer",

            "MCQ Answer",

            "Explain Topic",

            "Short Answer",

            "Long Answer",

            "5 Marks Answer",

            "10 Marks Answer",

            "Important Questions"

        ]

    )


    st.divider()


    # ========================================================
    # WRITE ANSWER
    # ========================================================

    if exam_option == "Write Answer":


        question = st.text_area(

            "Enter your Question"

        )


        if st.button(

            "🤖 Generate Answer",

            use_container_width=True

        ):


            if question:


                prompt = f"""

Answer this exam question:

{question}

Give a clear,
accurate
and well-structured answer.

Include headings and points.

"""


                with st.spinner(

                    "Generating Answer..."

                ):


                    answer = ask_ai(
                        prompt
                    )


                st.markdown(
                    answer
                )


                show_voice_buttons(
                    answer
                )


                add_history(

                    "Exam Answer",

                    question,

                    answer,

                    "Exam Helper"

                )


    # ========================================================
    # MCQ
    # ========================================================

    elif exam_option == "MCQ Answer":


        mcq_question = st.text_area(

            "Enter MCQ Question"

        )


        option_a = st.text_input(
            "Option A"
        )


        option_b = st.text_input(
            "Option B"
        )


        option_c = st.text_input(
            "Option C"
        )


        option_d = st.text_input(
            "Option D"
        )


        if st.button(

            "✅ Find Correct Answer",

            use_container_width=True

        ):


            if mcq_question:


                prompt = f"""

Solve this MCQ.

Question:

{mcq_question}

Options:

A. {option_a}

B. {option_b}

C. {option_c}

D. {option_d}

Give:

1. Correct Option
2. Correct Answer
3. Short Explanation

"""


                with st.spinner(

                    "Finding Answer..."

                ):


                    answer = ask_ai(
                        prompt
                    )


                st.markdown(
                    answer
                )


                show_voice_buttons(
                    answer
                )


                add_history(

                    "MCQ Answer",

                    mcq_question,

                    answer,

                    "Exam Helper"

                )


    # ========================================================
    # EXPLAIN TOPIC
    # ========================================================

    elif exam_option == "Explain Topic":


        topic = st.text_area(

            "Enter Topic"

        )


        if st.button(

            "📚 Explain",

            use_container_width=True

        ):


            if topic:


                prompt = f"""

Explain this topic:

{topic}

Explain from basic to advanced.

Use:

• Simple Definition
• Explanation
• Important Points
• Examples
• Summary

"""


                answer = ask_ai(
                    prompt
                )


                st.markdown(
                    answer
                )


                show_voice_buttons(
                    answer
                )


    # ========================================================
    # SHORT ANSWER
    # ========================================================

    elif exam_option == "Short Answer":


        question = st.text_area(

            "Enter Question"

        )


        if st.button(

            "Generate Short Answer"

        ):


            prompt = f"""

Give a short exam answer
for the following question:

{question}

Use simple points.

"""


            answer = ask_ai(
                prompt
            )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


    # ========================================================
    # LONG ANSWER
    # ========================================================

    elif exam_option == "Long Answer":


        question = st.text_area(

            "Enter Question"

        )


        if st.button(

            "Generate Long Answer"

        ):


            prompt = f"""

Give a detailed long answer
for this exam question:

{question}

Include:

• Introduction
• Definition
• Detailed Explanation
• Important Points
• Examples
• Conclusion

"""


            answer = ask_ai(
                prompt
            )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


    # ========================================================
    # 5 MARKS
    # ========================================================

    elif exam_option == "5 Marks Answer":


        question = st.text_area(

            "Enter Question"

        )


        if st.button(

            "Generate 5 Marks Answer"

        ):


            prompt = f"""

Write a proper 5 marks answer
for:

{question}

Use exam style format.

"""


            answer = ask_ai(
                prompt
            )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


    # ========================================================
    # 10 MARKS
    # ========================================================

    elif exam_option == "10 Marks Answer":


        question = st.text_area(

            "Enter Question"

        )


        if st.button(

            "Generate 10 Marks Answer"

        ):


            prompt = f"""

Write a detailed 10 marks answer
for:

{question}

Include:

Introduction

Definition

Explanation

Important Points

Examples

Diagram explanation if needed

Conclusion

"""


            answer = ask_ai(
                prompt
            )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


    # ========================================================
    # IMPORTANT QUESTIONS
    # ========================================================

    elif exam_option == "Important Questions":


        subject = st.text_input(

            "Enter Subject"

        )


        topic = st.text_input(

            "Enter Topic"

        )


        if st.button(

            "Generate Important Questions"

        ):


            prompt = f"""

Generate important exam questions.

Subject:

{subject}

Topic:

{topic}

Include:

• Very Important Questions
• Short Questions
• Long Questions
• 5 Marks Questions
• 10 Marks Questions
• MCQs

"""


            answer = ask_ai(
                prompt
            )


            st.markdown(
                answer
            )


# ============================================================
# PROJECT & LAB GUIDE
# ============================================================

elif page == "Project & Lab Guide":


    st.title(
        "🔬 Project & Lab Guide"
    )


    project_option = st.selectbox(

        "Select Option",

        [

            "Project Idea",

            "Complete Project Guide",

            "Lab Experiment",

            "Project Report",

            "Project Viva Questions",

            "Lab Viva Questions",

            "Circuit Explanation",

            "Programming Project"

        ]

    )


    topic = st.text_area(

        "Enter Project / Topic / Experiment"

    )


    if st.button(

        "🚀 Generate Guide",

        use_container_width=True

    ):


        if topic:


            prompt = f"""

You are an expert
Project and Lab Guide.

Option:

{project_option}

Topic:

{topic}

Generate a detailed guide.

Include relevant sections such as:

• Introduction
• Objective
• Requirements
• Components
• Software
• Hardware
• Theory
• Working Principle
• Block Diagram Explanation
• Step-by-Step Procedure
• Implementation
• Code Explanation
• Output
• Result
• Advantages
• Applications
• Conclusion
• Viva Questions

Make it suitable for students.

"""


            with st.spinner(

                "🤖 Generating Guide..."

            ):


                answer = ask_ai(
                    prompt
                )


            st.markdown(
                answer
            )


            show_voice_buttons(
                answer
            )


            add_history(

                project_option,

                topic,

                answer,

                "Project & Lab Guide"

            )


# ============================================================
# GATE PREPARATION
# ============================================================

elif page == "GATE Preparation":


    st.title(
        "🎯 GATE Preparation"
    )


    st.write(

        "AI-powered preparation for GATE examination."

    )


    gate_option = st.selectbox(

        "Select Option",

        [

            "Study Plan",

            "Topic Explanation",

            "Practice Questions",

            "MCQs",

            "Previous Year Question Style",

            "Important Topics",

            "Revision Plan",

            "Weekly Study Plan"

        ]

    )


    branch = st.selectbox(

        "Select Branch",

        [

            "Electrical Engineering",

            "Electronics Engineering",

            "Computer Science",

            "Mechanical Engineering",

            "Civil Engineering",

            "Other"

        ]

    )


    topic = st.text_area(

        "Enter Topic / Subject"

    )


    study_hours = st.number_input(

        "Daily Study Hours",

        min_value=1,

        max_value=24,

        value=3

    )


    if st.button(

        "🎯 Generate GATE Plan",

        use_container_width=True

    ):


        prompt = f"""

You are an expert GATE mentor.

GATE Option:

{gate_option}

Branch:

{branch}

Topic:

{topic}

Daily Study Hours:

{study_hours}

Create a useful
and practical preparation guide.

Include:

• Study Strategy
• Important Concepts
• Important Topics
• Practice Questions
• MCQs if required
• Preparation Tips
• Revision Strategy
• Common Mistakes
• Daily Plan

Make it suitable for a student.

"""


        with st.spinner(

            "🎯 Preparing GATE Content..."

        ):


            answer = ask_ai(
                prompt
            )


        st.markdown(
            answer
        )


        show_voice_buttons(
            answer
        )


        add_history(

            "GATE " + gate_option,

            topic,

            answer,

            "GATE Preparation"

        )


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":


    st.title(
        "⚙️ Settings"
    )


    # ========================================================
    # AI SETTINGS
    # ========================================================

    st.subheader(
        "🤖 AI Settings"
    )


    language = st.selectbox(

        "🌐 AI Language",

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


    st.success(

        f"Language: {language}"

    )


    st.divider()


    # ========================================================
    # API SETTINGS
    # ========================================================

    st.subheader(
        "🔑 Gemini API Settings"
    )


    api_key_input = st.text_input(

        "Gemini API Key",

        value=st.session_state.api_key,

        type="password",

        placeholder="Paste your Gemini API Key"

    )


    if st.button(

        "💾 Save API Key",

        use_container_width=True

    ):


        if api_key_input:


            st.session_state.api_key = (

                api_key_input

            )


            st.success(

                "✅ API Key saved for this session."

            )


        else:


            st.warning(

                "Please enter an API Key."

            )


    st.info(

        """
For permanent deployment,
use Streamlit Secrets
instead of writing the API key
directly inside the code.
"""

    )


    st.divider()


    # ========================================================
    # VOICE SETTINGS
    # ========================================================

    st.subheader(
        "🔊 AI Voice"
    )


    st.write(

        """
Use these controls below
to listen to AI responses.
"""

    )


    if st.session_state.last_answer:


        show_voice_buttons(

            st.session_state.last_answer

        )


    else:


        st.info(

            "Ask a question first. AI response voice controls will appear here."

        )


    st.divider()


    # ========================================================
    # HISTORY
    # ========================================================

    st.subheader(
        "🕘 History"
    )


    if len(

        st.session_state.history

    ) == 0:


        st.info(

            "No history available."

        )


    else:


        st.write(

            f"Total History: {len(st.session_state.history)}"

        )


        for index, item in enumerate(

            st.session_state.history

        ):


            with st.expander(

                f"{item['category']} • {item['title']} • {item['time']}"

            ):


                st.markdown(

                    "### ❓ Question"

                )


                st.write(

                    item["question"]

                )


                st.markdown(

                    "### 🤖 Answer"

                )


                st.markdown(

                    item["answer"]

                )


                show_voice_buttons(

                    item["answer"]

                )


    st.divider()


    # ========================================================
    # CLEAR HISTORY
    # ========================================================

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


    # ========================================================
    # APP INFORMATION
    # ========================================================

    st.subheader(
        "ℹ️ App Information"
    )


    st.write(

        "App Name: Tech Mithra AI"

    )


    st.write(

        "Features: AI Chat, Exam Helper, Event Planner, Project Guide and GATE Preparation"

    )


    st.write(

        "History is stored until you clear it."

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(

    "🤖 Tech Mithra AI • Your Smart AI Study Assistant"

)
