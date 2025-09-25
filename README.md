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

- [The FastMCP Client](https://gofastmcp.com/clients/client#the-fastmcp-client)


# やりたいこと

- webで検索
- 要約

# 参考

- [マルチAIエージェントシステム開発ガイド: LangGraphとMCPによるバックエンドからStreamlitでのUI構築まで](https://zenn.dev/hiratsukaaa682/articles/d03653b8ed6fa3)
- [MCPサーバーおすすめ31選！AIエージェントと連携](https://miralab.co.jp/media/mcp_recommended_servers_ai_agents/#index_id12)
