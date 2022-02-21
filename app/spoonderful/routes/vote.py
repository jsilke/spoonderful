from fastapi import status, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.spoonderful.data import schemas, database, models
from app.spoonderful.auth import oauth2
from app.spoonacular.response import SpoonacularResponse


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/new", status_code=status.HTTP_201_CREATED)
def new_vote_on_recipe(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Voting logic that covers adding a valid vote.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if not found_vote:
        if _check_recipe_id(vote.recipe_id):
            # Add the vote if it does not exist.
            new_vote = _add_vote(vote, current_user)
            db.add(new_vote)
            db.commit()

            return {"message": "Successfully added vote."}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipe id {vote.recipe_id} does not exist!",
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User has alredy voted on recipe {vote.recipe_id}",
    )


@router.delete("/remove", status_code=status.HTTP_200_OK)
def remove_vote_on_recipe(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Voting logic that covers removing votes.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if found_vote:
        # Remove vote when same activity is repeated (e.g. clicking like on a liked recipe should remove the like).
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully removed vote."}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User has not voted on {vote.recipe_id}",
    )


@router.put("/change", status_code=status.HTTP_200_OK)
def change_vote_on_recipe(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Voting logic that covers changing votes.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if found_vote:
        if vote.direction != found_vote.direction:
            # Switch the vote when the opposite behaviour is selected.
            new_vote = _add_vote(vote, current_user)
            vote_query.delete(synchronize_session=False)
            db.add(new_vote)
            db.commit()

            return {"message": "Successfully changed vote."}

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User has alredy voted on recipe {vote.recipe_id}",
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User has not voted on {vote.recipe_id}",
        )


def _add_vote(vote: schemas.Vote, current_user: int) -> models.Vote:
    """
    Internal function that creates a new entry for the votes table.
    """
    new_vote = models.Vote(
        recipe_id=vote.recipe_id,
        user_id=current_user.id,
        direction=vote.direction,
    )

    return new_vote


def _check_recipe_id(recipe_id: models.Vote.recipe_id) -> bool:
    """
    Validates the recipe id using Spoonacular's API.
    """
    spoon = SpoonacularResponse.get_recipe_from_id(recipe_id)

    return spoon.response.status_code == 200
