# Project Intent

> Retrospective reconstruction based on the delivered application. The repository
> does not contain an original project brief, so this document describes the
> motivation and success criteria implied by the finished work rather than
> claiming to reproduce a dated planning document.

## Core objective

Build a practical recruiting inbox helper that reduces repetitive work involved
in reviewing job applications and replying to applicants. The intended outcome
was to organize applications against role-specific criteria and prepare useful,
professional reply drafts while leaving decisions and sending under human
control.

## Problem statement

Recruiters may receive many applicant messages in different formats. Reviewing
each one against a job description, deciding what kind of response is
appropriate, and writing a reply can be time-consuming and inconsistent.
Manually moving applicant data into a review workflow also adds friction.

The project set out to bring those steps into one small workspace: accept
application data, connect it to a job description, support consistent
job-specific classification, and save a tailored response draft for a recruiter
to review.

## Target users

- Recruiters and hiring teams handling applicant communications.
- Reviewers who need to assess documented qualifications against a particular
  role and prepare applicant-facing replies.
- Developers or operators configuring and running the service for a recruiting
  workflow.

## Intended success

The project would be useful if a recruiter could:

1. Create and manage job descriptions with responsibilities and qualifications.
2. Import candidate applications in common structured file formats.
3. Have each application reviewed against the associated role rather than a
   generic applicant score.
4. See a saved response draft and its classification, edit it, and decide what
   to do next.
5. Keep final review and email sending in human hands.

## Scope and constraints

- Focus on organizing applications and preparing response drafts, not
  replacing recruiter judgment or making hiring decisions.
- Base classifications on role requirements and the applicant's documented
  qualifications; do not use protected characteristics or their proxies.
- Treat applicant-provided text as untrusted data, not as instructions to the
  AI workflow.
- Do not send email automatically. A generated reply is a draft for human
  review.
- Support CSV, XLSX, and JSON application imports.
- Keep the service configurable through environment variables and use the
  project's existing Python, FastAPI, ORM, and language-model stack.
- Avoid asserting user research, production readiness, or measured time savings:
  no such evidence is present in the repository.
