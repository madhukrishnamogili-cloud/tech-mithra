
import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import re

st.set_page_config(
    page_title="Tech Mithra EEE 3D Lab",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #101827;
    color: white;
}
h1,h2,h3 { color: #42d9ff !important; }
div.stButton > button {
    width: 100%;
    background: #17334a;
    color: white;
    border-radius: 10px;
}
[data-testid="stMetric"] {
    background: #172b40;
    padding: 12px;
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
            "Frequency": "DC Supply",
            "Speed": "1500 RPM",
            "Power Factor": "Not applicable",
            "Efficiency": "85–90%",
            "Poles": "4",
            "Torque": "6.37 N-m (at 1500 RPM, 1 kW)",
            "Phase": "DC"
        },
        "principle": "A current-carrying conductor placed in a magnetic field experiences a force. This force produces torque and rotates the armature.",
        "parts": {
            "yoke": {
                "name": "Yoke",
                "function": "Provides mechanical support and a magnetic flux path.",
                "working": "The yoke supports the poles and provides a path for magnetic flux.",
                "material": "Cast iron or steel."
            },
            "pole": {
                "name": "Pole Core",
                "function": "Carries magnetic flux.",
                "working": "The pole core carries the flux produced by the field winding and distributes it through the air gap.",
                "material": "Laminated steel."
            },
            "field winding": {
                "name": "Field Winding",
                "function": "Produces the main magnetic field.",
                "working": "DC current flowing through the winding produces magnetic flux.",
                "material": "Insulated copper wire."
            },
            "armature": {
                "name": "Armature",
                "function": "Rotating part of the machine.",
                "working": "Current in the armature conductors interacts with the magnetic field to produce torque.",
                "material": "Laminated steel and copper winding."
            },
            "commutator": {
                "name": "Commutator",
                "function": "Maintains unidirectional torque.",
                "working": "It reverses armature conductor connections at suitable intervals.",
                "material": "Copper segments and insulation."
            },
            "brush": {
                "name": "Brushes",
                "function": "Transfer electrical current.",
                "working": "Carbon brushes maintain sliding electrical contact with the commutator.",
                "material": "Carbon or graphite."
            },
            "shaft": {
                "name": "Shaft",
                "function": "Transfers mechanical power.",
                "working": "The shaft rotates with the armature and transfers torque to the load.",
                "material": "Steel."
            }
        }
    },

    "Transformer": {
        "category": "Static Electrical Machines",
        "parameters": {
            "Primary Voltage": "230 V AC",
            "Secondary Voltage": "115 V AC",
            "Rated Current": "As per rating",
            "Rated Power": "1 kVA",
            "Frequency": "50 Hz",
            "Power Factor": "Load dependent",
            "Efficiency": "95–98%",
            "Phase": "Single Phase",
            "Turns Ratio": "2:1",
            "Cooling": "Air / Oil"
        },
        "principle": "A transformer works on mutual electromagnetic induction. Alternating flux in the core induces EMF in the secondary winding.",
        "parts": {
            "core": {
                "name": "Magnetic Core",
                "function": "Provides a path for magnetic flux.",
                "working": "The alternating flux produced by the primary winding flows through the core and links both windings.",
                "material": "Laminated silicon steel."
            },
            "primary winding": {
                "name": "Primary Winding",
                "function": "Receives input electrical energy.",
                "working": "AC supply to the primary winding produces alternating magnetic flux.",
                "material": "Insulated copper or aluminium."
            },
            "secondary winding": {
                "name": "Secondary Winding",
                "function": "Delivers output electrical energy.",
                "working": "Changing magnetic flux induces EMF in the secondary winding.",
                "material": "Insulated copper or aluminium."
            },
            "insulation": {
                "name": "Insulation",
                "function": "Prevents electrical short circuits.",
                "working": "Separates the windings electrically and isolates them from the core.",
                "material": "Paper, pressboard and insulating materials."
            },
            "tank": {
                "name": "Tank",
                "function": "Protects internal components.",
                "working": "Houses the core, windings and oil in oil-filled transformers.",
                "material": "Steel."
            },
            "bushing": {
                "name": "Bushings",
                "function": "Provide insulated electrical terminals.",
                "working": "Allow conductors to pass through the transformer tank safely.",
                "material": "Porcelain or composite insulation."
            }
        }
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
            "Efficiency": "85–90%",
            "Poles": "4",
            "Phase": "3 Phase",
            "Connection": "Star / Delta"
        },
        "principle": "Three-phase AC supply produces a rotating magnetic field in the stator. This field induces rotor current and produces torque.",
        "parts": {
            "stator": {
                "name": "Stator",
                "function": "Produces the rotating magnetic field.",
                "working": "Three-phase supply to stator windings creates a rotating magnetic field.",
                "material": "Laminated steel and copper winding."
            },
            "rotor": {
                "name": "Rotor",
                "function": "Produces mechanical torque.",
                "working": "The rotating magnetic field induces current in the rotor. Interaction with the magnetic field produces torque.",
                "material": "Aluminium or copper conductors with steel core."
            },
            "air gap": {
                "name": "Air Gap",
                "function": "Separates stator and rotor.",
                "working": "Provides magnetic coupling while allowing the rotor to rotate.",
                "material": "Air."
            },
            "bearing": {
                "name": "Bearings",
                "function": "Support the rotating shaft.",
                "working": "Reduce friction and allow smooth shaft rotation.",
                "material": "Bearing steel."
            },
            "fan": {
                "name": "Cooling Fan",
                "function": "Removes heat.",
                "working": "Circulates air around the motor body to improve cooling.",
                "material": "Plastic or metal."
            },
            "shaft": {
                "name": "Shaft",
                "function": "Transfers mechanical power.",
                "working": "Transfers rotor torque to the connected load.",
                "material": "Steel."
            },
            "terminal box": {
                "name": "Terminal Box",
                "function": "Provides electrical connections.",
                "working": "Houses the terminals used to connect the motor windings to the supply.",
                "material": "Insulated enclosure."
            }
        }
    },

    "Single Phase Induction Motor": {
        "category": "AC Machines",
        "parameters": {
            "Rated Voltage": "230 V AC",
            "Rated Current": "4 A",
            "Rated Power": "0.5 HP",
            "Frequency": "50 Hz",
            "Speed": "1440 RPM",
            "Power Factor": "0.75",
            "Efficiency": "70–80%",
            "Phase": "Single Phase",
            "Starting": "Capacitor / Split Phase"
        },
        "principle": "A single-phase AC supply produces a pulsating magnetic field. A starting arrangement helps the motor develop starting torque.",
        "parts": {
            "stator": {
                "name": "Stator",
                "function": "Contains motor windings.",
                "working": "Carries the main and auxiliary windings that create the magnetic field.",
                "material": "Laminated steel and copper."
            },
            "rotor": {
                "name": "Rotor",
                "function": "Develops mechanical torque.",
                "working": "Induced rotor current interacts with the magnetic field to produce torque.",
                "material": "Aluminium bars and steel core."
            },
            "main winding": {
                "name": "Main Winding",
                "function": "Produces the main magnetic field.",
                "working": "Carries the main AC current and establishes the alternating magnetic field.",
                "material": "Insulated copper."
            },
            "auxiliary winding": {
                "name": "Auxiliary Winding",
                "function": "Helps the motor start.",
                "working": "Creates a phase difference with the main winding current to produce starting torque.",
                "material": "Insulated copper."
            },
            "capacitor": {
                "name": "Capacitor",
                "function": "Creates phase shift.",
                "working": "Shifts the auxiliary winding current relative to the main winding current.",
                "material": "Electrical capacitor."
            }
        }
    },

    "Synchronous Motor": {
        "category": "AC Machines",
        "parameters": {
            "Rated Voltage": "415 V AC",
            "Rated Power": "5 HP",
            "Frequency": "50 Hz",
            "Speed": "1500 RPM",
            "Power Factor": "Adjustable",
            "Poles": "4",
            "Phase": "3 Phase",
            "Excitation": "DC"
        },
        "principle": "The rotor magnetic field locks with the rotating magnetic field of the stator and runs at synchronous speed.",
        "parts": {
            "stator": {
                "name": "Stator",
                "function": "Produces the rotating magnetic field.",
                "working": "Three-phase supply creates a rotating magnetic field at synchronous speed.",
                "material": "Laminated steel and copper."
            },
            "rotor": {
                "name": "Rotor",
                "function": "Carries the magnetic field system.",
                "working": "The rotor field locks with the rotating stator field during synchronised operation.",
                "material": "Steel and field winding."
            },
            "field winding": {
                "name": "Field Winding",
                "function": "Produces rotor magnetic flux.",
                "working": "DC excitation creates the rotor magnetic field.",
                "material": "Insulated copper."
            },
            "damper winding": {
                "name": "Damper Winding",
                "function": "Helps with starting and damping oscillations.",
                "working": "Induced currents in the damper winding help during asynchronous starting and reduce hunting.",
                "material": "Copper or aluminium bars."
            },
            "shaft": {
                "name": "Shaft",
                "function": "Transfers mechanical power.",
                "working": "Connects the rotor to the mechanical load.",
                "material": "Steel."
            }
        }
    },

    "Alternator": {
        "category": "AC Generators",
        "parameters": {
            "Rated Voltage": "415 V AC",
            "Rated Power": "5 kVA",
            "Frequency": "50 Hz",
            "Speed": "1500 RPM",
            "Power Factor": "0.8",
            "Poles": "4",
            "Phase": "3 Phase",
            "Excitation": "DC"
        },
        "principle": "An alternator converts mechanical energy into AC electrical energy by electromagnetic induction.",
        "parts": {
            "stator": {
                "name": "Stator",
                "function": "Houses the armature winding.",
                "working": "The rotating magnetic field links the stationary three-phase winding and induces AC EMF.",
                "material": "Laminated steel and copper."
            },
            "rotor": {
                "name": "Rotor",
                "function": "Produces the rotating magnetic field.",
                "working": "The rotor field rotates and cuts the stator conductors, inducing EMF.",
                "material": "Steel and field winding."
            },
            "exciter": {
                "name": "Exciter",
                "function": "Provides rotor field excitation.",
                "working": "Supplies DC excitation to the rotor field system.",
                "material": "Depends on excitation system."
            },
            "bearing": {
                "name": "Bearings",
                "function": "Support the rotor shaft.",
                "working": "Allow smooth rotation and maintain alignment.",
                "material": "Bearing steel."
            },
            "shaft": {
                "name": "Shaft",
                "function": "Receives mechanical input.",
                "working": "Connects the prime mover to the rotor.",
                "material": "Steel."
            }
        }
    },

    "BLDC Motor": {
        "category": "Special Electrical Machines",
        "parameters": {
            "Rated Voltage": "24 V DC",
            "Rated Current": "5 A",
            "Rated Power": "100 W",
            "Speed": "3000 RPM",
            "Phase": "3 Phase",
            "Controller": "Electronic",
            "Efficiency": "85–90%"
        },
        "principle": "Electronic switching energises stator windings in sequence. Permanent magnets on the rotor follow the rotating magnetic field.",
        "parts": {
            "stator": {
                "name": "Stator",
                "function": "Contains the motor windings.",
                "working": "The controller energises stator phases in sequence to create a rotating magnetic field.",
                "material": "Laminated steel and copper."
            },
            "rotor": {
                "name": "Rotor",
                "function": "Rotating permanent-magnet assembly.",
                "working": "Permanent magnets follow the rotating stator field and produce mechanical rotation.",
                "material": "Permanent magnets and steel."
            },
            "permanent magnet": {
                "name": "Permanent Magnets",
                "function": "Produce rotor magnetic flux.",
                "working": "Their magnetic field interacts with the stator field to produce torque.",
                "material": "Permanent magnet material."
            },
            "controller": {
                "name": "Electronic Controller",
                "function": "Controls motor switching.",
                "working": "Switches stator currents electronically according to rotor position information.",
                "material": "Electronic power components."
            }
        }
    }
}

# ---------------- FORMULAS ----------------

def show_formulas(machine):
    st.markdown("### 📐 Important Electrical Formulae")

    if machine == "Transformer":
        st.latex(r"\frac{V_1}{V_2}=\frac{N_1}{N_2}")
        st.latex(r"\eta=\frac{Output}{Input}\times100")

    elif machine in ["Three Phase Induction Motor", "Synchronous Motor", "Alternator"]:
        st.latex(r"N_s=\frac{120f}{P}")

        if machine == "Three Phase Induction Motor":
            st.latex(r"s=\frac{N_s-N_r}{N_s}\times100")

        if machine == "Alternator":
            st.latex(r"f=\frac{PN}{120}")

    elif machine == "DC Motor":
        st.latex(r"T=\frac{9.55P}{N}")
        st.latex(r"E_b=V-I_aR_a")

    elif machine == "BLDC Motor":
        st.latex(r"P=VI")
        st.latex(r"T=\frac{9.55P}{N}")

# ---------------- HEADER ----------------

st.title("⚡ TECH MITHRA")
st.subheader("B.Tech EEE | Interactive Electrical Machines 3D Lab")
st.caption("Electrical Parameters • Real 3D Models • Clickable Machine Parts")

machine_name = st.sidebar.selectbox(
    "Select EEE Machine",
    list(MACHINES.keys())
)

data = MACHINES[machine_name]

st.sidebar.markdown("---")
st.sidebar.write("**Department:** Electrical & Electronics Engineering")
st.sidebar.write("**Course:** B.Tech")
st.sidebar.write("**Subject:** Electrical Machines")

st.header("🔧 " + machine_name)
st.write("Category:", data["category"])

# ---------------- ELECTRICAL PARAMETERS ----------------

st.markdown("## ⚡ Electrical Parameters")

params = list(data["parameters"].items())
cols = st.columns(3)

for i, (name, value) in enumerate(params):
    with cols[i % 3]:
        st.metric(name, value)

st.info(
    "ఈ ratings demonstration కోసం ఇచ్చిన sample values. "
    "Actual machine nameplate ratings, design మరియు manufacturer ఆధారంగా మారుతాయి."
)

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🌐 Interactive 3D Model",
    "⚙️ Parts Details",
    "📘 Theory & Formulae",
    "🎓 Viva"
])

# ---------------- 3D MODEL UPLOAD ----------------

with tab1:
    st.markdown("## 🌐 Realistic Interactive 3D Model")

    st.write(
        "ఈ Machine‌కు సంబంధించిన GLB 3D model file upload చేయండి. "
        "మోడల్‌లోని Stator, Rotor వంటి parts వేరువేరు meshes‌గా ఉండాలి."
    )

    model_file = st.file_uploader(
        "Upload " + machine_name + " 3D Model (.glb)",
        type=["glb"],
        key="model_" + machine_name
    )

    if model_file:
        model_b64 = base64.b64encode(
            model_file.getvalue()
        ).decode("utf-8")

        parts_json = json.dumps(data["parts"])

        html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
    margin: 0;
    background: #101827;
    color: white;
    font-family: Arial;
}
#viewer {
    width: 100%;
    height: 530px;
    position: relative;
    overflow: hidden;
    border-radius: 12px;
    background: #101827;
}
#details {
    position: absolute;
    bottom: 12px;
    left: 12px;
    right: 12px;
    max-height: 175px;
    overflow-y: auto;
    background: rgba(10,20,35,0.94);
    padding: 12px;
    border: 1px solid #42d9ff;
    border-radius: 10px;
    z-index: 5;
}
#details h3 { color: #42d9ff; margin: 0 0 8px; }
#details p { font-size: 14px; margin: 6px 0; }
#hint {
    position: absolute;
    top: 10px;
    left: 10px;
    background: #17334a;
    padding: 8px 12px;
    border-radius: 8px;
    z-index: 4;
    font-size: 13px;
}
canvas { display: block; }
</style>

<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
</head>

<body>
<div id="viewer">
    <div id="hint">Drag: Rotate | Scroll: Zoom | Click: Select Part</div>
    <div id="details">
        <h3>3D Machine Details</h3>
        <p>Click any separately modelled part to see its details.</p>
    </div>
</div>

<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const MODEL_DATA = "__MODEL__";
const PARTS = __PARTS__;

const container = document.getElementById("viewer");
const details = document.getElementById("details");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101827);

const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);
camera.position.set(4, 3, 5);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
container.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff, 0x445566, 2));

const light = new THREE.DirectionalLight(0xffffff, 2.5);
light.position.set(5, 8, 5);
scene.add(light);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

let clickableMeshes = [];
let selectedMesh = null;

const loader = new GLTFLoader();

function normalizeName(name) {
    return name.toLowerCase()
        .replace(/[_-]/g, " ")
        .replace(/\.\d+$/, "")
        .trim();
}

function showPart(mesh) {
    const originalName = mesh.name || "Unnamed Part";
    const key = normalizeName(originalName);

    let info = PARTS[key];

    if (!info) {
        const match = Object.keys(PARTS).find(k =>
            key.includes(k) || k.includes(key)
        );
        if (match) info = PARTS[match];
    }

    if (info) {
        details.innerHTML = `
            <h3>${info.name}</h3>
            <p><b>Function:</b> ${info.function}</p>
            <p><b>Working:</b> ${info.working}</p>
            <p><b>Material:</b> ${info.material}</p>
        `;
    } else {
        details.innerHTML = `
            <h3>${originalName}</h3>
            <p>This 3D mesh has no matching description yet.</p>
            <p>Rename the mesh in your 3D model or add its details to the machine database.</p>
        `;
    }
}

loader.parse(
    Uint8Array.from(atob(MODEL_DATA), c => c.charCodeAt(0)).buffer,
    "",
    function(gltf) {
        const model = gltf.scene;

        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        model.position.sub(center);

        const maxDimension = Math.max(size.x, size.y, size.z);
        if (maxDimension > 0) {
            model.scale.setScalar(3 / maxDimension);
        }

        model.traverse(obj => {
            if (obj.isMesh) {
                clickableMeshes.push(obj);
            }
        });

        scene.add(model);

        camera.position.set(4, 3, 5);
        controls.target.set(0, 0, 0);
        controls.update();

        details.innerHTML = `
            <h3>3D Model Loaded Successfully</h3>
            <p>Found ${clickableMeshes.length} mesh objects.</p>
            <p>Click a separate machine part to inspect it.</p>
        `;
    },
    function(error) {
        details.innerHTML = "<h3>Model loading error</h3><p>Check that the uploaded file is a valid GLB model.</p>";
        console.error(error);
    }
);

renderer.domElement.addEventListener("pointerdown", function(event) {
    const rect = renderer.domElement.getBoundingClientRect();

    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(pointer, camera);

    const hits = raycaster.intersectObjects(clickableMeshes, true);

    if (hits.length > 0) {
        selectedMesh = hits[0].object;
        showPart(selectedMesh);
    }
});

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});
</script>
</body>
</html>
"""

        html = html.replace("__MODEL__", model_b64)
        html = html.replace("__PARTS__", parts_json)

        components.html(html, height=550, scrolling=False)

    else:
        st.warning(
            "ముందుగా ఈ Machine యొక్క .GLB 3D model file upload చేయండి. "
            "మోడల్ లేకుండా నిజమైన clickable 3D view చూపించడం సాధ్యం కాదు."
        )

    with st.expander("3D Model తయారుచేసేటప్పుడు పాటించాల్సిన నియమాలు"):
        st.markdown("""
        - ప్రతి భాగాన్ని వేరే Mesh/Object‌గా తయారు చేయాలి.
        - Mesh పేర్లను `Stator`, `Rotor`, `Shaft`, `Bearing` లాగా పెట్టాలి.
        - Model‌ను `.GLB` format‌లో export చేయాలి.
        - Parts వేరువేరుగా ఉంటే వాటిపై క్లిక్ చేసి వివరాలు చూడవచ్చు.
        """)

# ---------------- PART DETAILS ----------------

with tab2:
    st.markdown("## ⚙️ Machine Parts and Working")

    for key, part in data["parts"].items():
        with st.expander("🔩 " + part["name"]):
            st.markdown("**Function**")
            st.write(part["function"])

            st.markdown("**Working**")
            st.write(part["working"])

            st.markdown("**Material**")
            st.write(part["material"])

# ---------------- THEORY ----------------

with tab3:
    st.markdown("## 📘 Working Principle")
    st.write(data["principle"])

    show_formulas(machine_name)

    st.markdown("## 🏭 Applications")
    if machine_name == "DC Motor":
        st.write("Electric traction, cranes, lifts, rolling mills and variable-speed drives.")
    elif machine_name == "Transformer":
        st.write("Power transmission, distribution, substations and electrical isolation.")
    elif "Induction Motor" in machine_name:
        st.write("Pumps, fans, compressors, conveyors and domestic appliances.")
    elif machine_name == "Synchronous Motor":
        st.write("Constant-speed industrial drives and power-factor correction.")
    elif machine_name == "Alternator":
        st.write("Power stations, hydroelectric plants and generator sets.")
    else:
        st.write("Robotics, automation, electric vehicles and precision control.")

# ---------------- VIVA ----------------

with tab4:
    st.markdown("## 🎓 Viva Questions")

    viva_questions = {
        "DC Motor": [
            ("What is a DC motor?", "It converts DC electrical energy into mechanical energy."),
            ("What is back EMF?", "The induced EMF that opposes the applied voltage."),
            ("What is the function of a commutator?", "It helps maintain unidirectional torque.")
        ],
        "Transformer": [
            ("What is a transformer?", "A static device that transfers AC power through electromagnetic induction."),
            ("What is its working principle?", "Mutual electromagnetic induction."),
            ("What is a step-up transformer?", "A transformer that increases voltage.")
        ],
        "Three Phase Induction Motor": [
            ("What is slip?", "The difference between synchronous speed and rotor speed divided by synchronous speed."),
            ("What is synchronous speed?", "Ns = 120f/P RPM."),
            ("Why is rotor speed less than synchronous speed?", "A speed difference is required to induce rotor current.")
        ],
        "Single Phase Induction Motor": [
            ("Is it self-starting?", "No, it is not inherently self-starting."),
            ("What is the use of a capacitor?", "It helps create phase shift and starting torque.")
        ],
        "Synchronous Motor": [
            ("What is synchronous speed?", "Ns = 120f/P RPM."),
            ("What is excitation?", "DC supply given to the rotor field winding.")
        ],
        "Alternator": [
            ("What is an alternator?", "A machine that converts mechanical energy into AC electrical energy."),
            ("What is its frequency equation?", "f = PN/120.")
        ],
        "BLDC Motor": [
            ("What is a BLDC motor?", "A brushless DC motor with electronic commutation."),
            ("What is the use of a controller?", "It switches the motor phases electronically.")
        ]
    }

    for i, (question, answer) in enumerate(viva_questions[machine_name], 1):
        with st.expander(f"Q{i}. {question}"):
            st.write("**Answer:**", answer)

st.sidebar.markdown("---")
st.sidebar.success("EEE 3D Learning Lab")
st.caption("TECH MITHRA | B.Tech Electrical & Electronics Engineering")
