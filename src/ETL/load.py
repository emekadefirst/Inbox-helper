import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4
from src.ETL.reader import READERS
from src.modules.application.dtos import ApplicationImportRow
from src.ETL.reader import normalize_row
from pydantic import ValidationError

@dataclass
class ImportReport:
    total: int = 0
    created: int = 0
    skipped_duplicates: int = 0
    errors: list[dict] = field(default_factory=list)
    created_ids: list = field(default_factory=list)

async def import_applications(path: str, repo, jobs_repo) -> ImportReport:
    reader = READERS.get(Path(path).suffix.lower())
    if reader is None:
        raise ValueError("Unsupported file type. Use .csv, .xlsx or .json")

    raw_rows = await asyncio.to_thread(lambda: list(reader(path)))   # parse off the event loop
    report = ImportReport(total=len(raw_rows))

    jobs = {j.title.lower(): j.id for j in await jobs_repo.find(limit=1000)}
    parsed: list[tuple[int, ApplicationImportRow, object]] = []
    for i, raw in enumerate(raw_rows, start=2):                    # row 1 is the header
        try:
            row = ApplicationImportRow(**normalize_row(raw))
        except ValidationError as e:
            report.errors.append({"row": i, "reason": e.errors()[0]["msg"]})
            continue
        job_id = None
        if row.job_title:
            
            job_id = jobs.get(row.job_title.lower())
            if job_id is None:
                report.errors.append({"row": i, "reason": f"unknown job_title: {row.job_title}"})
                continue
        parsed.append((i, row, job_id))

    # dedupe: within the file, and against the database
    existing = set(await repo.model.filter(
        from_email__in=[r.from_email.lower() for _, r, _ in parsed]
    ).values_list("from_email", "job_id", "subject"))
    seen, to_create = set(), []
    for i, row, job_id in parsed:
        key = (row.from_email.lower(), job_id, row.subject)
        if key in existing or key in seen:
            report.skipped_duplicates += 1
            continue
        seen.add(key)
        to_create.append({
            "id": uuid4(), "job_id": job_id, "from_email": row.from_email.lower(),
            **row.model_dump(exclude={"from_email", "job_title"}),
        })

    if to_create:
        await repo.bulk_create(to_create)
        report.created = len(to_create)
        report.created_ids = [r["id"] for r in to_create]
    return report