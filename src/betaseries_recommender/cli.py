import argparse
import os
import sys

import pandas as pd
from dotenv import load_dotenv

from .api import BetaSeriesAPI
from .processing import process_data


def fetch_movies(client, limit=1000):
    print(f"Fetching top {limit} movies...")
    data = []

    try:
        # Hard cap at API limit of 1000
        limit = min(limit, 1000)

        movies_list = client.get_movies_list(limit=limit, order="popularity", page=1)
        movies = movies_list.get("movies", [])

        for i, movie in enumerate(movies):
            if i % 10 == 0 or i == len(movies) - 1:
                print(f"Fetching... ({len(data) + 1}/{limit})", end="\r", flush=True)

            try:
                movie_id = movie.get("id")
                details = client.get_movie_details(movie_id).get("movie", {})
                notes = details.get("notes", {})
                data.append(
                    {
                        "title": movie.get("title"),
                        "total_notes": notes.get("total", 0),
                        "mean_notes": notes.get("mean", 0.0),
                    }
                )
            except Exception:
                continue

    except Exception as e:
        print(f"\nError fetching movies: {e}")

    print(f"\nFinished fetching {len(data)} movies.")
    return data


def fetch_shows(client, limit=1000):
    print(f"Fetching top {limit} TV shows...")
    data = []

    try:
        # Hard cap at API limit of 1000
        limit = min(limit, 1000)

        shows_list = client.get_shows_list(
            fields=["title", "notes"], limit=limit, order="popularity", page=1
        )
        shows = shows_list.get("shows", [])

        for i, show in enumerate(shows):
            if i % 10 == 0 or i == len(shows) - 1:
                print(f"Fetching... ({len(data) + 1}/{limit})", end="\r", flush=True)

            notes = show.get("notes", {})
            data.append(
                {
                    "title": show.get("title"),
                    "total_notes": notes.get("total", 0),
                    "mean_notes": notes.get("mean", 0.0),
                }
            )

    except Exception as e:
        print(f"\nError fetching shows: {e}")

    print(f"\nFinished fetching {len(data)} shows.")
    return data


def main():
    parser = argparse.ArgumentParser(description="BetaSeries Recommender System CLI")

    parser.add_argument(
        "--type",
        choices=["movies", "shows", "both"],
        default="both",
        help="Type of content to fetch and process",
    )
    parser.add_argument(
        "--sort",
        choices=["mean_notes", "total_notes", "weighted_average"],
        default="weighted_average",
        help="Column to sort by",
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="Number of rows in the generated table"
    )
    parser.add_argument(
        "--output", required=True, help="Path to save the output CSV file"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("API_KEY")
    access_token = os.getenv("ACCESS_TOKEN")

    if not api_key:
        print("Error: API_KEY not found in environment variables.")
        sys.exit(1)

    client = BetaSeriesAPI(api_key, access_token)

    data = []

    # Hardcoded limit of 1000 per type (API max)
    # If "both", we fetch 1000 movies + 1000 shows = 2000 total items

    if args.type in ["movies", "both"]:
        data.extend(fetch_movies(client, limit=1000))

    if args.type in ["shows", "both"]:
        data.extend(fetch_shows(client, limit=1000))

    if not data:
        print("No data fetched.")
        sys.exit(0)

    df = pd.DataFrame(data)

    # Process
    try:
        result_df = process_data(
            df,
            sort_by=args.sort,
            limit=args.limit,
        )

        # Save
        result_df.to_csv(args.output, index=False)
        print(f"Successfully saved {len(result_df)} rows to {args.output}")
        print(
            result_df[["title", "weighted_average", "mean_notes", "total_notes"]].head()
        )

    except Exception as e:
        print(f"Error processing data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
