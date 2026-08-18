studiohome

Generative Architecture & Civil Engine

studiohome is an experimental generative architecture, engineering, urban simulation, and civilization intelligence platform built with Streamlit.

It provides a unified project cockpit where architectural design, structural engineering, MEP analysis, site intelligence, zoning compliance, cost analysis, simulation, and experimental urban/civilization systems can operate as interconnected modules.

---

Overview

studiohome is designed around a modular architecture.

At the center is the Executive Project Cockpit, which provides a high-level view of the active project and acts as the control layer for the rest of the system.

The current project model includes:

- Project intent
- Building typology
- Site area
- Number of floors
- Structural grid
- Structural system
- Live load
- Unit construction rate
- Gross floor area
- Estimated CAPEX
- Embodied carbon
- Energy / sustainability rating

The application also maintains shared civilization-state parameters for the experimental urban intelligence modules.

---

Core Architecture

                    ┌───────────────────────────┐
                    │     studiohome App        │
                    │     Streamlit Controller  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Executive Project       │
                    │        Cockpit            │
                    └─────────────┬─────────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
      Design & Engineering   Urban & Civilization   Shared State
             │                    │                    │
             ▼                    ▼                    ▼
       AI / Architecture      RL City             Project
       Structure              Learning             RL Engine
       MEP                     Diplomacy            Civilization
       GIS                     War                  State
       Cost                    Culture
       Massing                 Consciousness
       Zoning                  Meta-Evo
       Export
       Full Sim

---

Features

Executive Cockpit

The Executive Cockpit provides centralized project telemetry including:

- Active project typology
- Project CAPEX
- Embodied carbon
- Storey count
- System synchronization status
- Cross-disciplinary performance
- Quick module actions

The cockpit currently provides direct actions for:

- Zoning Code Audit
- Full Simulation Audit
- Unified BIM Export

---

Design & Engineering

The Design & Engineering suite contains the following modules:

Module| Purpose
AI Brain| Generative design and project intelligence
Architecture| Architectural design intelligence
Structure| Structural engineering / FEA workflows
MEP| Mechanical, electrical and plumbing systems
GIS & Site| Site and geographic intelligence
Cost| Construction cost and project economics
Massing| Building massing and form exploration
Zoning Code| Planning and regulatory compliance
Export Suite| Project and BIM-oriented exports
Full Sim| Integrated project simulation

Each module is intended to remain independently maintainable while sharing the central project state.

---

Urban & Civilization Intelligence

studiohome also contains an experimental simulation layer exploring larger-scale urban and civilization systems.

RL City

Reinforcement-learning-oriented city simulation.

City Learning

City-scale learning and adaptive intelligence.

Diplomacy

Simulation of relationships and interactions between urban or civilization entities.

War

Experimental conflict and geopolitical simulation.

Culture

Cultural development and behavioral simulation.

Consciousness

Experimental higher-level intelligence modeling.

Meta-Evo

Meta-evolution and long-horizon adaptive systems.

These modules are intentionally experimental and should not be interpreted as validated models of real-world societies, cities, or human behavior.

---

Project State

The application initializes a shared project state through Streamlit's session state.

Example:

st.session_state.project = {
    "intent": "...",
    "typology": "Commercial Innovation Hub",
    "site_area": 2500.0,
    "floors": 12,
    "grid_spacing": 8.0,
    "structural_system": "Mass Timber CLT & Glulam Frame",
    "live_load": 4.0,
    "unit_rate": 1650.0,
    "total_gfa": 30000.0,
    "estimated_cost": 49500000.0,
    "carbon_score": 420.0,
    "energy_rating": "LEED Platinum",
}

This shared state allows individual modules to operate as parts of the same project rather than as isolated applications.

---

Reinforcement Learning Engine

The application initializes:

from rl_engine import RLCityEngine

and stores the engine in:

st.session_state.rl_engine

This provides a shared entry point for reinforcement-learning-oriented city simulations.

---

Navigation

The Streamlit interface is organized into three navigation categories.

Overview & Control

- Executive Cockpit

Design & Engineering

- AI Brain
- Architecture
- Structure
- MEP
- GIS & Site
- Cost
- Massing
- Zoning Code
- Export Suite
- Full Sim

Urban & Civilization

- RL City
- City Learning
- Diplomacy
- War
- Culture
- Consciousness
- Meta-Evo

The selected module is rendered through the central module router.

---

Module Contract

Modules are imported from the "modules" package.

The controller expects each active module to expose:

render()

The routing layer follows this pattern:

module_mapping = {
    "AI Brain": ai_brain,
    "Architecture": architecture,
    "Structure": structure,
    # ...
}

and renders the selected module with:

module_mapping[active_tab].render()

This keeps the main application controller relatively simple while allowing individual systems to evolve independently.

---

User Interface

studiohome currently uses a dark, glassmorphism-inspired interface.

The visual system includes:

- Dark radial background
- Blue primary accent
- Glass-style cards
- Translucent sidebar
- Rounded controls
- Project telemetry cards
- Plotly visualizations
- Modular navigation
- Wide desktop layout

The application is designed to feel more like a digital project control room than a conventional Streamlit dashboard.

---

Installation

Clone the repository:

git clone https://github.com/jameswol-ai/studiohome.git
cd studiohome

Create a virtual environment:

python -m venv .venv

Activate it on Linux/macOS:

source .venv/bin/activate

On Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

---

Running Locally

Start the Streamlit application:

streamlit run streamlit_app.py

The application should then be available through the local Streamlit server.

---

Project Structure

A typical project structure is:

studiohome/
│
├── streamlit_app.py
├── rl_engine.py
├── requirements.txt
├── README.md
│
├── modules/
│   ├── __init__.py
│   │
│   ├── ai_brain.py
│   ├── architecture.py
│   ├── structure.py
│   ├── mep.py
│   ├── gis_site.py
│   ├── cost.py
│   ├── massing.py
│   ├── zoning_code.py
│   ├── export_suite.py
│   ├── full_sim.py
│   │
│   ├── rl_city.py
│   ├── city_learning.py
│   ├── diplomacy.py
│   ├── war.py
│   ├── culture.py
│   ├── consciousness.py
│   └── meta_evo.py
│
└── assets/

The exact structure may evolve as additional services, engines, data models, and visualization layers are introduced.

---

Development Principles

studiohome is being developed around several principles:

1. Modular by default

Individual disciplines should remain independently testable and maintainable.

2. Shared project intelligence

Modules should communicate through a common project state rather than creating disconnected copies of project information.

3. Progressive integration

New capabilities should first work independently before being integrated into the Executive Cockpit.

4. Engineering visibility

Important design and engineering decisions should be exposed through dashboards, metrics, simulations, and visualizations.

5. Experimental intelligence

AI, reinforcement learning, urban simulation, and civilization modules are treated as experimental research systems.

6. Preserve working behavior

Changes to the main controller should avoid unnecessary changes to existing modules.

---

Current Application Flow

Application startup
        │
        ▼
Streamlit page configuration
        │
        ▼
Initialize RL engine
        │
        ▼
Initialize shared project state
        │
        ▼
Initialize civilization state
        │
        ▼
Load interface styling
        │
        ▼
Build navigation
        │
        ▼
Select active module
        │
        ├───────────────┐
        │               │
        ▼               ▼
Executive Cockpit    Module Renderer
        │               │
        ▼               ▼
Project telemetry    Specialized system
        │
        ▼
Quick inter-module actions

---

Deep Linking

The controller supports selecting an initial module through the Streamlit query parameter:

?tab=Executive%20Cockpit

The application reads:

params = st.query_params
st.session_state.active_tab = params.get(
    "tab",
    "Executive Cockpit",
)

If an invalid module is supplied, the application falls back to:

Executive Cockpit

---

Validation

Before deploying changes, perform a Python syntax check:

python -m py_compile streamlit_app.py

Then run the application:

streamlit run streamlit_app.py

For a quick verification that only one page configuration call exists:

test "$(grep -c "st\.set_page_config" streamlit_app.py)" -eq 1 \
    && echo "OK: exactly one set_page_config()" \
    || echo "ERROR: duplicate set_page_config() calls"

---

Deployment

The project can be deployed as a Streamlit application.

The deployed application should use:

streamlit_app.py

as the application entry point.

Before deployment, verify:

- All module imports resolve
- "rl_engine.py" is available
- All modules expose the expected "render()" function
- Dependencies are listed in "requirements.txt"
- No duplicate "st.set_page_config()" calls exist
- The application starts without exceptions
- Executive Cockpit renders successfully
- Navigation reaches every registered module

---

Roadmap

Planned development can progressively connect the currently modular systems into a deeper project intelligence layer.

Potential areas include:

- Persistent project database
- Real-time project state synchronization
- Parametric architectural generation
- Structural optimization
- Energy simulation
- Carbon optimization
- Automated zoning analysis
- Cost optimization
- BIM interoperability
- GIS integration
- Multi-objective optimization
- Reinforcement-learning city generation
- Scenario simulation
- Cross-module dependency graphs
- Automated design alternatives
- Unified project versioning
- Export and reporting pipelines
- Advanced AI project orchestration

---

Status

Development stage: Experimental / Active Development

studiohome is a rapidly evolving research and development platform. APIs, module interfaces, data structures, simulation assumptions, and UI components may change as the system develops.

The current implementation should therefore be treated as an evolving prototype rather than a production-grade engineering certification platform.

---

Repository

GitHub:

https://github.com/jameswol-ai/studiohome

Live application:

https://studiohome.streamlit.app/

---

License

Add the project's intended license here before public distribution.

If no license has been selected yet, the repository should not be assumed to grant permission for unrestricted reuse, modification, or redistribution.