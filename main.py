import asyncio
import streamlit as st
from client import (
    search_with_brave_api,
    search_and_summarize_results,
)

def main():
    st.title("Brave Search Client")
    st.write("Brave Search APIを使ってウェブ検索と要約を行います")

    query = st.text_input("検索クエリを入力してください:", value="FastMCP")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("検索実行"):
            if query:
                try:
                    result = asyncio.run(search_with_brave_api(query))
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

    with col2:
        if st.button("要約実行"):
            if query:
                try:
                    with st.spinner("検索中..."):
                        result = asyncio.run(search_and_summarize_results(query))

                    if result["search_result"] and result["search_result"].content:
                        content_text = result["search_result"].content[0].text

                        st.markdown("### 検索結果")
                        with st.expander("詳細な検索結果を表示", expanded=False):
                            st.text(content_text)

                        st.markdown("### 要約")
                        st.markdown(result["summary"])
                    else:
                        st.warning("検索結果が見つかりませんでした。")

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
            else:
                st.warning("検索クエリを入力してください")
if __name__ == "__main__":
    main()
