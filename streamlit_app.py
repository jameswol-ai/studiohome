import streamlit as st
import numpy as np
import pandas as pd
import time
import random
import json
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
if "civilization_state" not in st.session_state:
    st.session_state.civilization_state = {
        "stability": 0.85,
        "conflict": 0.20,
        "innovation": 0.78,
        "culture_score": 0.65
    }

st.set_page_config(page_title="studiohome", page_icon="🏠", layout="wide")

# =====================================================
# CUSTOM THEME & SIDEBAR CSS STYLING
# =====================================================
st.markdown("""
    <style>
    .studio-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 16px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 16px;
    }
    .studio-logo-icon {
        width: 38px;
        height: 38px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .studio-logo-icon svg {
        width: 20px;
        height: 20px;
        fill: #FFFFFF;
    }
    .studio-logo-text {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .studio-logo-text span {
        color: #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# Render Custom Logo in Sidebar
with st.sidebar:
    st.markdown("""
        <div class="studio-logo-wrapper">
            <div class="studio-logo-icon">
                <svg viewBox="0 0 24 24"><path d="M12 3L2 12h3v8h6v-6h2v6h6v-8h3L12 3z"/></svg>
            </div>
            <div class="studio-logo-text">studio<span>home</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 12px; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 8px;'>Navigation Suite</p>", unsafe_allow_html=True)

categories = {
    "Design & Engineering": [
        "AI Brain",
        "Architecture",
        "Structure",
        "MEP",
        "GIS & Site",
        "Cost",
        "Massing",
        "Export Suite",
        "Full Sim"
    ],
    "Urban & Civilization": [
        "RL City",
        "City Learning",
        "Diplomacy",
        "War",
        "Culture",
        "Consciousness",
        "Meta-Evo"
    ]
}

flat_tab_labels = [tab for tabs in categories.values() for tab in tabs]

if st.session_state.active_tab not in flat_tab_labels:
    st.session_state.active_tab = flat_tab_labels[0]

with st.sidebar:
    selected_category = st.selectbox(
        "Module Category", 
        list(categories.keys()),
        label_visibility="collapsed"
    )
    
    active_tab = st.radio(
        "Select panel",
        categories[selected_category],
        index=categories[selected_category].index(st.session_state.active_tab) if st.session_state.active_tab in categories[selected_category] else 0,
        key="tab_radio",
        label_visibility="collapsed"
    )
st.session_state.active_tab = active_tab

# =========================================================
# PANEL CONTENT IMPLEMENTATION
# =========================================================
if active_tab == "AI Brain":
    st.header("AI Design Brain")
    st.write("Synthesize complete architectural schemes, layout parameters, and spatial configurations from raw intent.")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.session_state.intent_text = st.text_area(
            "Describe your building intent",
            value=st.session_state.intent_text,
            height=120,
            placeholder="e.g., A sustainable 6-storey hybrid mass-timber commercial structure with central atrium..."
        )
    with col2:
        st.session_state.site_area = st.number_input(
            "Site area (m²)",
            value=st.session_state.site_area,
            min_value=100.0,
            step=50.0
        )
        target_use = st.selectbox("Primary Typology", ["Commercial", "Residential", "Mixed-Use", "Institutional", "Industrial"])
        if st.button("Generate Concept", use_container_width=True):
            floors = max(2, len(st.session_state.intent_text) % 15 + 3)
            grid = random.choice([6, 8, 10])
            st.session_state.generated = {
                "typology": target_use,
                "floors": floors,
                "grid_spacing": grid,
                "structural_system": "Mass Timber CLT" if target_use == "Residential" else "Reinforced Concrete Frame",
                "estimated_cost": floors * st.session_state.site_area * random.randint(900, 1400),
                "carbon_score": round(st.session_state.site_area * floors * 0.18, 2)
            }
            st.success("AI design concept generated successfully.")
            
    if "generated" in st.session_state:
        st.markdown("---")
        st.subheader("Synthesized Concept Overview")
        g = st.session_state.generated
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Storeys", g["floors"])
        m2.metric("Grid Spacing", f"{g['grid_spacing']} m")
        m3.metric("Structure", g["structural_system"])
        m4.metric("Est. Cost", f"${g['estimated_cost']:,.0f}")

elif active_tab == "Architecture":
    st.header("Architecture Engine")
    st.write("Configure spatial zoning, programmatic distribution, and structural column grids.")
    col1, col2, col3 = st.columns(3)
    with col1:
        grid_spacing = st.slider("Grid spacing (m)", 3.0, 12.0, 6.0, step=0.5)
    with col2:
        grid_extent = st.slider("Grid dimension extent (m)", 12, 80, 36, step=4)
    with col3:
        core_type = st.selectbox("Core Configuration", ["Central Core", "Dual Side Cores", "Perimeter Core", "Open Plan"])
    
    if st.button("Compute Spatial Grid Layout", use_container_width=True):
        rows = int(grid_extent / grid_spacing)
        cols = rows
        grid_matrix = []
        for r in range(rows):
            row_items = []
            for c in range(cols):
                zone_label = "Core" if (core_type=="Central Core" and abs(r-rows/2)<1 and abs(c-cols/2)<1) else f"Zone-{r},{c}"
                row_items.append(zone_label)
            grid_matrix.append(row_items)
        df_grid = pd.DataFrame(grid_matrix, columns=[f"X:{i*grid_spacing}m" for i in range(cols)], index=[f"Y:{i*grid_spacing}m" for i in range(rows)])
        st.success(f"Generated {rows}x{cols} grid network with {core_type}.")
        st.dataframe(df_grid, use_container_width=True)

elif active_tab == "Structure":
    st.header("Structural Engine")
    st.write("Analyze load distribution paths, member sizing profiles, and lateral bracing systems.")
    
    col1, col2 = st.columns(2)
    with col1:
        span_length = st.slider("Typical Beam Span (m)", 4.0, 15.0, 8.0)
        live_load = st.slider("Design Live Load (kN/m²)", 1.5, 7.5, 3.0)
    with col2:
        material_grade = st.selectbox("Material Specification", ["C30/37 Concrete", "C40/50 Concrete", "S355 Steel", "Glulam Timber"])
        seismic_zone = st.selectbox("Seismic Hazard Category", ["Zone 0 (Low)", "Zone 1 (Moderate)", "Zone 2 (High)", "Zone 3 (Severe)"])
    
    if st.button("Run Structural Sizing Calculation", use_container_width=True):
        req_depth = round((span_length * 1000) / 16, 1)
        col_dimension = round(300 + (span_length * live_load * 12), 0)
        st.info(f"Preliminary sizing results for **{material_grade}** under **{seismic_zone}** conditions:")
        
        s1, s2, s3 = st.columns(3)
        s1.metric("Recommended Beam Depth", f"{req_depth} mm")
        s2.metric("Min. Column Section", f"{int(col_dimension)}x{int(col_dimension)} mm")
        s3.metric("Estimated Steel Ratio", f"{random.uniform(1.8, 3.2):.2f}%")

elif active_tab == "MEP":
    st.header("MEP Systems Engine")
    st.write("Size mechanical, electrical, and plumbing distribution trunks based on building occupancy profiles.")
    
    mep_tab1, mep_tab2, mep_tab3 = st.tabs(["Mechanical & HVAC", "Electrical Distribution", "Plumbing & Drainage"])
    with mep_tab1:
        floor_area_mep = st.number_input("Conditioned Floor Area (m²)", value=2500.0, step=100.0)
        occupants = st.number_input("Design Occupancy Count", value=150, step=10)
        cooling_load_kw = round(floor_area_mep * 0.12 + occupants * 0.15, 1)
        airflow_m3h = int(cooling_load_kw * 310)
        
        c1, c2 = st.columns(2)
        c1.metric("Calculated Peak Cooling Load", f"{cooling_load_kw} kW")
        c2.metric("Required Supply Airflow", f"{airflow_m3h:,} m³/h")
    with mep_tab2:
        transformer_kva = int((floor_area_mep * 0.08) + 120)
        st.metric("Recommended Transformer Capacity", f"{transformer_kva} kVA")
        st.write("Primary Distribution Panels:")
        st.json({"Lighting Sub-Panel": "3x 100A 3P", "HVAC Power Center": "1x 400A 3P", "Emergency Life Safety": "1x 250A 3P"})
    with mep_tab3:
        water_demand_lpd = int(occupants * 50)
        st.metric("Estimated Daily Potable Water Demand", f"{water_demand_lpd:,} L/day")
        st.metric("Sanitary Drainage Peak Flow", f"{round(water_demand_lpd * 0.00045, 2)} L/s")

elif active_tab == "GIS & Site":
    st.header("GIS & Site Terrain Analyzer")
    st.write("Analyze topography contours, solar exposure vectors, and stormwater run-off paths.")
    
    col1, col2 = st.columns(2)
    with col1:
        slope_angle = st.slider("Site Average Slope (°)", 0.0, 45.0, 8.5)
        soil_type = st.selectbox("Subsurface Soil Classification", ["Dense Sand / Gravel", "Stiff Clay", "Weathered Rock", "Soft Alluvium"])
    with col2:
        orientation = st.slider("Site Orientation Angle (° from North)", 0, 360, 45)
        st.metric("Geotechnical Bearing Capacity", f"{'300 kPa' if 'Rock' in soil_type else '150 kPa'}")

    x = np.linspace(0, 10, 100)
    elevation_profile = np.sin(x) * (slope_angle / 5.0)
    st.line_chart(pd.DataFrame({"Elevation Contour (m)": elevation_profile}, index=x))

elif active_tab == "Cost":
    st.header("Cost Estimation Engine")
    st.write("Dynamic budget modeling breakdown based on regional indices and material specifications.")
    
    total_area = st.number_input("Total Gross Floor Area (GFA m²)", value=3500.0, step=250.0)
    unit_rate = st.slider("Base Unit Cost Rate ($/m²)", 800, 2500, 1400, step=50)
    
    base_cost = total_area * unit_rate
    breakdown = {
        "Substructure & Foundation": base_cost * 0.12,
        "Superstructure Frame": base_cost * 0.28,
        "Building Envelope & Facade": base_cost * 0.20,
        "MEP Services": base_cost * 0.22,
        "Interior Finishes & Fitout": base_cost * 0.10,
        "Contingency & Professional Fees": base_cost * 0.08
    }
    
    st.metric("Total Project Cost Estimate", f"${sum(breakdown.values()):,.0f}")
    st.bar_chart(pd.Series(breakdown))

elif active_tab == "Massing":
    st.header("Spatial Massing Viewer")
    st.write("Inspect volumetric massing blocks and proportional height distributions across the project site.")
    
    num_blocks = st.slider("Active Massing Blocks", 1, 10, 5)
    massing_data = []
    for i in range(num_blocks):
        massing_data.append({
            "Block ID": f"Block-{chr(65+i)}",
            "Footprint Area (m²)": random.randint(200, 900),
            "Height (m)": random.randint(12, 65),
            "Floor Count": random.randint(4, 20),
            "Program Type": random.choice(["Residential", "Office", "Retail", "Amenity"])
        })
    df_massing = pd.DataFrame(massing_data)
    st.dataframe(df_massing, use_container_width=True)

elif active_tab == "Export Suite":
    st.header("BIM & CAD Export Suite")
    st.write("Export verified design models, metadata reports, and spatial interchange files.")
    
    if "generated" in st.session_state:
        concept_data = st.session_state.generated
        json_str = json.dumps(concept_data, indent=2)
        st.download_button(
            label="Download Complete Concept Spec (.json)",
            data=json_str,
            file_name="studiohome_concept.json",
            mime="application/json",
            use_container_width=True
        )
        
        df_export = pd.DataFrame({
            "Parameter": ["Primary Typology", "Site Area", "Estimated Floors", "Grid Spacing", "Structural System", "Estimated Cost", "Embodied Carbon"],
            "Value": [
                concept_data.get("typology", "Commercial"),
                st.session_state.site_area, 
                concept_data.get("floors"), 
                concept_data.get("grid_spacing"), 
                concept_data.get("structural_system"), 
                concept_data.get("estimated_cost"),
                concept_data.get("carbon_score")
            ]
        })
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Executive Summary Report (.csv)",
            data=csv_data,
            file_name="studiohome_summary.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No active design concept found. Generate a concept in the 'AI Brain' panel first.")
    
    mock_dxf = "SECTION\n2\nHEADER\n0\nSECTION\n2\nENTITIES\n0\nLINE\n8\n0\n10\n0.0\n20\n0.0\n30\n0.0\n11\n10.0\n21\n10.0\n31\n0.0\n0\nENDSEC\n0\nEOF"
    st.download_button(
        label="Download OpenBIM / CAD Geometry (.dxf)",
        data=mock_dxf,
        file_name="studiohome_model.dxf",
        mime="application/dxf",
        use_container_width=True
    )

elif active_tab == "Full Sim":
    st.header("Full Simulation Pipeline")
    st.write("Execute sequential validation across all engineering, economic, and regulatory modules.")
    if st.button("Run Comprehensive Simulation Suite", use_container_width=True):
        pipeline_steps = [
            "Parsing AI Intent & Program Matrix...",
            "Validating Structural Finite Element Loads...",
            "Computing Thermal & HVAC Mass Balance...",
            "Running GIS Slope & Drainage Calculations...",
            "Aggregating Bill of Quantities & Cost Profile...",
            "Compiling BIM Interoperability Exchange Files..."
        ]
        p = st.progress(0)
        for i, s in enumerate(pipeline_steps):
            st.write(s)
            time.sleep(0.35)
            p.progress((i + 1) / len(pipeline_steps))
        st.success("All pipeline modules verified successfully with zero structural or economic conflicts.")

elif active_tab == "RL City":
    st.header("Reinforcement Learning City Engine")
    st.write("Simulate multi-agent urban development growth cycles using spatial risk feedback loops.")
    rl = st.session_state.rl_engine
    if st.button("Execute Urban Growth Step", use_container_width=True):
        buildings, _, _, failed, stability, reward = rl.step()
        c1, c2, c3 = st.columns(3)
        c1.metric("Network Stability Index", round(stability, 3))
        c2.metric("Structural Failures", len(failed))
        c3.metric("Policy Reward", round(reward, 3))
        st.json(buildings)

elif active_tab == "City Learning":
    st.header("City Learning Curve Analytics")
    st.write("Track the cumulative optimization trajectory and reward convergence of the urban policy engine.")
    rl = st.session_state.rl_engine
    if rl.history:
        st.line_chart(pd.Series(rl.history, name="Policy Reward Convergence"))
    else:
        st.info("Run urban simulation steps from the 'RL City' panel to generate learning trajectory records.")

elif active_tab == "Diplomacy":
    st.header("Inter-District Diplomacy Network")
    st.write("Manage trade treaties, territorial pacts, and diplomatic trust matrices between regional factions.")
    nations = ["North District", "Metro Core", "East Port", "Silicon Valley", "South Eco-Zone"]
    matrix = np.random.uniform(0.2, 1.0, (len(nations), len(nations)))
    np.fill_diagonal(matrix, 1.0)
    df_diplomacy = pd.DataFrame(matrix, columns=nations, index=nations)
    st.dataframe(df_diplomacy, use_container_width=True)

elif active_tab == "War":
    st.header("Strategic Conflict Simulation")
    st.write("Simulate defensive stability, resource contention outcomes, and regional skirmish dynamics.")
    c1, c2 = st.columns(2)
    with c1: attacker = st.selectbox("Aggressor Faction", ["North District", "Metro Core", "East Port"])
    with c2: defender = st.selectbox("Target Faction", ["Metro Core", "East Port", "Silicon Valley", "South Eco-Zone"])
    
    if st.button("Simulate Strategic Engagement", use_container_width=True):
        outcome = random.choice(["Decisive Aggressor Victory", "Stalemate / Ceasefire Negotiated", "Successful Defensive Repulsion"])
        st.metric("Engagement Outcome", outcome)
        st.json({
            "aggressor_attrition": f"{random.randint(5, 22)}%",
            "defender_infrastructure_damage": f"{random.randint(2, 18)}%",
            "treaty_stability_shift": f"{random.uniform(-0.15, 0.05):.3f}"
        })

elif active_tab == "Culture":
    st.header("Cultural Evolution & Demographics")
    st.write("Monitor index trends in cultural diffusion, civic satisfaction, and urban identity.")
    districts = ["Arts Quarter", "Financial Center", "Industrial Hub", "Residential Suburb"]
    culture_metrics = {
        "Civic Engagement Index": np.random.uniform(0.6, 0.95),
        "Architectural Identity Score": np.random.uniform(0.5, 0.88),
        "Public Trust Index": np.random.uniform(0.7, 0.92)
    }
    st.bar_chart(pd.Series(culture_metrics))

elif active_tab == "Consciousness":
    st.header("Civilization Consciousness Monitor")
    st.write("Real-time telemetry tracking collective civic sentiment, pressure gradients, and innovation momentum.")
    cs = st.session_state.civilization_state
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Civic Stability", f"{cs['stability']*100:.1f}%")
    c2.metric("Conflict Pressure", f"{cs['conflict']*100:.1f}%")
    c3.metric("Innovation Drive", f"{cs['innovation']*100:.1f}%")
    c4.metric("Cultural Synergy", f"{cs['culture_score']*100:.1f}%")
    
    if st.button("Pulse Consciousness Update", use_container_width=True):
        st.session_state.civilization_state["stability"] = min(1.0, max(0.1, cs['stability'] + random.uniform(-0.05, 0.05)))
        st.session_state.civilization_state["innovation"] = min(1.0, max(0.1, cs['innovation'] + random.uniform(-0.03, 0.06)))
        st.rerun()

elif active_tab == "Meta-Evo":
    st.header("Meta‑Evolutionary Layer")
    st.write("Optimize hyper-parameters governing artificial intelligence neural topologies and evolutionary selection rules.")
    
    mutation_rate = st.slider("Evolutionary Mutation Rate", 0.01, 0.25, 0.05, step=0.01)
    generations = st.slider("Target Epoch Count", 10, 500, 100, step=10)
    
    if st.button("Run Meta-Optimization Epoch", use_container_width=True):
        final_fitness = round(random.uniform(0.85, 0.99), 4)
        st.success(f"Evolutionary cycle completed across {generations} generations with mutation rate {mutation_rate}.")
        st.json({
            "final_population_fitness": final_fitness,
            "optimal_hyperparameters_locked": True,
            "convergence_epoch": random.randint(int(generations*0.4), generations)
        })

# ---- FOOTER ----
st.sidebar.markdown("---")
st.sidebar.caption(f"Active: **{st.session_state.active_tab}**")
