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

# def deal_with_annotations(message):
#     message_content = message.content[0].text
#     annotations = message_content.annotations
#     citations = []

#     # Iterate over the annotations and add footnotes
#     for index, annotation in enumerate(annotations):
#         # Replace the text with a footnote
#         message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

#         # Gather citations based on annotation attributes
#         if (file_citation := getattr(annotation, 'file_citation', None)):
#             cited_file = client.files.retrieve(file_citation.file_id)
#             citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
#         # elif (file_path := getattr(annotation, 'file_path', None)):
#         #     cited_file = client.files.retrieve(file_path.file_id)
#         #     citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
#         #     # Note: File download functionality not implemented above for brevity


#     message_content.value += '\n' + '\n'.join(citations)

for msg in messages.data[::-1]:
    if msg.role == "user":
        st.chat_message(msg.role, avatar = avatar_dic[msg.role]).write(msg.content[0].text.value)
    else:
        with st.chat_message("assistant", avatar = avatar_dic["assistant"]):
            for content in msg.content:
                if content.type =="image_file":
                    image_data = client.files.content(content.image_file.file_id)
                    image_data_bytes = image_data.read()
                    st.image(image_data_bytes, caption='Image', use_column_width=True)
                elif content.type =="text":
                    st.write(content.text.value)

if 'message_file' not in st.session_state:
    st.session_state.message_file = None


# Text files

text_contents = '''
Foo, Bar
123, 456
789, 000
'''

# Different ways to use the API

st.download_button('Download CSV', text_contents, 'text/csv')
st.download_button('anotheroe', text_contents, 'text/csv')
        

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

    st.chat_message("user", avatar = avatar_dic["user"]).write(prompt)

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            message = messages.data[0]
            with st.chat_message("assistant", avatar = avatar_dic["assistant"]):
                for content in message.content:
                    if content.type == "image_file":
                        image_data = client.files.content(content.image_file.file_id)
                        image_data_bytes = image_data.read()
                        st.image(image_data_bytes, caption='Image', use_column_width=True)
                    elif content.type == "text":
                        st.write(content.text.value)
            
            break

    
    
    



