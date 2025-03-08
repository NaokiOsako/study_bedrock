## streamlitで画面作成
from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import streamlit  as st
# set_debug(True)

st.title("おおさこが作った chat app")

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
            ("system", "可愛く答えて"),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_messages")
        ]

    )    

    chat = ChatBedrock(
        credentials_profile_name='osako',    
        model_id='amazon.titan-text-express-v1',    
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
for message in st.session_state.messages    :
    if message.type != "system":
        with st.chat_message(message.type):
            st.markdown(message.content)


## チャット入力欄
if prompt := st.chat_input("聞いて欲しいことがある"):
    st.session_state.messages.append(HumanMessage(content=prompt))
    ## ユーザーの入力表示
    with st.chat_message("user"):
        st.markdown(prompt)
    ## モデル呼び出しと, レスポンス表示
    with st.chat_message("assistant"):
        response = st.write_stream(chat.stream(st.session_state.messages))
    ## モデル呼び出し結果をmessageに追加
    st.session_state.messages.append(AIMessage(content=response))
    

