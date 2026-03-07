# CIAS – Computational Index for Environmental Contamination Assessment

CIAS is a scientific web application designed to compute **heavy-metal pollution indices** for environmental samples such as **water, soil, and sediments**.

The platform provides automated calculations used in environmental monitoring and ecological risk assessment. It integrates established scientific models used in environmental chemistry and toxicology to evaluate contamination levels and potential health risks.

---

## Project Objective

Environmental contamination by heavy metals is a major global concern. Researchers typically calculate multiple indices to evaluate pollution levels and ecological risk. However, these calculations are often performed manually or with spreadsheets.

CIAS aims to provide a **programmatic and reproducible platform** for computing these indices automatically.

The system allows users to:

* input heavy metal concentrations from environmental samples
* compute pollution indices
* evaluate contamination severity
* store and retrieve analysis reports

---

## Core Features

* Heavy Metal Pollution Index (HPI) calculation
* Contamination Factor (CF) analysis
* Geoaccumulation Index (Igeo) evaluation
* Pollution Load Index (PLI) computation
* Ecological Risk Index (ERI) assessment
* Storage of environmental reports in a database
* REST API for automated environmental data analysis

---

## Scientific Background

The indices implemented in this project are widely used in environmental research to evaluate heavy-metal contamination.

The system currently supports calculations for:

### Water Quality Assessment

* Heavy Metal Pollution Index (HPI)
* Heavy Metal Evaluation Index (HEI)

### Soil Contamination Assessment

* Contamination Factor (CF)
* Geoaccumulation Index (Igeo)
* Pollution Load Index (PLI)

### Sediment Ecological Risk Assessment

* Ecological Risk Factor (Er)
* Potential Ecological Risk Index (RI)

---

## Technology Stack

Backend framework: Flask
Database: SQLAlchemy
Migration system: Flask-Migrate
API format: REST
Language: Python

---

## Running the Project

Clone the repository:

```
git clone https://github.com/Abdul1091/CIAS
cd CIAS/backend
```

Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```

```

Run the server:

```
python run.py
```

The API will start locally.

---

## Scientific References

Müller, G. (1969).
Index of geoaccumulation in sediments of the Rhine River.

Hakanson, L. (1980).
An ecological risk index for aquatic pollution control.

Prasad, B., & Bose, J. (2001).
Evaluation of heavy metal pollution index for groundwater.

United States Environmental Protection Agency (EPA).
Risk Assessment Guidance for Superfund (RAGS).

---

## Future Development

* Integration of additional pollution indices
* Visualization of environmental contamination data
* Support for environmental datasets
* Frontend dashboard for interactive analysis