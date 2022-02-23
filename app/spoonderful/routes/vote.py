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
    `recipe_id` should be a valid Spoonacular recipe id and `direction` should be 0 for dislike or 1 for like.
    Confirms recipe validity using `_check_recipe_id`.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if not found_vote:
        if _check_recipe_id(vote.recipe_id):
            # Add the vote if it does not exist for a valid recipe.
            new_vote = _make_vote(vote, current_user.id)
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
    `recipe_id` should be a valid Spoonacular recipe id and `direction` should be 0 for dislike or 1 for like.
    For the vote to be removed successfully, the `direction` of the `vote` argument should match what is stored
    in the database.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if found_vote:
        if found_vote.direction == vote.direction:
            # Remove vote when same activity is repeated (e.g. clicking like on a liked recipe should remove the like).
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "Successfully removed vote."}

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User vote on recipe {vote.recipe_id} is in the opposite direction!",
        )

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User has not voted on recipe {vote.recipe_id}.",
    )


@router.put("/change", status_code=status.HTTP_200_OK)
def change_vote_on_recipe(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """
    Voting logic that covers changing votes.
    `recipe_id` should be a valid Spoonacular recipe id and `direction` should be 0 for dislike or 1 for like.
    For the vote to be changed successfully, the `direction` of the `vote` argument should oppose what is stored
    in the database.
    """
    vote_query = db.query(models.Vote).filter(
        models.Vote.recipe_id == vote.recipe_id, models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    if found_vote:
        if vote.direction != found_vote.direction:
            # Switch the vote when the opposite behaviour is selected (e.g. clicking dislike on a liked recipe).
            new_vote = _make_vote(vote, current_user.id)
            vote_query.delete(synchronize_session=False)
            db.add(new_vote)
            db.commit()

            return {"message": "Successfully changed vote."}

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Vote direction matches user vote direction for recipe {vote.recipe_id}",
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User has not yet voted on recipe {vote.recipe_id}",
        )


def _make_vote(vote: schemas.Vote, current_user_id: int) -> models.Vote:
    """
    Internal function that creates a new entry for the votes table.
    """
    new_vote = models.Vote(
        recipe_id=vote.recipe_id,
        user_id=current_user_id,
        direction=vote.direction,
    )

    return new_vote


def _check_recipe_id(recipe_id: models.Vote.recipe_id) -> bool:
    """
    Validates the recipe id using Spoonacular's API.
    """
    spoon = SpoonacularResponse.get_recipe_from_id(recipe_id)

    return spoon.response.status_code == 200
