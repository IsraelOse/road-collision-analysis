"""Data loader block: read the collision and vehicle CSVs."""
from __future__ import annotations
from pathlib import Path
from typing import Tuple
import pandas as pd
from utils.config import COLLISIONS_CSV, VEHICLES_CSV
from utils.logging_config import get_logger
logger = get_logger(__name__)

def load_data(coll_path: Path = COLLISIONS_CSV,
              veh_path: Path = VEHICLES_CSV) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return (collisions, vehicles) DataFrames."""
    coll = pd.read_csv(coll_path)
    veh = pd.read_csv(veh_path)
    logger.info("Loaded collisions %s and vehicles %s", coll.shape, veh.shape)
    return coll, veh
