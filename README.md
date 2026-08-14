# fso-qkd-simulator
Wave-optics simulation framework for Free-Space Optical Quantum Key Distribution (FSO-QKD) links, incorporating 2D FFT propagation, Kolmogorov phase screens, and closed-loop PAT tracking.
# Numerical Modeling and PAT Simulation of an Atmospheric Free-Space Optical (FSO) Link for QKD

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end wave-optics and atmospheric turbulence simulation framework built in Python to evaluate the performance of Free-Space Quantum Key Distribution (FSO-QKD) links.

This pipeline models 2D spatial Gaussian beam propagation using the Angular Spectrum Method (FFT), atmospheric wavefront aberrations via Kolmogorov turbulence phase screens, Quadrant Photodiode (QPD) spatial centroid tracking using closed-loop PID control, and Single-Mode Fiber (SMF) overlap coupling for BB84 secret key rate analysis.

---

## Technical Architecture

```
[2D Wave-Optics Engine] ➔ [Kolmogorov Phase Screen] ➔ [PAT System (QPD + PID)] ➔ [SMF Overlap & QKD Engine]
   (FFT Propagation)       (Turbulence Distortion)     (Centroid Feedback)       (QBER & Secret Key)
```

### Key Physical Features
* **Wave Optics Propagation:** Solves the Paraxial Wave Equation in 2D using Angular Spectrum Method FFTs (`src/wave_optics.py`).
* **Atmospheric Physics:** Generates dynamic Kolmogorov spatial phase screens driven by $C_n^2$ and Fried Parameter $r_0$ (`src/turbulence.py`).
* **Closed-Loop PAT Tracking:** Simulates Quadrant Photodiode (QPD) spatial integration and Fast Steering Mirror (FSM) PID loop feedback to mitigate micro-radian angular jitter (`src/pat_system.py`).
* **Quantum Detection Performance:** Computes Single-Mode Fiber (SMF) spatial overlap integrals to quantify QBER spikes and Decoy-State BB84 secret key generation bounds (`src/qkd_metrics.py`).

---

## Mathematical Formulation

### 1. Fresnel Wave Propagation (Angular Spectrum Method)
The complex electric field $E(x,y,z)$ propagates through free space via the spatial frequency transfer function:

$$E(x, y, z) = \mathcal{F}^{-1} \left\{ \mathcal{F}\{E(x,y,0)\} \cdot \exp\left(-i z \frac{k_x^2 + k_y^2}{2k}\right) \right\}$$

### 2. Single-Mode Fiber Overlap Integral
The spatial coupling efficiency $\eta_{\text{smf}}$ into the receiving single-mode fiber is derived from the complex overlap integral:

$$\eta_{\text{smf}} = \frac{\left| \iint_{\text{Aperture}} E_{\text{rx}}(x,y) \cdot E_{\text{fiber}}^*(x,y) \, dx \, dy \right|^2}{\iint_{\text{Aperture}} |E_{\text{rx}}(x,y)|^2 \, dx \, dy \cdot \iint |E_{\text{fiber}}(x,y)|^2 \, dx \, dy}$$

---

## Repository Structure

```text
fso-qkd-simulator/
│
├── README.md                  <-- Project Overview & Math Models
├── requirements.txt           <-- Python dependencies
├── LICENSE                    <-- MIT License
├── .gitignore                 <-- Python build exclusion rules
│
├── src/                       <-- Core Physics & System Modules
│   ├── __init__.py
│   ├── wave_optics.py         <-- 2D FFT Propagation Engine
│   ├── turbulence.py          <-- Kolmogorov Phase Screen Generator
│   ├── pat_system.py          <-- QPD Centroid & PID Tracking
│   └── qkd_metrics.py         <-- SMF Overlap Integral & QBER Analysis
│
└── examples/
    └── run_simulation.py      <-- Main Pipeline Executable
```

---

## Quick Start

### Installation
```bash
git clone [https://github.com/Swatee-05/fso-qkd-simulator.git](https://github.com/Swatee-05/fso-qkd-simulator.git)
cd fso-qkd-simulator
pip install -r requirements.txt
```

### Run Simulation
```bash
python examples/run_simulation.py
```

---

## Author
**Sushree Swateeprajnya Behera**  
Experimental Quantum Hardware Researcher  
[LinkedIn](https://www.linkedin.com/in/sushree-swateeprajnya-behera) | [Email](mailto:sushreeswateeprajnyabehera@gmail.com)
