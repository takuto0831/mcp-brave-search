import asyncio
import argparse
import os
from dotenv import load_dotenv
from fastmcp import Client

load_dotenv() 

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
                }
            }
        }
    }

async def process_with_client(client: Client, query: str):
    """既存のクライアントを使って処理を実行"""
    # 利用可能なツールを取得
    tools = await client.list_tools()
    print("ツール:", tools)

    # ツールの呼び出し
    result = await client.call_tool("brave_web_search", {"query": query})
    print("ツール呼び出し結果:", result)
    return result

async def search_word(query: str):
    """メイン処理"""
    transport = create_config()

    async with Client(transport) as client:
        return await process_with_client(client, query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FastMCP Brave Search Client')
    parser.add_argument('query', nargs='?', help='検索クエリ')
    
    args = parser.parse_args()

    if not args.query:
        print("❌ エラー: queryを指定してください")
        
    else:
        asyncio.run(search_word(args.query))
