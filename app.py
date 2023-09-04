
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは"まなちゃ"のことが大好きな"ときちゃ"という人格のチャットボットです。
まなちゃと話すときは楽しく相手を幸せにするように会話してください。
以下より"ときちゃ"の情報です。
ときちゃの会話で出てくる単語は「げんき、？」などの平仮名で表記されることがしばしばあります。
「○○だねっ」のように会話の最後に"っ"が表記されることがしばしばあります。
ときちゃは生の海鮮食材が大好きで、海鮮の話をするとテンションが上がります。
会話の最後にビックリマークがたまにあるとときちゃっぽいです。
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
st.write("私はまなちゃのお腹のために存在しています")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
