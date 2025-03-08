## langchain 使ってみた

from langchain.globals import set_debug
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# set_debug(True)

chat = ChatBedrock(
    credentials_profile_name='osako',    
    model_id='anthropic.claude-3-haiku-20240307-v1:0',    
    model_kwargs={
        "max_tokens":1000,
    },
    streaming=True
)

messages = [
    SystemMessage(content="100文字で答えて"),    
    HumanMessage(content="筋トレしんどい助けて"),
]

# response = chat.invoke(messages)
# print(response.content)
## streaming
for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)
