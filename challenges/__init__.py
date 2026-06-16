from .beginner import BEGINNER_CHALLENGES
from .intermediate import INTERMEDIATE_CHALLENGES
from .advanced import ADVANCED_CHALLENGES
from .random_analyst import ANALYST_CHALLENGES

ALL_CHALLENGES = {}
for _c in BEGINNER_CHALLENGES + INTERMEDIATE_CHALLENGES + ADVANCED_CHALLENGES + ANALYST_CHALLENGES:
    ALL_CHALLENGES[_c["id"]] = _c


def get_challenge(challenge_id):
    return ALL_CHALLENGES.get(challenge_id)


def list_challenges(difficulty=None, category=None):
    result = list(ALL_CHALLENGES.values())
    if difficulty:
        result = [c for c in result if c["difficulty"] == difficulty]
    if category:
        result = [c for c in result if c["category"] == category]
    return result


def get_categories():
    seen = {}
    for c in ALL_CHALLENGES.values():
        cat = c["category"]
        diff = c["difficulty"]
        if cat not in seen:
            seen[cat] = {"name": cat, "difficulties": set(), "count": 0}
        seen[cat]["difficulties"].add(diff)
        seen[cat]["count"] += 1
    return list(seen.values())
