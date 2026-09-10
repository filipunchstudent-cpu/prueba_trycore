from decimal import Decimal

from backend.app.database import Base, SessionLocal, engine
from backend.app.models import ActivityModel, ProjectModel


def seed_demo_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        existing = db.query(ProjectModel).filter_by(name="Proyecto demo EVM").first()

        if existing:
            return

        project = ProjectModel(name="Proyecto demo EVM")
        db.add(project)
        db.flush()

        activities = [
            ActivityModel(
                project_id=project.id,
                name="Descubrimiento",
                bac=Decimal("1000"),
                planned_percent=Decimal("100"),
                actual_percent=Decimal("100"),
                ac=Decimal("800"),
            ),
            ActivityModel(
                project_id=project.id,
                name="Desarrollo",
                bac=Decimal("4000"),
                planned_percent=Decimal("50"),
                actual_percent=Decimal("25"),
                ac=Decimal("1500"),
            ),
            ActivityModel(
                project_id=project.id,
                name="Pruebas",
                bac=Decimal("1000"),
                planned_percent=Decimal("20"),
                actual_percent=Decimal("10"),
                ac=Decimal("200"),
            ),
        ]

        db.add_all(activities)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo data loaded")