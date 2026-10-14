## INBOX-HELPER for RECRUITER
Takes a pile of candidate messages, groups them by what the person wants, and drafts a short reply for each. A human reviews every draft before it is sent

# Clone the repo
```
git clone https://github.com/emekadefirst/Inbox-helper.git

```

# Change into DIR

```
cd Inbox-helper

```

# Generate environment variable file and it keys
```
cp .env.sample .env

```

# Create environment using Python UV package manager

```
uv sync --frozen

```

# Activate Virtual Environment

```
# bash terminal

python -m .venv/Scripts/activate

# using CMD or PowerShell

 .venv\Scripts\activate

```

# Create Migrations if abscent

```
uv run tortoise init

uv run tortoise makemigrations

```

# Apply Migrations to your DataBase

```
uv run tortoise migrate

```

# Run App

```
uv run dev

```