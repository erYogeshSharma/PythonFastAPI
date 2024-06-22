from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session


from .. import schemas, models, database, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')

    # Create a JWT token
    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
