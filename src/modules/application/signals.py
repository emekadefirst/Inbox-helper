import asyncio
import logging

from tortoise.signals import post_save

from src.modules.application.models import Application
from src.intelligence.agents import screening_agent

logger = logging.getLogger(__name__)

_background_tasks: set[asyncio.Task] = set()


def _task_finished(task: asyncio.Task) -> None:
    """Keep background tasks alive and log failures."""
    _background_tasks.discard(task)

    if task.cancelled():
        return

    error = task.exception()
    if error is not None:
        logger.error(
            "Application screening task failed",
            exc_info=(type(error), error, error.__traceback__),
        )


def run_async_task(coro) -> None:
    """Schedule a background coroutine on the current event loop."""
    task = asyncio.create_task(coro)
    _background_tasks.add(task)
    task.add_done_callback(_task_finished)


@post_save(Application)
async def screen_application(
    sender,
    instance: Application,
    created: bool,
    using_db,
    update_fields,
    **kwargs,
) -> None:
    """Screen a newly created application in the background."""

    if not created:
        return

    application_id = str(instance.id)

    run_async_task(
        screening_agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Process this job application using the available "
                            "tools and the application-processing instructions. "
                            f"Application ID: {application_id}. "
                            "Retrieve the application and its associated job "
                            "description, including the saved classification "
                            "scheme. Compare the applicant's documented "
                            "qualifications with the job requirements, select "
                            "one valid category or an appropriate reserved "
                            "outcome, and generate a concise email draft. "
                            "Save the draft for human review. Do not send email."
                        ),
                    }
                ]
            }
        )
    )
