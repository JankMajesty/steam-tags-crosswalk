"""
Internal matching helpers for the SteamDB / VGMS crosswalk pipeline.

These functions implement vocabulary-agnostic alias matching and gap analysis,
used by `scripts/build_crosswalk.py`. Extracting them as a fully general-purpose
library is left as future work; see the README.
"""

from crosswalk.matching import (
    auto_match,
    build_alias_map,
    empty_mapping,
    find_vocab_gaps,
    is_classified,
    match_tag,
)

__all__ = [
    "auto_match",
    "build_alias_map",
    "empty_mapping",
    "find_vocab_gaps",
    "is_classified",
    "match_tag",
]
