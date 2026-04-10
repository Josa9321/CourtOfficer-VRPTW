# Court Officer Routing System

Optimizing judicial efficiency through mathematical programming and real-time geospatial data.

---

## Overview

The Court Officer Routing System is a specialized tool built to optimize the weekly schedule of a **Court Officer** (*Oficial de Justiça*). It models the problem as a **Vehicle Routing Problem with Time Windows (VRPTW)**, ensuring that judicial mandates are served not only via the shortest path, but strictly within each mandate's required time window.

> **Note:** The system currently supports up to **25 geographical points** per optimization run.

---

## Features

- **VRPTW Optimization** — A Mixed Integer Linear Programming model that enforces time constraints for every delivery and visit.
- **Real-World Traffic Data** — Integrates with the Google Routes API to fetch accurate travel durations and distances based on real-time traffic conditions.
- **Automated Scheduling** — Produces a structured document detailing the full optimized daily agenda for the week.
- **Smart Navigation Links** — Generates Google Maps URLs for every route. To work around Google's waypoint limit, long routes are automatically split into sequential links of up to 10 points each, ensuring seamless turn-by-turn navigation.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| Optimization | [Pyomo](http://www.pyomo.org/) (MILP) |
| External APIs | Google Routes API |

---

## How It Works

```
Addresses & Time Windows & Service Time
        │
        ▼
  Google Routes API
  (Distance & Time Matrix)
        │
        ▼
  Pyomo MILP Solver
  (Minimize total travel time)
        │
        ▼
  Weekly Report + Google Maps Links
```

1. **Input** — Provide a list of up to **25 geographical points** (judicial mandates) along with their required time windows.
2. **Geocoding & Matrix** — The system queries the Google Routes API to build a complete distance and travel-time matrix between all points.
3. **Optimization** — The Pyomo model applies MILP constraints to find the globally optimal schedule that minimizes total travel time while respecting every time window.
4. **Output** — A structured weekly report is generated, complete with sequential Google Maps navigation links ready for field use.

---

## Getting Started

### Prerequisites

- Python 3.x
- A valid **Google Routes API** key
- A supported MILP solver (e.g., [HiGHS](https://highs.dev/), [CPLEX](https://www.ibm.com/br-pt/products/ilog-cplex-optimization-studio), or [Gurobi](https://www.gurobi.com/))

### Installation

```bash
git clone https://github.com/Josa9321/CourtOfficer-VRPTW
cd CourtOfficer-VRPTW
pip install -r requirements.txt
```

### Configuration

Create a file named `.api` in the project root directory containing your Google Routes API key:
```
your_api_key_here
```

### Usage

Run the solver from the terminal, passing a JSON instance file as argument. A solution file prefixed with `solution_` will be generated in the same directory.

```bash
python run.py instance.json  # generates solution_instance.json
```

<!-- --- -->
<!---->
<!-- ## License -->
<!---->
<!-- This project is licensed under the [MIT License](LICENSE). -->
<!---->
