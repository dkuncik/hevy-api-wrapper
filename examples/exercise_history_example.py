"""
Exercise History endpoint examples demonstrating all available operations.

This example shows how to:
- Get exercise history for a specific exercise
- Filter exercise history by date range
- Analyze progress over time
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from hevy_api_wrapper import Client

load_dotenv()

API_KEY = os.getenv("HEVY_API_TOKEN")
if not API_KEY:
    raise ValueError("HEVY_API_TOKEN not found in environment variables")

client = Client(api_key=API_KEY)


def get_exercise_history_example(exercise_template_id: str):
    """Example: Get all exercise history for a specific exercise."""
    print("=== Get Exercise History (All Time) ===")

    history = client.exercise_history.get_exercise_history(exercise_template_id)

    print(f"Exercise Template ID: {exercise_template_id}")
    print(f"Total history entries: {len(history.exercise_history)}")

    if history.exercise_history:
        print("\nRecent entries (each entry is one set):")
        for entry in history.exercise_history[:10]:  # Show first 10 sets
            print(f"  - Workout: {entry.workout_title}")
            print(f"    Date: {entry.workout_start_time}")
            print(f"    Set type: {entry.set_type}")
            if entry.weight_kg:
                print(f"    Weight: {entry.weight_kg}kg x {entry.reps} reps")
            elif entry.distance_meters:
                print(f"    Distance: {entry.distance_meters}m in {entry.duration_seconds}s")
            elif entry.duration_seconds:
                print(f"    Duration: {entry.duration_seconds}s")

    print()


def get_exercise_history_with_date_range_example(exercise_template_id: str):
    """Example: Get exercise history filtered by date range."""
    print("=== Get Exercise History (Date Range) ===")

    # Get history for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    history = client.exercise_history.get_exercise_history(
        exercise_template_id,
        start_date=start_date.isoformat() + "Z",
        end_date=end_date.isoformat() + "Z",
    )

    print(f"Exercise Template ID: {exercise_template_id}")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print(f"History entries in range: {len(history.exercise_history)}")

    if history.exercise_history:
        # Group by workout to find max weight per workout
        workouts = {}
        for entry in history.exercise_history:
            if entry.workout_id not in workouts:
                workouts[entry.workout_id] = {
                    "title": entry.workout_title,
                    "date": entry.workout_start_time,
                    "max_weight": 0,
                }
            if entry.weight_kg:
                workouts[entry.workout_id]["max_weight"] = max(
                    workouts[entry.workout_id]["max_weight"], entry.weight_kg
                )

        print("\nWorkouts in range:")
        for workout_id, data in workouts.items():
            print(f"  - {data['title']} ({data['date']})")
            if data["max_weight"] > 0:
                print(f"    Max weight: {data['max_weight']}kg")

    print()


def analyze_progress_example(exercise_template_id: str):
    """Example: Analyze progress over time."""
    print("=== Analyze Progress ===")

    history = client.exercise_history.get_exercise_history(exercise_template_id)

    if not history.exercise_history:
        print("No history data available for analysis.")
        print()
        return

    # Count unique workouts
    unique_workouts = set(entry.workout_id for entry in history.exercise_history)

    print(f"Exercise Template ID: {exercise_template_id}")
    print(f"Total workouts: {len(unique_workouts)}")
    print(f"Total sets: {len(history.exercise_history)}")

    # Calculate statistics on sets with weight
    weight_sets = [entry for entry in history.exercise_history if entry.weight_kg]

    if weight_sets:
        # Max weight ever lifted
        max_weight = max(entry.weight_kg for entry in weight_sets)
        print(f"Max weight ever: {max_weight}kg")

        # Average weight across all sets
        avg_weight = sum(entry.weight_kg for entry in weight_sets) / len(weight_sets)
        print(f"Average weight: {avg_weight:.1f}kg")

        # Total volume (weight × reps)
        total_volume = sum((entry.weight_kg or 0) * (entry.reps or 0) for entry in history.exercise_history)
        print(f"Total volume: {total_volume:,.0f}kg")

        # Average sets per workout
        avg_sets = len(history.exercise_history) / len(unique_workouts)
        print(f"Average sets per workout: {avg_sets:.1f}")

    print()


def compare_recent_performance_example(exercise_template_id: str):
    """Example: Compare recent performance to previous months."""
    print("=== Compare Recent Performance ===")

    # Get last 60 days of history
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    history = client.exercise_history.get_exercise_history(
        exercise_template_id,
        start_date=start_date.isoformat() + "Z",
        end_date=end_date.isoformat() + "Z",
    )

    if not history.exercise_history:
        print("No history data available for comparison.")
        print()
        return

    print(f"Exercise Template ID: {exercise_template_id}")

    # Split into two periods: last 30 days and previous 30 days
    cutoff_date = end_date - timedelta(days=30)
    # Make cutoff_date timezone-aware to match entry_date
    cutoff_date = cutoff_date.replace(tzinfo=datetime.now().astimezone().tzinfo)

    recent_entries = []
    previous_entries = []

    for entry in history.exercise_history:
        entry_date = datetime.fromisoformat(entry.workout_start_time.replace("Z", "+00:00"))
        if entry_date >= cutoff_date:
            recent_entries.append(entry)
        else:
            previous_entries.append(entry)

    # Count unique workouts in each period
    recent_workouts = set(entry.workout_id for entry in recent_entries)
    previous_workouts = set(entry.workout_id for entry in previous_entries)

    print(f"Recent period (last 30 days): {len(recent_workouts)} workouts, {len(recent_entries)} sets")
    print(f"Previous period (30-60 days ago): {len(previous_workouts)} workouts, {len(previous_entries)} sets")

    # Calculate average max weight per workout for each period
    def get_avg_max_weight_per_workout(entries):
        workout_max_weights = {}
        for entry in entries:
            if entry.weight_kg:
                if entry.workout_id not in workout_max_weights:
                    workout_max_weights[entry.workout_id] = entry.weight_kg
                else:
                    workout_max_weights[entry.workout_id] = max(workout_max_weights[entry.workout_id], entry.weight_kg)
        return sum(workout_max_weights.values()) / len(workout_max_weights) if workout_max_weights else 0

    recent_avg_max = get_avg_max_weight_per_workout(recent_entries)
    previous_avg_max = get_avg_max_weight_per_workout(previous_entries)

    print(f"\nAverage max weight per workout:")
    print(f"  Recent: {recent_avg_max:.1f}kg")
    print(f"  Previous: {previous_avg_max:.1f}kg")

    if previous_avg_max > 0:
        improvement = ((recent_avg_max - previous_avg_max) / previous_avg_max) * 100
        print(f"  Change: {improvement:+.1f}%")

    print()


def find_popular_exercises_example():
    """Example: Find which exercises have the most history (most frequently performed)."""
    print("=== Find Popular Exercises ===")

    # Get some exercise templates
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=20)

    exercise_frequency = []

    print("Analyzing exercise frequency...")
    for template in templates.exercise_templates[:10]:  # Check first 10
        try:
            history = client.exercise_history.get_exercise_history(template.id)
            # Count unique workouts
            unique_workouts = set(entry.workout_id for entry in history.exercise_history)
            if len(unique_workouts) > 0:
                exercise_frequency.append(
                    (
                        template.title,
                        len(unique_workouts),
                        len(history.exercise_history),
                    )
                )
        except Exception:
            # Skip exercises that have no history or error
            pass

    # Sort by frequency (workouts)
    exercise_frequency.sort(key=lambda x: x[1], reverse=True)

    print(f"\nMost frequently performed exercises:")
    for title, workout_count, set_count in exercise_frequency[:5]:
        print(f"  - {title}: {workout_count} workouts ({set_count} total sets)")

    print()


def main():
    """Run all exercise history examples."""
    print("=" * 50)
    print("EXERCISE HISTORY ENDPOINT EXAMPLES")
    print("=" * 50)
    print()

    # First, get an exercise template ID to use for examples
    print("Finding an exercise with history...")
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=10)

    # Try to find an exercise with history
    exercise_id = None
    for template in templates.exercise_templates:
        try:
            history = client.exercise_history.get_exercise_history(template.id)
            if len(history.exercise_history) > 0:
                exercise_id = template.id
                print(f"Using exercise: {template.title} (ID: {exercise_id})")
                print()
                break
        except Exception:
            pass

    if not exercise_id:
        print("No exercises with history found. Please log some workouts first!")
        print("Using 'bench_press' as example ID (may not have data).")
        exercise_id = "bench_press"
        print()

    # Get all-time history
    get_exercise_history_example(exercise_id)

    # Get history with date range
    get_exercise_history_with_date_range_example(exercise_id)

    # Analyze progress
    analyze_progress_example(exercise_id)

    # Compare recent performance
    compare_recent_performance_example(exercise_id)

    # Find popular exercises
    find_popular_exercises_example()

    print("=" * 50)
    print("All exercise history examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
