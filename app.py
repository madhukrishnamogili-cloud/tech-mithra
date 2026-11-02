import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Tech Mithra AI",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: white;
}
h1,h2,h3 {
    color: #00d4ff;
}
div.stButton > button {
    background: #087ea4;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# MACHINE DATABASE

machines = {
    "DC Machines": {
        "parts": {
            "Yoke": "Provides mechanical support and acts as a magnetic path.",
            "Pole Core": "Carries the field winding and produces magnetic flux.",
            "Field Winding": "Produces the magnetic field.",
            "Armature Core": "Provides a path for magnetic flux.",
            "Armature Winding": "Conductors in which EMF is induced.",
            "Commutator": "Converts internally induced AC into DC at the terminals.",
            "Brushes": "Transfer current between the rotating commutator and external circuit."
        },
        "working": "DC machine works on electromagnetic induction as a generator and force on a current-carrying conductor as a motor.",
        "applications": "Electric traction, battery charging, cranes and industrial drives.",
        "notes": "DC machines are classified into DC generators and DC motors. Important equations: Eb = PΦZN/60A and T ∝ ΦIa.",
        "viva": [
            "What is a DC machine?",
            "What is the function of a commutator?",
            "What is back EMF?",
            "What is armature reaction?",
            "What are the types of DC motors?"
        ]
    },

    "Transformer": {
        "parts": {
            "Magnetic Core": "Provides a low reluctance path for magnetic flux.",
            "Primary Winding": "Receives electrical energy from the AC supply.",
            "Secondary Winding": "Delivers electrical energy to the load.",
            "Insulation": "Prevents electrical leakage between windings.",
            "Transformer Oil": "Provides cooling and insulation in oil-filled transformers.",
            "Tank": "Houses and protects the transformer.",
            "Bushing": "Provides insulated terminals for electrical connections."
        },
        "working": "Transformer works on mutual electromagnetic induction. AC in the primary winding produces changing flux that induces EMF in the secondary winding.",
        "applications": "Power transmission, distribution, chargers and electrical isolation.",
        "notes": "EMF equation: E = 4.44 f N Φm. Turns ratio: V1/V2 = N1/N2 for an ideal transformer.",
        "viva": [
            "What is a transformer?",
            "What is mutual induction?",
            "What are transformer losses?",
            "Why is transformer oil used?",
            "What is the turns ratio?"
        ]
    },

    "Three Phase Induction Motor": {
        "parts": {
            "Stator": "Stationary part that produces a rotating magnetic field.",
            "Rotor": "Rotating part that develops mechanical torque.",
            "Air Gap": "Small gap between stator and rotor.",
            "Shaft": "Transfers mechanical power.",
            "Bearings": "Support smooth shaft rotation.",
            "Fan": "Provides cooling.",
            "Frame": "Provides mechanical protection."
        },
        "working": "A three-phase supply creates a rotating magnetic field. This induces rotor current and produces electromagnetic torque.",
        "applications": "Pumps, fans, compressors and industrial machinery.",
        "notes": "Synchronous speed Ns = 120f/P. Slip s = (Ns-N)/Ns.",
        "viva": [
            "What is an induction motor?",
            "Define slip.",
            "What is synchronous speed?",
            "Why can an induction motor not run at synchronous speed?",
            "What is a squirrel cage rotor?"
        ]
    },

    "Single Phase Induction Motor": {
        "parts": {
            "Stator": "Produces the magnetic field.",
            "Main Winding": "Provides the main magnetic field.",
            "Auxiliary Winding": "Helps in starting.",
            "Capacitor": "Creates phase difference for starting in capacitor motors.",
            "Rotor": "Develops mechanical torque.",
            "Centrifugal Switch": "Disconnects the starting winding in applicable designs."
        },
        "working": "A single-phase supply produces a pulsating magnetic field. Starting arrangements create the required starting torque.",
        "applications": "Ceiling fans, pumps, refrigerators and washing machines.",
        "notes": "Single-phase induction motors are not inherently self-starting. Common types include split-phase, capacitor-start and shaded-pole motors.",
        "viva": [
            "Why is a single-phase motor not self-starting?",
            "What is the function of a capacitor?",
            "What is a shaded-pole motor?",
            "What is a split-phase motor?",
            "Where are single-phase motors used?"
        ]
    },

    "Synchronous Machines": {
        "parts": {
            "Stator": "Contains the armature winding.",
            "Rotor": "Carries the field system.",
            "Field Winding": "Produces rotor magnetic flux.",
            "Damper Winding": "Helps with starting in applicable motors and reduces oscillations.",
            "Shaft": "Transfers mechanical power.",
            "Bearings": "Support the rotor."
        },
        "working": "The rotor magnetic field locks with the rotating stator magnetic field and runs at synchronous speed.",
        "applications": "Power generation, power factor correction and industrial drives.",
        "notes": "Synchronous speed Ns = 120f/P. Power factor can be controlled by field excitation.",
        "viva": [
            "What is a synchronous machine?",
            "Define synchronous speed.",
            "What is excitation?",
            "What is a synchronous condenser?",
            "What is hunting?"
        ]
    },

    "Alternator": {
        "parts": {
            "Stator Core": "Provides a magnetic path and supports the armature winding.",
            "Armature Winding": "Generates three-phase EMF.",
            "Rotor": "Carries the DC field winding.",
            "Field Winding": "Produces the rotor magnetic field.",
            "Slip Rings": "Supply DC excitation to applicable rotor designs.",
            "Shaft": "Receives mechanical input.",
            "Cooling System": "Removes heat."
        },
        "working": "Mechanical rotation of the rotor field induces alternating EMF in the stationary stator winding.",
        "applications": "Thermal, hydro and wind power generation.",
        "notes": "Frequency f = PN/120. EMF equation: E = 4.44 Kp Kd Φ T f per phase.",
        "viva": [
            "What is an alternator?",
            "Why is the armature placed on the stator?",
            "What is voltage regulation?",
            "What is an EMF equation?",
            "What is the function of excitation?"
        ]
    },

    "Special Electrical Machines": {
        "parts": {
            "Stepper Motor": "Moves through fixed angular steps.",
            "Servo Motor": "Provides controlled position or speed.",
            "BLDC Motor": "Uses electronic commutation.",
            "Reluctance Motor": "Produces torque due to magnetic reluctance.",
            "Universal Motor": "Can operate on AC or DC supply within its ratings."
        },
        "working": "Special machines use different electromagnetic principles and electronic control techniques depending on their construction.",
        "applications": "Robotics, automation, CNC machines and electric vehicles.",
        "notes": "Important types include stepper motors, servo motors, BLDC motors and switched reluctance motors.",
        "viva": [
            "What is a BLDC motor?",
            "What is a stepper motor?",
            "What is a servo motor?",
            "What is reluctance torque?",
            "Where are special machines used?"
        ]
    }
}

# HOME

st.title("⚡ TECH MITHRA AI")
st.subheader("B.Tech Electrical & Electronics Engineering")
st.write("Your Digital Electrical Machines Laboratory")

st.markdown("---")

st.header("⚡ Electrical Machines")

machine = st.selectbox(
    "Select Electrical Machine",
    list(machines.keys())
)

data = machines[machine]

st.markdown("---")

st.header("📚 " + machine)

# TABS

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "3D View",
    "Parts",
    "Working",
    "Notes",
    "Applications",
    "Viva"
])

# 3D VIEW

with tab1:
    st.subheader("Interactive 3D Learning Model")

    st.info(
        "Use mouse or touch to rotate and zoom the 3D schematic. "
        "These are educational component markers, not manufacturing CAD models."
    )

    part_names = list(data["parts"].keys())

    fig = go.Figure()

    for i, part in enumerate(part_names):

        fig.add_trace(go.Scatter3d(
            x=[i % 3],
            y=[i // 3],
            z=[i * 0.4],
            mode="markers+text",
            marker=dict(
                size=15,
                color=i * 40,
                colorscale="Turbo"
            ),
            text=[part],
            textposition="top center",
            name=part
        ))

    fig.update_layout(
        height=500,
        paper_bgcolor="#0b1020",
        font=dict(color="white"),
        scene=dict(
            bgcolor="#0b1020",
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        ),
        margin=dict(l=0, r=0, b=0, t=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# PARTS

with tab2:
    st.subheader("🔩 Parts & Components")

    selected_part = st.selectbox(
        "Select Component",
        part_names
    )

    st.markdown("### " + selected_part)

    st.write(data["parts"][selected_part])

    st.success("Component details")

# WORKING

with tab3:
    st.subheader("⚙️ Working Principle")
    st.write(data["working"])

# NOTES

with tab4:
    st.subheader("📝 Complete Notes")
    st.write(data["notes"])

# APPLICATIONS

with tab5:
    st.subheader("🔬 Applications")
    st.write(data["applications"])

# VIVA

with tab6:
    st.subheader("🎯 Viva Questions")

    for i, question in enumerate(data["viva"], 1):
        st.write(f"{i}. {question}")

st.markdown("---")

st.caption(
    "TECH MITHRA AI | B.Tech EEE Learning Platform"
)
