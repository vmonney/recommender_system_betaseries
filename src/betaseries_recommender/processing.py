import pandas as pd


def calculate_weighted_average(
    df: pd.DataFrame, threshold_count: int = 250
) -> pd.DataFrame:
    """Calculate the weighted average rating for each item in the DataFrame.

    Formula:
        (R * v + C * m) / (v + m)
    Where:
        R = mean_notes (Average rating for the item)
        v = total_notes (Number of votes for the item)
        C = mean vote across the whole report
        m = minimum votes required to be listed (derived from top N popular items)
    """
    if df.empty:
        return df

    v = df["total_notes"]
    mean_notes = df["mean_notes"]
    global_mean = df["mean_notes"].mean()

    # Calculate m: total_notes of the N-th most popular item (by total_notes)
    # Note: if dataframe has fewer rows than threshold_count, take the last one (min of the set)
    if len(df) >= threshold_count:
        m = df.nlargest(threshold_count, "total_notes").iloc[-1]["total_notes"]
    else:
        m = df["total_notes"].min()

    df["weighted_average"] = ((mean_notes * v) + (global_mean * m)) / (v + m)
    return df


def process_data(
    df: pd.DataFrame,
    sort_by: str = "weighted_average",
    limit: int = 50,
    threshold_count: int = 250,
) -> pd.DataFrame:
    """Process the DataFrame: calculate weighted average, sort, and truncate."""
    if df.empty:
        return df

    # Ensure required columns exist
    required_cols = ["title", "total_notes", "mean_notes"]
    if not all(col in df.columns for col in required_cols):
        msg = f"DataFrame missing required columns: {required_cols}"
        raise ValueError(msg)

    # Calculate weighted average
    df = calculate_weighted_average(df, threshold_count)

    # Sort
    if sort_by not in df.columns:
        msg = f"Column '{sort_by}' not found in DataFrame usage for sorting."
        raise ValueError(msg)

    df_sorted = df.sort_values(sort_by, ascending=False)

    # Limit
    return df_sorted.head(limit)
