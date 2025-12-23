# BetaSeries Recommender CLI

## Key Features
- **Project Structure**: Modular code in `src/betaseries_recommender` (API, Processing, CLI).
- **Configurable**:
    - Choose `--type` (movies, shows, both).
    - Sort by `--sort` (weighted_average, mean_notes, total_notes).
    - Set table size with `--limit`.
    - **Fetch Limit**: Control how many items are fetched from the API with `--fetch-limit` (default 2000).

## Installation
This project uses `conda` for environment management. 

1. Ensure you have Conda installed (e.g., Miniconda or Anaconda).
2. Create and activate the environment using `environment.yml`:

```bash
conda env create -f environment.yml
conda activate betaseries
```

3. Ensure dependencies are up to date if you already have the environment:
```bash
conda env update -f environment.yml --prune
```

## Usage

Run the tool using `main.py`:

**1. Generate recommendation for Movies only, sorted by weighted average (default):**
```bash
python main.py --type movies --output movies_rec.csv
```

**2. Generate for both Movies and Shows, sorted by total notes, top 100:**
```bash
python main.py --type both --sort total_notes --limit 100 --output top_popular.csv
```

**4. Faster execution with lower fetch limit:**
Fetch fewer items (e.g., 200) for quicker testing (default is 2000):
```bash
python main.py --type movies --fetch-limit 200 --output quick_test.csv
```

## Structure
- `src/betaseries_recommender/`:
    - `api.py`: Interaction with BetaSeries API.
    - `processing.py`: Core logic for weighted average and sorting.
    - `cli.py`: Command line interface.
- `tests/`:
    - `test_processing.py`: Unit tests for calculation logic.
- `main.py`: Entry point.
....
----------------------------------------------------------------------

