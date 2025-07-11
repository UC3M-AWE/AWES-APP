# AWES-APP

## Overview
AWES-APP is a web-based simulation and analysis tool for Airborne Wind Energy Systems (AWES), developed at UC3M. It enables users to simulate, visualize, and analyze the performance of pumping kite power systems using the Quasi-Steady Model (QSM) described by R. Van der Vlugt et al. ([QSM Paper](https://arxiv.org/abs/1705.04133)).

## Features
- Interactive web interface built with Streamlit
- Location-aware simulation (uses ERA5 data for roughness and altitude)
- Implements the QSM for pumping kite cycles (traction, retraction, transition phases)
- Customizable system and environmental parameters
- Multiple analysis types: time series, boxplots, energy, power, torque-speed, etc.
- Export simulation data for further analysis
- Modern UC3M-themed UI/UX

## How It Works
1. **Model Core (qsm.py):**
   - Implements the Quasi-Steady Model for pumping kite power systems.
   - Simulates the kite's motion in three phases: traction (power generation), retraction (energy consumption), and transition.
   - Calculates forces, speeds, and power at each time step using physical equations and system/environment parameters.
   - Returns time series and aggregate results for each cycle.

2. **Web App (AWES_app_copy_version20250709.py):**
   - Provides a Streamlit-based user interface for simulation setup, visualization, and data export.
   - Allows users to select location, wind profile, kite area, gearbox ratio, and other parameters.
   - Runs QSM simulations for selected scenarios and displays results in interactive Plotly charts.
   - Supports advanced analysis types, including boxplots for power distribution (reel-in/reel-out), mean/max ratios, and more.
   - Integrates with ERA5 NetCDF data for realistic site-specific simulation.

## Usage
1. **Install Requirements:**
   - Python 3.8+
   - Streamlit
   - Plotly
   - NumPy, Pandas
   - netCDF4 (for location data)

2. **Run the App:**
   ```bash
   python -m streamlit run AWES_app_copy_version20250709.py
   ```
   - Open the provided local URL in your browser.

3. **Simulation Workflow:**
   - Select your location on the map (loads roughness and altitude from ERA5 data).
   - Set simulation parameters in the sidebar (wind speed, kite area, gearbox ratio, etc.).
   - Choose analysis type (e.g., time series, boxplot, energy, etc.).
   - Click 'Simulate' to run the QSM model and view results.
   - Export data as CSV for further analysis.

## Technical Details
- **QSM Model:**
  - The QSM is implemented in `qsm.py` and models the kite, tether, and ground station as a set of coupled equations.
  - Each simulation step assumes steady-state conditions and solves for forces, speeds, and power.
  - The model supports custom wind profiles, system properties, and operational limits.

- **App Structure:**
  - `AWES_app_copy_version20250709.py`: Main Streamlit app, UI logic, simulation orchestration, plotting, and export.
  - `qsm.py`: QSM model implementation, phase logic, and simulation engine.
  - `location_utils.py`: Loads roughness and altitude from ERA5 NetCDF data.
  - `utils.py`: Helper functions for plotting and data manipulation.

## Example Analysis Types
- **AWES Cycle (linear/rotational variables):** Time series of reeling speed, tether force, and power.
- **Torque-speed char.:** Scatter plot of torque vs. rotational speed.
- **Power-distribution boxplot (reel-in/reel-out):** Boxplots showing mean and variance of power during retraction or generation phases.
- **Mean-max power ratio:** Ratio of mean to max power for cycle or generation phase.
- **Energy complete cycle/reel-out:** Total energy produced or consumed.

## References
- [Quasi-Steady Model of a Pumping Kite Power System (QSM Paper)](https://arxiv.org/abs/1705.04133)

## License
This project is for academic/research use at UC3M. Contact the authors for collaboration or usage outside UC3M.
