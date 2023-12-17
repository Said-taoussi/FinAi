from openai import OpenAI
import streamlit as st

OPENAI_API_KEY = "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"
avatar_dic = {"assistant": "🤖", "user": "🐶"}


# the sidebar
with st.sidebar:
    """
    ## About the FinAI
    FinApp is ...

    """

    openai_api_key = OPENAI_API_KEY#st.text_input("Put your OpenAI API Key here :", key="chatbot_api_key", type="password")
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "---"
    uploaded_file = st.file_uploader("Upload a file", type=("c", "cpp", "docx", "html", "java", "json", "md", "pdf", "php", "pptx", "py", "py", "rb", "tex", "txt"))

# def arabic_page():
#     pass

# def latin_page():
#     pass



@st.cache_data
def initialize():
    client = OpenAI(api_key=openai_api_key)
    thread_id = client.beta.threads.create().id
    assistant_id = "asst_Sqa1ly27CcP2oPrySxMTkXSU"
    return assistant_id, thread_id

st.title("💵 FinAI")
st.caption("Your personal financial assistant")


assistant_id, thread_id = initialize()

client = OpenAI(api_key=openai_api_key)
messages = client.beta.threads.messages.list(thread_id=thread_id)



for msg in messages.data[::-1]:
    st.chat_message(msg.role, avatar = avatar_dic[msg.role]).write(msg.content[0].text.value)

if 'message_file' not in st.session_state:
    st.session_state.message_file = None


 
        

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()
    
    
    if uploaded_file:
        st.session_state.message_file = client.files.create(
            file= uploaded_file,
            purpose='assistants'
        )
    else:
        if st.session_state.message_file:
            client.files.delete(st.session_state.message_file.id)
            st.session_state.message_file = None
            
    


    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
        file_ids=[] if not st.session_state.message_file else [st.session_state.message_file.id]
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            response_msg = messages.data[0].content[0].text.value
            break

    
    st.chat_message("user", avatar = avatar_dic["user"]).write(prompt)
    st.chat_message("assistant", avatar = avatar_dic["assistant"]).write(response_msg)
