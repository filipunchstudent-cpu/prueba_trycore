from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import ActivityModel, ProjectModel
from backend.app.schemas import (
    ActivityCreate,
    ActivityWithMetrics,
    MetricsResponse,
    ProjectCreate,
    ProjectWithMetrics,
)
from backend.app.services.evm import calculate_evm, consolidate_metrics

router = APIRouter(prefix="/api")


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


def _activity_with_metrics(activity: ActivityModel) -> ActivityWithMetrics:
    metrics = calculate_evm(
        bac=activity.bac,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        ac=activity.ac,
    )

    return ActivityWithMetrics(
        id=activity.id,
        name=activity.name,
        bac=activity.bac,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        ac=activity.ac,
        metrics=_metrics_response(metrics),
    )


def _project_with_metrics(project: ProjectModel) -> ProjectWithMetrics:
    activities = [_activity_with_metrics(activity) for activity in project.activities]
    total = consolidate_metrics([activity.metrics for activity in activities])

    return ProjectWithMetrics(
        id=project.id,
        name=project.name,
        activities=activities,
        metrics=_metrics_response(total),
    )


def _get_project(db: Session, project_id: int) -> ProjectModel:
    project = db.get(ProjectModel, project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


def _get_activity(
    project: ProjectModel,
    activity_id: int,
) -> ActivityModel:
    for activity in project.activities:
        if activity.id == activity_id:
            return activity

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Activity not found",
    )


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/projects", response_model=ProjectWithMetrics, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = ProjectModel(name=payload.name)

    db.add(project)
    db.commit()
    db.refresh(project)

    return _project_with_metrics(project)


@router.get("/projects", response_model=list[ProjectWithMetrics])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(ProjectModel).order_by(ProjectModel.id).all()

    return [_project_with_metrics(project) for project in projects]


@router.get("/projects/{project_id}", response_model=ProjectWithMetrics)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return _project_with_metrics(_get_project(db, project_id))


@router.put("/projects/{project_id}", response_model=ProjectWithMetrics)
def update_project(
    project_id: int,
    payload: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = _get_project(db, project_id)
    project.name = payload.name

    db.commit()
    db.refresh(project)

    return _project_with_metrics(project)


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)

    db.delete(project)
    db.commit()

    return None


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityWithMetrics,
    status_code=201,
)
def create_activity(
    project_id: int,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
):
    project = _get_project(db, project_id)

    activity = ActivityModel(
        project_id=project.id,
        name=payload.name,
        bac=payload.bac,
        planned_percent=payload.planned_percent,
        actual_percent=payload.actual_percent,
        ac=payload.ac,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return _activity_with_metrics(activity)


@router.put(
    "/projects/{project_id}/activities/{activity_id}",
    response_model=ActivityWithMetrics,
)
def update_activity(
    project_id: int,
    activity_id: int,
    payload: ActivityCreate,
    db: Session = Depends(get_db),
):
    project = _get_project(db, project_id)
    activity = _get_activity(project, activity_id)

    activity.name = payload.name
    activity.bac = payload.bac
    activity.planned_percent = payload.planned_percent
    activity.actual_percent = payload.actual_percent
    activity.ac = payload.ac

    db.commit()
    db.refresh(activity)

    return _activity_with_metrics(activity)


@router.delete("/projects/{project_id}/activities/{activity_id}", status_code=204)
def delete_activity(
    project_id: int,
    activity_id: int,
    db: Session = Depends(get_db),
):
    project = _get_project(db, project_id)
    activity = _get_activity(project, activity_id)

    db.delete(activity)
    db.commit()

    return None