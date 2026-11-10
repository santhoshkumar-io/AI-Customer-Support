# Harbor & Pine support automation

Gmail poller -> classifier -> support agent -> Supabase Postgres.

## Setup

```bash
conda env create -f environment.yml
conda activate aics
pip install pydantic-evals google-auth-oauthlib   # dev only: evals and token script
```

Copy `.env.example` to `.env` and fill in the values.

## Run

```bash
python -m app.poller                      # poll Gmail
python -m scripts.seed_knowledge_base     # load knowledge_base/*.md into Supabase
python -m evals.run_evals                 # run the golden-email evals
docker compose up --build                 # API and poller in containers
```
