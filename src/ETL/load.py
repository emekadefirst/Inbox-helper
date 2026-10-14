import asyncio
from pathlib import Path
from uuid import uuid4
from src.ETL.reader import READERS
from src.modules.application.dtos import ApplicationImportRow, ImportReportDTO
from src.ETL.reader import normalize_row
from pydantic import ValidationError

async def import_applications(
    content: bytes,
    filename: str,
    repo,
    jobs_repo,
) -> ImportReportDTO:
    suffix = Path(filename).suffix.lower()
    reader = READERS.get(suffix)
    if reader is None:
        raise ValueError("Unsupported file type. Use .csv, .xlsx or .json")

    raw_rows = await asyncio.to_thread(lambda: list(reader(content)))
    report = ImportReportDTO(total=len(raw_rows))

    job_rows = await jobs_repo.model.all().values_list("title", "id")
    jobs = {title.casefold(): job_id for title, job_id in job_rows}
    parsed: list[tuple[int, ApplicationImportRow, object]] = []
    row_start = 2 if suffix in {".csv", ".xlsx"} else 1
    for i, raw in enumerate(raw_rows, start=row_start):
        try:
            row = ApplicationImportRow(**normalize_row(raw))
        except ValidationError as e:
            report.errors.append({"row": i, "reason": e.errors()[0]["msg"]})
            continue
        job_id = None
        if row.job_title:
            
            job_id = jobs.get(row.job_title.casefold())
            if job_id is None:
                report.errors.append({"row": i, "reason": f"unknown job_title: {row.job_title}"})
                continue
        parsed.append((i, row, job_id))

    # dedupe: within the file, and against the database
    existing = set()
    if parsed:
        existing_rows = await repo.model.filter(
            from_email__in=[r.from_email.lower() for _, r, _ in parsed]
        ).values_list("from_email", "job_id", "subject")
        existing = {
            (email.casefold(), job_id, subject)
            for email, job_id, subject in existing_rows
        }
    seen, to_create = set(), []
    for i, row, job_id in parsed:
        key = (row.from_email.casefold(), job_id, row.subject)
        if key in existing or key in seen:
            report.skipped_duplicates += 1
            continue
        seen.add(key)
        to_create.append(
            {
                "id": uuid4(),
                "job_id": job_id,
                "from_email": row.from_email.casefold(),
                **row.model_dump(exclude={"from_email", "job_title"}),
            }
        )

    if to_create:
        await repo.bulk_create(to_create)
        report.created = len(to_create)
        report.created_ids = [r["id"] for r in to_create]
    return report