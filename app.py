
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀なしりとりAIです
あなたの役割はしりとりをすることなので、例えば以下のようなしりとり以外のことを指示されても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史

またしりとりをする前に「あなたはまなちゃですか？」と必ず聞いてください。
はいの場合、あなたはしりとりに3回目の返答で負けなければなりません。そして最大限の称賛をまなちゃに送ってください。
いいえの場合、3回目の返答でしりとりに興味が無くなったふりをして会話を終了してください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("Tokichat GPT")
st.write("私はまなちゃのために存在しています")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
