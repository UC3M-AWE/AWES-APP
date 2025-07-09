#python -m streamlit run AWES_app.py
#http://192.168.1.79:8501

import streamlit as st
import numpy as np
import time
import pandas as pd
from qsm import Cycle, LogProfile, SystemProperties, TractionPhase
import plotly.graph_objs as go

class KiteApp:
    
    def __init__(self):
        #region Initial data
        wind_step = int(20)
        drum_radius = 0.2  # radius of the drum

        h_ref = 10  # Reference height
        altitude = 1450  # Sta. María de la Alameda
        h_0 = 0.073  # Roughness length Vortex data
        rmax = 200
        rmin = 100
        tether_angle = 26.6 * np.pi / 180.

        doomie=False
        #endregion
        
        #st.set_option('deprecation.showPyplotGlobalUse', False)

        st.sidebar.title("AWES App UC3M")
        cycletype = st.sidebar.selectbox("Select Cycle Type", [
            "AWES Cycle (linear variables)", "AWES Cycle (rotational variables)", "Torque-speed char.", "Max. power reel in",
            "Max. power reel out", "Max. speed reel out", "Mean Power",
            "Mean-max power ratio complete cycle", "Mean-max power ratio only generation",
            "Energy complete cycle", "Energy reel-out", "Torque-speed boxplot",
            "Power-speed boxplot"
        ])

        if cycletype == "AWES Cycle (linear variables)":
            wind_speed = st.sidebar.text_input(r"Wind speed (m/s)", 5, key="add_wind_speed")
            kite_area = st.sidebar.text_input(r"Kite area (m^2)", 7, key="add_kite_area")
            scale_factor = st.sidebar.text_input("Select Gearbox Ratio", 4.26, key="add_scale_factor")

            update_text = st.empty()
            update_text.info("Values Updated")

            time.sleep(2)
            update_text.empty()

            st.markdown(
                f'<div style="background-color:#f0f0f0;padding:10px;border-radius:5px;">'
                f'<p style="font-weight:bold;">Newest updated values:</p>'
                f'<p style="display:inline;">AWES Cycle:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{cycletype}</p>'
                f'<p style="display:inline;">Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{wind_speed} m/s</p>'
                f'<p style="display:inline;">Kite area:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{kite_area} m²</p>'
                f'<p style="display:inline;">Scale Factor:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;">{scale_factor}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            doomie=True
            if st.sidebar.button("Simulate", key="add_simulate"):
                sys_props=self.initiate(float(kite_area),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)
                self.add_linear_profile(float(wind_speed), float(kite_area), float(scale_factor), cycletype,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props) #se cambia scale_factor para que sea double

        elif cycletype == "AWES Cycle (rotational variables)":
            wind_speed = st.sidebar.text_input(r"Wind speed (m/s)", 5, key="add_wind_speed")
            kite_area = st.sidebar.text_input(r"Kite area (m^2)", 7, key="add_kite_area")
            scale_factor = st.sidebar.text_input("Select Gearbox Ratio", 4.26, key="add_scale_factor")

            update_text = st.empty()
            update_text.info("Values Updated")

            time.sleep(2)
            update_text.empty()

            st.markdown(
                f'<div style="background-color:#f0f0f0;padding:10px;border-radius:5px;">'
                f'<p style="font-weight:bold;">Newest updated values:</p>'
                f'<p style="display:inline;">AWES Cycle:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{cycletype}</p>'
                f'<p style="display:inline;">Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{wind_speed} m/s</p>'
                f'<p style="display:inline;">Kite area:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{kite_area} m²</p>'
                f'<p style="display:inline;">Scale Factor:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;">{scale_factor}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            doomie=True
            if st.sidebar.button("Simulate", key="add_simulate"):
                sys_props=self.initiate(float(kite_area),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)
                self.add_rotational_profile(float(wind_speed), float(kite_area), float(scale_factor), cycletype,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props) #se cambia scale_factor para que sea double

        elif cycletype in [
                "Torque-speed char.",
                "Max. speed reel out",
                "Energy complete cycle",
                "Torque-speed boxplot",
                "Power-speed boxplot"
            ]:
            
                        # Sidebar
            kite_area_value = st.sidebar.text_input(r'Kite area (m^2)', 7)
            scale_factor_value = st.sidebar.text_input("Select Gearbox Ratio",4.26)
            min_wind_speed_value = st.sidebar.text_input(r'Minimum wind speed (m/s)', 5)
            max_wind_speed_value = st.sidebar.text_input(r'Maximum wind speed(m/s)', 12)
            update_text = st.empty()
            update_text.info("Values Updated")

            time.sleep(2)
            update_text.empty()
            st.markdown(
                f'<div style="background-color:#f0f0f0;padding:10px;border-radius:5px;">'
                f'<p style="font-weight:bold;">Newest updated values:</p>'
                f'<p style="display:inline;">AWES Cycle:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{cycletype}</p>'
                f'<p style="display:inline;">Minimum Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{min_wind_speed_value} m/s</p>'
                f'<p style="display:inline;">Maximum Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{max_wind_speed_value} m/s</p>'
                f'<p style="display:inline;">Kite area:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{kite_area_value} m²</p>'
                f'<p style="display:inline;">Gear box ratio:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;">{scale_factor_value}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            # Botón para simular
            if st.sidebar.button("Simulate", key="add_simulate"):
                self.initiate(float(kite_area_value),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)

                # Convertir los valores de cadena a flotante
                try:
                    kite_area = float(kite_area_value)
                    min_wind_speed = float(min_wind_speed_value)
                    max_wind_speed = float(max_wind_speed_value)
                except ValueError:
                    st.error(
                        "Please enter valid numerical values for kite area, minimum wind speed, and maximum wind speed.")
                    st.stop()  # Detener la ejecución del script si hay un error de valor

                # Llamar a la función para generar los gráficos
                st.subheader("Graph")
                fig = self.energy_plots(kite_area_value, scale_factor_value, cycletype, min_wind_speed_value, max_wind_speed_value)
                # Mostrar la figura en Streamlit
                st.plotly_chart(fig)

            else:
                # Placeholder for additional code
                pass
        
        elif cycletype in [
                "Max. power reel in",
                "Max. power reel out",
                "Mean Power",
                "Mean-max power ratio complete cycle",
                "Mean-max power ratio only generation",
                "Energy complete cycle",
                "Energy reel-out",
            ]:
            

            # Sidebar
            kite_area_value = st.sidebar.text_input(r'Kite area (m^2)', 7)
            min_wind_speed_value = st.sidebar.text_input(r'Minimum wind speed (m/s)', 5)
            max_wind_speed_value = st.sidebar.text_input(r'Maximum wind speed(m/s)', 12)
            update_text = st.empty()
            update_text.info("Values Updated")

            time.sleep(2)
            update_text.empty()
            st.markdown(
                f'<div style="background-color:#f0f0f0;padding:10px;border-radius:5px;">'
                f'<p style="font-weight:bold;">Newest updated values:</p>'
                f'<p style="display:inline;">AWES Cycle:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{cycletype}</p>'
                f'<p style="display:inline;">Minimum Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{min_wind_speed_value} m/s</p>'
                f'<p style="display:inline;">Maximum Wind speed:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{max_wind_speed_value} m/s</p>'
                f'<p style="display:inline;">Kite area:</p>'
                f'<p style="color:blue;display:inline;margin-left:5px;margin-right:20px;">{kite_area_value} m²</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            # Botón para simular
            if st.sidebar.button("Simulate", key="add_simulate"):
                self.initiate(float(kite_area_value),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)
                # Convertir los valores de cadena a flotante
                try:
                    kite_area = float(kite_area_value)
                    min_wind_speed = float(min_wind_speed_value)
                    max_wind_speed = float(max_wind_speed_value)
                except ValueError:
                    st.error(
                        "Please enter valid numerical values for kite area, minimum wind speed, and maximum wind speed.")
                    st.stop()  # Detener la ejecución del script si hay un error de valor
                # Llamar a la función para generar los gráficos
                st.subheader("Graph")
                fig = self.energy_plots(kite_area_value, 1, cycletype, min_wind_speed_value, max_wind_speed_value) #scale_factor mandamos 1 porque no se usa
                # Mostrar la figura en Streamlit
                st.plotly_chart(fig)   

          
        if st.sidebar.button("Clear Plot", key="clear_plot"):
            self.clear_plot()


        if doomie is False:
            self.plot_graph()

        if ('plot_data' in st.session_state and st.session_state['plot_data']) or ('energy_plot_data' in st.session_state and st.session_state['energy_plot_data']):
            self.export_data_button(cycletype)

    def plot_graphs_linear(self):
        if 'plot_data' in st.session_state:
            fig1 = go.Figure()
            fig2 = go.Figure()
            fig3 = go.Figure()

            colors = ['blue', 'red', 'green', 'purple', 'orange', 'pink']  # Colores para los gráficos adicionales
            for idx, (fig_data1, fig_data2, fig_data3, wind_speed, kite_area, data) in enumerate(
                    st.session_state['plot_data']):
                color = colors[idx % len(colors)]  # Asignar color cíclicamente
                fig1.add_trace(
                    go.Scatter(x=data["time"], y=data["reeling_speed"], mode='lines',
                               name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}', line=dict(color=color))
                )
                fig2.add_trace(
                    go.Scatter(x=data["time"], y=data["tether_force"], mode='lines',
                               name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}', line=dict(color=color))
                )
                fig3.add_trace(
                    go.Scatter(x=data["time"], y=data["power"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}',
                               line=dict(color=color))
                )

            fig1.update_layout(
                title='Reeling Speed vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Reeling Speed (m/s)',
                width=1000,
                height=400,
                showlegend=True
            )

            fig2.update_layout(
                title='Tether Force vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Tether Force (N)',
                width=1000,
                height=400,
                showlegend=True
            )

            fig3.update_layout(
                title='Power vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Power (W)',
                width=1000,
                height=400,
                showlegend=True
            )

            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
            st.plotly_chart(fig3)


    def plot_graphs_rotational(self):
        if 'plot_data' in st.session_state:
            fig1 = go.Figure()
            fig2 = go.Figure()
            fig3 = go.Figure()

            colors = ['blue', 'red', 'green', 'purple', 'orange', 'pink']  # Colores para los gráficos adicionales
            for idx, (fig_data1, fig_data2, fig_data3, wind_speed, kite_area, data) in enumerate(
                    st.session_state['plot_data']):
                color = colors[idx % len(colors)]  # Asignar color cíclicamente
                # Calculate omega_rpm using list comprehension
                omega_rpm = [val * 60 / (2 * np.pi) for val in data["omega"]]
                fig1.add_trace(
                    go.Scatter(x=data["time"], y=omega_rpm, mode='lines',
                               name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}', line=dict(color=color))
                )
                fig2.add_trace(
                    go.Scatter(x=data["time"], y=data["torque"], mode='lines',
                               name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}', line=dict(color=color))
                )
                fig3.add_trace(
                    go.Scatter(x=data["time"], y=data["power"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}',
                               line=dict(color=color))
                )

            fig1.update_layout(
                title='Rotational speed vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Rotational speed (rpm)',
                width=1000,
                height=400,
                showlegend=True
            )

            fig2.update_layout(
                title='Torque vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Torque (Nm)',
                width=1000,
                height=400,
                showlegend=True
            )

            fig3.update_layout(
                title='Power vs Time',
                xaxis_title='Time (s)',
                yaxis_title='Power (W)',
                width=1000,
                height=400,
                showlegend=True
            )

            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
            st.plotly_chart(fig3)


    def add_linear_profile(self, wind_speed, kite_area, scale_factor, cycletype,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props):

        try:
            wind_speed_value = float(wind_speed)
            kite_area_value = float(kite_area)
        except ValueError:
            st.error("Please enter valid numerical values for wind speed and kite area.")
            return

        #self.initiate(float(kite_area),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)
        fig1, fig2, fig3, data = awes_cycle_linear(wind_speed_value, kite_area_value, scale_factor,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props)

        if fig1 is not None and fig2 is not None and fig3 is not None:
            if 'plot_data' not in st.session_state:
                st.session_state['plot_data'] = []

            st.session_state['plot_data'].append((fig1, fig2, fig3, wind_speed_value, kite_area_value, data))
            self.plot_graphs_linear()
            
    def add_rotational_profile(self, wind_speed, kite_area, scale_factor, cycletype,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props):

        try:
            wind_speed_value = float(wind_speed)
            kite_area_value = float(kite_area)
        except ValueError:
            st.error("Please enter valid numerical values for wind speed and kite area.")
            return

        #self.initiate(float(kite_area),wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle)
        fig1, fig2, fig3, data = awes_cycle_rotational(wind_speed_value, kite_area_value, scale_factor,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props)

        if fig1 is not None and fig2 is not None and fig3 is not None:
            if 'plot_data' not in st.session_state:
                st.session_state['plot_data'] = []

            st.session_state['plot_data'].append((fig1, fig2, fig3, wind_speed_value, kite_area_value, data))
            self.plot_graphs_rotational()

    def energy_plots(self,kite_area, gearbox_ratio, graph_type, min_wind_speed, max_wind_speed):
        data=sweep_data(kite_area, gearbox_ratio, min_wind_speed, max_wind_speed)
         # Verificar si ya hay datos almacenados en session_state
        if 'energy_plot_data' not in st.session_state:
            st.session_state['energy_plot_data'] = []

        # Añadir los datos de la simulación actual a session_state
        st.session_state['energy_plot_data'].append({
            "kite_area": kite_area,
            "gearbox_ratio": gearbox_ratio,
            "min_wind_speed": min_wind_speed,
            "max_wind_speed": max_wind_speed,
            "data": data
        })
        max_powers= [np.max(sublist) if sublist else np.nan for sublist in data["power"]]
        min_powers= [np.max(np.min(sublist)) if sublist else np.nan for sublist in data["power"]]
        mean_powers= [np.mean(sublist) if sublist else np.nan for sublist in data["power"]]
        mean_powers_gen = [np.mean([x for x in sublist if x > 0]) if any(x > 0 for x in sublist) else np.nan for sublist in data["power"]]
        max_omega_gen = [60 * sublist[-1] / (2 * np.pi) if sublist else np.nan for sublist in data["omega"]]

        energy_all = [
        energy_calc(time,power) if power else np.nan
        for power, time in zip(data["power"], data["time"])
        ]

        energy_gen = []
        for power_list, time_list in zip(data["power"], data["time"]):
            positive_powers = [power for power in power_list if power > 0]
            positive_times = [time for time, power in zip(time_list, power_list) if power > 0]
            energy_gen.append(energy_calc(positive_times, positive_powers))

        fig = self.generate_energy_plots(graph_type, max_powers, min_powers, mean_powers, mean_powers_gen, max_omega_gen, energy_all, energy_gen)
        return fig

    def initiate(self,kite_area,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle):

        m_p_area = (13.9 - 3.7) / (19 - 5)  # y = mx+n / Area to Projected Area based on Ozone Edge specs
        n_p_area = 13.9 - m_p_area * 19

        m_weight = (4.7 - 2.2) / (19 - 5)  # y = mx+n / Weight from area based on Ozone Edge specs
        n_weight = 4.7 - m_weight * 19

        sys_props = {
            'kite_projected_area': kite_area * m_p_area + n_p_area,  # kite_area,  # [m^2]
            'kite_mass': kite_area * m_weight + n_weight + 0.5,  # estimated weight + electronics  [kg]
            'tether_density': 724.,  # [kg/m^3]
            'tether_diameter': 0.002,  # [m]
            'kite_lift_coefficient_powered': 0.69,  # [-]
            'kite_drag_coefficient_powered': 0.69 / 3.6,  # [-]
            'kite_lift_coefficient_depowered': .17,  # [-]
            'kite_drag_coefficient_depowered': .17 / 3.5,  # [-]
            'tether_drag_coefficient': 2 * 1.1,  # [-]
            'reeling_speed_min_limit': 0.,  # [m/s]
            'reeling_speed_max_limit': 10.,  # [m/s]
            'tether_force_min_limit': 500.,  # [N]
            'tether_force_max_limit': 50000.,  # [N]
        }
        sys_props = SystemProperties(sys_props)

        rmax = 200
        rmin = 100
        tether_angle = 26.6 * np.pi / 180.
        return sys_props
        
    def generate_energy_plots(self, graph_type, max_powers, min_powers, mean_powers, mean_powers_gen, max_omega_gen, energy_all, energy_gen):
        if 'energy_plot_data' not in st.session_state or not st.session_state['energy_plot_data']:
            return None

        fig = go.Figure()
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'pink']  # Colores para diferenciar las simulaciones

        for idx, sim_data in enumerate(st.session_state['energy_plot_data']):
            data = sim_data["data"]
            kite_area = sim_data["kite_area"]
            gearbox_ratio = sim_data["gearbox_ratio"]
            Min_wind_speed = sim_data['min_wind_speed']
            Max_wind_speed = sim_data['max_wind_speed']
            color = colors[idx % len(colors)]  # Asignar color cíclicamente

            if graph_type == "Torque-speed char.":
                omega = data["omega"]
                omega_rpm = [[val * 60 / (2 * np.pi) for val in sublist] for sublist in omega]
                torque = data["torque"]

                # Flatten the lists for plotting
                torque_flat = [item for sublist in torque for item in sublist]
                omega_rpm_flat = [item for sublist in omega_rpm for item in sublist]

                
                fig.add_trace(
                    go.Scatter(x=omega_rpm_flat, y=torque_flat, mode='markers', marker=dict(symbol='circle', size=2,opacity=0.5,color=color),
                name=f'Kite area: {kite_area}, Gearbox ratio: {gearbox_ratio}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'))
                fig.update_layout(
                    xaxis_title='Omega (RPM)',
                    yaxis_title='Torque (Nm)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
                )
            elif graph_type == "Max. power reel in":

                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=min_powers,
                        mode='lines+markers',
                        marker=dict(symbol='circle',size=2, opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}')
                        )
                            
                fig.update_layout(

                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Max power reel in (W)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Max. power reel out":

                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=max_powers,
                        mode='lines+markers',
                        marker=dict(symbol='circle',size=2, opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        )
                            )
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Max power reel out (W)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Max. speed reel out":

                
                fig.add_trace(go.Scatter(x=data["wind"], y=max_omega_gen,mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Gearbox ratio: {gearbox_ratio}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'))

                fig.update_layout(
                    xaxis_title='Wind Speed (m/s)',
                    yaxis_title='Speed (rpm)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
                )

                

            elif graph_type == "Mean Power":

                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=mean_powers,
                        mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        )
                            )
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Mean Power (W)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Mean-max power ratio complete cycle":
                mean_max_total=[mean_power / max_power for mean_power, max_power in zip(mean_powers, max_powers)]

                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=mean_max_total,
                        mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        )
                            )
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Mean power/Max power (pu)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                


            elif graph_type == "Mean-max power ratio only generation":
                
                mean_max_gen=[mean_power_gen / max_power for mean_power_gen, max_power in zip(mean_powers_gen, max_powers)]

                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=mean_max_gen,
                        mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        )
                            )
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Mean power/Max power (pu)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Energy complete cycle":
                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=energy_all,
                        mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                        name=f'Kite area: {kite_area}, Gearbox ratio: {gearbox_ratio}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        ))
                            
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Energy (J)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Energy reel-out":
                
                fig.add_trace(
                    go.Scatter(
                        x=data["wind"],
                        y=energy_gen,
                        mode='lines+markers',
                        marker=dict(symbol='circle', opacity=0.5,color=color),
                name=f'Kite area: {kite_area}, Min wind speed: {Min_wind_speed}, Max wind speed: {Max_wind_speed}'
                        )
                            )
                fig.update_layout(
                    xaxis_title='Wind speed (m/s)',
                    yaxis_title='Energy (J)',
                    showlegend=True,
                    width=1000,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)'
            )

                

            elif graph_type == "Torque-speed boxplot":
                # Convert omega to rpm
                omega = data["omega"]
                omega_rpm = [[val * 60 / (2 * np.pi) for val in sublist] for sublist in omega]
                torque = data["torque"]

                # Flatten torque and omega_rpm for plotting
                torque_flat = np.array([item for sublist in torque for item in sublist])
                omega_rpm_flat = np.array([item for sublist in omega_rpm for item in sublist])

                # Calculate unique rounded values for omega_rpm
                unique_values = np.linspace(np.min(omega_rpm_flat), np.max(omega_rpm_flat), num=20)
                rounded_arr = np.array([min(unique_values, key=lambda x: abs(x - val)) for val in omega_rpm_flat.ravel()]).reshape(omega_rpm_flat.shape)

                # Create a dictionary to store x values corresponding to each unique value in rounded_arr
                x_dict = {}
                for i, val in enumerate(rounded_arr):
                    if val not in x_dict:
                        x_dict[val] = []
                    x_dict[val].append(torque_flat[i])

                # Prepare data for the box plot
                data_plot = []
                for i, (rpm, torques) in enumerate(x_dict.items(), start=1):
                    data_plot.append(go.Box(
                        y=torques,
                        name=f'{int(rpm)}',
                        boxpoints='outliers',  # Show all points for better distribution visibility
                        jitter=0.3,  # Add jitter for better point distribution
                        whiskerwidth=0.2,
                        marker=dict(
                            size=2, color='blue'
                        ),
                        line=dict(width=1),

                    ))

                # Create the Plotly figure
                fig = go.Figure(data=data_plot)

                # Update layout
                fig.update_layout(
                    xaxis=dict(
                        title='Speed (rpm)',
                        showgrid=True,
                        zeroline=False,
                        title_font=dict(size=24),
                        tickfont=dict(size=22)    # Tamaño de los números del eje X
                    ),
                    yaxis=dict(
                        title='Torque (Nm)',
                        title_font=dict(size=24),
                        tickfont=dict(size=22)    # Tamaño de los números del eje X
                    ),
                    height=600,  # Adjust height as needed
                    width=1000,  # Adjust width as needed
                    showlegend=False
                )


                

            elif graph_type == "Power-speed boxplot":
                # Convert omega to rpm
                omega = data["omega"]
                omega_rpm = [[val * 60 / (2 * np.pi) for val in sublist] for sublist in omega]
                power = data["power"]

                # Flatten torque and omega_rpm for plotting
                power_flat = np.array([item for sublist in power for item in sublist])
                omega_rpm_flat = np.array([item for sublist in omega_rpm for item in sublist])

                # Calculate unique rounded values for omega_rpm
                unique_values = np.linspace(np.min(omega_rpm_flat), np.max(omega_rpm_flat), num=20)
                rounded_arr = np.array([min(unique_values, key=lambda x: abs(x - val)) for val in omega_rpm_flat.ravel()]).reshape(omega_rpm_flat.shape)

                # Create a dictionary to store x values corresponding to each unique value in rounded_arr
                x_dict = {}
                for i, val in enumerate(rounded_arr):
                    if val not in x_dict:
                        x_dict[val] = []
                    x_dict[val].append(power_flat[i])

                # Prepare data for the box plot
                data_plot = []
                for i, (rpm, powers) in enumerate(x_dict.items(), start=1):
                    data_plot.append(go.Box(
                        y=powers,
                        name=f'{int(rpm)}',
                        boxpoints='outliers',  # Show all points for better distribution visibility
                        jitter=0.3,  # Add jitter for better point distribution
                        whiskerwidth=0.2,
                        marker=dict(
                            size=2,
                            color='blue'
                        ),
                        line=dict(width=1),
                    ))

                # Create the Plotly figure
                fig = go.Figure(data=data_plot)

                # Update layout
                fig.update_layout(
                    xaxis=dict(
                        title='Speed (rpm)',
                        showgrid=True,
                        zeroline=False,
                        
                        tickfont=dict(size=22)    # Tamaño de los números del eje X
                    ),
                    yaxis=dict(
                        title='Power (W)',
                        showgrid=True,
                        zeroline=False,
                        
                        tickfont=dict(size=22)    # Tamaño de los números del eje X
                    ),
                    height=600,  # Adjust height as needed
                    width=1000,  # Adjust width as needed
                    showlegend=False
                )

        return fig

    def plot_graph(self):
        if 'plot_data' in st.session_state:
            for idx, (fig1, fig2, fig3, _, _, _) in enumerate(st.session_state['plot_data']):
                st.plotly_chart(fig1, use_container_width=True)
                st.plotly_chart(fig2, use_container_width=True)
                st.plotly_chart(fig3, use_container_width=True)

    def export_data_button(self, graph_type):
        combined_data = []
        if ('plot_data' in st.session_state and st.session_state['plot_data']):
            for idx, (_, _, _, wind_speed, kite_area, data) in enumerate(st.session_state['plot_data']):
                for i in range(len(data['time'])):
                    combined_data.append({
                        'Profile': idx + 1,
                        'Time': data['time'][i],
                        'Reeling Speed': data['reeling_speed'][i],
                        'Tether Force': data['tether_force'][i],
                        'Power': data['power'][i],
                        'Wind Speed': wind_speed,
                        'Kite Area': kite_area
                    })

        
        if 'energy_plot_data' in st.session_state and st.session_state['energy_plot_data']:
            combined_data = []
            
            for idx, sim_data in enumerate(st.session_state['energy_plot_data']):
                data = sim_data["data"]
                max_wind = sim_data["max_wind_speed"]
                min_wind = sim_data["min_wind_speed"]
                kite_area = sim_data["kite_area"]
                if graph_type == "Torque-speed char.":    
                    # Aplanar las listas de omega y power
                    for i in range(len(data["time"])):  # Asumimos que time tiene la longitud correcta
                        time_points = data["time"][i]
                        omega_points = data["omega"][i]
                        power_points = data["power"][i]
                        torque_points = data["torque"][i]
                        
                        # Iterar por cada punto de tiempo
                        for time, omega, power, torque in zip(time_points, omega_points, power_points, torque_points):
                            combined_data.append({
                                'Profile': idx + 1,
                                'Time': time,
                                'Omega': float(omega),  # Convertir a float nativo
                                'Power': float(power),  # Convertir a float nativo
                                'Torque': float(torque),  # Convertir a float nativo
                                'Max Wind Speed': max_wind,
                                'Min Wind Speed': min_wind,
                                'Kite Area': kite_area
                            })
                elif graph_type == "Mean-max power ratio only generation":
                    mean_powers_gen = [np.mean([x for x in sublist if x > 0]) if any(x > 0 for x in sublist) else np.nan for sublist in data["power"]]
                    max_powers = [np.max(sublist) if sublist else np.nan for sublist in data["power"]]
                    mean_max_gen_points = [mean_power_gen / max_power for mean_power_gen, max_power in zip(mean_powers_gen, max_powers)]
                    
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        mean_max_gen = mean_max_gen_points[i]
                        
                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Mean-Max Ratio': mean_max_gen,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })
                elif graph_type == "Max. power reel in":
                    min_powers= [np.max(np.min(sublist)) if sublist else np.nan for sublist in data["power"]]
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        min_power = min_powers[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Min. Power': min_power,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })
                elif graph_type == "Max. power reel out":
                    max_powers = [np.max(sublist) if sublist else np.nan for sublist in data["power"]]
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        max_power = max_powers[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Max. Power': max_power,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })
                elif graph_type == "Max. speed reel out":
                    max_omega_gen = [60 * sublist[-1] / (2 * np.pi) if sublist else np.nan for sublist in data["omega"]]
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        max_omega = max_omega_gen[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Max. Omega': max_omega,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })

                elif graph_type == "Mean Power":
                    mean_powers= [np.mean(sublist) if sublist else np.nan for sublist in data["power"]]
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        mean_power = mean_powers[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Mean Power': mean_power,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })

                elif graph_type == "Mean-max power ratio complete cycle":
                    mean_powers= [np.mean(sublist) if sublist else np.nan for sublist in data["power"]]
                    max_powers = [np.max(sublist) if sublist else np.nan for sublist in data["power"]]
                    mean_max_total=[mean_power / max_power for mean_power, max_power in zip(mean_powers, max_powers)]
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        mean_max = mean_max_total[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Mean/Max Power': mean_max,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })

                elif graph_type == "Energy complete cycle":
                    energy_all = [
                    energy_calc(time,power) if power else np.nan
                    for power, time in zip(data["power"], data["time"])
                    ]   
                    for i in range(len(data["wind"])):
                        wind_speed = data["wind"][i]  # Asume que es un valor único
                        energy = energy_all[i]

                        combined_data.append({
                            'Profile': idx + 1,
                            'Wind speed': wind_speed,
                            'Energy': energy,
                            'Max Wind Speed': max_wind,
                            'Min Wind Speed': min_wind,
                            'Kite Area': kite_area    
                        })

                elif graph_type == "Torque-speed boxplot":
                    omega = data["omega"]
                    torque = data["torque"]

                    # Convert omega a RPM y aplanar
                    omega_rpm = [[val * 60 / (2 * np.pi) for val in sublist] for sublist in omega]
                    torque_flat = np.array([item for sublist in torque for item in sublist])
                    omega_rpm_flat = np.array([item for sublist in omega_rpm for item in sublist])

                    # Crear bins y agrupar
                    unique_values = np.linspace(np.min(omega_rpm_flat), np.max(omega_rpm_flat), num=20)
                    rounded_arr = np.array([
                        min(unique_values, key=lambda x: abs(x - val)) for val in omega_rpm_flat.ravel()
                    ]).reshape(omega_rpm_flat.shape)

                    x_dict = {}
                    for i, val in enumerate(rounded_arr):
                        if val not in x_dict:
                            x_dict[val] = []
                        x_dict[val].append(torque_flat[i])

                    # Agregar los datos a combined_data
                    for rpm_bin, torques in x_dict.items():
                        for torque_val in torques:
                            combined_data.append({
                                'Profile': idx + 1,
                                'Speed (rpm)': float(rpm_bin),
                                'Torque (Nm)': float(torque_val),
                                'Max Wind Speed': max_wind,
                                'Min Wind Speed': min_wind,
                                'Kite Area': kite_area
                            })
                elif graph_type == "Power-speed boxplot":
                    omega = data["omega"]
                    power = data["power"]

                    # Convert omega a RPM y aplanar
                    omega_rpm = [[val * 60 / (2 * np.pi) for val in sublist] for sublist in omega]
                    power_flat = np.array([item for sublist in power for item in sublist])
                    omega_rpm_flat = np.array([item for sublist in omega_rpm for item in sublist])

                    # Crear bins y agrupar
                    unique_values = np.linspace(np.min(omega_rpm_flat), np.max(omega_rpm_flat), num=20)
                    rounded_arr = np.array([
                        min(unique_values, key=lambda x: abs(x - val)) for val in omega_rpm_flat.ravel()
                    ]).reshape(omega_rpm_flat.shape)

                    x_dict = {}
                    for i, val in enumerate(rounded_arr):
                        if val not in x_dict:
                            x_dict[val] = []
                        x_dict[val].append(power_flat[i])

                    # Agregar los datos a combined_data
                    for rpm_bin, powers in x_dict.items():
                        for power_val in powers:
                            combined_data.append({
                                'Profile': idx + 1,
                                'Speed (rpm)': float(rpm_bin),
                                'Power (W)': float(power_val),
                                'Max Wind Speed': max_wind,
                                'Min Wind Speed': min_wind,
                                'Kite Area': kite_area
                            })


            # Crear DataFrame y exportar
            if combined_data:
                df = pd.DataFrame(combined_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Export Data",
                    data=csv,
                    file_name="awes_energy_data.csv",
                    mime="text/csv"
                )

        df = pd.DataFrame(combined_data)
        csv = df.to_csv(index=False)
        st.download_button(label="Download CSV", data=csv, file_name='awes_data.csv', mime='text/csv')

    def clear_plot(self):
        st.session_state['plot_data'] = []
        st.session_state['energy_plot_data'] = []

def awes_cycle_linear(wind_speed, kite_area, gearbox_ratio,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props):
    data = {
        "reeling_speed": [],
        "tether_force": [],
        "time": [],
        "wind": [],
        "power": [],
        "torque": [],
        "omega": [],
        "mean_power": []
    }

    env_state = LogProfile()
    env_state.set_reference_height(h_ref)
    env_state.set_reference_wind_speed(wind_speed)
    env_state.set_reference_roughness_length(h_0)
    env_state.set_altitude_ground(altitude)
    max_wind_speed_1 = wind_speed * np.log(altitude + rmax * np.sin(tether_angle) / h_0) / np.log(h_ref / h_0)

    cycle_settings = {
        'cycle': {
            'tether_length_start_retraction': rmax,
            'tether_length_end_retraction': rmin,
            'include_transition_energy': False,
            'elevation_angle_traction': 26.6 * np.pi / 180.,
            'traction_phase': TractionPhase,
        },
        'retraction': {
            'control': ('tether_force_ground', 900),
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
        'transition': {
            'control': ('tether_force_ground', 900),
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
        'traction': {
            'control': ('max_power_reeling_factor', 3069),
            'time_step': 0.01 * (rmax - rmin) / 7.3,
            'azimuth_angle': 10.6 * np.pi / 180.,
            'course_angle': 96.4 * np.pi / 180.,
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
    }
    cycle = Cycle(cycle_settings)

    try:
        error, time, average, traction, retraction = cycle.run_simulation(sys_props, env_state, print_summary=False)

        steady_states = cycle.steady_states
        times = cycle.time
        reeling_speeds = [state.reeling_speed for state in steady_states]
        tether_force_ground = [state.tether_force_ground for state in steady_states]
        power_ground = [state.power_ground for state in steady_states]
        torques = [force * drum_radius / gearbox_ratio for force in tether_force_ground]
        omegas = [(speed / drum_radius) * gearbox_ratio for speed in reeling_speeds]

        data["reeling_speed"] = reeling_speeds
        data["tether_force"] = tether_force_ground
        data["time"] = times
        data["wind"] = wind_speed
        data["power"] = power_ground
        data["torque"] = torques
        data["omega"] = omegas
        mean_power = sum(power_ground) / len(power_ground)

        data["mean_power"].append(mean_power)

        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(x=data["time"], y=data["reeling_speed"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}'))
        fig1.update_layout(
            title='Reeling Speed vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Reeling Speed (m/s)',
            width=1000,
            height=400,
        )

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=data["time"], y=data["tether_force"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}'))
        fig2.update_layout(
            title='Tether Force vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Tether Force (N)',
            width=1000,
            height=400,
        )

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=data["time"], y=data["power"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}'))
        fig3.update_layout(
            title='Power vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Power (W)',
            width=1000,
            height=400,
        )

        return fig1, fig2, fig3, data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None

def awes_cycle_rotational(wind_speed, kite_area, gearbox_ratio,wind_step,drum_radius,h_ref,altitude,h_0,rmax,rmin,tether_angle,sys_props):
    data = {
        "reeling_speed": [],
        "tether_force": [],
        "time": [],
        "wind": [],
        "power": [],
        "torque": [],
        "omega": [],
        "mean_power": []
    }

    env_state = LogProfile()
    env_state.set_reference_height(h_ref)
    env_state.set_reference_wind_speed(wind_speed)
    env_state.set_reference_roughness_length(h_0)
    env_state.set_altitude_ground(altitude)
    max_wind_speed_1 = wind_speed * np.log(altitude + rmax * np.sin(tether_angle) / h_0) / np.log(h_ref / h_0)

    cycle_settings = {
        'cycle': {
            'tether_length_start_retraction': rmax,
            'tether_length_end_retraction': rmin,
            'include_transition_energy': False,
            'elevation_angle_traction': 26.6 * np.pi / 180.,
            'traction_phase': TractionPhase,
        },
        'retraction': {
            'control': ('tether_force_ground', 900),
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
        'transition': {
            'control': ('tether_force_ground', 900),
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
        'traction': {
            'control': ('max_power_reeling_factor', 3069),
            'time_step': 0.01 * (rmax - rmin) / 7.3,
            'azimuth_angle': 10.6 * np.pi / 180.,
            'course_angle': 96.4 * np.pi / 180.,
            'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
        },
    }
    cycle = Cycle(cycle_settings)

    try:
        error, time, average, traction, retraction = cycle.run_simulation(sys_props, env_state, print_summary=False)

        steady_states = cycle.steady_states
        times = cycle.time
        reeling_speeds = [state.reeling_speed for state in steady_states]
        tether_force_ground = [state.tether_force_ground for state in steady_states]
        power_ground = [state.power_ground for state in steady_states]
        torques = [force * drum_radius / gearbox_ratio for force in tether_force_ground]
        omegas = [(speed / drum_radius) * gearbox_ratio for speed in reeling_speeds]
        # Calculate omega_rpm using list comprehension
        omega_rpm = [val * 60 / (2 * np.pi) for val in data["omega"]]

        data["reeling_speed"] = reeling_speeds
        data["tether_force"] = tether_force_ground
        data["time"] = times
        data["wind"] = wind_speed
        data["power"] = power_ground
        data["torque"] = torques
        data["omega"] = omegas
        mean_power = sum(power_ground) / len(power_ground)

        data["mean_power"].append(mean_power)

        fig1 = go.Figure()
        fig1.add_trace(
            go.Scatter(x=data["time"], y=omega_rpm, mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}. Gearbox ratio: {gearbox_ratio}'))
        fig1.update_layout(
            title='Rotational speed vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Rotational speed (rpm)',
            width=1000,
            height=400,
        )

        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=data["time"], y=data["torque"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}. Gearbox ratio: {gearbox_ratio}'))
        fig2.update_layout(
            title='Torque vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Torque (Nm)',
            width=1000,
            height=400,
        )

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=data["time"], y=data["power"], mode='lines', name=f'Wind speed: {wind_speed} m/s. Kite area: {kite_area}. Gearbox ratio: {gearbox_ratio}'))
        fig3.update_layout(
            title='Power vs Time',
            xaxis_title='Time (s)',
            yaxis_title='Power (W)',
            width=1000,
            height=400,
        )

        return fig1, fig2, fig3, data

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None, None


def energy_calc(times, powers):

    diffs = np.diff(times)
    powered_values = powers[:-1] * diffs
    result = np.sum(powered_values)
    return result

def sweep_data(kite_area, gearbox_ratio, min_wind_speed, max_wind_speed):
    data = {
        "reeling_speed": [],
        "tether_force": [],
        "time": [],
        "wind": [],
        "power": [],
        "torque": [],
        "omega": [],
        "mean_power": []
    }
    gearbox_ratio=float(gearbox_ratio)
    kite_area=float(kite_area)
    wind_step = 20
    drum_radius = 0.2  # radius of the drum

    h_ref = 10  # Reference height
    altitude = 1450  # Sta. María de la Alameda
    h_0 = 0.073  # Roughness length Vortex data

    m_p_area = (13.9 - 3.7) / (19 - 5)  # y = mx+n / Area to Projected Area based on Ozone Edge specs
    n_p_area = 13.9 - m_p_area * 19

    m_weight = (4.7 - 2.2) / (19 - 5)  # y = mx+n / Weight from area based on Ozone Edge specs
    n_weight = 4.7 - m_weight * 19

    sys_props = {
        'kite_projected_area': kite_area * m_p_area + n_p_area,  # kite_area,  # [m^2]
        'kite_mass': kite_area * m_weight + n_weight + 0.5,  # estimated weight + electronics  [kg]
        'tether_density': 724.,  # [kg/m^3]
        'tether_diameter': 0.002,  # [m]
        'kite_lift_coefficient_powered': 0.69,  # [-]
        'kite_drag_coefficient_powered': 0.69 / 3.6,  # [-]
        'kite_lift_coefficient_depowered': .17,  # [-]
        'kite_drag_coefficient_depowered': .17 / 3.5,  # [-]
        'tether_drag_coefficient': 2 * 1.1,  # [-]
        'reeling_speed_min_limit': 0.,  # [m/s]
        'reeling_speed_max_limit': 10.,  # [m/s]
        'tether_force_min_limit': 500.,  # [N]
        'tether_force_max_limit': 50000.,  # [N]
    }
    sys_props = SystemProperties(sys_props)

    rmax = 200
    rmin = 100
    tether_angle = 26.6 * np.pi / 180.


    for current_wind_speed in np.linspace(float(min_wind_speed), float(max_wind_speed), wind_step, True): #por algún motivo no los reconocía como float
        # Configure simulation and kite parameters
        env_state = LogProfile()
        env_state.set_reference_height(h_ref)
        env_state.set_reference_wind_speed(current_wind_speed)
        env_state.set_reference_roughness_length(h_0)
        env_state.set_altitude_ground(altitude)
        max_wind_speed_1 = current_wind_speed * np.log(altitude + rmax * np.sin(tether_angle) / h_0) / np.log(h_ref / h_0)

        cycle_settings = {
            'cycle': {
                'tether_length_start_retraction': rmax,
                'tether_length_end_retraction': rmin,
                'include_transition_energy': False,
                'elevation_angle_traction': 26.6 * np.pi / 180.,
                'traction_phase': TractionPhase,
            },
            'retraction': {
                'control': ('tether_force_ground', 900),
                'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
            },
            'transition': {
                'control': ('tether_force_ground', 900),
                'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
            },
            'traction': {
                'control': ('max_power_reeling_factor', 3069),
                'time_step': 0.01 * (rmax - rmin) / 7.3,
                'azimuth_angle': 10.6 * np.pi / 180.,
                'course_angle': 96.4 * np.pi / 180.,
                'time_step': 0.01 * (rmax - rmin) / max_wind_speed_1,
            },
        }
        cycle = Cycle(cycle_settings)

        try:
            error, time, average, traction, retraction = cycle.run_simulation(sys_props, env_state, print_summary=False)

            # Extract data_5 and store it in the dictionary
            steady_states = cycle.steady_states
            times = cycle.time
            reeling_speeds = [state.reeling_speed for state in steady_states]
            tether_force_ground = [state.tether_force_ground for state in steady_states]
            power_ground = [state.power_ground for state in steady_states]
            torques = [force * drum_radius / gearbox_ratio for force in tether_force_ground]
            omegas = [(speed / drum_radius) * gearbox_ratio for speed in reeling_speeds]

            data["reeling_speed"].append(reeling_speeds)
            data["tether_force"].append(tether_force_ground)
            data["time"].append(times)
            data["wind"].append(current_wind_speed)
            data["power"].append(power_ground)
            data["torque"].append(torques)
            data["omega"].append(omegas)
            # Calculate the mean power and add it to the dictionary
            mean_power = sum(power_ground) / len(power_ground)
            

            data["mean_power"].append(mean_power)

        except:
            pass

    return data

if __name__ == "__main__":
    app = KiteApp()