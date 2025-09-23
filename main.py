import asyncio
import streamlit as st
from client import search_word

def main():
    print("Hello from brave-search!")


def main():
    st.title("Brave Search Client")
    st.write("Brave Search APIを使ってウェブ検索を行います")

    query = st.text_input("検索クエリを入力してください:", value="FastMCP")

    if st.button("検索実行"):
        if query:
            try:
                result = asyncio.run(search_word(query))
                print("=== デバッグ情報 ===")
                print(f"Result Contents type: {type(result.content)}")
                print(f"Result Contents item type: {type(result.content[0])}")
                print(f"Result Contents item text type: {type(result.content[0].text)}")
                print(f"Result Contents item: {result.content[0].text}")
                content_text = result.content[0].text if result.content else []

                if content_text != []:
                    st.markdown("### 検索結果")
                    st.markdown(f"### 結果 {content_text}")
                        
                else:
                    st.warning("検索結果が見つかりませんでした。")
                    
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("検索クエリを入力してください")
if __name__ == "__main__":
    main()
