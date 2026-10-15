"""Data exporter block: write the safety summary tables."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from utils.config import OUTPUTS, SUMMARY_CSV
from utils.logging_config import get_logger
logger = get_logger(__name__)

def export_summary(summary: pd.DataFrame, driver_age: pd.DataFrame) -> Path:
    """Write the by-force safety summary and the driver-age-by-force table."""
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUMMARY_CSV, index=False)
    driver_age.to_csv(OUTPUTS / "driver_age_by_force.csv", index=False)
    logger.info("Wrote %s (%d forces)", SUMMARY_CSV.name, len(summary))
    return SUMMARY_CSV
