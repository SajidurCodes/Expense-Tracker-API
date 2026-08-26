from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import date as date_type
from typing import Annotated, Optional
from database import SessionLocal
from models import Transactions
from fastapi.responses import JSONResponse
from router.auth import get_current_user


router = APIRouter()


class CreateTransactions(BaseModel):


    title: str
    amount: float = Field(gt=0)
    type: str
    category: str
    date: date_type





class UpdateTransaction(BaseModel):


    title: Optional[str] = Field(default=None)
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    date: Optional[date_type] = Field(default=None)






def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/transactions')
def create_transactions(user: user_dependency,db: db_dependency,new_transaction: CreateTransactions):



    if user is None:



        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    if new_transaction.type not in ['income', 'expense']:


        raise HTTPException(
            status_code=400,
            detail='Type must be income or expense'
        )

    

    transaction_model = Transactions(
        title=new_transaction.title,
        amount=new_transaction.amount,
        type=new_transaction.type,
        category=new_transaction.category,
        date=new_transaction.date,
        owner_id=user.get('id')
    )



    db.add(transaction_model)


    db.commit()

    db.refresh(transaction_model)


    return transaction_model


@router.get('/transactions')
def read_all(user: user_dependency, db: db_dependency):



    if user is None:


        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    return db.query(Transactions).filter(Transactions.owner_id == user.get('id')).all()


@router.get('/transactions/filter')
def filter_transactions(user: user_dependency,db: db_dependency,type: Optional[str] = None,category: Optional[str] = None,minimum_amount: Optional[float] = None,maximum_amount: Optional[float] = None):




    if user is None:


        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    transaction_query = db.query(Transactions).filter(Transactions.owner_id == user.get('id'))



    if type is not None:

        if type not in ['income', 'expense']:
            raise HTTPException(
                status_code=400,
                detail='Type must be income or expense'
            )
        

        transaction_query = transaction_query.filter(Transactions.type == type)



    if category is not None:

        transaction_query = transaction_query.filter(Transactions.category == category)



    if minimum_amount is not None:
        transaction_query = transaction_query.filter(Transactions.amount >= minimum_amount)



    if maximum_amount is not None:

        transaction_query = transaction_query.filter(Transactions.amount <= maximum_amount)

    return transaction_query.all()





@router.get('/transactions/{transaction_id}')
def read_specific_transactions(user: user_dependency,db: db_dependency,transaction_id: int):



    if user is None:


        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )

    

    specific_transaction = db.query(Transactions).filter(Transactions.owner_id == user.get('id')).filter(Transactions.id == transaction_id).first()




    if specific_transaction is not None:

        return specific_transaction

    
    else:



        raise HTTPException(
            status_code=404,
            detail='Transaction not found'
        )







@router.put('/transactions/{transaction_id}')
def update_transactions(user: user_dependency,db: db_dependency,transaction_id: int,update_transaction: UpdateTransaction):




    if user is None:


        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )


    

    transaction = db.query(Transactions).filter(Transactions.owner_id == user.get('id')).filter(Transactions.id == transaction_id).first()






    if transaction is None:


        raise HTTPException(
            status_code=404,
            detail='Transaction not found'
        )

    

    if (update_transaction.type is not None and update_transaction.type not in ['income', 'expense']):



        raise HTTPException(
            status_code=400,
            detail='Type must be income or expense'
        )

    

    update_data = update_transaction.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(transaction, key, value)



    db.commit()


    db.refresh(transaction)



    return transaction


@router.delete('/transactions/{transaction_id}')
def delete_transactions(user: user_dependency,db: db_dependency,transaction_id: int):




    if user is None:


        raise HTTPException(
            status_code=401,
            detail='Failed Authentication'
        )



    transaction = db.query(Transactions).filter(Transactions.owner_id == user.get('id')).filter(Transactions.id == transaction_id).first()




    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail='Transaction not found!!!!!!'
        )




    db.query(Transactions).filter(Transactions.owner_id == user.get('id')).filter(Transactions.id == transaction_id).delete()



    db.commit()



    return JSONResponse(
        status_code=200,
        content={'message': 'Transaction deleted successfully!!!!!!!!!!!'}
    )