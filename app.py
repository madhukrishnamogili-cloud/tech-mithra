
import streamlit as st
import streamlit.components.v1 as components
import base64
import json

st.set_page_config(
    page_title="Tech Mithra - Electrical Machines 3D Lab",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background: #0b1220; color: white;}
h1,h2,h3 {color: #e5efff;}
[data-testid="stMetric"] {
    background: #17243a;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- MACHINE DATA ----------------

PARTS = {
    "Yoke": {
        "function": "Provides mechanical support and a magnetic path.",
        "working": "It carries the magnetic flux between the poles.",
        "material": "Cast iron or steel."
    },
    "Pole Core": {
        "function": "Supports the field winding and produces magnetic poles.",
        "working": "It guides magnetic flux towards the armature.",
        "material": "Laminated or solid magnetic steel."
    },
    "Field Winding": {
        "function": "Produces the main magnetic field.",
        "working": "DC current through the winding creates magnetic flux.",
        "material": "Insulated copper."
    },
    "Armature": {
        "function": "Carries armature conductors.",
        "working": "Current-carrying conductors experience force in the magnetic field.",
        "material": "Laminated electrical steel and copper."
    },
    "Commutator": {
        "function": "Provides current reversal in armature conductors.",
        "working": "It helps maintain unidirectional torque.",
        "material": "Copper segments with insulation."
    },
    "Brushes": {
        "function": "Transfer current between the stationary circuit and rotating commutator.",
        "working": "They maintain electrical contact with the commutator.",
        "material": "Carbon or graphite."
    },
    "Shaft": {
        "function": "Transfers mechanical output.",
        "working": "It transmits rotation to the connected load.",
        "material": "Steel."
    },
    "Bearing": {
        "function": "Supports the rotating shaft.",
        "working": "It reduces friction during rotation.",
        "material": "Bearing steel."
    },
    "Fan": {
        "function": "Provides cooling.",
        "working": "It moves air over the motor body.",
        "material": "Metal or engineering plastic."
    }
}

st.title("⚡ Tech Mithra – Electrical Machines 3D Lab")
st.caption("B.Tech EEE | Interactive Electrical Machines Learning")

st.sidebar.title("⚙️ Machine Selection")
machine = st.sidebar.selectbox(
    "Select Machine",
    ["DC Motor"]
)

st.sidebar.success("Current Module: DC Motor")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧊 3D Exploded View",
    "⚡ Electrical Parameters",
    "📘 Study Material",
    "🎓 Viva Questions"
])

# ---------------- 3D VIEW ----------------

with tab1:
    st.header("DC Motor – Interactive 3D Model")

    st.info(
        "Upload a multi-part DC Motor GLB model. "
        "Each component should be a separate mesh with a meaningful name."
    )

    uploaded_model = st.file_uploader(
        "Upload DC Motor 3D Model (.glb)",
        type=["glb"],
        help="Use a GLB model with separate meshes for Yoke, Armature, Shaft, etc."
    )

    if uploaded_model:
        model_bytes = uploaded_model.getvalue()
        model_b64 = base64.b64encode(model_bytes).decode("utf-8")
        parts_json = json.dumps(PARTS)

        html = r"""
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    background: #0b1220;
    color: white;
    font-family: Arial, sans-serif;
}
#viewer {
    width: 100%;
    height: 510px;
    position: relative;
    overflow: hidden;
    border-radius: 12px;
}
#info {
    background: #17243a;
    padding: 14px;
    margin-top: 10px;
    border-radius: 10px;
    min-height: 95px;
}
#controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    padding: 10px 0;
    align-items: center;
}
button {
    background: #2563eb;
    border: none;
    color: white;
    padding: 10px 15px;
    border-radius: 8px;
    cursor: pointer;
}
button:hover { background: #1d4ed8; }
input { width: 150px; }
#hint {
    position: absolute;
    top: 10px;
    left: 10px;
    background: #17243add;
    padding: 8px;
    border-radius: 6px;
    z-index: 2;
}
</style>
</head>
<body>

<div id="viewer">
    <div id="hint">Drag: Rotate | Scroll: Zoom | Click: Select Part</div>
</div>

<div id="controls">
    <button id="explode">💥 Explode</button>
    <button id="assemble">🔧 Assemble</button>
    <label>Explosion: <span id="amount">0%</span></label>
    <input id="slider" type="range" min="0" max="100" value="0">
</div>

<div id="info">
    <b>Selected Part:</b> Click any motor component.<br>
    <span id="partName">No part selected</span>
    <p id="partDetails">Part information will appear here.</p>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

import { OrbitControls } from
'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';

import { GLTFLoader } from
'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js';

const MODEL_DATA = "MODEL_BASE64";
const PARTS = PARTS_DATA;

const viewer = document.getElementById("viewer");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1220);

const camera = new THREE.PerspectiveCamera(
    45, viewer.clientWidth / viewer.clientHeight, 0.1, 1000
);

camera.position.set(5, 4, 7);

const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(viewer.clientWidth, viewer.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
viewer.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

scene.add(new THREE.HemisphereLight(0xffffff, 0x334455, 2));

const light1 = new THREE.DirectionalLight(0xffffff, 3);
light1.position.set(5, 8, 6);
scene.add(light1);

const light2 = new THREE.DirectionalLight(0x66aaff, 1.5);
light2.position.set(-5, 2, -5);
scene.add(light2);

const grid = new THREE.GridHelper(12, 12, 0x334466, 0x223344);
scene.add(grid);

let model = null;
let meshParts = [];
let selected = null;
let pointerStart = null;

function showPart(mesh) {
    const rawName = mesh.name || "Unnamed Part";
    const key = Object.keys(PARTS).find(
        k => rawName.toLowerCase().includes(k.toLowerCase())
    );

    document.getElementById("partName").textContent = rawName;

    if (key) {
        const p = PARTS[key];
        document.getElementById("partDetails").innerHTML =
            "<b>Function:</b> " + p.function +
            "<br><b>Working:</b> " + p.working +
            "<br><b>Material:</b> " + p.material;
    } else {
        document.getElementById("partDetails").textContent =
            "No description is mapped for this mesh name. " +
            "Rename the mesh to a supported part name.";
    }
}

function selectMesh(mesh) {
    if (selected && selected.material) {
        selected.material.emissive?.setHex(0x000000);
    }

    selected = mesh;

    if (selected.material && selected.material.emissive) {
        selected.material.emissive.setHex(0x224466);
    }

    showPart(mesh);
}

const loader = new GLTFLoader();

const binary = Uint8Array.from(
    atob(MODEL_DATA),
    c => c.charCodeAt(0)
).buffer;

loader.parse(binary, "", (gltf) => {
    model = gltf.scene;
    scene.add(model);

    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);

    model.position.sub(center);

    camera.position.set(maxDim * 1.8, maxDim * 1.3, maxDim * 2.2);
    camera.near = Math.max(maxDim / 1000, 0.001);
    camera.far = maxDim * 100;
    camera.updateProjectionMatrix();

    controls.target.set(0, 0, 0);
    controls.update();

    model.updateMatrixWorld(true);

    model.traverse((obj) => {
        if (obj.isMesh) {
            const worldPosition = new THREE.Vector3();
            obj.getWorldPosition(worldPosition);

            const direction = worldPosition.clone().normalize();

            if (direction.length() < 0.001) {
                direction.set(0, 1, 0);
            } else {
                direction.normalize();
            }

            const distance = maxDim * 0.35;
            const targetWorld = worldPosition.clone().add(
                direction.multiplyScalar(distance)
            );

            const targetLocal = obj.parent.worldToLocal(targetWorld);

            meshParts.push({
                mesh: obj,
                original: obj.position.clone(),
                exploded: targetLocal.clone()
            });
        }
    });

    document.getElementById("partDetails").textContent =
        "Model loaded. Click a component to see its details.";
}, (error) => {
    document.getElementById("partDetails").textContent =
        "Could not load the GLB model. Check that the file is valid.";
    console.error(error);
});

function setExplosion(value) {
    const t = value / 100;
    document.getElementById("amount").textContent = value + "%";

    meshParts.forEach(item => {
        item.mesh.position.lerpVectors(
            item.original,
            item.exploded,
            t
        );
    });
}

document.getElementById("explode").onclick = () => {
    document.getElementById("slider").value = 100;
    setExplosion(100);
};

document.getElementById("assemble").onclick = () => {
    document.getElementById("slider").value = 0;
    setExplosion(0);
};

document.getElementById("slider").oninput = (e) => {
    setExplosion(Number(e.target.value));
};

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

renderer.domElement.addEventListener("pointerdown", (e) => {
    pointerStart = {x: e.clientX, y: e.clientY};
});

renderer.domElement.addEventListener("pointerup", (e) => {
    if (!pointerStart) return;

    const moved = Math.hypot(
        e.clientX - pointerStart.x,
        e.clientY - pointerStart.y
    );

    pointerStart = null;
    if (moved > 5 || !model) return;

    const rect = renderer.domElement.getBoundingClientRect();

    pointer.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(pointer, camera);

    const hits = raycaster.intersectObjects(model.children, true);

    if (hits.length) {
        selectMesh(hits[0].object);
    }
});

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
    camera.aspect = viewer.clientWidth / viewer.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(viewer.clientWidth, viewer.clientHeight);
});
</script>
</body>
</html>
"""
        html = html.replace("MODEL_BASE64", model_b64)
        html = html.replace("PARTS_DATA", parts_json)

        components.html(html, height=680, scrolling=False)

    else:
        st.warning("ముందుగా DC Motor యొక్క .glb 3D model upload చేయండి.")
        st.markdown("""
        **GLB model‌లో ఉండాల్సిన separate mesh names:**

        - Yoke
        - Pole Core
        - Field Winding
        - Armature
        - Commutator
        - Brushes
        - Shaft
        - Bearing
        - Fan
        """)

    st.subheader("DC Motor Parts – Study List")

    selected_part = st.selectbox(
        "Select a part to study",
        list(PARTS.keys())
    )

    p = PARTS[selected_part]

    st.markdown(f"### 🔩 {selected_part}")
    st.write("**Function:**", p["function"])
    st.write("**Working:**", p["working"])
    st.write("**Material:**", p["material"])


# ---------------- ELECTRICAL PARAMETERS ----------------

with tab2:
    st.header("⚡ DC Motor Electrical Parameters")
    st.caption("Illustrative example values only. Actual values depend on the motor nameplate.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rated Voltage", "220 V")
    c2.metric("Rated Current", "5 A")
    c3.metric("Rated Power", "1 kW")

    c4, c5, c6 = st.columns(3)
    c4.metric("Speed", "1500 RPM")
    c5.metric("Frequency", "DC Supply")
    c6.metric("Efficiency", "85%")

    st.subheader("Motor Calculations")

    st.latex(r"N_s = \frac{120f}{P}")
    st.write("Synchronous speed formula – used for AC machines, not DC motor speed calculation.")

    st.latex(r"E_b = V - I_aR_a")
    st.write("Back EMF equation")

    st.latex(r"T = \frac{9.55P}{N}")
    st.write("Torque in N·m, when P is in watts and N is in RPM.")

    st.subheader("Try Your Own Values")

    voltage = st.number_input("Voltage (V)", min_value=0.0, value=220.0)
    current = st.number_input("Current (A)", min_value=0.0, value=5.0)
    power = voltage * current

    st.metric("Input Electrical Power (V × I)", f"{power:.2f} W")


# ---------------- STUDY MATERIAL ----------------

with tab3:
    st.header("📘 DC Motor Study Material")

    with st.expander("1. Working Principle"):
        st.write("""
        A DC motor works on the principle that a current-carrying
        conductor placed in a magnetic field experiences a force.

        The direction of force is given by Fleming's Left-Hand Rule.
        The commutator helps maintain unidirectional torque.
        """)

    with st.expander("2. Applications"):
        st.write("""
        - Electric traction
        - Cranes and hoists
        - Conveyors
        - Machine tools
        - Robotics and control systems
        """)

    with st.expander("3. Advantages"):
        st.write("""
        - Easy speed control
        - High starting torque in suitable DC motor types
        - Simple control characteristics
        """)

    with st.expander("4. Limitations"):
        st.write("""
        - Brushes and commutator need maintenance.
        - Brush wear can occur.
        - Some environments are unsuitable for brushed motors.
        """)

    with st.expander("5. Important Formulae"):
        st.latex(r"E_b = V - I_aR_a")
        st.latex(r"T = \frac{9.55P}{N}")
        st.latex(r"P_{in} = VI")


# ---------------- VIVA ----------------

with tab4:
    st.header("🎓 DC Motor Viva Questions")

    questions = [
        ("What is a DC motor?",
         "A DC motor converts DC electrical energy into mechanical energy."),

        ("What is the working principle of a DC motor?",
         "A current-carrying conductor placed in a magnetic field experiences a force."),

        ("What is the function of a commutator?",
         "It reverses the armature conductor current at suitable intervals to maintain unidirectional torque."),

        ("What is back EMF?",
         "Back EMF is the induced voltage in the armature that opposes the applied voltage."),

        ("What is the function of brushes?",
         "Brushes transfer electrical current between the external circuit and commutator."),

        ("Which rule gives the direction of force?",
         "Fleming's Left-Hand Rule."),

        ("What is the function of a yoke?",
         "It provides mechanical support and a magnetic return path."),

        ("Name two applications of DC motors.",
         "Electric traction and cranes are two applications.")
    ]

    for i, (question, answer) in enumerate(questions, 1):
        with st.expander(f"Q{i}. {question}"):
            st.write(answer)

st.divider()
st.caption("Tech Mithra | B.Tech EEE Learning Lab")
