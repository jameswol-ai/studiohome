import streamlit as st
import numpy as np
import pandas as pd
import time
import random
from collections import defaultdict

# =====================================================
# IMPROVED RL CITY ENGINE
# =====================================================
class CityPolicy:
    def __init__(self, lr=0.2, decay=0.99, max_size=1000):
        self.risk_map = defaultdict(float)
        self.lr = lr
        self.decay = decay
        self.max_size = max_size

    def choose_location(self, max_attempts=10):
        for _ in range(max_attempts):
            x, y = random.randint(0, 25), random.randint(0, 25)
            if self.risk_map[(x, y)] <= 2.0:
                return x, y
        return random.randint(0, 25), random.randint(0, 25)

    def update(self, failed_nodes):
        for n in failed_nodes:
            x, y, z = n
            self.risk_map[(x, y)] += self.lr
        for k in list(self.risk_map.keys()):
            self.risk_map[k] *= self.decay
            if self.risk_map[k] < 0.01:
                del self.risk_map[k]
        if len(self.risk_map) > self.max_size:
            sorted_keys = sorted(self.risk_map, key=self.risk_map.get)
            for k in sorted_keys[:len(self.risk_map)-self.max_size]:
                del self.risk_map[k]

class RLBuildingEngine:
    def generate(self, policy):
        buildings = []
        for _ in range(5):
            x, y = policy.choose_location()
            buildings.append({
                "x": x,
                "y": y,
                "floors": random.randint(3, 10),
                "grid": random.choice([6, 8, 10, 12])
            })
        return buildings

class RLPhysics:
    def build_nodes(self, buildings):
        nodes = []
        for b in buildings:
            for z in range(b["floors"]):
                for x in range(0, b["grid"], 2):
                    for y in range(0, b["grid"], 2):
                        nodes.append((x + b["x"], y + b["y"], z))
        return nodes

    def loads(self, nodes):
        load = {n: 0.0 for n in nodes}
        if not nodes:
            return load
        max_z = max(n[2] for n in nodes)
        for n in nodes:
            if n[2] == max_z:
                load[n] += 1.0
        for _ in range(2):
            for (x, y, z), l in list(load.items()):
                below = (x, y, z - 1)
                if below in load:
                    load[below] += l * 0.7
        return load

    def collapse(self, load):
        return {n for n, l in load.items() if l > 2.0}

class RLCityEngine:
    def __init__(self):
        self.policy = CityPolicy()
        self.builder = RLBuildingEngine()
        self.physics = RLPhysics()
        self.history = []

    def step(self):
        buildings = self.builder.generate(self.policy)
        nodes = self.physics.build_nodes(buildings)
        loads = self.physics.loads(nodes)
        failed = self.physics.collapse(loads)
        self.policy.update(failed)
        stability = max(0, 1 - len(failed) / max(1, len(nodes)))
        reward = stability - 0.3 * len(failed)
        self.history.append(reward)
        return buildings, nodes, loads, failed, stability, reward

# =====================================================
# SESSION STATE CONFIG
# =====================================================
if "intent_text" not in st.session_state:
    st.session_state.intent_text = ""
if "site_area" not in st.session_state:
    st.session_state.site_area = 1000.0
if "rl_engine" not in st.session_state:
    st.session_state.rl_engine = RLCityEngine()
if "active_tab" not in st.session_state:
    params = st.query_params
    st.session_state.active_tab = params.get("tab", "AI Brain")

st.set_page_config(page_title="studiohome", layout="wide")

# =====================================================
# CUSTOM LOGO STYLING
# =====================================================
st.markdown("""
    <style>
    .custom-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 2px solid #262730;
        margin-bottom: 20px;
    }
    .custom-logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #FF4B4B, #FF8E53);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .custom-logo-text {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #FFFFFF, #A3A8B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    <div class="custom-logo-container">
        <div class="custom-logo-icon">SH</div>
        <div class="custom-logo-text">studiohome</div>
    </div>
""", unsafe_allow_html=True)

# ---- SIDEBAR PANEL SELECTION ----
tab_labels = [
    "AI Brain",
    "Architecture",
    "Structure",
    "MEP",
    "GIS & Site",
    "Cost",
    "Massing",
    "Full Sim",
    "RL City",
    "City Learning",
    "Diplomacy",
    "War",
    "Culture",
    "Consciousness",
    "Meta-Evo"
]

if st.session_state.active_tab not in tab_labels:
    st.session_state.active_tab = tab_labels[0]

with st.sidebar:
    st.markdown("### Navigation Panels")
    active_tab = st.radio(
        "Select panel",
        tab_labels,
        index=tab_labels.index(st.session_state.active_tab),
        key="tab_radio",
        label_visibility="collapsed"
    )
st.session_state.active_tab = active_tab

# =========================================================
# PANEL CONTENT IMPLEMENTATION
# =========================================================
if active_tab == "AI Brain":
    st.header("AI Design Brain")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.intent_text = st.text_area(
            "Describe your building intent",
            value=st.session_state.intent_text,
            height=100,
            placeholder="e.g., A 5-storey mixed-use building with courtyard..."
        )
    with col2:
        st.session_state.site_area = st.number_input(
            "Site area (m²)",
            value=st.session_state.site_area,
            min_value=100.0
        )
        if st.button("Generate Concept", use_container_width=True):
            floors = max(2, len(st.session_state.intent_text) % 20 + 3)
            grid = random.choice([6, 8, 10])
            st.session_state.generated = {
                "floors": floors,
                "grid_spacing": grid,
                "structural_system": random.choice(["RC Frame", "Steel", "Timber"]),
                "estimated_cost": floors * st.session_state.site_area * random.randint(800, 1200)
            }
            st.success(f"AI generated concept: {st.session_state.generated}")

elif active_tab == "Architecture":
    st.header("Architecture Engine")
    col1, col2 = st.columns(2)
    with col1:
        grid_spacing = st.slider("Grid spacing (m)", 2.0, 10.0, 6.0)
    with col2:
        grid_extent = st.slider("Grid size (m)", 10, 60, 30)
    if st.button("Show Grid Data"):
        rows = int(grid_extent / grid_spacing)
        grid_data = [[f"({i*grid_spacing:.0f},{j*grid_spacing:.0f})" for j in range(rows)] for i in range(rows)]
        st.dataframe(grid_data[:10])

elif active_tab == "Structure":
    st.header("Structural Engine")
    elements = {
        "Columns": "Vertical load‑bearing members (concrete/steel)",
        "Beams": "Horizontal members spanning between columns",
        "Slabs": "Floor/roof plates (one‑way or two‑way)",
        "Foundation": "Spread footings, piles, or raft",
        "Shear Walls": "Lateral stability cores"
    }
    st.table(elements.items())

elif active_tab == "MEP":
    st.header("MEP Systems")
    mep_tab1, mep_tab2, mep_tab3 = st.tabs(["Mechanical", "Electrical", "Plumbing"])
    with mep_tab1:
        st.metric("Cooling Load", f"{random.randint(80, 250)} kW")
    with mep_tab2:
        st.metric("Total Load", f"{random.randint(50, 500)} kVA")
    with mep_tab3:
        st.metric("Daily Water", f"{random.randint(1000, 5000)} L")

elif active_tab == "GIS & Site":
    st.header("Terrain Analysis")
    x = np.linspace(0, 10, 100)
    st.line_chart(np.column_stack([x, np.sin(x)]))

elif active_tab == "Cost":
    st.header("Cost Engine")
    area = st.number_input("Floor Area (m²)", value=500.0)
    cost = area * random.randint(400, 1200) if "generated" not in st.session_state else st.session_state.generated["estimated_cost"]
    st.metric("Estimated Cost", f"${cost:,.0f}")
    st.bar_chart({"Foundation": 15, "Structure": 30, "MEP": 25, "Finishes": 20, "Other": 10})

elif active_tab == "Massing":
    st.header("Spatial Massing Viewer")
    df_mass = pd.DataFrame({
        "x": np.random.randint(0, 20, 30),
        "y": np.random.randint(0, 20, 30),
        "height": np.random.randint(1, 15, 30)
    })
    st.dataframe(df_mass)

elif active_tab == "Full Sim":
    st.header("Full Simulation Pipeline")
    if st.button("Run All Modules"):
        steps = ["AI Design", "Architecture Grid", "Structural Physics", "MEP Sizing", "Cost Estimation", "Export Pipeline"]
        p = st.progress(0)
        for i, s in enumerate(steps):
            st.write(f"Executing: {s}...")
            time.sleep(0.3)
            p.progress((i+1)/len(steps))
        st.success("Simulation pipeline completed successfully!")

elif active_tab == "RL City":
    st.header("Reinforcement Learning City Engine")
    rl = st.session_state.rl_engine
    if st.button("Run City Step"):
        buildings, _, _, failed, stability, reward = rl.step()
        c1, c2, c3 = st.columns(3)
        c1.metric("Stability", round(stability, 3))
        c2.metric("Failures", len(failed))
        c3.metric("Reward", round(reward, 3))
        st.json(buildings)

elif active_tab == "City Learning":
    st.header("City Learning Curve")
    rl = st.session_state.rl_engine
    if rl.history:
        st.line_chart(rl.history)
    else:
        st.info("Run RL City steps first from the RL City panel.")

elif active_tab == "Diplomacy":
    st.header("Diplomacy Network")
    nations = ["Alpha","Beta","Gamma","Delta","Epsilon"]
    matrix = np.random.rand(len(nations), len(nations))
    df = pd.DataFrame(matrix, columns=nations, index=nations)
    st.dataframe(df)

elif active_tab == "War":
    st.header("War System")
    c1, c2 = st.columns(2)
    with c1: attacker = st.selectbox("Attacker", ["Alpha","Beta","Gamma"])
    with c2: defender = st.selectbox("Defender", ["Beta","Gamma","Delta"])
    if st.button("Simulate Battle"):
        st.metric("Outcome", random.choice(["Victory","Stalemate","Defeat"]))

elif active_tab == "Culture":
    st.header("Culture System")
    cities = ["City A","City B","City C","City D"]
    st.bar_chart(dict(zip(cities, np.random.rand(4))))

elif active_tab == "Consciousness":
    st.header("Civilization Consciousness")
    state = np.random.rand(10)
    st.json({
        "stability": float(np.mean(state)),
        "conflict_pressure": float(np.std(state)),
        "innovation_drive": float(np.max(state))
    })

elif active_tab == "Meta-Evo":
    st.header("Meta‑Evolution View")
    st.info("Meta‑learning layer active (conceptual)")
    if st.button("Run Meta Step"):
        st.json({"epoch": random.randint(1,100), "fitness": random.uniform(0.7,1.0)})

# ---- FOOTER ----
st.sidebar.caption(f"Active panel: {st.session_state.active_tab}")
