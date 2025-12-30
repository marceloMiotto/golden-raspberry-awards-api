import re
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Tuple, Any

from sqlalchemy import select, func
from app.db.models import Movie


def get_winners(db):
    stmt = (
        select(Movie.producers, Movie.year)
        .where(func.trim(func.lower(Movie.winner)) == "yes")
    )
    return db.execute(stmt).all()


def _parse_producers(producers_str: str) -> List[str]:
    if not producers_str:
        return []

    normalized = re.sub(r"\s+and\s+", ",", producers_str.strip(), flags=re.IGNORECASE)
    parts = [p.strip() for p in normalized.split(",")]
    return [p for p in parts if p]


def calculate_intervals(winners: Iterable[Tuple[str, int]]) -> Dict[str, List[Dict[str, Any]]]:
    years_by_producer: DefaultDict[str, List[int]] = defaultdict(list)

    for producers_str, year in winners:
        if not producers_str or year is None:
            continue

        for producer in _parse_producers(producers_str):
            years_by_producer[producer].append(year)

    all_intervals: List[Dict[str, Any]] = []

    for producer, years in years_by_producer.items():
        unique_years = sorted(set(years))
        if len(unique_years) < 2:
            continue

        for prev_year, next_year in zip(unique_years, unique_years[1:]):
            all_intervals.append({
                "producer": producer,
                "interval": next_year - prev_year,
                "previousWin": prev_year,
                "followingWin": next_year
            })

    if not all_intervals:
        return {"min": [], "max": []}

    min_val = min(item["interval"] for item in all_intervals)
    max_val = max(item["interval"] for item in all_intervals)

    return {
        "min": [i for i in all_intervals if i["interval"] == min_val],
        "max": [i for i in all_intervals if i["interval"] == max_val],
    }


def get_awards_intervals(db) -> dict:
    winners = get_winners(db)
    return calculate_intervals(winners)
