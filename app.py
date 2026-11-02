
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EEE Machines 3D Learning",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #17243a);
    color: white;
}
h1, h2, h3 { color: #65d6ff !important; }
div[data-testid="stTabs"] button {
    color: white;
}
</style>
""", unsafe_allow_html=True)

MACHINES = {
    "DC Machines": {
        "model": "https://sketchfab.com/models/e9ac2cf2f2d04180b02965c01f7a9a19/embed",
        "principle": "A current-carrying conductor placed in a magnetic field experiences a force. This principle is used in a DC motor.",
        "parts": {
            "Yoke": "Provides mechanical support and a path for magnetic flux.",
            "Pole Core": "Carries the field winding and produces magnetic flux.",
            "Field Winding": "Produces the main magnetic field.",
            "Armature": "Rotating part in which EMF is induced.",
            "Commutator": "Helps maintain unidirectional torque in a DC motor.",
            "Brushes": "Transfer current between the external circuit and commutator."
        },
        "applications": "Electric traction, cranes, lifts, rolling mills and variable-speed drives.",
        "notes": "DC machines can work as motors or generators. A motor converts electrical energy into mechanical energy."
    },
    "Transformer": {
        "model": "https://sketchfab.com/models/9e7076096b0346dfbbc729f75f1b41be/embed",
        "principle": "A transformer works on the principle of mutual electromagnetic induction.",
        "parts": {
            "Core": "Provides a low-reluctance path for magnetic flux.",
            "Primary Winding": "Receives electrical energy from the supply.",
            "Secondary Winding": "Delivers electrical energy to the load.",
            "Insulation": "Prevents unwanted electrical contact between windings and core.",
            "Tank": "Houses and protects the transformer components."
        },
        "applications": "Power transmission, distribution systems, chargers, substations and electrical isolation.",
        "notes": "A transformer changes AC voltage levels without changing frequency. It can be step-up or step-down."
    },
    "Three Phase Induction Motor": {
        "model": "https://sketchfab.com/models/b02c98e04e614d97897e3dababb70bc8/embed",
        "principle": "A three-phase supply produces a rotating magnetic field. This field induces current in the rotor and produces torque.",
        "parts": {
            "Stator": "Stationary part that produces the rotating magnetic field.",
            "Rotor": "Rotating part that develops mechanical torque.",
            "Air Gap": "Small gap between stator and rotor.",
            "Bearings": "Support the shaft and allow smooth rotation.",
            "Cooling Fan": "Helps remove heat from the motor.",
            "Shaft": "Transfers mechanical output to the load."
        },
        "applications": "Pumps, fans, compressors, conveyors and industrial drives.",
        "notes": "An induction motor works with electromagnetic induction. Its rotor speed is normally below synchronous speed."
    },
    "Single Phase Induction Motor": {
        "model": None,
        "principle": "A single-phase AC supply produces a pulsating magnetic field. A starting arrangement helps the motor start rotating.",
        "parts": {
            "Stator": "Contains the main and auxiliary windings.",
            "Rotor": "Usually a squirrel-cage rotor that develops torque.",
            "Main Winding": "Produces the main magnetic field.",
            "Auxiliary Winding": "Helps produce starting torque.",
            "Capacitor": "Provides phase shift in capacitor-start or capacitor-run motors.",
            "Centrifugal Switch": "Disconnects the starting winding in some motor designs."
        },
        "applications": "Ceiling fans, small pumps, refrigerators and domestic appliances.",
        "notes": "A single-phase induction motor is not inherently self-starting."
    },
    "Synchronous Machines": {
        "model": None,
        "principle": "The rotor rotates in synchronism with the rotating magnetic field produced by the stator.",
        "parts": {
            "Stator": "Contains the armature winding.",
            "Rotor": "Carries the field system.",
            "Field Winding": "Produces the rotor magnetic field.",
            "Damper Winding": "Helps reduce oscillations in some synchronous machines.",
            "Shaft": "Transfers mechanical power."
        },
        "applications": "Power generation, power-factor improvement and constant-speed drives.",
        "notes": "Synchronous speed is Ns = 120f/P RPM."
    },
    "Alternator": {
        "model": None,
        "principle": "An alternator converts mechanical energy into AC electrical energy by electromagnetic induction.",
        "parts": {
            "Stator": "Contains the three-phase armature winding.",
            "Rotor": "Produces the rotating magnetic field.",
            "Exciter": "Supplies field current to the rotor.",
            "Slip Rings": "Used in some alternator designs to supply rotor field current.",
            "Shaft": "Receives mechanical input from the prime mover."
        },
        "applications": "Power stations, diesel generator sets and hydroelectric plants.",
        "notes": "Alternators generate AC voltage. Frequency depends on speed and number of poles."
    },
    "Special Electrical Machines": {
        "model": None,
        "principle": "Special machines use different electromagnetic arrangements to produce controlled motion or electrical output.",
        "parts": {
            "Stator": "Stationary magnetic structure.",
            "Rotor": "Moving part of the machine.",
            "Windings": "Produce or interact with magnetic fields.",
            "Controller": "Controls operation in electronically controlled machines.",
            "Position Sensor": "Detects rotor position in some designs."
        },
        "applications": "Robotics, automation, electric vehicles and precision control.",
        "notes": "Examples include stepper motors, servo motors, BLDC motors and switched reluctance motors."
    }
}

st.title("⚡ B.Tech EEE – Electrical Machines")
st.caption("Learn machine construction, working principles and applications with 3D models.")

machine_name = st.sidebar.selectbox(
    "Select Electrical Machine",
    list(MACHINES.keys())
)

data = MACHINES[machine_name]

st.header("🔧 " + machine_name)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌐 3D Model",
    "⚙️ Parts",
    "📘 Working",
    "📝 Notes",
    "🎓 Viva"
])

with tab1:
    st.subheader("Interactive 3D Machine View")
    if data["model"]:
        st.info("Drag to rotate • Scroll to zoom • Use the viewer controls")
        components.iframe(
            data["model"] + "?autostart=0&ui_theme=dark",
            height=550,
            scrolling=False
        )
    else:
        st.warning(
            "ఈ Machine కోసం ప్రత్యేకమైన 3D model ఇంకా జోడించలేదు. "
            "ప్రస్తుతానికి Parts మరియు Working వివరాలు చూడవచ్చు."
        )

with tab2:
    st.subheader("Machine Parts and Functions")
    for part, description in data["parts"].items():
        with st.expander("🔹 " + part):
            st.write(description)

with tab3:
    st.subheader("Working Principle")
    st.write(data["principle"])
    st.subheader("Applications")
    st.write(data["applications"])

with tab4:
    st.subheader("Study Notes")
    st.write(data["notes"])
    st.markdown("### Important Points")
    for part, description in data["parts"].items():
        st.markdown(f"- **{part}:** {description}")

with tab5:
    st.subheader("Viva Questions")
    questions = {
        "DC Machines": [
            ("What is a DC machine?", "A machine that converts mechanical energy into DC electrical energy or vice versa."),
            ("What is the function of a commutator?", "It helps maintain unidirectional torque in a DC motor."),
            ("What is back EMF?", "The EMF induced in the armature that opposes the applied voltage.")
        ],
        "Transformer": [
            ("What is a transformer?", "A static device that transfers AC power between circuits through electromagnetic induction."),
            ("What is the function of the core?", "It provides a path for magnetic flux."),
            ("What is the turns ratio?", "The ratio of secondary winding turns to primary winding turns.")
        ],
        "Three Phase Induction Motor": [
            ("What is an induction motor?", "An AC motor in which rotor current is induced by the stator magnetic field."),
            ("What is slip?", "The difference between synchronous speed and rotor speed divided by synchronous speed."),
            ("What is synchronous speed?", "Ns = 120f/P RPM.")
        ]
    }

    default_questions = [
        ("What is the working principle?", data["principle"]),
        ("Name two main parts.", ", ".join(list(data["parts"].keys())[:2])),
        ("Mention two applications.", data["applications"])
    ]

    selected_questions = questions.get(machine_name, default_questions)

    for i, (question, answer) in enumerate(selected_questions, 1):
        with st.expander(f"Q{i}. {question}"):
            st.write("**Answer:**", answer)

st.sidebar.markdown("---")
st.sidebar.caption("EEE Learning App | 3D Learning Edition")
