import asyncio
import argparse
import os
from dotenv import load_dotenv
from fastmcp import Client
import openai

load_dotenv()

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_config():
    return {
        "mcpServers": {
            "brave-search": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-brave-search"
                ],
                "env": {
                    "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")
                },
                "transport": "stdio"
            },
            "firecrawl-mcp": {
                "command": "npx",
                "args": [
                    "-y",
                    "firecrawl-mcp"
                ],
                "env": {
                    "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
                    "FIRECRAWL_RETRY_MAX_ATTEMPTS": "5",
                    "FIRECRAWL_RETRY_INITIAL_DELAY": "2000",
                    "FIRECRAWL_RETRY_MAX_DELAY": "30000",
                    "FIRECRAWL_RETRY_BACKOFF_FACTOR": "3",
                    "FIRECRAWL_CREDIT_WARNING_THRESHOLD": "2000",
                    "FIRECRAWL_CREDIT_CRITICAL_THRESHOLD": "500"
                },
                "transport": "stdio"
            }
        }
    }

async def execute_brave_search(client: Client, query: str):
    """Brave Search APIを使って検索を実行"""
    # 利用可能なツールを取得
    tools = await client.list_tools()
    print("ツール:", tools)

    # ツールの呼び出し
    result = await client.call_tool("brave_web_search", {"query": query})
    print("ツール呼び出し結果:", result)
    return result

async def summarize_text(text: str) -> str:
    """OpenAI APIを使ってテキストを要約"""
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": "あなたは検索結果を日本語で要約するアシスタントです。重要なポイントを簡潔にまとめてください。"
                },
                {
                    "role": "user",
                    "content": f"以下のテキストを要約してください:\n\n{text}"
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"要約エラー: {str(e)}"

async def search_and_summarize_results(query: str):
    """検索を実行し、結果をOpenAI APIで要約する"""
    search_result = await search_with_brave_api(query)

    if search_result and search_result.content:
        content_text = search_result.content[0].text
        summary = await summarize_text(content_text)
        return {
            "search_result": search_result,
            "summary": summary
        }
    return {
        "search_result": search_result,
        "summary": "要約できる内容がありませんでした。"
    }

async def search_with_brave_api(query: str):
    """Brave Search APIでクエリを検索する"""
    transport = create_config()

    async with Client(transport) as client:
        return await execute_brave_search(client, query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FastMCP Brave Search Client')
    parser.add_argument('query', nargs='?', help='検索クエリ')
    
    args = parser.parse_args()

    if not args.query:
        print("❌ エラー: queryを指定してください")
        
    else:
        asyncio.run(search_with_brave_api(args.query))
