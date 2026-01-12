from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import schemas, models


def created_book(db: Session, book: schemas.BookCreate):
    db_book = models.Books(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip:int = 0, limit: int = 100):
    return db.query(models.Books).offset(skip).limit(limit).all()


#特定の行を更新する, 任意の列を更新する
def update_book(db: Session, book: schemas.BookUpdate, id : int):
    #idで一致する行を検索
    db_book = db.query(models.Books).filter(models.Books.id == id).first()
    if db_book is None:
        return None
    #クエリパラメータからの入力値を変更したい値として、モデルで管理し選択した行でキーが一致する列の値を更新する
    new_book = book.model_dump(exclude_unset=True)
    # for k, v in db_book.__dict__.items():
    #     print(f'key: {k} value : {v}')
    for k,v in new_book.items():
        setattr(db_book, k, v)
    # for k, v in db_book.__dict__.items():
    #     print(f'key: {k} value : {v}')
    # db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

#idで検索して削除する機能
def del_book(id: int, db : Session) -> None | dict :
    db_book = db.query(models.Books).filter(id == models.Books.id).first()
    if db_book is None:
        return None

    title = db_book.title
    db.delete(db_book)
    db.commit()
    return {"title": title ,"message": f"User with ID {id} deleted successfully"}

#名前検索できる機能
def search_books_by_title(db: Session, title : str) -> None| dict:
    # .contains(keyword) を使うことで「あいまい検索（LIKE %keyword%）」になる
    db_book = db.query(models.Books).filter(models.Books.title.contains(title)).all()
    return db_book