"""
Collect Steam sub-genre tags from the Steam Store API.

Fetches the complete tag list from Steam's populartags endpoint, saves the raw
response for provenance, then filters to sub-genre tags using SteamDB's
editorial Sub-Genre category as the filter source. SteamDB imposes genre/
sub-genre structure on Steam's flat tag namespace, acting as a classificatory
system of record for tag categorization.

The filtered output includes two popularity metrics:
- steam_api_popularity_rank: position in Steam's API response (overall tag popularity)
- steamdb_subgenre_rank: position within SteamDB's Sub-Genre category listing
"""

import json
from datetime import date
from pathlib import Path

import requests


# SteamDB Sub-Genre tags, ordered by SteamDB popularity ranking.
# Source: SteamDB tag browser, Sub-Genres category (transcribed 2026-04-16).
# Value = SteamDB popularity rank within the Sub-Genre category.
STEAMDB_SUBGENRE_NAMES: dict[str, int] = {
    "Exploration": 1,
    "2D Platformer": 2,
    "Roguelite": 3,
    "FPS": 4,
    "Immersive Sim": 5,
    "Action Roguelike": 6,
    "3D Platformer": 7,
    "Choose Your Own Adventure": 8,
    "Turn-Based Tactics": 9,
    "Hidden Object": 10,
    "Side Scroller": 11,
    "Puzzle Platformer": 12,
    "Shoot 'Em Up": 13,
    "Bullet Hell": 14,
    "Hack and Slash": 15,
    "Clicker": 16,
    "Dungeon Crawler": 17,
    "Idler": 18,
    "Top-Down Shooter": 19,
    "Time Management": 20,
    "Third-Person Shooter": 21,
    "Collectathon": 22,
    "Precision Platformer": 23,
    "Real Time Tactics": 24,
    "Arena Shooter": 25,
    "Card Battler": 26,
    "Tactical RPG": 27,
    "Wargame": 28,
    "Creature Collector": 29,
    "Metroidvania": 30,
    "Souls-like": 31,
    "Runner": 32,
    "Flight": 33,
    "CRPG": 34,
    "Twin Stick Shooter": 35,
    "Match 3": 36,
    "Mystery Dungeon": 37,
    "Looter Shooter": 38,
    "Spectacle fighter": 39,
    "Roguelike Deckbuilder": 40,
    "Hero Shooter": 41,
    "Solitaire": 42,
    "Combat Racing": 43,
    "Action RTS": 44,
    "Trading Card Game": 45,
    "Sokoban": 46,
    "Boomer Shooter": 47,
    "Typing": 48,
    "Political Sim": 49,
    "Shop Keeper": 50,
    "Escape Room": 51,
    "Traditional Roguelike": 52,
    "On-Rails Shooter": 53,
    "Spelling": 54,
    "Outbreak Sim": 55,
    "Roguevania": 56,
    "Medical Sim": 57,
    "Extraction Shooter": 58,
    "Boss Rush": 59,
    "Mahjong": 60,
    "Cricket": 61,
}


def fetch_steam_tags() -> list[dict]:
    """Fetch the complete tag list from Steam's populartags endpoint."""
    url = "https://store.steampowered.com/tagdata/populartags/english"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def filter_subgenre_tags(
    all_tags: list[dict],
) -> list[dict]:
    """Filter the full tag list to SteamDB sub-genre tags only.

    Returns tags enriched with both Steam API popularity rank and SteamDB
    sub-genre rank.
    """
    subgenre_lookup = {
        name.lower(): rank for name, rank in STEAMDB_SUBGENRE_NAMES.items()
    }

    subgenre_tags = []
    for api_rank, tag in enumerate(all_tags, start=1):
        tag_name_lower = tag["name"].lower()
        if tag_name_lower in subgenre_lookup:
            subgenre_tags.append({
                "tagid": tag["tagid"],
                "name": tag["name"],
                "steam_api_popularity_rank": api_rank,
                "steamdb_subgenre_rank": subgenre_lookup[tag_name_lower],
            })

    return subgenre_tags


def main() -> None:
    output_dir = Path(__file__).parent.parent / "data" / "steam"
    output_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()

    # Fetch all tags
    print("Fetching Steam tags...")
    all_tags = fetch_steam_tags()
    print(f"  Retrieved {len(all_tags)} total tags")

    # Save raw response
    raw_path = output_dir / f"steam_tags_raw_{today}.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "fetch_date": today,
                "source_url": "https://store.steampowered.com/tagdata/populartags/english",
                "total_tags": len(all_tags),
                "tags": all_tags,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"  Raw tags saved to: {raw_path}")

    # Filter to SteamDB sub-genre tags
    subgenre_tags = filter_subgenre_tags(all_tags)
    print(f"\n  Matched {len(subgenre_tags)} sub-genre tags out of "
          f"{len(STEAMDB_SUBGENRE_NAMES)} in SteamDB list")

    # Report any SteamDB tags not found in Steam's API response
    found_names = {t["name"].lower() for t in subgenre_tags}
    missing = [
        name for name in STEAMDB_SUBGENRE_NAMES
        if name.lower() not in found_names
    ]
    if missing:
        print(f"\n  Tags in SteamDB list but NOT found in Steam API ({len(missing)}):")
        for name in missing:
            print(f"    - {name}")

    # Save filtered sub-genre tags
    subgenre_path = output_dir / "steam_subgenre_tags.json"
    with open(subgenre_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "fetch_date": today,
                "description": (
                    "Steam tags filtered to SteamDB's Sub-Genre category. "
                    "SteamDB imposes genre/sub-genre structure on Steam's flat "
                    "tag namespace, acting as a third-party editorial classification "
                    "of the folksonomy."
                ),
                "filtering_criteria": (
                    "Tags are sourced from SteamDB's Sub-Genre category, which "
                    "represents a community-maintained editorial classification "
                    "of Steam's unstructured tag list. This provides an external "
                    "authority for sub-genre categorization rather than relying "
                    "on researcher judgment for tag selection."
                ),
                "source": "SteamDB tag browser, Sub-Genres category",
                "transcription_date": "2026-04-16",
                "total_subgenre_tags": len(subgenre_tags),
                "tags": subgenre_tags,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"  Sub-genre tags saved to: {subgenre_path}")

    # Print top 25 by Steam API popularity
    print(f"\n  Top 25 sub-genre tags by Steam API popularity rank:")
    sorted_by_api = sorted(subgenre_tags, key=lambda t: t["steam_api_popularity_rank"])
    for tag in sorted_by_api[:25]:
        print(f"    API #{tag['steam_api_popularity_rank']:>3} "
              f"(DB #{tag['steamdb_subgenre_rank']:>2}): {tag['name']}")


if __name__ == "__main__":
    main()
