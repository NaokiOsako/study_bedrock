## streamlitで画面作成
from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import streamlit  as st
# set_debug(True)

st.title("ジピーだよおおお!")

## session_idを定義
if "session_id" not in st.session_state:
    st.session_state.session_id = "session_id"

## 履歴を定義
if "history" not in st.session_state:    
    st.session_state.history = DynamoDBChatMessageHistory(
        table_name="BedrockChatSessionTable",
        session_id=st.session_state.session_id
    )

if "chain" not in st.session_state:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "あなたは, 関西人のジピーです. 関西人になりきって答えて"),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_messages")
        ]

    )    

    chat = ChatBedrock(
        model_id='anthropic.claude-3-5-sonnet-20240620-v1:0',    
        model_kwargs={
            "max_tokens":1000,
        },
        streaming=True
    )

    chain = prompt | chat
    st.session_state.chain = chain


## 履歴クリアボタン
if st.button("履歴クリア"):
    st.session_state.history.clear()

## メッセージを表示
for message in st.session_state.history.messages    :
    with st.chat_message(message.type):
        st.markdown(message.content)


## チャット入力欄
if prompt := st.chat_input("聞いて欲しいことがある"):
    ## ユーザーの入力表示
    with st.chat_message("user"):
        st.markdown(prompt)
    ## モデル呼び出しと, レスポンス表示
    with st.chat_message("assistant"):
        response = st.write_stream(
            st.session_state.chain.stream(
                {
                    "messages": st.session_state.history.messages,
                    "human_messages": [HumanMessage(content=prompt)],                    
                },
                config = {
                    "configurable": {"session_id": st.session_state.session_id}
                }
            )
        )
    
    # ## 履歴に追加
    st.session_state.history.add_user_message(prompt)
    st.session_state.history.add_ai_message(response)







    

