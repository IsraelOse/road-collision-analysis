"""Transformer block: clean collisions and vehicles (pure functions)."""
from __future__ import annotations
import numpy as np
import pandas as pd
from utils.config import VALID_SEVERITY, INVALID_SPEED_LIMITS
from utils.logging_config import get_logger
logger = get_logger(__name__)

def clean_collisions(coll: pd.DataFrame) -> pd.DataFrame:
    """De-duplicate by collision, validate severity/speed, coerce counts."""
    df = coll.drop_duplicates(subset="collision_index", keep="first").copy()
    df["collision_severity"] = pd.to_numeric(df["collision_severity"], errors="coerce")
    df.loc[~df["collision_severity"].isin(VALID_SEVERITY), "collision_severity"] = np.nan
    if "speed_limit" in df.columns:
        df["speed_limit"] = pd.to_numeric(df["speed_limit"], errors="coerce")
        df.loc[df["speed_limit"].isin(INVALID_SPEED_LIMITS), "speed_limit"] = np.nan
    for c in ["number_of_vehicles", "number_of_casualties"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    logger.info("Cleaned collisions: %d unique rows", len(df))
    return df

def clean_vehicles(veh: pd.DataFrame) -> pd.DataFrame:
    """Coerce driver age and engine capacity, nulling negative sentinels."""
    df = veh.copy()
    if "age_of_driver" in df.columns:
        df["age_of_driver"] = pd.to_numeric(df["age_of_driver"], errors="coerce")
        df.loc[df["age_of_driver"] < 0, "age_of_driver"] = np.nan
    if "engine_capacity_cc" in df.columns:
        df["engine_capacity_cc"] = pd.to_numeric(df["engine_capacity_cc"], errors="coerce")
        df.loc[df["engine_capacity_cc"] < 0, "engine_capacity_cc"] = np.nan
    return df
