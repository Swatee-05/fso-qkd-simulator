import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add src to python path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.wave_optics import WaveOpticsPropagator
from src.turbulence import AtmosphericTurbulence
from src.pat_system import PATSystem
from src.qkd_metrics import QKDDetectionSystem

if __name__ == "__main__":
    print("Running Wave-Optics FSO-QKD Simulation...")

    z_link = 5000.0  # 5 km link
    N_grid = 256
    L_grid = 0.4     # 40 cm window

    prop = WaveOpticsPropagator(N=N_grid, L_grid=L_grid, wavelength=1550e-9, w0=0.03)
    turb = AtmosphericTurbulence(Cn2=2e-14, alpha_dB_km=0.8)
    pat = PATSystem(jitter_std_urad=12.0)
    qkd = QKDDetectionSystem(rx_aperture_diam=0.25)

    E_in = prop.get_initial_field(P_mW=10.0)
    E_free = prop.propagate_free_space(E_in, z_link)
    phase_screen = turb.generate_phase_screen(prop, z_link)
    E_turbulent = E_free * np.exp(1j * phase_screen)

    time_steps = np.linspace(0, 0.5, 200)
    state_x, state_y = [0.0, 0.0], [0.0, 0.0]
    uncompensated_jitter_x = np.random.normal(0, pat.jitter_std, len(time_steps))
    
    pat_errors_x, coupling_efficiencies, qber_list, skr_list = [], [], [], []

    for jitter_x in uncompensated_jitter_x:
        shift_pixels = int(jitter_x * z_link / (L_grid / N_grid))
        E_jittered = np.roll(E_turbulent, shift_pixels, axis=1)
        I_jittered = np.abs(E_jittered)**2

        dx, dy = pat.compute_qpd_centroid(I_jittered, prop.X, prop.Y)
        u_x, u_y, state_x, state_y = pat.run_pid_step(dx, dy, state_x, state_y)
        residual_error = jitter_x - (u_x * 1e-4)
        pat_errors_x.append(residual_error * 1e6)

        eta_smf = qkd.calculate_smf_coupling(E_jittered, prop)
        coupling_efficiencies.append(eta_smf)

        loss_atten = 10**(-(turb.alpha_dB * (z_link / 1000.0)) / 10.0)
        P_rx = 10.0 * loss_atten * eta_smf

        qber, skr = qkd.compute_qkd_metrics(P_rx)
        qber_list.append(qber * 100)
        skr_list.append(skr / 1000)

    print("\n=== SIMULATION COMPLETE ===")
    print(f"Mean Coupling Efficiency into SMF: {np.mean(coupling_efficiencies)*100:.2f}%")
    print(f"Mean Quantum Bit Error Rate (QBER): {np.mean(qber_list):.2f}%")
    print(f"Mean Secret Key Rate (SKR): {np.mean(skr_series if 'skr_series' in locals() else skr_list):.2f} kbps")
