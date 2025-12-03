"""
Exercise Template endpoint examples demonstrating all available operations.

This example shows how to:
- List exercise templates with pagination
- Create a custom exercise template
- Get a specific exercise template by ID
"""

import os

from dotenv import load_dotenv

from hevy_api_wrapper import Client
from hevy_api_wrapper.models import (
    CreateCustomExercise,
    CreateCustomExerciseRequestBody,
    CustomExerciseType,
    EquipmentCategory,
    MuscleGroup,
)

load_dotenv()

API_KEY = os.getenv("HEVY_API_TOKEN")
if not API_KEY:
    raise ValueError("HEVY_API_TOKEN not found in environment variables")

client = Client(api_key=API_KEY)


def list_exercise_templates_example():
    """Example: List exercise templates with pagination."""
    print("=== List Exercise Templates ===")

    # Get first page with 20 templates
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=20)
    print(f"Page: {templates.page}")
    print(f"Total pages: {templates.page_count}")
    print(f"Templates on this page: {len(templates.exercise_templates)}")

    for template in templates.exercise_templates[:5]:  # Show first 5
        print(f"  - {template.title} (ID: {template.id})")
        print(f"    Type: {template.type}")
        if template.primary_muscle_group:
            print(f"    Primary muscle: {template.primary_muscle_group}")
        if template.secondary_muscle_groups:
            print(
                f"    Secondary muscles: {', '.join(template.secondary_muscle_groups)}"
            )

    print()


def create_custom_exercise_example():
    """Example: Create a custom exercise template."""
    print("=== Create Custom Exercise ===")

    exercise_data = CreateCustomExercise(
        title="Bulgarian Split Squat (Dumbbell)",
        exercise_type=CustomExerciseType.weight_reps,
        muscle_group=MuscleGroup.quadriceps,
        other_muscles=[MuscleGroup.glutes, MuscleGroup.hamstrings],
        equipment_category=EquipmentCategory.dumbbell,
    )

    body = CreateCustomExerciseRequestBody(exercise=exercise_data)

    response = client.exercise_templates.create_custom_exercise(body)

    print(f"Created custom exercise with ID: {response.id}")
    print()

    return response.id


def get_exercise_template_example(template_id: str):
    """Example: Get a specific exercise template by ID."""
    print("=== Get Exercise Template ===")

    template = client.exercise_templates.get_exercise_template(template_id)

    print(f"Title: {template.title}")
    print(f"Template ID: {template.id}")
    print(f"Type: {template.type}")
    print(f"Is Custom: {template.is_custom}")

    if template.primary_muscle_group:
        print(f"Primary muscle group: {template.primary_muscle_group}")

    if template.secondary_muscle_groups:
        print(f"Secondary muscle groups: {', '.join(template.secondary_muscle_groups)}")

    print()


def search_exercise_templates_example():
    """Example: Search for specific exercises by name."""
    print("=== Search Exercise Templates ===")

    # Get a large batch and filter client-side (API doesn't have built-in search)
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=100)

    # Search for exercises containing "bench"
    search_term = "bench"
    matching_exercises = [
        template
        for template in templates.exercise_templates
        if search_term.lower() in template.title.lower()
    ]

    print(f"Found {len(matching_exercises)} exercises matching '{search_term}':")
    for template in matching_exercises[:10]:  # Show first 10
        print(f"  - {template.title} (ID: {template.id})")

    print()


def filter_by_muscle_group_example():
    """Example: Filter exercises by muscle group."""
    print("=== Filter by Muscle Group ===")

    # Get templates and filter by chest
    templates = client.exercise_templates.get_exercise_templates(page=1, page_size=100)

    target_muscle = MuscleGroup.chest
    chest_exercises = [
        template
        for template in templates.exercise_templates
        if template.primary_muscle_group == target_muscle
    ]

    print(f"Found {len(chest_exercises)} exercises targeting {target_muscle}:")
    for template in chest_exercises[:10]:  # Show first 10
        print(f"  - {template.title} (ID: {template.id})")
        print(f"    Type: {template.type}")

    print()


def main():
    """Run all exercise template examples."""
    print("=" * 50)
    print("EXERCISE TEMPLATE ENDPOINT EXAMPLES")
    print("=" * 50)
    print()

    # List exercise templates
    list_exercise_templates_example()

    # Create a custom exercise
    custom_exercise_id = create_custom_exercise_example()

    # Get the custom exercise we just created
    get_exercise_template_example(custom_exercise_id)

    # Search exercises
    search_exercise_templates_example()

    # Filter by muscle group
    filter_by_muscle_group_example()

    print("=" * 50)
    print("All exercise template examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
