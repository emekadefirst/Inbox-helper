from pydantic import BaseModel, Field, model_validator


class Category(BaseModel):
    label: str = Field(pattern=r"^[a-z][a-z0-9_]{2,40}$")  # snake_case, used as an enum value
    criteria: str = Field(min_length=10)   # what an applicant must show, taken from the JD
    reply_goal: str = Field(min_length=5)  # what the reply should accomplish


# Fixed labels added by code. The model never generates these.
SYSTEM_CATEGORIES = [
    Category(
        label="needs_info",
        criteria="Résumé missing, unreadable, or too little information to judge.",
        reply_goal="Politely ask for the missing material.",
    ),
    Category(
        label="unclear",
        criteria="Cannot be decided from the material provided.",
        reply_goal="Neutral acknowledgement; a team member will follow up.",
    ),
]
SYSTEM_LABELS = {c.label for c in SYSTEM_CATEGORIES}


class SchemeDraft(BaseModel):
    """What the model returns in stage 1."""
    categories: list[Category] = Field(min_length=3, max_length=6)

    @model_validator(mode="after")
    def check_labels(self):
        labels = [c.label for c in self.categories]
        if len(labels) != len(set(labels)):
            raise ValueError("category labels must be unique")
        if SYSTEM_LABELS & set(labels):
            raise ValueError(f"labels reserved for the system: {sorted(SYSTEM_LABELS)}")
        return self


class ClassificationScheme(SchemeDraft):
    """What gets stored on JobDescription.generated_classification."""
    version: int = 1

    @property
    def all_categories(self) -> list[Category]:
        return [*self.categories, *SYSTEM_CATEGORIES]

    @property
    def all_labels(self) -> list[str]:
        return [c.label for c in self.all_categories]