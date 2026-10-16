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
        return

    error = task.exception()
    if error is not None:
        logger.error(
            "Background classification task failed",
            exc_info=(type(error), error, error.__traceback__),
        )


def run_async_task(coro) -> None:
    """Schedule a coroutine on the currently running event loop."""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_task_finished)


@post_save(JobDescription)
async def generate_job_classification(
    sender,
    instance: JobDescription,
    created: bool,
    **kwargs,
) -> None:
    """Generate a scheme when a new job description is created."""

    if not created:
        return

    if instance.generated_classification:
        return

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
        )
    )
