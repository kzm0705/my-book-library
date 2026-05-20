from fastapi import FastAPI ,HTTPException, Request
from fastapi import Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware 

from . import schemas, models, crud
from typing import List, Optional
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
import os

from scripts import external_api

#フロントエンドのテンプレートを返す
# main.pyがある場所からの絶対パスを取得（推奨）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
src_dir = os.path.join(BASE_DIR, "src")

#fastapiのインスタンス
app = FastAPI(title="book-library-API")

app.mount("/src", StaticFiles(directory=src_dir), name="src")

DEFAULT_IMAGE_URL = ".\\src\\Gemini_Generated_Image_9f4anq9f4anq9f4a.png"

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 全てのサイトからのアクセスを許可（開発用）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/books/", response_model=List[schemas.Book])
def reading_books( db:Session = Depends(get_db), limit : int = Query(default=5, le=100), skip : int = Query(default=0, ge=0), sort_by : str = Query(default=None)):
    
    books = crud.get_sorted_books(db=db, skip=skip, limit=limit, sort_by = sort_by)

    if books is None or not books:
      raise HTTPException(status_code=404, detail="なにも保存されていないです")
    
    for book in books:
        if book.img_url == "" or book.img_url is None:
            book.img_url = DEFAULT_IMAGE_URL
    # for book in books:
    #     print(f"{book.id} {book.title} {book.author} {book.status} {book.read_date} {book.memo} {book.isbn} {book.img_url}")
    return books

@app.post("/create", response_model=schemas.Book)
def create_book(isbn: str = Query(
        ...,
        min_length=10,
        max_length=17,
        pattern=r"^[0-9-]+$",
        description="ISBNコード（10桁または13桁、ハイフン可）"
    ),
    db: Session = Depends(get_db)
):

    # db_book = crud.created_book(db=db, book=book
    book_data = external_api.get_book_info_from_opendb(isbn=isbn)
    if book_data is None:
        raise HTTPException(status_code=404, detail="APIから情報が取得できませんでした")
    
    new_book = schemas.BookCreate(
        title=book_data["title"],
        author=book_data["author"],
        isbn=isbn,
        img_url=book_data["image_url"]
    )

    db_book = crud.created_book(db=db, book=new_book)
    print(f'正常に登録できたよ！ {db_book.id} {db_book.title} {db_book.author} {db_book.isbn} {db_book.img_url}')
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


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # HTMLに渡したいデータ
    user_data = {"name": "カズマ", "message": "デプロイ準備中！"}
    books = [
        {"title": "Python入門", "status": "読了"},
        {"title": "FastAPI実践", "status": "読書中"},
    ]
    
    # index.htmlにデータを流し込む
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": user_data, "books" : books}
    )






