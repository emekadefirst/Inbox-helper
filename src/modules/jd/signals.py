import asyncio
import logging

from tortoise.signals import post_save

from src.modules.jd.models import JobDescription
from src.intelligence.agents import classifying_agent

logger = logging.getLogger(__name__)

_background_tasks: set[asyncio.Task] = set()


def _task_finished(task: asyncio.Task) -> None:
    """Keep a reference to the task and log any background failure."""
    _background_tasks.discard(task)

    if task.cancelled():
        logger.warning("Background task %s was cancelled", task.get_name())
        return

    error = task.exception()
    if error is not None:
        logger.error(
            "Background task %s failed",
            task.get_name(),
            exc_info=(type(error), error, error.__traceback__),
        )
        return

    logger.info("Background task %s completed", task.get_name())


def run_async_task(coro, task_name: str) -> None:
    """Schedule a coroutine on the currently running event loop."""
    task = asyncio.create_task(coro, name=task_name)
    _background_tasks.add(task)
    task.add_done_callback(_task_finished)
    logger.info("Scheduled background task %s", task_name)


@post_save(JobDescription)
async def generate_job_classification(
    sender,
    instance: JobDescription,
    created: bool,
    using_db,
    update_fields,
    **kwargs,
) -> None:
    """Generate a scheme when a new job description is created."""

    if not created:
        return

    if instance.generated_classification:
        return

    task_name = f"JD classification {instance.id}"
    run_async_task(
        classifying_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Generate and save a classification scheme for "
                            f"job description ID {instance.id}. "
                            "Retrieve the job description using the available "
                            "tool, derive the categories from its actual "
                            "requirements, and save the completed scheme "
                            "using submit_scheme. Do not invent requirements."
                        ),
                    }
                ]
            }
        ),
        task_name,
    )
