"""
Vocabulary-agnostic matching functions for folksonomy-to-controlled-vocabulary
crosswalk construction.

These functions operate on any controlled vocabulary that uses thesaurus
conventions (preferred/non-preferred terms, USE FOR aliases) and any source
tag list. They provide automated string matching and gap analysis, with
support for manual classifications that override automated results.

Vocabulary JSON format expected:
    {
        "vocabulary": "Name",
        "terms": {
            "Preferred Term": {
                "term_type": "preferred",
                "use_for": ["Alias 1", "Alias 2"],
                "scope_note": "Definition",
                "broader_term": "Parent" (optional),
                "narrower_terms": [...] (optional),
                "related_terms": [...] (optional)
            },
            "Alias 1": {
                "term_type": "non-preferred",
                "use": "Preferred Term"
            }
        }
    }

Source tags format expected:
    [{"name": "Tag Name", ...}, ...]
    Additional fields (rank, id, etc.) are preserved in output.
"""

from typing import Any


def build_alias_map(vocab: dict) -> dict[str, dict]:
    """Build a lookup from lowercase aliases to preferred term info.

    Works on any vocabulary whose terms have term_type and use_for fields.
    Maps preferred term names AND their USE FOR aliases to the preferred
    term entry.
    """
    alias_map: dict[str, dict] = {}

    for term_name, term_data in vocab["terms"].items():
        if term_data["term_type"] == "non-preferred":
            continue
        entry = {
            "preferred_term": term_name,
            "term_data": term_data,
        }
        alias_map[term_name.lower()] = entry
        for alias in term_data.get("use_for", []):
            alias_key = alias.lower()
            if alias_key not in alias_map:
                alias_map[alias_key] = entry

    return alias_map


def auto_match(tag_name: str, alias_map: dict) -> dict | None:
    """Attempt automated case-insensitive matching of a tag against an alias map.

    Returns a match result dict if found, or None if no match.
    """
    tag_lower = tag_name.lower()
    if tag_lower in alias_map:
        match = alias_map[tag_lower]
        return {
            "match_type": "exact",
            "cv_term": match["preferred_term"],
            "confidence": "high",
            "semantic_relationship": "equivalent",
            "notes": "Automated exact match (case-insensitive).",
        }
    return None


def find_vocab_gaps(vocab: dict, matched_terms: set[str]) -> list[dict]:
    """Find preferred terms in a vocabulary that have no matching source tag.

    Returns a list of gap entries for unmatched preferred terms.
    """
    gaps = []
    for term_name, term_data in vocab["terms"].items():
        if term_data["term_type"] != "preferred":
            continue
        if term_name in matched_terms:
            continue
        gap: dict[str, Any] = {
            "cv_term": term_name,
            "match_type": "gap_target",
            "notes": "Controlled vocabulary term with no corresponding source tag.",
        }
        if "broader_term" in term_data:
            gap["cv_broader_term"] = term_data.get("broader_term")
        gaps.append(gap)

    return gaps


def is_classified(mapping: dict) -> bool:
    """Check if a manual classification entry has been filled in."""
    return bool(mapping.get("match_type"))


def empty_mapping() -> dict:
    """Return an empty/unclassified mapping result."""
    return {
        "match_type": "gap_source",
        "cv_term": None,
        "confidence": "low",
        "semantic_relationship": "no_match",
        "notes": "UNCLASSIFIED: needs manual review.",
    }


def match_tag(
    tag_name: str,
    alias_map: dict,
    manual: dict | None = None,
    vocab: dict | None = None,
) -> dict:
    """Match a single tag against a vocabulary.

    Checks manual classification first (if provided and filled in),
    then falls back to automated matching. Enriches result with
    broader_term info if the vocabulary provides it.

    Args:
        tag_name: The source tag name to match.
        alias_map: Alias map built from the target vocabulary.
        manual: Manual classification dict for this tag/vocab (optional).
        vocab: The target vocabulary dict, for broader_term lookup (optional).

    Returns:
        A match result dict.
    """
    if manual and is_classified(manual):
        result = dict(manual)
        # Add broader term info if available
        if result.get("cv_term") and vocab:
            cv_term = result["cv_term"]
            if cv_term in vocab.get("terms", {}):
                term_data = vocab["terms"][cv_term]
                if "broader_term" in term_data:
                    result["cv_broader_term"] = term_data.get("broader_term")
        return result

    result = auto_match(tag_name, alias_map)
    if result and result.get("cv_term") and vocab:
        cv_term = result["cv_term"]
        if cv_term in vocab.get("terms", {}):
            term_data = vocab["terms"][cv_term]
            if "broader_term" in term_data:
                result["cv_broader_term"] = term_data.get("broader_term")
    if result is None:
        result = empty_mapping()

    return result
