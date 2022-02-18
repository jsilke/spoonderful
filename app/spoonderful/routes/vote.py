from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.spoonderful.data import schemas, database, models
from app.spoonderful.auth import oauth2


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_on_recipe(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Voting logic that covers adding, removing, and changing votes. No recipe_id checking is performed at this time.
    """
    # TODO Refactor.
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if found_vote:
        if vote.direction == found_vote.direction:
            # Remove vote when same activity is repeated (e.g. clicking like on a liked recipe should remove the like).
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "Successfully removed vote."}
        else:
            # Switch the vote when the opposite behaviour is selected.
            new_vote = _add_vote(vote, current_user)
            vote_query.delete(synchronize_session=False)
            db.add(new_vote)
            db.commit()

            return {"message": "Successfully changed vote."}

    else:
        # Add the vote if it does not exist.
        new_vote = _add_vote(vote, current_user)
        db.add(new_vote)
        db.commit()

        return {"message": "Successfully added vote."}


def _add_vote(vote: schemas.Vote, current_user: int) -> models.Vote:
    """
    Internal function that creates a new entry for the votes table.
    """
    new_vote = models.Vote(
        post_id=vote.recipe_id,
        user_id=current_user.id,
        direction=vote.direction,
    )

    return new_vote
