from  sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, crud, to_hira

def update_existing_books():

    db = SessionLocal()
    
    try:
        books = db.query(models.Books).all()
        print(f'全{len(books)}件のデータを更新します')
        for book in books:
            book.title_kana = to_hira.generate_hira(book.title)
        print("すべて完了しました。")
        db.commit()

    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    update_existing_books()