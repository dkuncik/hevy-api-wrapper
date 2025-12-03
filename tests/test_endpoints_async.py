import pytest
import respx

from hevy_api_wrapper import AsyncClient
from hevy_api_wrapper.errors import NotFoundError
from hevy_api_wrapper.models import (
    CreateCustomExercise,
    CreateCustomExerciseRequestBody,
    CustomExerciseType,
    EquipmentCategory,
    MuscleGroup,
    PostRoutineFolder,
    PostRoutineFolderRequestBody,
    PostRoutinesRequestBody,
    PostRoutinesRequestBodyRoutine,
    PostRoutinesRequestExercise,
    PostRoutinesRequestSet,
    PostWorkoutsRequestBody,
    PostWorkoutsRequestBodyWorkout,
    PostWorkoutsRequestExercise,
    PostWorkoutsRequestSet,
    PutRoutinesRequestBody,
    PutRoutinesRequestBodyRoutine,
    PutRoutinesRequestExercise,
    PutRoutinesRequestSet,
)

BASE = "https://api.hevyapp.com"


def sample_workout_json():
    return {
        "id": "w-1",
        "title": "Morning Workout",
        "routine_id": "r-1",
        "description": "desc",
        "start_time": "2021-09-14T12:00:00Z",
        "end_time": "2021-09-14T12:30:00Z",
        "updated_at": "2021-09-14T12:31:00Z",
        "created_at": "2021-09-14T12:00:00Z",
        "exercises": [
            {
                "index": 0,
                "title": "Bench Press (Barbell)",
                "notes": "",
                "exercise_template_id": "05293BCA",
                "supersets_id": None,
                "sets": [
                    {
                        "index": 0,
                        "type": "normal",
                        "weight_kg": 100,
                        "reps": 10,
                        "distance_meters": None,
                        "duration_seconds": None,
                        "rpe": 9.5,
                        "custom_metric": None,
                    }
                ],
            }
        ],
    }


def sample_routine_json():
    return {
        "id": "r-1",
        "title": "Upper Body",
        "folder_id": None,
        "updated_at": "2021-09-14T12:31:00Z",
        "created_at": "2021-09-14T12:00:00Z",
        "exercises": [
            {
                "index": 0,
                "title": "Bench Press (Barbell)",
                "rest_seconds": 60,
                "notes": "",
                "exercise_template_id": "05293BCA",
                "supersets_id": None,
                "sets": [
                    {
                        "index": 0,
                        "type": "normal",
                        "weight_kg": 100,
                        "reps": 10,
                        "rep_range": None,
                        "distance_meters": None,
                        "duration_seconds": None,
                        "rpe": None,
                        "custom_metric": None,
                    }
                ],
            }
        ],
    }


def sample_exercise_template_json():
    return {
        "id": "T-1",
        "title": "Bench Press (Barbell)",
        "type": "weight_reps",
        "primary_muscle_group": "chest",
        "secondary_muscle_groups": ["triceps"],
        "is_custom": False,
    }


def sample_exercise_history_json():
    return {
        "exercise_history": [
            {
                "workout_id": "w-1",
                "workout_title": "Morning Workout",
                "workout_start_time": "2021-09-14T12:00:00Z",
                "workout_end_time": "2021-09-14T12:30:00Z",
                "exercise_template_id": "05293BCA",
                "weight_kg": 100,
                "reps": 10,
                "distance_meters": None,
                "duration_seconds": None,
                "rpe": 9.5,
                "custom_metric": None,
                "set_type": "normal",
            }
        ]
    }


def sample_routine_folder_json(id: int = 42, title: str = "Push Pull"):
    return {
        "id": id,
        "index": 0,
        "title": title,
        "updated_at": "2021-09-14T12:31:00Z",
        "created_at": "2021-09-14T12:00:00Z",
    }


@respx.mock
@pytest.mark.asyncio
async def test_workouts_endpoints_async():
    respx.get(f"{BASE}/v1/workouts").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "workouts": [sample_workout_json()],
        },
    )
    # Create - API returns workout wrapped in array
    respx.post(f"{BASE}/v1/workouts").respond(201, json={"workout": [sample_workout_json()]})
    respx.get(f"{BASE}/v1/workouts/w-1").respond(200, json=sample_workout_json())
    # Update - API returns workout wrapped in array
    respx.put(f"{BASE}/v1/workouts/w-1").respond(200, json={"workout": [sample_workout_json()]})
    respx.get(f"{BASE}/v1/workouts/events").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "events": [
                {"type": "updated", "workout": sample_workout_json()},
            ],
        },
    )
    respx.get(f"{BASE}/v1/workouts/count").respond(200, json={"workout_count": 42})

    c = AsyncClient(api_key="test-key")

    page = await c.workouts.get_workouts(page=1, page_size=5)
    assert page.page == 1 and len(page.workouts) == 1

    body = PostWorkoutsRequestBody(
        workout=PostWorkoutsRequestBodyWorkout(
            title="Morning Workout",
            description="desc",
            start_time="2021-09-14T12:00:00Z",
            routine_id="r-1",
            end_time="2021-09-14T12:30:00Z",
            is_private=False,
            exercises=[
                PostWorkoutsRequestExercise(
                    exercise_template_id="05293BCA",
                    superset_id=None,
                    notes=None,
                    sets=[PostWorkoutsRequestSet(type="normal", weight_kg=100, reps=10)],
                )
            ],
        )
    )

    created = await c.workouts.create_workout(body)
    assert created.id == "w-1"

    single = await c.workouts.get_workout("w-1")
    assert single.title == "Morning Workout"

    updated = await c.workouts.update_workout("w-1", body)
    assert updated.id == "w-1"

    events = await c.workouts.get_events(page=1, page_size=5)
    assert events.page_count == 1 and len(events.events) == 1

    count = await c.workouts.get_count()
    assert count == 42

    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_routines_endpoints_async():
    respx.get(f"{BASE}/v1/routines").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "routines": [sample_routine_json()],
        },
    )
    # Create - API returns routine wrapped in array
    respx.post(f"{BASE}/v1/routines").respond(201, json={"routine": [sample_routine_json()]})
    respx.get(f"{BASE}/v1/routines/r-1").respond(200, json={"routine": sample_routine_json()})
    # Update - API returns routine wrapped in array
    respx.put(f"{BASE}/v1/routines/r-1").respond(200, json={"routine": [sample_routine_json()]})

    c = AsyncClient(api_key="test-key")

    page = await c.routines.get_routines(page=1, page_size=5)
    assert page.page == 1 and len(page.routines) == 1

    create_body = PostRoutinesRequestBody(
        routine=PostRoutinesRequestBodyRoutine(
            title="Upper Body",
            folder_id=None,
            notes=None,
            exercises=[
                PostRoutinesRequestExercise(
                    exercise_template_id="05293BCA",
                    superset_id=None,
                    rest_seconds=60,
                    notes=None,
                    sets=[PostRoutinesRequestSet(type="normal", weight_kg=100, reps=10)],
                )
            ],
        )
    )

    created = await c.routines.create_routine(create_body)
    assert created.id == "r-1"

    fetched = await c.routines.get_routine("r-1")
    assert fetched.routine.id == "r-1"

    update_body = PutRoutinesRequestBody(
        routine=PutRoutinesRequestBodyRoutine(
            title="Upper Body",
            notes=None,
            exercises=[
                PutRoutinesRequestExercise(
                    exercise_template_id="05293BCA",
                    superset_id=None,
                    rest_seconds=60,
                    notes=None,
                    sets=[PutRoutinesRequestSet(type="normal", weight_kg=100, reps=10)],
                )
            ],
        )
    )

    updated = await c.routines.update_routine("r-1", update_body)
    assert updated.title == "Upper Body"

    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_exercise_templates_endpoints_async():
    respx.get(f"{BASE}/v1/exercise_templates").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "exercise_templates": [sample_exercise_template_json()],
        },
    )
    respx.post(f"{BASE}/v1/exercise_templates").respond(200, json={"id": 123})
    respx.get(f"{BASE}/v1/exercise_templates/T-1").respond(200, json=sample_exercise_template_json())

    c = AsyncClient(api_key="test-key")

    page = await c.exercise_templates.get_exercise_templates(page=1, page_size=100)
    assert page.page_count == 1 and len(page.exercise_templates) == 1

    body = CreateCustomExerciseRequestBody(
        exercise=CreateCustomExercise(
            title="Custom Bench",
            exercise_type=CustomExerciseType.weight_reps,
            equipment_category=EquipmentCategory.barbell,
            muscle_group=MuscleGroup.chest,
            other_muscles=[MuscleGroup.triceps],
        )
    )

    created = await c.exercise_templates.create_custom_exercise(body)
    assert created.id == 123

    tmpl = await c.exercise_templates.get_exercise_template("T-1")
    assert tmpl.id == "T-1"

    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_routine_folders_endpoints_async():
    respx.get(f"{BASE}/v1/routine_folders").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "routine_folders": [sample_routine_folder_json()],
        },
    )
    # Create - API returns routine_folder wrapped in object
    respx.post(f"{BASE}/v1/routine_folders").respond(
        201, json={"routine_folder": sample_routine_folder_json(100, "New Folder")}
    )
    respx.get(f"{BASE}/v1/routine_folders/42").respond(200, json=sample_routine_folder_json())

    c = AsyncClient(api_key="test-key")

    page = await c.routine_folders.get_routine_folders(page=1, page_size=5)
    assert len(page.routine_folders) == 1

    body = PostRoutineFolderRequestBody(routine_folder=PostRoutineFolder(title="New Folder"))
    created = await c.routine_folders.create_routine_folder(body)
    assert created.id == 100

    folder = await c.routine_folders.get_routine_folder(42)
    assert folder.id == 42

    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_exercise_history_endpoint_async():
    respx.get(f"{BASE}/v1/exercise_history/05293BCA").respond(200, json=sample_exercise_history_json())

    c = AsyncClient(api_key="test-key")
    hist = await c.exercise_history.get_exercise_history("05293BCA")
    assert len(hist.exercise_history) == 1
    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_not_found_raises_error_async():
    respx.get(f"{BASE}/v1/workouts/does-not-exist").respond(404, json={"message": "not found"})

    c = AsyncClient(api_key="test-key")
    with pytest.raises(NotFoundError):
        await c.workouts.get_workout("does-not-exist")
    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_workout_events_with_custom_since_async():
    respx.get(f"{BASE}/v1/workouts/events").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "events": [
                {"type": "updated", "workout": sample_workout_json()},
            ],
        },
    )

    c = AsyncClient(api_key="test-key")
    events = await c.workouts.get_events(page=1, page_size=5, since="2024-01-01T00:00:00Z")
    assert events.page == 1 and len(events.events) == 1
    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_workout_without_routine_id_async():
    """Test that workout can be created without routine_id (it gets omitted from request)."""
    respx.post(f"{BASE}/v1/workouts").respond(
        201,
        json={
            "workout": [
                {
                    "id": "w-no-routine",
                    "title": "Standalone Workout",
                    "routine_id": None,
                    "description": "No routine",
                    "start_time": "2021-09-14T12:00:00Z",
                    "end_time": "2021-09-14T12:30:00Z",
                    "updated_at": "2021-09-14T12:31:00Z",
                    "created_at": "2021-09-14T12:00:00Z",
                    "exercises": [],
                }
            ]
        },
    )

    c = AsyncClient(api_key="test-key")

    # Create workout without routine_id
    body = PostWorkoutsRequestBody(
        workout=PostWorkoutsRequestBodyWorkout(
            title="Standalone Workout",
            description="No routine",
            start_time="2021-09-14T12:00:00Z",
            routine_id=None,  # Should be omitted from JSON
            end_time="2021-09-14T12:30:00Z",
            is_private=False,
            exercises=[],
        )
    )

    created = await c.workouts.create_workout(body)
    assert created.id == "w-no-routine"
    assert created.routine_id is None

    await c.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_exercise_template_with_bodyweight_assisted_async():
    """Test that bodyweight_assisted exercise type is supported."""
    respx.get(f"{BASE}/v1/exercise_templates").respond(
        200,
        json={
            "page": 1,
            "page_count": 1,
            "exercise_templates": [
                {
                    "id": "T-2",
                    "title": "Pull-up (Assisted)",
                    "type": "bodyweight_assisted",
                    "primary_muscle_group": "lats",
                    "secondary_muscle_groups": ["biceps"],
                    "is_custom": False,
                }
            ],
        },
    )

    c = AsyncClient(api_key="test-key")

    page = await c.exercise_templates.get_exercise_templates(page=1, page_size=100)
    assert len(page.exercise_templates) == 1
    assert page.exercise_templates[0].type == CustomExerciseType.bodyweight_assisted

    await c.aclose()
