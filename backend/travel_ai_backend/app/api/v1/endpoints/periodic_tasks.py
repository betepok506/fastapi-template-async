from uuid import UUID, uuid4

from celery.schedules import crontab
from celery_sqlalchemy_scheduler.models import (
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
)

# from travel_ai_backend.app.api.celery_task import increment
from fastapi import APIRouter, Depends
from sqlmodel import select

from travel_ai_backend.app.core.celery import celery
from travel_ai_backend.app.deps.celery_deps import get_job_db

router = APIRouter()


@router.post("/by_crontab")
async def create_periodic_task_by_crontab(celery_session=Depends(get_job_db)):
    """
    Creates a new periodic task that runs at specified intervals using crontab syntax.
    """
    # crontab_schedule = CrontabSchedule(
    #         hour=22, minute=2, day_of_month=29, month_of_year=3, timezone="UTC"
    #     )
    # celery_session.add(crontab_schedule)
    # celery_session.commit()

    # periodic_task = PeriodicTask(
    #     crontab=crontab_schedule,
    #     name="new_interval_periodic_task_crontab_2",
    #     args="[9]",
    #     task="tasks.increment",
    #     one_off=False,
    # )
    # celery_session.add(periodic_task)
    # celery_session.commit()
    task_id = str(uuid4())
    celery.conf.beat_schedule[f"{task_id}-run-every-midnight"] = {
        "task": "tasks.increment",
        "schedule": crontab(minute="*/1"),
    }

    # eta = str(crontab(minute='*/1'))
    # increment.apply_async(args=[1],  schedule= str(timedelta(seconds=15)))

    return {"message": "Task created"}


@router.put("/by_crontab")
async def update_periodic_task_by_crontab(celery_session=Depends(get_job_db)):
    """
    Updates an existing periodic task that runs at specified intervals using crontab syntax.
    """
    query = select(PeriodicTask).where(
        PeriodicTask.name == "new_interval_periodic_task_crontab_2"
    )
    periodic_task = celery_session.execute(query).scalar_one_or_none()
    periodic_task.crontab = CrontabSchedule(
        hour=22, minute=14, day_of_month=29, month_of_year=3, timezone="UTC"
    )
    celery_session.add(periodic_task)
    celery_session.commit()
    return {"message": "Task updated"}


@router.delete("/by_crontab")
async def remove_periodic_task_by_crontab(celery_session=Depends(get_job_db)):
    """
    Removes an existing periodic task that runs at specified intervals using crontab syntax.
    """
    query = select(PeriodicTask).where(
        PeriodicTask.name == "new_interval_periodic_task_crontab"
    )
    periodic_task = celery_session.execute(query).scalar_one_or_none()
    periodic_task.enabled = False
    celery_session.add(periodic_task)
    celery_session.commit()
    return {"message": "Task removed"}


@router.post("/by_interval")
async def create_periodic_task_by_interval(
    interval: int, celery_session=Depends(get_job_db)
):
    """
    Creates a new periodic task that runs at specified intervals using the
    interval schedule.
    """
    periodic_task = PeriodicTask(
        interval=IntervalSchedule(
            every=interval, period=IntervalSchedule.SECONDS
        ),
        name="new_interval_periodic_task",
        args="[8]",
        task="tasks.increment",
    )
    celery_session.add(periodic_task)
    celery_session.commit()
    return {"message": "Periodic task created"}


@router.put("/by_interval")
async def update_periodic_task_by_interval(
    interval: int, celery_session=Depends(get_job_db)
):
    """
    Updates a periodic task that runs at specified intervals using the interval schedule.
    """
    # Retrieve the result using the task ID
    query = select(PeriodicTask).where(
        PeriodicTask.name == "new_interval_periodic_task"
    )
    periodic_task = celery_session.execute(query).scalar_one_or_none()
    periodic_task.interval = interval = (
        IntervalSchedule(every=interval, period=IntervalSchedule.SECONDS),
    )
    celery_session.add(periodic_task)
    celery_session.commit()
    return {"message": "Periodic task updated"}


@router.delete("/by_interval")
async def remove_periodic_task_by_interval(celery_session=Depends(get_job_db)):
    """
    Remove a periodic task that runs at specified intervals using the interval schedule.
    """
    # Retrieve the result using the task ID
    query = select(PeriodicTask).where(
        PeriodicTask.name == "new_interval_periodic_task"
    )
    periodic_task = celery_session.execute(query).scalar_one_or_none()
    periodic_task.enabled = False
    celery_session.add(periodic_task)
    celery_session.commit()
    return {"message": "Periodic task removed"}
