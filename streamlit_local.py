from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import streamlit  as st
# set_debug(True)

st.title("おおさこが作った chat app")
    

chat = ChatBedrock(
    credentials_profile_name='osako',    
    model_id='anthropic.claude-3-haiku-20240307-v1:0',    
    model_kwargs={
        "max_tokens":1000,
    },
    streaming=True
)

# セッション
if "messages" not in st.session_state:
    st.session_state.messages =  [
        SystemMessage(content="可愛く答えて欲しい"),    
    ]


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
    

