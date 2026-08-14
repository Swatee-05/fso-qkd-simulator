import numpy as np

class WaveOpticsPropagator:
    """
    2D spatial grid generation, TEM00 Gaussian field initialization,
    and Fresnel diffraction via the Angular Spectrum Method (FFT).
    """
    def __init__(self, N=256, L_grid=0.5, wavelength=1550e-9, w0=0.025):
        self.N = N                      # Grid dimensions (N x N points)
        self.L_grid = L_grid            # Physical width of spatial grid (meters)
        self.lam = wavelength          # Wavelength (m)
        self.k = 2 * np.pi / self.lam  # Wave number (rad/m)
        self.w0 = w0                   # Transmit waist radius (m)
        self.z_R = np.pi * (w0**2) / self.lam  # Rayleigh range (m)

        # Spatial Coordinates (x, y)
        dx = L_grid / N
        self.x = np.linspace(-L_grid/2, L_grid/2 - dx, N)
        self.y = np.linspace(-L_grid/2, L_grid/2 - dx, N)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        self.R2 = self.X**2 + self.Y**2

        # Spatial Frequency Coordinates (kx, ky) for FFT Transfer Function
        dk = 2 * np.pi / L_grid
        kx = np.fft.fftfreq(N, d=dx) * 2 * np.pi
        self.KX, self.KY = np.meshgrid(np.fft.fftshift(kx), np.fft.fftshift(kx))
        self.K2 = self.KX**2 + self.KY**2

    def get_initial_field(self, P_mW=10.0):
        """Generates a TEM00 Gaussian beam complex field E(x, y, 0)."""
        E0 = np.sqrt(2 * (P_mW * 1e-3) / (np.pi * self.w0**2))
        field = E0 * np.exp(-self.R2 / (self.w0**2)).astype(complex)
        return field

    def propagate_free_space(self, field, z):
        """Propagates complex field over distance z using Angular Spectrum Method (FFT)."""
        # Paraxial transfer function H(kx, ky) = exp(-i * z * (kx^2 + ky^2) / 2k)
        H = np.exp(-1j * z * self.K2 / (2 * self.k))
        
        field_k = np.fft.fftshift(np.fft.fft2(field))
        field_k_propagated = field_k * H
        field_out = np.fft.ifft2(np.fft.ifftshift(field_k_propagated))
        return field_out
