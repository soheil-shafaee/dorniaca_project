from fastapi import status, Depends, HTTPException, APIRouter, Response, Request
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db
from ..rate_limit import rate_limited

router= APIRouter(prefix="/users", tags=["Users"])



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutPublic)
@rate_limited(max_calls=5, time_frame=60)
def create_user(request: Request, user: schemas.UserCreate, db: Session= Depends(get_db)):
    """
    Create a new user.

    - **user**: Data for the new user.
    - **db**: Database session dependency.

    Returns:
    - Details of the newly created user.
    """
    user.hashedPassword= utils.hash(user.hashedPassword)
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOutPrivate)
@rate_limited(max_calls=5, time_frame=60)
def get_user(request: Request, id:int, db: Session= Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    """
    Retrieve a user by their ID.

    - **id**: The ID of the user to retrieve.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - User details if found.
    - HTTPException with status code 404 if user not found.
    - HTTPException with status code 403 if current user is not authorized.
    """
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User By Id {id}, Not Found!")
    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    return user


@router.put("/{id}", response_model=schemas.UserOutPrivate)
@rate_limited(max_calls=5, time_frame=60)
def update_user(request: Request, id:int, user:schemas.UserUpdate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    """
    Update an existing user.

    - **id**: ID of the user to update.
    - **user**: New data for the user.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - Updated details of the user.
    """
    updated_user_query = db.query(models.Users).filter(models.Users.id == id)
    new_user = updated_user_query.first()
    if new_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User By Id {id}. Not Found!!")
    if current_user.id != new_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    user.hashedPassword = utils.hash(user.hashedPassword)
    update_data= user.model_dump(exclude_unset=True)
    updated_user_query.update(update_data, synchronize_session=False)
    db.commit()
    return updated_user_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session= Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    """
    Delete a user by their ID.

    - **id**: ID of the user to delete.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - Response with status code 204 if successful.
    """
    user = db.query(models.Users).filter(models.Users.id == id)
    find_user = user.first()
    if find_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User by Id {id}, Not Found")
    if current_user.id != find_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    