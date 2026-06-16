from .beginner import BEGINNER_LESSONS
from .intermediate import INTERMEDIATE_LESSONS
from .advanced import ADVANCED_LESSONS

ALL_LESSONS = {}
for _l in BEGINNER_LESSONS + INTERMEDIATE_LESSONS + ADVANCED_LESSONS:
    ALL_LESSONS[_l["id"]] = _l


def get_lesson(lesson_id):
    return ALL_LESSONS.get(lesson_id)


def list_lessons(difficulty=None):
    result = list(ALL_LESSONS.values())
    if difficulty:
        result = [l for l in result if l["difficulty"] == difficulty]
    result.sort(key=lambda x: x["order"])
    return result
