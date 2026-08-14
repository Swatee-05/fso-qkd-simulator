import numpy as np

class PATSystem:
    """
    Models Quadrant Photodiode (QPD) spatial beam centroid sensing, 
    angular pointing jitter, and Fast Steering Mirror (FSM) PID control.
    """
    def __init__(self, jitter_std_urad=10.0, Kp=0.55, Ki=0.08, Kd=0.02):
        self.jitter_std = jitter_std_urad * 1e-6  # Convert urad to radians
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd

    def compute_qpd_centroid(self, intensity, X, Y):
        """Calculates normalized beam centroid displacement (dx, dy) on a QPD."""
        total_intensity = np.sum(intensity)
        if total_intensity == 0:
            return 0.0, 0.0
        
        q_right = np.sum(intensity[X > 0])
        q_left  = np.sum(intensity[X < 0])
        q_top   = np.sum(intensity[Y > 0])
        q_bot   = np.sum(intensity[Y < 0])
        
        delta_x = (q_right - q_left) / total_intensity
        delta_y = (q_top - q_bot) / total_intensity
        return delta_x, delta_y

    def run_pid_step(self, error_x, error_y, state_x, state_y, dt=0.001):
        """Executes a discrete time-step PID correction for X and Y tracking axes."""
        ix, px = state_x[0], state_x[1]
        iy, py = state_y[0], state_y[1]

        # PID Controller X-axis
        ix += error_x * dt
        dx = (error_x - px) / dt
        u_x = self.Kp * error_x + self.Ki * ix + self.Kd * dx

        # PID Controller Y-axis
        iy += error_y * dt
        dy = (error_y - py) / dt
        u_y = self.Kp * error_y + self.Ki * iy + self.Kd * dy

        return u_x, u_y, [ix, error_x], [iy, error_y]
