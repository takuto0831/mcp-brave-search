# How to

- brave search api keyを取得する

参考: https://brave.com/search/api/

- .env を作成して, API Keyを登録してください

```
BRAVE_API_KEY=YOUR_API_KEY
```

- 必要なmoduleを用意する

```
uv sync
```

- streamlit 上で brave search の検索結果を確認する

```
uv run streamlit run main.py
```

参考: https://gofastmcp.com/clients/client#the-fastmcp-client

