"""Data helpers for the Empirical Bayes lessons.

These do the plumbing that each chapter of the book does in its "Setup"
section: get the Lahman baseball data, and build the per-player tables.
The statistics are left for you to write in the notebooks.

Data: Sean Lahman's Baseball Database (CC BY-SA 3.0). The simplest route is to
download the CSV version from https://sabr.org/lahman-database/ and unzip it
anywhere inside data/lahman/ next to this file (the loader searches subfolders).
download_lahman() tries the Chadwick Bureau's GitHub copy, which may no longer
be available at that address.
"""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data" / "lahman"
RESULTS_DIR = HERE / "results"

TABLES = ["Batting", "Pitching", "People"]
SOURCE = ("https://raw.githubusercontent.com/chadwickbureau/"
          "baseballdatabank/master/core/{name}.csv")

# The book's values from Chapter 3, used when you haven't saved your own yet.
BOOK_PRIOR = {"alpha0": 101.4, "beta0": 287.3}


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def _find(name: str) -> Path | None:
    """Find NAME.csv anywhere under data/lahman (case-insensitive)."""
    if not DATA_DIR.exists():
        return None
    target = f"{name.lower()}.csv"
    for p in sorted(DATA_DIR.rglob("*.csv")):
        if p.name.lower() == target:
            return p
    return None


def download_lahman(force: bool = False, retries: int = 3) -> None:
    """Download the three Lahman tables the lessons use, with progress."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Lahman data folder: {DATA_DIR}")
    done, failed = [], []
    for i, name in enumerate(TABLES, start=1):
        existing = _find(name)
        if existing and not force:
            print(f"[{i}/{len(TABLES)}] {name}.csv already here "
                  f"({existing.stat().st_size / 1e6:.1f} MB), skipping")
            done.append(name)
            continue
        url = SOURCE.format(name=name)
        dest = DATA_DIR / f"{name}.csv"
        for attempt in range(1, retries + 1):
            try:
                print(f"[{i}/{len(TABLES)}] Downloading {name}.csv "
                      f"(attempt {attempt}/{retries}) ...", flush=True)
                with urllib.request.urlopen(url, timeout=60) as r:
                    total = int(r.headers.get("Content-Length") or 0)
                    got, chunks, next_report = 0, [], 1e6
                    while True:
                        chunk = r.read(256 * 1024)
                        if not chunk:
                            break
                        chunks.append(chunk)
                        got += len(chunk)
                        if got >= next_report:
                            pct = f" of {total / 1e6:.1f}" if total else ""
                            print(f"      {got / 1e6:.1f}{pct} MB", flush=True)
                            next_report += 1e6
                dest.write_bytes(b"".join(chunks))
                print(f"      saved {dest.name} ({got / 1e6:.1f} MB)")
                done.append(name)
                break
            except Exception as e:  # network errors, HTTP errors
                print(f"      failed: {e}")
                if attempt < retries:
                    wait = 2 * attempt
                    print(f"      retrying in {wait} s ...", flush=True)
                    time.sleep(wait)
                else:
                    failed.append(name)
    print(f"Done: {len(done)} of {len(TABLES)} tables ready.")
    if failed:
        print("Could not download: " + ", ".join(failed))
        print("Download the CSV version from https://sabr.org/lahman-database/ "
              f"and unzip it inside {DATA_DIR}. The lessons find the files there.")


def load_table(name: str) -> pd.DataFrame:
    """Load one Lahman table (Batting, Pitching or People), downloading if needed."""
    path = _find(name)
    if path is None:
        print(f"{name}.csv not found locally, downloading ...")
        download_lahman()
        path = _find(name)
        if path is None:
            raise FileNotFoundError(f"{name}.csv not found under {DATA_DIR}")
    try:  # recent SABR releases are UTF-8 (with a byte-order mark); older ones latin-1
        return pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1", low_memory=False)


# --------------------------------------------------------------------------
# Tables used in the book's Setup sections
# --------------------------------------------------------------------------

def pitcher_ids(min_games: int | None = 3) -> set:
    """Player IDs to treat as pitchers.

    min_games=None: anyone who ever pitched (the rule in Chapters 3-5).
    min_games=3:    pitched in more than 3 games (Chapters 6 onward;
                    keeps players like Ty Cobb who pitched a few times).
    """
    pitching = load_table("Pitching")
    if min_games is None:
        return set(pitching["playerID"])
    games = pitching.groupby("playerID")["G"].sum()
    return set(games[games > min_games].index)


def player_names() -> pd.DataFrame:
    """playerID, name and bats (handedness: L, R, B or missing)."""
    people = load_table("People")
    out = people[["playerID", "bats"]].copy()
    out["name"] = (people["nameFirst"].fillna("").astype(str) + " "
                   + people["nameLast"].fillna("").astype(str)).str.strip()
    return out[["playerID", "name", "bats"]]


def career(pitcher_rule: int | None = 3, extra: bool = False) -> pd.DataFrame:
    """Career hits and at-bats for non-pitchers, one row per player.

    pitcher_rule: passed to pitcher_ids() as min_games.
    extra: also include `year` (mean season played) and `bats`.
    """
    batting = load_table("Batting")
    batting = batting[batting["AB"] > 0]
    batting = batting[~batting["playerID"].isin(pitcher_ids(pitcher_rule))]
    out = (batting.groupby("playerID")
           .agg(H=("H", "sum"), AB=("AB", "sum"), year=("yearID", "mean"))
           .reset_index())
    out["average"] = out["H"] / out["AB"]
    out = player_names().merge(out, on="playerID", how="inner")
    cols = ["playerID", "name", "H", "AB", "average"]
    if extra:
        cols += ["year", "bats"]
    return out[cols].reset_index(drop=True)


def career_with_pitchers(league: str = "NL", since: int = 1980,
                         min_ab: int = 0) -> pd.DataFrame:
    """Chapter 9's data: pitchers included, flagged in `is_pitcher`."""
    batting = load_table("Batting")
    keep = (batting["AB"] > min_ab) & (batting["lgID"] == league) & (batting["yearID"] >= since)
    batting = batting[keep]
    out = (batting.groupby("playerID")
           .agg(H=("H", "sum"), AB=("AB", "sum"), year=("yearID", "mean"))
           .reset_index())
    out["average"] = out["H"] / out["AB"]
    out["is_pitcher"] = out["playerID"].isin(pitcher_ids(3))
    out = player_names().merge(out, on="playerID", how="inner")
    return out[["playerID", "name", "H", "AB", "average", "year", "is_pitcher"]]


def hit_types(pitcher_rule: int | None = 3) -> pd.DataFrame:
    """Chapter 10's data: singles, doubles, triples, home runs and non-hits."""
    batting = load_table("Batting")
    batting = batting[batting["AB"] > 0]
    batting = batting[~batting["playerID"].isin(pitcher_ids(pitcher_rule))]
    sums = (batting.groupby("playerID")[["AB", "H", "2B", "3B", "HR"]]
            .sum(min_count=1).fillna(0).astype(int).reset_index()
            .rename(columns={"2B": "Double", "3B": "Triple"}))
    sums["Single"] = sums["H"] - sums["Double"] - sums["Triple"] - sums["HR"]
    sums["NonHit"] = sums["AB"] - sums["H"]
    out = player_names().merge(sums, on="playerID", how="inner")
    return out[["playerID", "name", "AB", "H", "Single", "Double",
                "Triple", "HR", "NonHit"]]


# --------------------------------------------------------------------------
# Passing results between lessons
# --------------------------------------------------------------------------

def save_result(key: str, value) -> None:
    """Save a small result (numbers, lists, dicts) for later lessons."""
    RESULTS_DIR.mkdir(exist_ok=True)
    path = RESULTS_DIR / "results.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data[key] = value
    path.write_text(json.dumps(data, indent=2))
    print(f"Saved '{key}' to {path.name}")


def load_result(key: str, default=None):
    """Load a result saved by an earlier lesson, or `default` if missing."""
    path = RESULTS_DIR / "results.json"
    if path.exists():
        data = json.loads(path.read_text())
        if key in data:
            return data[key]
    if default is not None:
        print(f"No saved '{key}' yet; using the fallback {default}")
    return default


def load_prior() -> tuple[float, float]:
    """alpha0, beta0 from Lesson 02 if saved, otherwise the book's values."""
    p = load_result("prior", BOOK_PRIOR)
    return float(p["alpha0"]), float(p["beta0"])
