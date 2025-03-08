from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# set_debug(True)

chat = ChatBedrock(
    credentials_profile_name='osako',    
    model_id='amazon.titan-text-express-v1',    
    model_kwargs={
        "max_tokens":1000,
    },
    streaming=True
)

messages = [
    HumanMessage(content="どんな会社?, 1000文字で答えて"),
]

# response = chat.invoke(messages)
# print(response.content)
## streaming
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)

