# What I Unlearned

> A project-grounded reflection. It describes lessons suggested by the
> delivered design, not claims about user research or a documented personal
> development diary.

Building Inbox Helper is a reminder that adding AI to a workflow is not the
same as solving the workflow. The tempting shortcut is to treat a model's
classification as the result. But recruiting decisions concern people, and a
confidently worded answer is not proof that its reasoning is correct. I
unlearned the idea that automation should be measured by how much human
involvement it removes. In this project, the more responsible goal is to remove
repetitive preparation while preserving human judgment. The product therefore
saves a draft for review and does not send it.

I also unlearned the assumption that a general-purpose evaluation is a fair or
useful one. A model can bring in unstated preferences unless the task is
carefully bounded. The relevant question is not whether an applicant seems
impressive in the abstract; it is whether their documented qualifications
match the requirements of this particular role. That distinction is why the
workflow builds a job-specific classification scheme and instructs the model
to ignore protected characteristics and proxy attributes.

Another shift was recognizing that the text being processed is not necessarily
an instruction source. Applicant messages may contain requests, opinions, or
even text that resembles commands to the model. It is easy to overlook this
boundary when input is presented as ordinary text. I learned to treat
applicant-provided content as data and to make that rule explicit in the
workflow, instead of assuming the model will infer it safely.

I unlearned the idea that a single large import is automatically convenient.
Batching helps only when the operator can tell what happened to each record.
Invalid rows, unknown job titles, and duplicates need visible outcomes; silently
discarding them would make the system appear successful while losing work.
The import report and row-level errors make the process more inspectable, even
though operational testing and stronger automated coverage remain important
next steps.

Finally, I unlearned the habit of treating a polished interface or a working
demo as evidence of a finished operational system. The code provides a useful
local workflow, but production use also depends on questions beyond the
visible feature set: who is authorized to view candidate records, how long
those records are kept, what happens to background work during a restart, and
how processing failures are monitored. Those concerns should be addressed
deliberately rather than hidden behind an assumption of readiness.

The lasting lesson is restraint. Good assistance is specific, inspectable, and
easy for a person to correct. It should reduce tedious work without pretending
to know more than the evidence supports or taking consequential actions on a
reviewer's behalf.
