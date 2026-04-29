"""
Build a crosswalk mapping SteamDB sub-genre tags to VGMS controlled vocabularies.

This script maps each SteamDB sub-genre tag independently against both VGMS
Gameplay Genre (v1.3) and VGMS Mechanics (v1.1) controlled vocabularies. It
uses the crosswalk library for vocabulary-agnostic matching, with Steam/VGMS-
specific orchestration and output formatting here.

This script serves as an example of how to use the crosswalk library for a
specific folksonomy-to-controlled-vocabulary mapping project.
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

# Add project root to path so we can import the crosswalk library
sys.path.insert(0, str(Path(__file__).parent.parent))

from crosswalk.matching import (
    build_alias_map,
    find_vocab_gaps,
    is_classified,
    match_tag,
)


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_manual_classifications(path: Path) -> dict[str, dict]:
    """Load manual classifications from JSON file.

    Translates the VGMS-specific field name (vgms_term) to the generic
    library field name (cv_term) for compatibility.
    """
    if not path.exists():
        return {}
    data = load_json(path)
    raw = data.get("classifications", {})

    translated: dict[str, dict] = {}
    for tag_name, tag_data in raw.items():
        translated[tag_name] = {}
        for vocab_key in ("genre", "mechanics"):
            mapping = tag_data.get(vocab_key, {})
            entry = dict(mapping)
            if "vgms_term" in entry:
                entry["cv_term"] = entry.pop("vgms_term")
            translated[tag_name][vocab_key] = entry
    return translated


def _to_vgms_output(mapping: dict) -> dict:
    """Translate generic library field names back to VGMS-specific names for output."""
    result = dict(mapping)
    if "cv_term" in result:
        result["vgms_term"] = result.pop("cv_term")
    if "cv_broader_term" in result:
        result["vgms_broader_term"] = result.pop("cv_broader_term")
    if result.get("match_type") == "gap_source":
        result["match_type"] = "gap_steam"
    if result.get("match_type") == "gap_target":
        result["match_type"] = "gap_vgms"
    return result


def build_crosswalk(
    genre_vocab: dict,
    mech_vocab: dict,
    steam_tags: list[dict],
    manual_classifications: dict[str, dict],
) -> list[dict]:
    """Build the complete crosswalk between Steam tags and VGMS vocabularies."""
    genre_aliases = build_alias_map(genre_vocab)
    mech_aliases = build_alias_map(mech_vocab)
    mappings = []

    for tag in steam_tags:
        tag_name = tag["name"]
        manual = manual_classifications.get(tag_name, {})

        genre_result = match_tag(
            tag_name, genre_aliases,
            manual=manual.get("genre"),
            vocab=genre_vocab,
        )
        mech_result = match_tag(
            tag_name, mech_aliases,
            manual=manual.get("mechanics"),
            vocab=mech_vocab,
        )

        mappings.append({
            "steam_tag": tag_name,
            "steam_tagid": tag["tagid"],
            "steam_api_popularity_rank": tag["steam_api_popularity_rank"],
            "steamdb_subgenre_rank": tag["steamdb_subgenre_rank"],
            "genre_mapping": _to_vgms_output(genre_result),
            "mechanics_mapping": _to_vgms_output(mech_result),
        })

    return mappings


def find_all_gaps(
    genre_vocab: dict,
    mech_vocab: dict,
    mappings: list[dict],
) -> dict[str, list[dict]]:
    """Find VGMS terms from both vocabularies with no matching SteamDB tag."""
    matched_genre = set()
    matched_mech = set()

    for m in mappings:
        gm = m.get("genre_mapping") or {}
        mm = m.get("mechanics_mapping") or {}
        if gm.get("vgms_term"):
            matched_genre.add(gm["vgms_term"])
        if mm.get("vgms_term"):
            matched_mech.add(mm["vgms_term"])

    genre_gaps = [_to_vgms_output(g) for g in find_vocab_gaps(genre_vocab, matched_genre)]
    mech_gaps = [_to_vgms_output(g) for g in find_vocab_gaps(mech_vocab, matched_mech)]

    return {
        "genre_gaps": genre_gaps,
        "mechanics_gaps": mech_gaps,
    }


# ---------------------------------------------------------------------------
# Summary generation (Steam/VGMS-specific formatting)
# ---------------------------------------------------------------------------

def _count_match_types(mappings: list[dict], mapping_key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for m in mappings:
        sub = m.get(mapping_key) or {}
        mt = sub.get("match_type", "unknown")
        counts[mt] = counts.get(mt, 0) + 1
    return counts


def generate_summary(
    mappings: list[dict],
    vgms_gaps: dict[str, list[dict]],
    genre_vocab: dict,
    mech_vocab: dict,
    output_path: Path,
) -> None:
    """Generate a human-readable markdown summary of the crosswalk."""
    genre_counts = _count_match_types(mappings, "genre_mapping")
    mech_counts = _count_match_types(mappings, "mechanics_mapping")

    genre_preferred = sum(
        1 for t in genre_vocab["terms"].values() if t["term_type"] == "preferred"
    )
    mech_preferred = sum(
        1 for t in mech_vocab["terms"].values() if t["term_type"] == "preferred"
    )

    lines = [
        "# SteamDB Sub-Genre Tags to VGMS Crosswalk: Summary",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Overview",
        "",
        f"- **Total SteamDB sub-genre tags analyzed:** {len(mappings)}",
        "",
        "### Genre Mapping Results",
        f"- Exact matches: {genre_counts.get('exact', 0)}",
        f"- Partial matches: {genre_counts.get('partial', 0)}",
        f"- Steam gaps (no VGMS Genre equivalent): {genre_counts.get('gap_steam', 0)}",
        f"- VGMS Genre terms unmatched: {len(vgms_gaps['genre_gaps'])} (of {genre_preferred} preferred)",
        "",
        "### Mechanics Mapping Results",
        f"- Exact matches: {mech_counts.get('exact', 0)}",
        f"- Partial matches: {mech_counts.get('partial', 0)}",
        f"- Steam gaps (no VGMS Mechanics equivalent): {mech_counts.get('gap_steam', 0)}",
        f"- VGMS Mechanics terms unmatched: {len(vgms_gaps['mechanics_gaps'])} (of {mech_preferred} preferred)",
        "",
        "## Crosswalk Table",
        "",
        "| # | SteamDB Tag | API Rank | DB Rank | Genre Match | Genre Term | Genre Rel | Mech Match | Mech Term | Mech Rel |",
        "|---|-------------|----------|---------|-------------|------------|-----------|------------|-----------|----------|",
    ]

    for i, m in enumerate(mappings, 1):
        gm = m.get("genre_mapping") or {}
        mm = m.get("mechanics_mapping") or {}
        lines.append(
            f"| {i} | {m['steam_tag']} | {m['steam_api_popularity_rank']} | "
            f"{m['steamdb_subgenre_rank']} | "
            f"{gm.get('match_type', '-')} | {gm.get('vgms_term') or '-'} | "
            f"{gm.get('semantic_relationship') or '-'} | "
            f"{mm.get('match_type', '-')} | {mm.get('vgms_term') or '-'} | "
            f"{mm.get('semantic_relationship') or '-'} |"
        )

    # Genre gaps
    lines.extend(["", "## Steam Gaps: Tags with No VGMS Genre Equivalent", ""])
    genre_gaps_steam = [
        m for m in mappings
        if (m.get("genre_mapping") or {}).get("match_type") == "gap_steam"
        and "UNCLASSIFIED" not in (m.get("genre_mapping") or {}).get("notes", "")
    ]
    if genre_gaps_steam:
        for m in genre_gaps_steam:
            gm = m["genre_mapping"]
            lines.append(f"### {m['steam_tag']} (API #{m['steam_api_popularity_rank']}, DB #{m['steamdb_subgenre_rank']})")
            lines.append("")
            lines.append(gm.get("notes", ""))
            gap = gm.get("gap_analysis", {})
            if gap:
                lines.append("")
                lines.append(f"- **Gap type:** {gap.get('gap_type', 'N/A')}")
                lines.append(f"- **Suggested action:** {gap.get('suggested_action', 'N/A')}")
            lines.append("")
    else:
        lines.extend(["*No classified genre gaps yet.*", ""])

    # Mechanics gaps
    lines.extend(["## Steam Gaps: Tags with No VGMS Mechanics Equivalent", ""])
    mech_gaps_steam = [
        m for m in mappings
        if (m.get("mechanics_mapping") or {}).get("match_type") == "gap_steam"
        and "UNCLASSIFIED" not in (m.get("mechanics_mapping") or {}).get("notes", "")
    ]
    if mech_gaps_steam:
        for m in mech_gaps_steam:
            mm = m["mechanics_mapping"]
            lines.append(f"### {m['steam_tag']} (API #{m['steam_api_popularity_rank']}, DB #{m['steamdb_subgenre_rank']})")
            lines.append("")
            lines.append(mm.get("notes", ""))
            gap = mm.get("gap_analysis", {})
            if gap:
                lines.append("")
                lines.append(f"- **Gap type:** {gap.get('gap_type', 'N/A')}")
                lines.append(f"- **Suggested action:** {gap.get('suggested_action', 'N/A')}")
            lines.append("")
    else:
        lines.extend(["*No classified mechanics gaps yet.*", ""])

    # VGMS unmatched terms
    lines.extend([
        "## VGMS Genre Terms with No SteamDB Sub-Genre Equivalent", "",
        "| VGMS Term | Broader Term |", "|-----------|-------------|",
    ])
    for g in vgms_gaps["genre_gaps"]:
        bt = g.get("vgms_broader_term") or "Top-level"
        lines.append(f"| {g['vgms_term']} | {bt} |")

    lines.extend([
        "", "## VGMS Mechanics Terms with No SteamDB Sub-Genre Equivalent", "",
        "| VGMS Term |", "|-----------|",
    ])
    for g in vgms_gaps["mechanics_gaps"]:
        lines.append(f"| {g['vgms_term']} |")

    # Unclassified warning
    unclassified_genre = [
        m for m in mappings
        if "UNCLASSIFIED" in (m.get("genre_mapping") or {}).get("notes", "")
    ]
    unclassified_mech = [
        m for m in mappings
        if "UNCLASSIFIED" in (m.get("mechanics_mapping") or {}).get("notes", "")
    ]
    if unclassified_genre or unclassified_mech:
        lines.extend([
            "", "## Tags Pending Manual Classification", "",
            "The following tags have not been manually classified and are using "
            "automated matching only. Edit `data/crosswalk/manual_classifications.json` "
            "to provide manual mappings.", "",
        ])
        if unclassified_genre:
            lines.append(f"### Genre ({len(unclassified_genre)} tags)")
            lines.append("")
            for m in unclassified_genre:
                lines.append(f"- {m['steam_tag']}")
            lines.append("")
        if unclassified_mech:
            lines.append(f"### Mechanics ({len(unclassified_mech)} tags)")
            lines.append("")
            for m in unclassified_mech:
                lines.append(f"- {m['steam_tag']}")
            lines.append("")

    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    data_dir = Path(__file__).parent.parent / "data"

    genre_vocab = load_json(data_dir / "vgms" / "vgms_gameplay_genre.json")
    mech_vocab = load_json(data_dir / "vgms" / "vgms_mechanics.json")
    steam_data = load_json(data_dir / "steam" / "steam_subgenre_tags.json")
    steam_tags = steam_data["tags"]

    manual_path = data_dir / "crosswalk" / "manual_classifications.json"
    manual_classifications = load_manual_classifications(manual_path)

    classified_count = sum(
        1 for c in manual_classifications.values()
        if is_classified(c.get("genre", {})) or is_classified(c.get("mechanics", {}))
    )

    print(f"Loaded {len(genre_vocab['terms'])} genre terms, "
          f"{len(mech_vocab['terms'])} mechanics terms, "
          f"{len(steam_tags)} SteamDB sub-genre tags")
    print(f"Manual classifications: {classified_count} of {len(manual_classifications)} tags have entries")

    mappings = build_crosswalk(genre_vocab, mech_vocab, steam_tags, manual_classifications)
    vgms_gaps = find_all_gaps(genre_vocab, mech_vocab, mappings)

    genre_counts = _count_match_types(mappings, "genre_mapping")
    mech_counts = _count_match_types(mappings, "mechanics_mapping")

    print(f"\nGenre mapping results:")
    print(f"  Exact matches:    {genre_counts.get('exact', 0)}")
    print(f"  Partial matches:  {genre_counts.get('partial', 0)}")
    print(f"  Steam gaps:       {genre_counts.get('gap_steam', 0)}")
    print(f"  VGMS gaps:        {len(vgms_gaps['genre_gaps'])}")

    print(f"\nMechanics mapping results:")
    print(f"  Exact matches:    {mech_counts.get('exact', 0)}")
    print(f"  Partial matches:  {mech_counts.get('partial', 0)}")
    print(f"  Steam gaps:       {mech_counts.get('gap_steam', 0)}")
    print(f"  VGMS gaps:        {len(vgms_gaps['mechanics_gaps'])}")

    # Save crosswalk JSON
    crosswalk_path = data_dir / "crosswalk" / "crosswalk.json"
    crosswalk_path.parent.mkdir(parents=True, exist_ok=True)
    with open(crosswalk_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metadata": {
                    "title": "SteamDB Sub-Genre Tags to VGMS Crosswalk",
                    "date": date.today().isoformat(),
                    "methodology": (
                        "Each SteamDB sub-genre tag is independently mapped against "
                        "both VGMS Gameplay Genre (v1.3) and VGMS Mechanics (v1.1) "
                        "controlled vocabularies. Automated matching uses case-"
                        "insensitive string comparison including VGMS USE FOR aliases. "
                        "Manual classifications provide mappings requiring human "
                        "judgment, loaded from manual_classifications.json."
                    ),
                    "steam_data_date": steam_data["fetch_date"],
                    "steamdb_source": "SteamDB tag browser, Sub-Genres category",
                    "vgms_genre_version": genre_vocab["version"],
                    "vgms_mechanics_version": mech_vocab["version"],
                    "total_steamdb_tags": len(mappings),
                    "manual_classifications_count": classified_count,
                },
                "mappings": mappings,
                "vgms_unmatched": vgms_gaps,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"\nCrosswalk saved to: {crosswalk_path}")

    summary_path = Path(__file__).parent.parent / "output" / "crosswalk_summary.md"
    generate_summary(mappings, vgms_gaps, genre_vocab, mech_vocab, summary_path)
    print(f"Summary saved to: {summary_path}")


if __name__ == "__main__":
    main()
