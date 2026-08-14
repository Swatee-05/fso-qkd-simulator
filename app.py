import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from src.wave_optics import WaveOpticsPropagator
from src.turbulence import AtmosphericTurbulence
from src.pat_system import PATSystem
from src.qkd_metrics import QKDDetectionSystem

st.set_page_config(page_title="FSO-QKD Simulator", layout="wide")

st.title("⚡ Free-Space Optical QKD Link Simulator")
st.markdown("Interactive wave-optics and atmospheric turbulence model for quantum key distribution.")

# Sidebar Controls
st.sidebar.header("Simulation Parameters")
z_link = st.sidebar.slider("Link Distance (m)", 500, 10000, 5000, 500)
Cn2 = st.sidebar.select_slider("Turbulence Structure (Cn2)", 
                                options=[1e-16, 1e-15, 1e-14, 5e-14, 1e-13], 
                                value=1e-14, 
                                format_func=lambda x: f"{x:.1e} m^-2/3")
rx_diam = st.sidebar.slider("Receiver Aperture Diameter (m)", 0.05, 0.50, 0.20, 0.05)

if st.button("🚀 Run Simulation"):
    with st.spinner("Propagating wave field and simulating PAT tracking..."):
        prop = WaveOpticsPropagator(N=256, L_grid=0.4, wavelength=1550e-9, w0=0.03)
        turb = AtmosphericTurbulence(Cn2=Cn2, alpha_dB_km=0.8)
        pat = PATSystem(jitter_std_urad=12.0)
        qkd = QKDDetectionSystem(rx_aperture_diam=rx_diam)

        E_in = prop.get_initial_field(P_mW=10.0)
        E_free = prop.propagate_free_space(E_in, z_link)
        phase_screen = turb.generate_phase_screen(prop, z_link)
        E_turbulent = E_free * np.exp(1j * phase_screen)

        # Plotting
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # Intensity plot
        im0 = axes[0].imshow(np.abs(E_turbulent)**2, extent=[-0.2, 0.2, -0.2, 0.2], cmap='inferno')
        axes[0].set_title("Received Optical Irradiance Profile")
        axes[0].set_xlabel("x (m)")
        axes[0].set_ylabel("y (m)")
        fig.colorbar(im0, ax=axes[0])

        # Phase plot
        im1 = axes[1].imshow(phase_screen, extent=[-0.2, 0.2, -0.2, 0.2], cmap='twilight')
        axes[1].set_title("Atmospheric Phase Distortion (Kolmogorov)")
        axes[1].set_xlabel("x (m)")
        fig.colorbar(im1, ax=axes[1])

        st.pyplot(fig)

        # Calculate metrics
        eta_smf = qkd.calculate_smf_coupling(E_turbulent, prop)
        loss_atten = 10**(-(turb.alpha_dB * (z_link / 1000.0)) / 10.0)
        P_rx = 10.0 * loss_atten * eta_smf
        qber, skr = qkd.compute_qkd_metrics(P_rx)

        col1, col2, col3 = st.columns(3)
        col1.metric("SMF Coupling Efficiency", f"{eta_smf*100:.2f} %")
        col2.metric("Quantum Bit Error Rate (QBER)", f"{qber*100:.2f} %")
        col3.metric("Secret Key Rate (SKR)", f"{skr/1000:.2f} kbps")
