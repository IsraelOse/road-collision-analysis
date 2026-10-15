"""Central configuration for the Road Collision safety-analysis pipeline."""
from __future__ import annotations
from pathlib import Path
ROOT: Path = Path(__file__).resolve().parents[1]
COLLISIONS_CSV: Path = ROOT / "road_collision_2023.csv"
VEHICLES_CSV: Path = ROOT / "road_vehicle_2023.csv"
OUTPUTS: Path = ROOT / "outputs"
SUMMARY_CSV: Path = OUTPUTS / "analysis_result_road_safety_by_force.csv"
VALID_SEVERITY = [1, 2, 3]          # 1=fatal, 2=serious, 3=slight
INVALID_SPEED_LIMITS = [0, 5, 150]  # implausible sentinel values
