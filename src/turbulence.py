import numpy as np

class AtmosphericTurbulence:
    """
    Models Kolmogorov spatial turbulence spectrum using FFT Phase Screens
    and evaluates Fried Parameter (r0), Rytov Variance, and Beer-Lambert attenuation.
    """
    def __init__(self, Cn2=3e-14, alpha_dB_km=0.5):
        self.Cn2 = Cn2                  # Refractive Index Structure Parameter (m^-2/3)
        self.alpha_dB = alpha_dB_km     # Attenuation coefficient (dB/km)

    def fried_parameter(self, k, z):
        """Calculates Fried Parameter r0 (transverse coherence length)."""
        return (0.423 * (k**2) * self.Cn2 * z)**(-3/5)

    def generate_phase_screen(self, propagator, z):
        """Generates a 2D random phase screen phi(x,y) using Kolmogorov PSD."""
        r0 = self.fried_parameter(propagator.k, z)
        K = np.sqrt(propagator.K2)
        K[propagator.N // 2, propagator.N // 2] = 1e-10  # Prevent division by zero at DC

        # Kolmogorov Power Spectral Density: Phi_n(K) = 0.023 * r0^(-5/3) * K^(-11/3)
        PSD = 0.023 * (r0**(-5/3)) * (K**(-11/3))
        PSD[propagator.N // 2, propagator.N // 2] = 0.0

        # Complex Gaussian Random Draw
        white_noise = (np.random.normal(0, 1, (propagator.N, propagator.N)) + 
                       1j * np.random.normal(0, 1, (propagator.N, propagator.N))) / np.sqrt(2)
        
        phase_screen_fourier = white_noise * np.sqrt(PSD) * (2 * np.pi / propagator.L_grid)
        phase_screen = np.real(np.fft.ifft2(np.fft.ifftshift(phase_screen_fourier))) * (propagator.N**2)
        return phase_screen
