import numpy as np

class QKDDetectionSystem:
    """
    Calculates Single-Mode Fiber (SMF) overlap integral coupling efficiency,
    Quantum Bit Error Rate (QBER), and BB84 Secret Key Generation Rates.
    """
    def __init__(self, rx_aperture_diam=0.2, fiber_mode_waist=5e-6, det_eff=0.85, dark_counts=50.0):
        self.D_rx = rx_aperture_diam
        self.w_fiber = fiber_mode_waist
        self.eta_det = det_eff
        self.dark_rate = dark_counts

    def calculate_smf_coupling(self, E_rx, propagator):
        """Calculates spatial overlap integral between incoming field E_rx and LP01 fiber mode."""
        aperture_mask = (propagator.R2 <= (self.D_rx / 2.0)**2).astype(float)
        E_clipped = E_rx * aperture_mask
        E_fiber = np.exp(-propagator.R2 / (self.w_fiber**2)).astype(complex)

        numerator = np.abs(np.sum(E_clipped * np.conj(E_fiber)))**2
        denominator = np.sum(np.abs(E_clipped)**2) * np.sum(np.abs(E_fiber)**2)

        if denominator == 0:
            return 0.0
        return float(numerator / denominator)

    def compute_qkd_metrics(self, P_received_mW, pulse_rate=100e6, mu=0.1):
        """Calculates QBER and Secret Key Rate using decoy-state BB84 formalism."""
        E_photon = (6.626e-34 * 3e8) / 1550e-9
        photons_per_sec = (P_received_mW * 1e-3) / E_photon
        eta_channel = photons_per_sec / (pulse_rate * mu)
        eta_total = eta_channel * self.eta_det

        Y0 = self.dark_rate / pulse_rate
        Gain = 1.0 - np.exp(-mu * eta_total) + Y0
        
        e_opt = 0.012  # Baseline optical misalignment error (1.2%)
        QBER = (e_opt * (1.0 - np.exp(-mu * eta_total)) + 0.5 * Y0) / max(Gain, 1e-12)

        def h2(x):
            x = np.clip(x, 1e-12, 1.0 - 1e-12)
            return -x * np.log2(x) - (1.0 - x) * np.log2(1.0 - x)

        if QBER >= 0.11:  # Security threshold for BB84
            SKR = 0.0
        else:
            SKR = max(0.0, pulse_rate * 0.5 * Gain * (1.0 - 1.16 * h2(QBER) - h2(QBER)))

        return QBER, SKR
