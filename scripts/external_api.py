import requests

#google books apiからisbnで書籍情報を取得
def get_book_info_for_isbn(isbn: str):
    url = f"https://www.googleapis.com/books/v1/volumes?"
    params = {
        "q" : isbn
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        response.raise_for_status()
        if "items" in data and len(data["items"]) > 0:
            volume_info = data["items"][0]["volumeInfo"]
            return {
                "title": volume_info.get("title", "不明"),
                "author": ", ".join(volume_info.get("authors", ["不明"])),
                "image_url": volume_info.get("imageLinks", {}).get("thumbnail", "")
            }
        else:
            print(f"Google Books API: ISBN {isbn} に該当する書籍が見つかりませんでした。")
            return None
        
    except Exception as e:
        print(f"Google Books APIリクエストエラー: {e}")
        return None


# ISBNから書籍情報を取得
def get_book_info_from_opendb(isbn: str):
    url = f"https://api.openbd.jp/v1/get?isbn={isbn.replace('-', '')}&pretty"
    # params = {
    #     "q": f"isbn:{isbn}"
    # }

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # for item in data:
        #     print(item)
# OpenBDは該当がない場合 [None] を返すのでチェック
        if data and data[0] is not None:
            summary = data[0].get("summary", {})
            # if summary["cover"] == "":
            #     cover_url = requests.get("https://image.opencover.jp/v1/cover/spine/{}.webp".format(isbn.replace("-", ""))).url
                # print(cover_url)

            # summaryから基本情報を取得
            # OpenBDは最初からフリガナ(title_kana)を持っている場合がある
            return {
                "title": summary.get("title", "不明"),
                "author": summary.get("author", "不明"),
                "image_url": summary.get("cover", ""),  # 表紙画像URL
                "title_kana": summary.get("title_kana", ""),
                "description": data[0].get("onix", {}).get("CollateralDetail", {}).get("TextContent", [{}])[0].get("Text", "")
            }
        
    except Exception as e:
        print(f"OpenBD APIリクエストエラー: {e}")

    return None

if __name__ == "__main__":
    # テストコード
    isbn = "9784297108434"
    book_info = get_book_info_from_opendb(isbn)
    print(f"ISBN: {isbn}, Title: {book_info['title']}, Author: {book_info['author']}, Image URL: {book_info['image_url']}, Title Kana: {book_info['title_kana']}, Description: {book_info['description']}")