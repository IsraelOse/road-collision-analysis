"""
Pipeline orchestration: road_safety.
data_loaders -> transformers (clean -> aggregate) -> data_exporters.
Run:  python -m pipelines.road_safety.run
"""
from __future__ import annotations
import pandas as pd
from data_loaders.collision_loader import load_data
from transformers.clean import clean_collisions, clean_vehicles
from transformers.aggregate import valid_collisions, summary_by_force, driver_age_by_force
from data_exporters.local_exporter import export_summary
from utils.logging_config import get_logger
logger = get_logger("pipelines.road_safety")

def run() -> pd.DataFrame:
    logger.info("=== road_safety pipeline start ===")
    coll, veh = load_data()
    coll = clean_collisions(coll); veh = clean_vehicles(veh)
    valid = valid_collisions(coll)
    summary = summary_by_force(valid)
    driver_age = driver_age_by_force(valid, veh)
    export_summary(summary, driver_age)
    logger.info("=== complete: %d forces, %d total casualties ===",
                len(summary), int(summary["Total_Casualties"].sum()))
    return summary

if __name__ == "__main__":
    print(run().round(4).head(10).to_string(index=False))
