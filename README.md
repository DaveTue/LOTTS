# OrchTwin Digital Twin Service

## Overview

This project implements the **OrchTwin approach** to generate a **digital twin service** by transforming high-level orchestration models directly into executable code. 

It leverages a domain-specific language called **LOTTS** (*Language for Orchestrating Tools for Twinning Services*), defined using the **Rascal metamodeling language**. 

From a LOTTS specification (an OrchTwin model), this project automatically generates **Python code** that implements a complete digital twin service, integrating:

- **Co-simulation models** (FMUs, MATLAB/Simulink, Python models)
- **Sensors, actuators, databases, and UX interfaces** via TCP-IP
- **Explicit orchestration of execution logic and data exchange** between all components

The approach is designed to facilitate the **fast creation of modular, composable, and orchestrated digital twins**.

---

## Features

✅ Transform LOTTS models (written in Rascal) into Python implementations  
✅ Supports:
- FMU co-simulation
- Python-based models
- MATLAB/Simulink models (via MATLAB Engine for Python)
- Real-time sensor/actuator integration via TCP-IP
- Databases and user interfaces

✅ Explicit execution scheduling and data orchestration  
✅ Modular and extensible architecture

---

## Requirements

### Versions used

- **Python**: `3.11`  
- **MATLAB**: `2022b`

### Rascal

- Install **Rascal metamodeling language**  
  See: [https://www.rascal-mpl.org](https://www.rascal-mpl.org)

### Python packages

- `logging`, `os`, `queue`, `collections`, `networkx`, `matplotlib`, `threading`

You can install these via pip:

```bash
pip install networkx matplotlib
```

(Others like `logging`, `os`, `queue`, `collections`, `threading` are part of the Python standard library.)

### MATLAB Engine for Python

- Required to interface MATLAB/Simulink models.  
  Installation instructions:  
  [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)

---

## Getting Started

1. **Model your digital twin service** using the LOTTS language.  
   For example, describe your sensors, models, transformations, and execution flows.

2. **Run the Rascal transformation** to generate the Python code:

```bash
rascal
```
then in the Rascal console:

```rascal
import GeneratePythonFromDSL;
main();
```

3. **Run the generated Python code** to launch your orchestrated digital twin.

---

## Repository structure

```
.
├── src/
│   ├── API/               # Interfaces for FMU, MATLAB, Python models
├── sensors/
│   └── emmulated data use as sensor 
├── springExam.ipynb/   # example of working digitltwin of a RiceCooker
├── suppot_files/
│   └── files that supports the interface generation for simulink models
├── Models/
│   └── All models of simulation    
├── LOTTS/
│   └── Files of Rascal for LOTTS
└── README.md
```

---