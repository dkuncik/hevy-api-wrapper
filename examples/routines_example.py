"""
Routine and Routine Folder endpoint examples demonstrating all available operations.

This example shows how to:
- List routines with pagination
- Create a new routine
- Get a specific routine by ID
- Update an existing routine
- List routine folders with pagination
- Create a new routine folder
- Get a specific routine folder by ID
"""

import os

from dotenv import load_dotenv

from hevy_api_wrapper import Client
from hevy_api_wrapper.models import (
    PostRoutinesRequestBody,
    PostRoutinesRequestBodyRoutine,
    PostRoutinesRequestExercise,
    PostRoutinesRequestSet,
    PutRoutinesRequestBody,
    PutRoutinesRequestBodyRoutine,
    PutRoutinesRequestExercise,
    PutRoutinesRequestSet,
    PostRoutineFolderRequestBody,
    RepRange,
)

load_dotenv()

API_KEY = os.getenv("HEVY_API_TOKEN")
if not API_KEY:
    raise ValueError("HEVY_API_TOKEN not found in environment variables")

client = Client(api_key=API_KEY)


def list_routines_example():
    """Example: List routines with pagination."""
    print("=== List Routines ===")

    # Get first page with 5 routines
    routines = client.routines.get_routines(page=1, page_size=5)
    print(f"Page: {routines.page}")
    print(f"Total pages: {routines.page_count}")
    print(f"Routines on this page: {len(routines.routines)}")

    for routine in routines.routines:
        print(f"  - {routine.title} (ID: {routine.id})")
        if routine.folder_id:
            print(f"    Folder ID: {routine.folder_id}")

    print()


def create_routine_example():
    """Example: Create a new routine."""
    print("=== Create Routine ===")

    # Fetch real exercise template IDs from the API
    print("Fetching exercise templates from API...")
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=3)

    if len(templates.exercise_templates) < 3:
        raise ValueError("Need at least 3 exercise templates to create a routine")

    # Use the first 3 exercise templates
    exercise_1 = templates.exercise_templates[0]
    exercise_2 = templates.exercise_templates[1]
    exercise_3 = templates.exercise_templates[2]

    print(f"Using exercises: {exercise_1.title}, {exercise_2.title}, {exercise_3.title}")

    routine_data = PostRoutinesRequestBodyRoutine(
        title="Full Body Workout",
        exercises=[
            PostRoutinesRequestExercise(
                exercise_template_id=exercise_1.id,
                superset_id=0,
                notes="Keep chest up and core tight",
                sets=[
                    PostRoutinesRequestSet(
                        type="warmup",
                        weight_kg=60.0,
                        reps=10,
                        rep_range=RepRange(start=10, end=10),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=100.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=100.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=100.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                ],
            ),
            PostRoutinesRequestExercise(
                exercise_template_id=exercise_2.id,
                superset_id=0,
                notes="Control the descent",
                sets=[
                    PostRoutinesRequestSet(
                        type="warmup",
                        weight_kg=40.0,
                        reps=10,
                        rep_range=RepRange(start=10, end=10),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=80.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=80.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=80.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                ],
            ),
            PostRoutinesRequestExercise(
                exercise_template_id=exercise_3.id,
                superset_id=0,
                sets=[
                    PostRoutinesRequestSet(
                        type="warmup",
                        weight_kg=80.0,
                        reps=5,
                        rep_range=RepRange(start=5, end=5),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=140.0,
                        reps=5,
                        rep_range=RepRange(start=5, end=5),
                    ),
                    PostRoutinesRequestSet(
                        type="normal",
                        weight_kg=140.0,
                        reps=5,
                        rep_range=RepRange(start=5, end=5),
                    ),
                ],
            ),
        ],
    )

    body = PostRoutinesRequestBody(routine=routine_data)
    routine = client.routines.create_routine(body)

    print(f"Created routine: {routine.title}")
    print(f"Routine ID: {routine.id}")
    print(f"Number of exercises: {len(routine.exercises)}")
    print()

    return routine.id


def get_routine_example(routine_id: str):
    """Example: Get a specific routine by ID."""
    print("=== Get Routine ===")

    routine_response = client.routines.get_routine(routine_id)
    routine = routine_response.routine

    print(f"Title: {routine.title}")
    print(f"Routine ID: {routine.id}")
    print(f"Exercises: {len(routine.exercises)}")

    for exercise in routine.exercises:
        print(f"  - Exercise: {exercise.title}")
        print(f"    Sets: {len(exercise.sets)}")
        for set_data in exercise.sets:
            print(f"      {set_data.type}: {set_data.weight_kg}kg x {set_data.reps} reps")

    print()


def update_routine_example(routine_id: str):
    """Example: Update an existing routine."""
    print("=== Update Routine ===")

    # Get the existing routine first
    existing_routine = client.routines.get_routine(routine_id).routine

    # Use the first exercise from the existing routine if available
    exercise_id = existing_routine.exercises[0].exercise_template_id if existing_routine.exercises else None

    if not exercise_id:
        # Fallback: get a valid exercise ID
        templates = client.exercise_templates.get_exercise_templates(page=1, page_size=1)
        exercise_id = templates.exercise_templates[0].id

    # Update with modified data
    updated_data = PutRoutinesRequestBodyRoutine(
        title=existing_routine.title + " (Updated)",
        exercises=[
            PutRoutinesRequestExercise(
                exercise_template_id=exercise_id,
                superset_id=0,
                notes="Increased weight!",
                sets=[
                    PutRoutinesRequestSet(
                        type="warmup",
                        weight_kg=60.0,
                        reps=10,
                        rep_range=RepRange(start=10, end=10),
                    ),
                    PutRoutinesRequestSet(
                        type="normal",
                        weight_kg=110.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PutRoutinesRequestSet(
                        type="normal",
                        weight_kg=110.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                    PutRoutinesRequestSet(
                        type="normal",
                        weight_kg=110.0,
                        reps=8,
                        rep_range=RepRange(start=8, end=8),
                    ),
                ],
            ),
        ],
    )

    body = PutRoutinesRequestBody(routine=updated_data)
    routine = client.routines.update_routine(routine_id, body)

    print(f"Updated routine: {routine.title}")
    print(f"Number of exercises: {len(routine.exercises)}")
    print()


def list_routine_folders_example():
    """Example: List routine folders with pagination."""
    print("=== List Routine Folders ===")

    # Get first page with 5 folders
    folders = client.routine_folders.get_routine_folders(page=1, page_size=5)
    print(f"Page: {folders.page}")
    print(f"Total pages: {folders.page_count}")
    print(f"Folders on this page: {len(folders.routine_folders)}")

    for folder in folders.routine_folders:
        print(f"  - {folder.title} (ID: {folder.id})")

    print()


def create_routine_folder_example():
    """Example: Create a new routine folder."""
    print("=== Create Routine Folder ===")

    from hevy_api_wrapper.models.post_routine_folder import PostRoutineFolder
    folder_data = PostRoutineFolder(title="Strength Training Programs")
    body = PostRoutineFolderRequestBody(routine_folder=folder_data)
    folder = client.routine_folders.create_routine_folder(body)

    print(f"Created folder: {folder.title}")
    print(f"Folder ID: {folder.id}")
    print()

    return folder.id


def get_routine_folder_example(folder_id: int):
    """Example: Get a specific routine folder by ID."""
    print("=== Get Routine Folder ===")

    folder = client.routine_folders.get_routine_folder(folder_id)

    print(f"Title: {folder.title}")
    print(f"Folder ID: {folder.id}")
    print(f"Index: {folder.index}")
    print()


def main():
    """Run all routine and routine folder examples."""
    print("=" * 50)
    print("ROUTINE & ROUTINE FOLDER ENDPOINT EXAMPLES")
    print("=" * 50)
    print()

    # Routine operations
    print("--- ROUTINE OPERATIONS ---")
    print()

    # List routines
    list_routines_example()

    # Create a new routine
    routine_id = create_routine_example()

    # Get the routine we just created
    get_routine_example(routine_id)

    # Update the routine
    update_routine_example(routine_id)

    print()
    print("--- ROUTINE FOLDER OPERATIONS ---")
    print()

    # List routine folders
    list_routine_folders_example()

    # Create a new routine folder
    folder_id = create_routine_folder_example()

    # Get the folder we just created
    get_routine_folder_example(folder_id)

    print("=" * 50)
    print("All routine examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
