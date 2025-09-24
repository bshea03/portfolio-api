from sqlalchemy.orm import Session
from app.models.skill import Skill

def shift_ranks_for_insert(skill_id: int | None, category: str, new_rank: int, db: Session):
    """
    Shift all skills in a category at or after new_rank up by 1.
    If skill_id is given, exclude that skill (so we don't shift the one being moved).
    """
    query = db.query(Skill).filter(
        Skill.category == category,
        Skill.rank >= new_rank
    )
    if skill_id is not None:
        query = query.filter(Skill.id != skill_id)

    query.update({Skill.rank: Skill.rank + 1}, synchronize_session="fetch")

def apply_rank_update(skill: Skill, new_rank: int, category: str, db: Session):
    old_rank = skill.rank
    old_category = skill.category

    if category != old_category:
        # Moving to a different category
        # First close the gap in the old category
        db.query(Skill).filter(
            Skill.category == old_category,
            Skill.rank > old_rank
        ).update({Skill.rank: Skill.rank - 1}, synchronize_session="fetch")

        # Then make room in the new category
        db.query(Skill).filter(
            Skill.category == category,
            Skill.rank >= new_rank
        ).update({Skill.rank: Skill.rank + 1}, synchronize_session="fetch")

        skill.category = category
        skill.rank = new_rank
        db.flush()
        return

    # Same category move
    if new_rank < old_rank:
        # Moving UP: shift everyone in [new_rank, old_rank-1] down
        db.query(Skill).filter(
            Skill.category == category,
            Skill.rank >= new_rank,
            Skill.rank < old_rank,
            Skill.id != skill.id
        ).update({Skill.rank: Skill.rank + 1}, synchronize_session="fetch")

    elif new_rank > old_rank:
        # Moving DOWN: shift everyone in (old_rank, new_rank] up
        db.query(Skill).filter(
            Skill.category == category,
            Skill.rank <= new_rank,
            Skill.rank > old_rank,
            Skill.id != skill.id
        ).update({Skill.rank: Skill.rank - 1}, synchronize_session="fetch")

    # Finally assign the new rank
    skill.rank = new_rank
    skill.category = category
    db.flush()
    
def normalize_ranks(db: Session, category: str | None = None):
    """
    Normalize ranks so they are sequential and unique per category.
    If category is given, normalize only that category; otherwise all categories.
    """
    query = db.query(Skill.category).distinct()
    categories = [category] if category else [row[0] for row in query]

    for cat in categories:
        skills = (
            db.query(Skill)
            .filter(Skill.category == cat)
            .order_by(Skill.rank, Skill.id)  # tie-breaker for duplicates
            .all()
        )
        for i, skill in enumerate(skills, start=1):
            skill.rank = i

    db.commit()