#!/usr/bin/env python3
import pandas as pd
import argparse
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Generate presence-absence matrix for protein types per genome using scores."
    )
    parser.add_argument("--infile", required=True, help="Input CSV file (nifH_candidates_allgenomes.csv)")
    parser.add_argument("--outfile", default="nifH_presence_absence_by_type_allgenomes.csv", help="Output CSV file")
    parser.add_argument(
        "--agg",
        choices=["max", "mean", "sum", "min", "median"],
        default="max",
        help="Aggregation to apply when multiple scores exist per (genome, protein_type). Default: max"
    )
    parser.add_argument(
        "--description-column",
        default="description",
        help="Column name containing the protein description (default: description)"
    )
    parser.add_argument(
        "--score-column",
        default="score",
        help="Column name containing the score (default: score)"
    )
    args = parser.parse_args()

    # Load input file
    try:
        df = pd.read_csv(args.infile)
    except Exception as e:
        print(f"[ERROR] Failed to read input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate required columns
    required_cols = {"genome", args.description_column, args.score_column}
    missing = required_cols - set(df.columns)
    if missing:
        print(f"[ERROR] Missing required columns in input: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    # Normalize protein type from description
    df["protein_type"] = (
        df[args.description_column]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Ensure scores are numeric
    df[args.score_column] = pd.to_numeric(df[args.score_column], errors="coerce")

    # Drop rows with missing score or missing genome/protein_type
    before = len(df)
    df = df.dropna(subset=["genome", "protein_type", args.score_column])
    dropped = before - len(df)
    if dropped > 0:
        print(f"[INFO] Dropped {dropped} rows due to missing genome/protein_type/score.")

    # Aggregate scores per (genome, protein_type)
    aggfunc = {
        "max": "max",
        "mean": "mean",
        "sum": "sum",
        "min": "min",
        "median": "median",
    }[args.agg]

    # Pivot to genome × protein_type matrix with aggregated scores
    matrix = (
        df.pivot_table(
            index="genome",
            columns="protein_type",
            values=args.score_column,
            aggfunc=aggfunc,
        )
        .fillna(0)  # absent → 0
        .sort_index(axis=0)
        .sort_index(axis=1)
    )

    # Save to CSV
    try:
        Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
        matrix.to_csv(args.outfile)
    except Exception as e:
        print(f"[ERROR] Failed to write output file: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] Presence-absence score matrix saved as {args.outfile}")
    print(f"Shape: {matrix.shape}")
    print("Sample output:")
    # Show up to 5 rows and 8 columns for readability
    print(matrix.iloc[:5, :8])

if __name__ == "__main__":
    main()