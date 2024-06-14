from fastapi import Depends, HTTPException, status, APIRouter, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, oauth2
from ..database import get_db
from ..rate_limit import rate_limited


router = APIRouter(prefix="/listing", tags=["listing"])



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ListingOut)
@rate_limited(max_calls=5, time_frame=60)
async def create_listing(request: Request, listing: schemas.CreateListing, db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    """
    Create a new listing.

    - **listing**: Data for the new listing.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - Details of the newly created listing.
    """
    new_listing= models.Listing(ownerId=current_user.id, **listing.model_dump(exclude={'ownerId'}))
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing

@router.get("/{id}", response_model=schemas.ListingOut)
@rate_limited(max_calls=5, time_frame=60)
async def get_all_listing(request: Request, id:int, db:Session= Depends(get_db)):
    """
    Retrieve a single listing by its ID.
    
    - **id**: The ID of the listing to retrieve.
    - **db**: Database session dependency.

    Returns:
    - Listing details if found.
    - HTTPException with status code 404 if listing not found.
    """
    listing = db.query(models.Listing).filter(models.Listing.id == id).first()
    return listing



@router.put("/{id}", response_model=schemas.ListingOutUpdate)
@rate_limited(max_calls=5, time_frame=60)
async def updated_listing(request: Request, id:int, listing:schemas.UpdateListing, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    """
    Update an existing listing.

    - **id**: ID of the listing to update.
    - **listing**: New data for the listing.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - Updated details of the listing.
    """
    listed = db.query(models.Listing).filter(models.Listing.id == id)
    detail_listed = listed.first()
    if detail_listed== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing by Id {id}, Not Found")
    if detail_listed.ownerId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    listing_data = listing.model_dump(exclude_unset=True)
    listing_data["updatedAt"] = datetime.now()
    listed.update(listing_data, synchronize_session=False)
    db.commit()
    return listed.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleted_listing(id:int, db:Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    """
    Delete a listing by its ID.

    - **id**: ID of the listing to delete.
    - **db**: Database session dependency.
    - **current_user**: Current authenticated user.

    Returns:
    - Response with status code 204 if successful.
    """
    listed = db.query(models.Listing).filter(models.Listing.id == id)
    detail_listed = listed.first()
    if detail_listed == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Listing By Id {id}, Not Found")
    if detail_listed.ownerId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request action")
    listed.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
