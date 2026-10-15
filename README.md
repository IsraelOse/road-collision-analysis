# Road Collision Analysis (2023)

A data-processing pipeline over **2023 road-collision and vehicle records** that cleans, joins, and aggregates road-safety metrics per police force. Delivered as a **modular, production-style pipeline** with a companion analysis notebook.

## What it does
- Cleans collisions (de-duplicate by collision, validate severity to {fatal, serious, slight}, null implausible speed limits, coerce counts) and vehicles (null negative driver-age / engine sentinels).
- Derives a safety score and a multi-vehicle-collision flag.
- Aggregates per police force: multi-vehicle collision rate, collision count, total casualties.
- Joins vehicles to collisions to summarise driver age by force.

## Repository architecture
Decoupled, block-based; type hints and `logging` throughout.

```
.
├── data_loaders/        # Read collision + vehicle CSVs
│   └── collision_loader.py
├── transformers/        # clean + aggregate (pure functions)
│   ├── clean.py
│   └── aggregate.py
├── data_exporters/      # Write the by-force summary tables
│   └── local_exporter.py
├── utils/               # Shared config + logging
├── pipelines/
│   └── road_safety/     # run.py + metadata.yaml + requirements.txt
├── road_collision_analysis.ipynb   # Full EDA notebook
├── road_collision_2023.csv         # Collision records
├── road_vehicle_2023.csv           # Vehicle records
└── outputs/                         # Generated summary tables
```

## Run it
```bash
pip install -r pipelines/road_safety/requirements.txt
python -m pipelines.road_safety.run
```

## Verified
The pipeline reproduces the reference summary **exactly**: 44 police forces with identical multi-vehicle rates, collision counts, and total casualties (8,000 unique collisions, 10,269 casualties).

## Tech
Python · pandas · NumPy

*Project from the Master of Data Analytics program, University of Niagara Falls Canada.*
