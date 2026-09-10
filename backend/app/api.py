from decimal import Decimal

from fastapi import APIRouter, HTTPException, status

from backend.app.schemas import (
    Activity,
    ActivityCreate,
    ActivityWithMetrics,
    MetricsResponse,
    Project,
    ProjectCreate,
    ProjectWithMetrics,
)
from backend.app.services.evm import calculate_evm, consolidate_metrics


router = APIRouter(prefix="/api")

projects: dict[int, Project] = {}
next_project_id = 1
next_activity_id = 1


def _metrics_response(metrics) -> MetricsResponse:
    return MetricsResponse(
        bac=metrics.bac,
        pv=metrics.pv,
        ev=metrics.ev,
        ac=metrics.ac,
        cv=metrics.cv,
        sv=metrics.sv,
        cpi=metrics.cpi,
        spi=metrics.spi,
        eac=metrics.eac,
        vac=metrics.vac,
        cost_status=metrics.cost_status,
        schedule_status=metrics.schedule_status,
    )


def _activity_with_metrics(activity: Activity) -> ActivityWithMetrics:
    metrics = calculate_evm(
        bac=activity.bac,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        ac=activity.ac,
    )

    return ActivityWithMetrics(
        **activity.model_dump(),
        metrics=_metrics_response(metrics),
    )


def _project_with_metrics(project: Project) -> ProjectWithMetrics:
    activities = [_activity_with_metrics(activity) for activity in project.activities]
    total = consolidate_metrics([activity.metrics for activity in activities])

    return ProjectWithMetrics(
        id=project.id,
        name=project.name,
        activities=activities,
        metrics=_metrics_response(total),
    )


def _get_project(project_id: int) -> Project:
    project = projects.get(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/projects", response_model=ProjectWithMetrics, status_code=201)
def create_project(payload: ProjectCreate):
    global next_project_id

    project = Project(
        id=next_project_id,
        name=payload.name,
        activities=[],
    )
    projects[project.id] = project
    next_project_id += 1

    return _project_with_metrics(project)


@router.get("/projects", response_model=list[ProjectWithMetrics])
def list_projects():
    return [_project_with_metrics(project) for project in projects.values()]


@router.get("/projects/{project_id}", response_model=ProjectWithMetrics)
def get_project(project_id: int):
    return _project_with_metrics(_get_project(project_id))


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityWithMetrics,
    status_code=201,
)
def create_activity(project_id: int, payload: ActivityCreate):
    global next_activity_id

    project = _get_project(project_id)

    activity = Activity(
        id=next_activity_id,
        **payload.model_dump(),
    )

    project.activities.append(activity)
    next_activity_id += 1

    return _activity_with_metrics(activity)


@router.put(
    "/projects/{project_id}/activities/{activity_id}",
    response_model=ActivityWithMetrics,
)
def update_activity(project_id: int, activity_id: int, payload: ActivityCreate):
    project = _get_project(project_id)

    for index, activity in enumerate(project.activities):
        if activity.id == activity_id:
            updated = Activity(id=activity_id, **payload.model_dump())
            project.activities[index] = updated
            return _activity_with_metrics(updated)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found",
    )


@router.delete("/projects/{project_id}/activities/{activity_id}", status_code=204)
def delete_activity(project_id: int, activity_id: int):
    project = _get_project(project_id)

    for index, activity in enumerate(project.activities):
        if activity.id == activity_id:
            project.activities.pop(index)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found",
    )