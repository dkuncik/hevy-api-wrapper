"""API endpoint operation classes (sync and async)."""

from __future__ import annotations

from .exercise_history import ExerciseHistorySync, ExerciseHistoryAsync
from .exercise_templates import ExerciseTemplatesSync, ExerciseTemplatesAsync
from .routine_folders import RoutineFoldersSync, RoutineFoldersAsync
from .routines import RoutinesSync, RoutinesAsync
from .workouts import WorkoutsSync, WorkoutsAsync

__all__ = [
    "WorkoutsSync",
    "WorkoutsAsync",
    "RoutinesSync",
    "RoutinesAsync",
    "ExerciseTemplatesSync",
    "ExerciseTemplatesAsync",
    "RoutineFoldersSync",
    "RoutineFoldersAsync",
    "ExerciseHistorySync",
    "ExerciseHistoryAsync",
]
