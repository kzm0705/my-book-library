from fastapi import FastAPI ,HTTPException
from fastapi import Depends, Query
from . import schemas, models, crud
from typing import List, Optional
from .database import engine, SessionLocal
from sqlalchemy.orm import Session



app = FastAPI(title="book-library-API")


models.Base.metadata.create_all(bind=engine)


# fake_db : List[schemas.Book] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/books/", response_model=List[schemas.Book])
def reading_books( db:Session = Depends(get_db), limit : int = Query(default=5, le=100), skip : int = Query(default=0, ge=0), sort_by : str = Query(default=None)):
    
    result = crud.get_sorted_books(db=db, skip=skip, limit=limit, sort_by = sort_by)

    if result is None or not result:
      raise HTTPException(status_code=404, detail="なにも保存されていないです")
    return result


@app.post("/create", response_model=schemas.Book)
def create_book(book : schemas.BookCreate, db : Session = Depends(get_db)):
    db_book = crud.created_book(db=db, book=book)
    return db_book


@app.put("/update/{id}", response_model=schemas.Book)
def update_book( id : int , book: schemas.BookUpdate ,db : Session = Depends(get_db) ):
    db_book = crud.update_book(db=db, id=id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Search error: No account with this name exists")
    return db_book

@app.delete("/delete/{id}")
def delete_book(id: int, db : Session = Depends(get_db) ):
    result = crud.del_book(id=id, db=db)
    if result is None:
        raise HTTPException(status_code=404 , detail="Search error: No account with this name exists")
    return result

#名前検索機能
@app.get("/books/search", response_model=List[schemas.Book])
def search_books( title : str, db : Session = Depends(get_db)):
    result = crud.search_books_by_title(title=title, db=db)

    return result





