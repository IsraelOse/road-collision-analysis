"""
Transformer block: safety aggregations by police force.

Filters to valid-severity collisions, derives a safety score and a
multi-vehicle flag, and aggregates per police force. Also merges vehicles to
summarise driver age by force. Pure functions returning DataFrames.
"""
from __future__ import annotations
from typing import Tuple
import pandas as pd
from utils.logging_config import get_logger
logger = get_logger(__name__)

def valid_collisions(coll: pd.DataFrame) -> pd.DataFrame:
    """Keep only collisions with a valid severity and derive helper columns."""
    df = coll[coll["collision_severity"].notna()].copy()
    df["safety_score"] = 4 - df["collision_severity"]   # 1..3 -> 3..1 (higher = safer)
    df["multi_vehicle_collision"] = (df["number_of_vehicles"].fillna(0) >= 2).astype(int)
    logger.info("Valid-severity collisions: %d", len(df))
    return df

def summary_by_force(df: pd.DataFrame) -> pd.DataFrame:
    """Per-force multi-vehicle rate, collision count, and total casualties."""
    out = (df.groupby("police_force")
             .agg(Avg_Multi_Vehicle_Collision=("multi_vehicle_collision", "mean"),
                  N_Collisions=("collision_index", "nunique"),
                  Total_Casualties=("number_of_casualties", "sum"))
             .reset_index()
             .sort_values("Avg_Multi_Vehicle_Collision", ascending=False))
    return out

def driver_age_by_force(coll_valid: pd.DataFrame, veh: pd.DataFrame) -> pd.DataFrame:
    """Join vehicles to valid collisions and summarise driver age per force."""
    merged = coll_valid.merge(veh, on="collision_index", how="inner")
    out = (merged.groupby("police_force")
                 .agg(median_age_of_driver=("age_of_driver", "median"),
                      std_age_of_driver=("age_of_driver", "std"),
                      n_vehicle_rows=("collision_index", "count"),
                      n_vehicle_types=("vehicle_type", "nunique"))
                 .sort_values("median_age_of_driver", ascending=False)
                 .round(2).reset_index())
    return out
