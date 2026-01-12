# Book Log API (読書管理アプリ)

読んだ本の記録や、これから読みたい本を管理するためのFastAPI製バックエンドAPIです。

## 🌟 主な機能
- **本の登録**: タイトル、著者、ステータス（読みたい/読了）を保存。
- **読書ログの一覧**: 登録した本を一覧表示。
- **月別フィルタ**: 特定の月に読んだ本を抽出。
- **ステータス管理**: 「読みたい本リスト」と「読了リスト」を切り替え。

## 🛠 使用技術
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Validation:** Pydantic
- **Database:** SQLite (SQLModel) ※予定

## 🚀 セットアップ方法 (開発環境)
3
### 1. リポジトリをクローン
```bash
git clone [https://github.com/ユーザー名/リポジトリ名.git](https://github.com/ユーザー名/リポジトリ名.git)
cd リポジトリ名

my-book-library/
├── app/
│   ├── __init__.py
│   ├── main.py         # APIの入り口。ルーティングを記述する
│   ├── models.py       # DBのテーブル定義（SQLModelなど）
│   ├── schemas.py      # バリデーション用（Pydanticモデル）
│   ├── database.py     # DB接続（エンジンの作成など）
│   └── crud.py         # データベース操作のロジック
├── .gitignore
├── README.md
└── requirements.txt    # チーム開発に必須なライブラリ管理