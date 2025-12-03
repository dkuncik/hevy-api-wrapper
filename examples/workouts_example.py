"""
Workout endpoint examples demonstrating all available operations.

This example shows how to:
- List workouts with pagination
- Create a new workout
- Get a specific workout by ID
- Update an existing workout
- Get workout events (changes since a timestamp)
- Get total workout count
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from hevy_api_wrapper import Client
from hevy_api_wrapper.models import (
    PostWorkoutsRequestBody,
    PostWorkoutsRequestBodyWorkout,
    PostWorkoutsRequestExercise,
    PostWorkoutsRequestSet,
)

load_dotenv()

API_KEY = os.getenv("HEVY_API_TOKEN")
if not API_KEY:
    raise ValueError("HEVY_API_TOKEN not found in environment variables")

client = Client(api_key=API_KEY)


def list_workouts_example():
    """Example: List workouts with pagination."""
    print("=== List Workouts ===")

    # Get first page with 5 workouts
    workouts = client.workouts.get_workouts(page=1, page_size=5)
    print(f"Page: {workouts.page}")
    print(f"Workouts on this page: {len(workouts.workouts)}")

    for workout in workouts.workouts:
        print(f"  - {workout.title} (ID: {workout.id})")

    print()


def create_workout_example():
    """Example: Create a new workout."""
    print("=== Create Workout ===")

    # Fetch real exercise template IDs from the API
    print("Fetching exercise templates from API...")
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=2)

    if len(templates.exercise_templates) < 2:
        raise ValueError("Need at least 2 exercise templates to create a workout")

    exercise_1 = templates.exercise_templates[0]
    exercise_2 = templates.exercise_templates[1]

    print(f"Using exercises: {exercise_1.title}, {exercise_2.title}")

    # Create workout that starts 30 minutes ago so it appears at the top
    start_time = datetime.now() - timedelta(minutes=30)
    end_time = datetime.now()

    workout_data = PostWorkoutsRequestBodyWorkout(
        title="Push Day",
        description="Chest, shoulders, and triceps workout",
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        is_private=False,
        exercises=[
            PostWorkoutsRequestExercise(
                exercise_template_id=exercise_1.id,
                superset_id=0,
                notes="Focus on form",
                sets=[
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=80.0,
                        reps=10,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=85.0,
                        reps=8,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=90.0,
                        reps=6,
                    ),
                ],
            ),
            PostWorkoutsRequestExercise(
                exercise_template_id=exercise_2.id,
                superset_id=0,
                sets=[
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=50.0,
                        reps=10,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=50.0,
                        reps=10,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=50.0,
                        reps=8,
                    ),
                ],
            ),
        ],
    )

    body = PostWorkoutsRequestBody(workout=workout_data)
    workout = client.workouts.create_workout(body)

    print(f"Created workout: {workout.title}")
    print(f"Workout ID: {workout.id}")
    print(f"Number of exercises: {len(workout.exercises)}")
    print()

    return workout.id


def get_workout_example(workout_id: str):
    """Example: Get a specific workout by ID."""
    print("=== Get Workout ===")

    workout = client.workouts.get_workout(workout_id)

    print(f"Title: {workout.title}")
    print(f"Description: {workout.description}")
    print(f"Start time: {workout.start_time}")
    print(f"End time: {workout.end_time}")
    print(f"Exercises: {len(workout.exercises)}")

    for exercise in workout.exercises:
        print(f"  - Exercise: {exercise.title}")
        print(f"    Sets: {len(exercise.sets)}")
        for set_data in exercise.sets:
            print(
                f"      {set_data.type}: {set_data.weight_kg}kg x {set_data.reps} reps"
            )

    print()


def update_workout_example(workout_id: str):
    """Example: Update an existing workout."""
    print("=== Update Workout ===")

    # First get the existing workout
    existing_workout = client.workouts.get_workout(workout_id)

    # Use the first exercise template from the existing workout
    if len(existing_workout.exercises) > 0:
        exercise_template_id = existing_workout.exercises[0].exercise_template_id
    else:
        # Fallback: fetch from API
        templates = client.exercise_templates.get_exercise_templates(
            page=1, page_size=1
        )
        exercise_template_id = templates.exercise_templates[0].id

    # Update with modified data
    start_time = datetime.now() - timedelta(minutes=30)
    end_time = datetime.now()

    updated_data = PostWorkoutsRequestBodyWorkout(
        title=existing_workout.title + " (Updated)",
        description="Updated workout description",
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        is_private=False,
        exercises=[
            PostWorkoutsRequestExercise(
                exercise_template_id=exercise_template_id,
                superset_id=0,
                notes="Increased weight!",
                sets=[
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=85.0,
                        reps=10,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=90.0,
                        reps=8,
                    ),
                    PostWorkoutsRequestSet(
                        type="normal",
                        weight_kg=95.0,
                        reps=6,
                    ),
                ],
            ),
        ],
    )

    body = PostWorkoutsRequestBody(workout=updated_data)
    workout = client.workouts.update_workout(workout_id, body)

    print(f"Updated workout: {workout.title}")
    print(f"New description: {workout.description}")
    print()


def get_workout_events_example():
    """Example: Get workout events (changes since a timestamp)."""
    print("=== Get Workout Events ===")

    # Get events since 7 days ago
    since_date = (datetime.now() - timedelta(days=7)).isoformat() + "Z"

    events = client.workouts.get_events(page=1, page_size=10, since=since_date)

    print(f"Page: {events.page} of {events.page_count}")
    print(f"Events on this page: {len(events.events)}")

    for event in events.events:
        print(f"  - Type: {event.type}")
        if event.type == "updated":
            print(f"    Workout ID: {event.workout.id}")
            print(f"    Title: {event.workout.title}")
        elif event.type == "deleted":
            print(f"    Workout ID: {event.id}")
            print(f"    Deleted at: {event.deleted_at}")

    print()


def get_workout_count_example():
    """Example: Get total workout count."""
    print("=== Get Workout Count ===")

    count = client.workouts.get_count()

    print(f"Total workouts: {count}")
    print()


def main():
    """Run all workout examples."""
    print("=" * 50)
    print("WORKOUT ENDPOINT EXAMPLES")
    print("=" * 50)
    print()

    # List workouts
    list_workouts_example()

    # Create a new workout
    workout_id = create_workout_example()

    # Get the workout we just created
    get_workout_example(workout_id)

    # Update the workout
    update_workout_example(workout_id)

    # Get workout events
    get_workout_events_example()

    # Get total workout count
    get_workout_count_example()

    print("=" * 50)
    print("All workout examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
