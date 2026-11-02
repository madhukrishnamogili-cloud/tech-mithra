
import streamlit as st

st.set_page_config(
    page_title="Tech Mithra | EEE Machines",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #101827;
    color: white;
}
h1, h2, h3 {
    color: #42d9ff !important;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    border: 1px solid #2385a8;
    background: #172b40;
    color: white;
}
div.stButton > button:hover {
    background: #087da5;
    color: white;
}
[data-testid="stMetric"] {
    background: #172b40;
    padding: 14px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MACHINE DATABASE ----------------

MACHINES = {
    "DC Motor": {
        "category": "DC Machines",
        "parameters": {
            "Rated Voltage": "220 V DC",
            "Rated Current": "5 A",
            "Rated Power": "1 kW",
            "Speed": "1500 RPM",
            "Supply": "DC",
            "Efficiency": "85–90%"
        },
        "principle": "A current-carrying conductor placed in a magnetic field experiences a force. This force produces torque and rotates the armature.",
        "applications": "Electric traction, cranes, lifts, rolling mills and variable-speed drives.",
        "parts": {
            "Yoke": {
                "function": "Provides mechanical support and a magnetic flux path.",
                "working": "The yoke supports the poles and protects internal components. It also provides a low-reluctance path for magnetic flux.",
                "material": "Cast iron or steel."
            },
            "Pole Core": {
                "function": "Supports field winding and carries magnetic flux.",
                "working": "The pole core carries the magnetic flux produced by the field winding and distributes it through the air gap.",
                "material": "Laminated steel."
            },
            "Field Winding": {
                "function": "Produces the main magnetic field.",
                "working": "When DC supply passes through the field winding, it produces magnetic flux around the poles.",
                "material": "Insulated copper wire."
            },
            "Armature": {
                "function": "Rotating part of the DC machine.",
                "working": "Armature conductors carry current. Their interaction with the magnetic field produces electromagnetic torque.",
                "material": "Laminated steel core and copper winding."
            },
            "Commutator": {
                "function": "Maintains unidirectional torque.",
                "working": "It reverses the armature conductor connections at suitable intervals so that torque remains in the same direction.",
                "material": "Copper segments with insulation."
            },
            "Brushes": {
                "function": "Transfer current to the rotating commutator.",
                "working": "Carbon brushes maintain sliding electrical contact with the commutator.",
                "material": "Carbon or graphite."
            },
            "Shaft": {
                "function": "Transfers mechanical output.",
                "working": "The shaft rotates with the armature and transfers torque to the connected load.",
                "material": "Steel."
            }
        },
        "viva": [
            ("What is a DC motor?", "A machine that converts DC electrical energy into mechanical energy."),
            ("What is back EMF?", "The EMF induced in the armature that opposes the applied voltage."),
            ("What is the function of a commutator?", "It helps maintain unidirectional torque."),
            ("What is the function of brushes?", "They transfer current between the external circuit and commutator.")
        ]
    },

    "Transformer": {
        "category": "Static Electrical Machines",
        "parameters": {
            "Rated Voltage": "230/115 V AC",
            "Rated Current": "5 A",
            "Rated Power": "1 kVA",
            "Frequency": "50 Hz",
            "Phases": "Single Phase",
            "Efficiency": "95–98%"
        },
        "principle": "A transformer works on the principle of mutual electromagnetic induction. AC in the primary winding creates changing flux that induces EMF in the secondary winding.",
        "applications": "Power transmission, distribution, substations, chargers and electrical isolation.",
        "parts": {
            "Magnetic Core": {
                "function": "Provides a path for magnetic flux.",
                "working": "The alternating flux produced by the primary winding flows through the laminated core and links both windings.",
                "material": "Laminated silicon steel."
            },
            "Primary Winding": {
                "function": "Receives input electrical energy.",
                "working": "AC supply to the primary winding produces alternating magnetic flux in the core.",
                "material": "Insulated copper or aluminium."
            },
            "Secondary Winding": {
                "function": "Delivers output electrical energy.",
                "working": "The changing magnetic flux induces EMF in the secondary winding according to Faraday's law.",
                "material": "Insulated copper or aluminium."
            },
            "Insulation": {
                "function": "Prevents electrical short circuits.",
                "working": "Insulating materials separate windings and isolate live conductors from the core and tank.",
                "material": "Pressboard, paper and insulating materials."
            },
            "Transformer Oil": {
                "function": "Provides cooling and insulation in oil-filled transformers.",
                "working": "Oil carries heat away from the windings and core and helps provide electrical insulation.",
                "material": "Transformer insulating oil."
            },
            "Tank": {
                "function": "Protects internal transformer components.",
                "working": "The tank houses the core, windings and oil in an oil-filled transformer.",
                "material": "Steel."
            },
            "Bushings": {
                "function": "Provide insulated terminals.",
                "working": "They allow electrical conductors to pass safely through the transformer tank.",
                "material": "Porcelain or composite insulation."
            }
        },
        "viva": [
            ("What is a transformer?", "A static device that transfers AC power between circuits through electromagnetic induction."),
            ("What is the principle of a transformer?", "Mutual electromagnetic induction."),
            ("What is a step-up transformer?", "A transformer that increases the output voltage."),
            ("Does a transformer work on DC?", "A conventional transformer is designed for AC, not steady DC.")
        ]
    },

    "Three Phase Induction Motor": {
        "category": "AC Machines",
        "parameters": {
            "Rated Voltage": "415 V AC",
            "Rated Current": "3.5 A",
            "Rated Power": "2 HP",
            "Frequency": "50 Hz",
            "Speed": "1440 RPM",
            "Power Factor": "0.8",
            "Phases": "3 Phase"
        },
        "principle": "A three-phase AC supply produces a rotating magnetic field in the stator. This field induces rotor current, producing torque.",
        "applications": "Pumps, fans, compressors, conveyors and industrial drives.",
        "parts": {
            "Stator": {
                "function": "Produces the rotating magnetic field.",
                "working": "Three-phase supply to the stator windings produces a rotating magnetic field.",
                "material": "Laminated steel and copper winding."
            },
            "Rotor": {
                "function": "Produces mechanical torque.",
                "working": "The rotating magnetic field induces current in the rotor conductors. Their interaction with the field produces torque.",
                "material": "Aluminium or copper conductors with steel core."
            },
            "Air Gap": {
                "function": "Separates stator and rotor.",
                "working": "It provides the magnetic coupling between stator and rotor while allowing rotor rotation.",
                "material": "Air."
            },
            "Bearings": {
                "function": "Support the rotating shaft.",
                "working": "Bearings reduce friction and allow smooth shaft rotation.",
                "material": "Bearing steel."
            },
            "Cooling Fan": {
                "function": "Removes heat from the motor.",
                "working": "The fan circulates air around the motor body to improve cooling.",
                "material": "Plastic or metal."
            },
            "Shaft": {
                "function": "Transfers mechanical power.",
                "working": "The shaft carries rotor torque to the connected mechanical load.",
                "material": "Steel."
            },
            "Terminal Box": {
                "function": "Provides electrical connections.",
                "working": "It houses the terminals used to connect the motor windings to the supply.",
                "material": "Metal or insulated enclosure."
            }
        },
        "viva": [
            ("What is an induction motor?", "An AC motor in which rotor current is induced electromagnetically."),
            ("What is synchronous speed?", "Ns = 120f/P RPM."),
            ("What is slip?", "Slip = (Ns - N)/Ns."),
            ("Why is the rotor speed less than synchronous speed?", "A speed difference is required to induce rotor EMF and current.")
        ]
    },

    "Single Phase Induction Motor": {
        "category": "AC Machines",
        "parameters": {
            "Rated Voltage": "230 V AC",
            "Rated Current": "4 A",
            "Rated Power": "0.5 HP",
            "Frequency": "50 Hz",
            "Speed": "1440 RPM",
            "Phases": "Single Phase"
        },
        "principle": "A single-phase AC supply produces a pulsating magnetic field. A starting arrangement helps develop starting torque.",
        "applications": "Ceiling fans, small pumps, refrigerators and domestic appliances.",
        "parts": {
            "Stator": {
                "function": "Contains the motor windings.",
                "working": "The stator carries the main and auxiliary windings that create the magnetic field.",
                "material": "Laminated steel and copper."
            },
            "Rotor": {
                "function": "Develops mechanical torque.",
                "working": "The induced rotor current interacts with the magnetic field to produce torque.",
                "material": "Aluminium bars and steel core."
            },
            "Main Winding": {
                "function": "Produces the main magnetic field.",
                "working": "It carries the main AC current and establishes the motor's alternating magnetic field.",
                "material": "Insulated copper."
            },
            "Auxiliary Winding": {
                "function": "Helps the motor start.",
                "working": "It creates a phase difference with the main winding current to produce starting torque.",
                "material": "Insulated copper."
            },
            "Capacitor": {
                "function": "Creates phase shift in capacitor-type motors.",
                "working": "It shifts the auxiliary winding current relative to the main winding current.",
                "material": "Electrical capacitor."
            },
            "Centrifugal Switch": {
                "function": "Disconnects the starting winding in some designs.",
                "working": "It operates according to motor speed and disconnects the starting circuit when appropriate.",
                "material": "Mechanical switch contacts."
            }
        },
        "viva": [
            ("Is a single-phase induction motor self-starting?", "No, it is not inherently self-starting."),
            ("What is the function of a capacitor?", "It creates phase shift to help produce starting torque."),
            ("Where is it used?", "Fans, pumps and domestic appliances.")
        ]
    },

    "Synchronous Motor": {
        "category": "AC Machines",
        "parameters": {
            "Rated Voltage": "415 V AC",
            "Rated Power": "5 HP",
            "Frequency": "50 Hz",
            "Speed": "1500 RPM",
            "Power Factor": "Adjustable",
            "Phases": "3 Phase"
        },
        "principle": "The rotor magnetic field locks with the rotating magnetic field of the stator and rotates at synchronous speed.",
        "applications": "Industrial constant-speed drives and power-factor correction.",
        "parts": {
            "Stator": {
                "function": "Produces the rotating magnetic field.",
                "working": "Three-phase supply creates a rotating magnetic field at synchronous speed.",
                "material": "Laminated steel and copper."
            },
            "Rotor": {
                "function": "Carries the magnetic field system.",
                "working": "The rotor field locks with the rotating stator field after synchronisation.",
                "material": "Steel and field winding."
            },
            "Field Winding": {
                "function": "Produces rotor magnetic flux.",
                "working": "DC excitation creates the rotor magnetic field.",
                "material": "Insulated copper."
            },
            "Damper Winding": {
                "function": "Helps with starting and damping oscillations in suitable designs.",
                "working": "It carries induced currents during asynchronous starting and helps reduce hunting.",
                "material": "Copper or aluminium bars."
            },
            "Shaft": {
                "function": "Transfers mechanical power.",
                "working": "It connects the rotor to the mechanical load.",
                "material": "Steel."
            }
        },
        "viva": [
            ("What is synchronous speed?", "Ns = 120f/P RPM."),
            ("Does a synchronous motor run at constant speed?", "It runs at synchronous speed under normal synchronised operation."),
            ("What is excitation?", "DC supply given to the rotor field winding.")
        ]
    },

    "Alternator": {
        "category": "AC Generators",
        "parameters": {
            "Rated Voltage": "415 V AC",
            "Frequency": "50 Hz",
            "Rated Power": "5 kVA",
            "Speed": "1500 RPM",
            "Phases": "3 Phase",
            "Power Factor": "0.8"
        },
        "principle": "An alternator converts mechanical energy into AC electrical energy by electromagnetic induction.",
        "applications": "Power stations, hydroelectric plants and diesel generator sets.",
        "parts": {
            "Stator": {
                "function": "Houses the armature winding.",
                "working": "The rotating magnetic field links the stationary three-phase winding and induces AC EMF.",
                "material": "Laminated steel and copper."
            },
            "Rotor": {
                "function": "Produces the rotating magnetic field.",
                "working": "The rotor field rotates and cuts the stator conductors, inducing EMF.",
                "material": "Steel and field winding."
            },
            "Exciter": {
                "function": "Provides rotor field excitation.",
                "working": "It supplies the required DC excitation to the rotor field system.",
                "material": "Depends on excitation system."
            },
            "Bearings": {
                "function": "Support the rotor shaft.",
                "working": "They allow smooth rotation and maintain alignment.",
                "material": "Bearing steel."
            },
            "Shaft": {
                "function": "Receives mechanical input.",
                "working": "It connects the prime mover to the rotor.",
                "material": "Steel."
            },
            "Cooling System": {
                "function": "Removes heat.",
                "working": "Air, hydrogen or other designed cooling arrangements remove heat depending on alternator size.",
                "material": "Depends on design."
            }
        },
        "viva": [
            ("What is an alternator?", "A machine that converts mechanical energy into AC electrical energy."),
            ("What is the frequency equation?", "f = PN/120."),
            ("What is the function of an exciter?", "It supplies field excitation.")
        ]
    }
}

# ---------------- HEADER ----------------

st.title("⚡ TECH MITHRA")
st.subheader("B.Tech EEE | Electrical Machines Learning System")
st.caption("Machine Parameters • Interactive Parts • Working Principle • Viva")

# ---------------- SIDEBAR ----------------

st.sidebar.title("EEE Department")
st.sidebar.caption("Electrical Engineering Learning")

machine_name = st.sidebar.selectbox(
    "Select Machine",
    list(MACHINES.keys())
)

data = MACHINES[machine_name]

st.sidebar.markdown("---")
st.sidebar.write("**Department:** Electrical & Electronics Engineering")
st.sidebar.write("**Course:** B.Tech")
st.sidebar.write("**Subject:** Electrical Machines")
st.sidebar.write("**Learning Mode:** Interactive")

st.header("🔧 " + machine_name)
st.write("Category:", data["category"])

# ---------------- PARAMETERS ----------------

st.markdown("## 📊 Electrical Machine Parameters")

parameters = list(data["parameters"].items())

cols = st.columns(3)

for index, (name, value) in enumerate(parameters):
    with cols[index % 3]:
        st.metric(name, value)

st.info("గమనిక: ఇవి learning కోసం sample ratings మాత్రమే. Actual machine nameplate values మారవచ్చు.")

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧩 Machine Parts",
    "🌐 3D Model",
    "⚡ Working Principle",
    "📚 Notes & Applications",
    "🎓 Viva Questions"
])

# ---------------- CLICKABLE PARTS ----------------

with tab1:
    st.markdown("## 🧩 Click a Machine Part")
    st.write("ఒక Part మీద క్లిక్ చేస్తే దాని పూర్తి Working Details కనిపిస్తాయి.")

    if "selected_part" not in st.session_state:
        st.session_state.selected_part = {}

    selected = st.session_state.selected_part.get(machine_name)

    part_names = list(data["parts"].keys())

    cols = st.columns(3)

    for index, part in enumerate(part_names):
        with cols[index % 3]:
            if st.button("⚙️ " + part, key=f"{machine_name}_{part}"):
                st.session_state.selected_part[machine_name] = part
                selected = part

    st.divider()

    if selected and selected in data["parts"]:
        details = data["parts"][selected]

        st.markdown(f"## 🔍 {selected}")
        st.success("Function: " + details["function"])

        st.markdown("### ⚙️ How does it work?")
        st.write(details["working"])

        st.markdown("### 🧱 Material / Construction")
        st.write(details["material"])

    else:
        st.info("పైన ఉన్న Machine Part బటన్‌ను క్లిక్ చేయండి. దాని Working Details ఇక్కడ కనిపిస్తాయి.")

# ---------------- 3D MODEL ----------------

with tab2:
    st.markdown("## 🌐 3D Machine View")
    st.write("ఇక్కడ సంబంధిత Machine యొక్క 3D Model చూపించవచ్చు.")

    st.warning(
        "ఈ codeలో 3D viewer placeholder మాత్రమే. "
        "ప్రతి Machine‌కు సరైన GLB/GLTF 3D model file జోడించిన తర్వాత "
        "rotate, zoom మరియు model inspection అందుబాటులోకి వస్తాయి."
    )

    st.markdown("### Selected Machine")
    st.subheader(machine_name)

# ---------------- WORKING PRINCIPLE ----------------

with tab3:
    st.markdown("## ⚡ Working Principle")
    st.write(data["principle"])

    st.markdown("### Important Formulae")

    if machine_name in ["Three Phase Induction Motor", "Synchronous Motor", "Alternator"]:
        st.latex(r"N_s = \frac{120f}{P}")

    if machine_name == "Three Phase Induction Motor":
        st.latex(r"s = \frac{N_s-N_r}{N_s}")
        st.write("s = Slip, Ns = Synchronous speed, Nr = Rotor speed")

    if machine_name == "Alternator":
        st.latex(r"f = \frac{PN}{120}")

    if machine_name == "Transformer":
        st.latex(r"\frac{V_1}{V_2} = \frac{N_1}{N_2}")

# ---------------- NOTES ----------------

with tab4:
    st.markdown("## 📚 Applications")
    st.write(data["applications"])

    st.markdown("## 📝 Study Notes")
    st.write(data["principle"])

    st.markdown("### Machine Parts Summary")

    for part, details in data["parts"].items():
        with st.expander(part):
            st.write("**Function:**", details["function"])
            st.write("**Working:**", details["working"])

# ---------------- VIVA ----------------

with tab5:
    st.markdown("## 🎓 Viva Questions")

    for index, (question, answer) in enumerate(data["viva"], 1):
        with st.expander(f"Q{index}. {question}"):
            st.write("**Answer:**", answer)

st.sidebar.markdown("---")
st.sidebar.success("EEE Learning System Ready ⚡")
st.caption("Tech Mithra | B.Tech EEE Learning Project")
