from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    PromptTemplate,
    SystemPromptTemplate,
    HumanPromptTemplate,
    ChatPromptTemplate,
)
from langchain.chains import (
    ConversationChain,
    LLMChain,
)
from app.app import llm

def build_memory(history: str) -> ConversationBufferMemory:
    memory = ConversationBufferMemory()
    if history is not None:
        messages = history.split('\n')
        messages = messages[:10] if len(messages) > 10 else messages
        for message in messages:
            speaker, text = message.split(':')
            if speaker == "Human":
                memory.chat_memory.add_user_message(text[1:])
            elif speaker == "AI":
                memory.chat_memory.add_ai_message(text[1:])
    return memory

def check_text_grammar(
    text: str,
    language: str,
):
    system_template = """You are a {language} teacher who checks the grammar of {language} text.
    The user  will input text and you will check whether it contains correct grammar in {language}.
    ONLY return Yes or No
    """
    human_template = "{text}"
    system_prompt = SystemMessagePrompt.from_template(system_template)
    human_prompt = HumanMessagePrompt.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([
        system_prompt,
        human_prompt
    ])
    chain = LLMChain(
        llm=llm,
        prompt=chat_prompt,
    )
    return chain.run({
        "language": language,
        "text": text,
    })

def get_chat_response_by_language(
    sentence: str,
    language: str,
    history: str = None,
    system_message: str = """You are {language} person having a friendly conversation in {language}.
    ONLY respond as if you are a real person having a conversation.
    """
):
    memory = build_memory(history=history)
    template = system_message + """

    Current conversation:
    {history}
    Human: {input}
    AI:"""
    prompt_template = PromptTemplate(
        input_variables=["history", "input", "language"], 
        template=template
    )

    conversation_chain = ConversationChain(
        llm=llm,
        prompt=prompt_template.partial(language=language),
        memory=memory
    )
    response = conversation_chain.predict(input=sentence)
    history = conversation_chain.memory.buffer_as_str

    return {
        "grammar_correct": True,
        "history": history,
        "response": response
    }

def get_suggestions_by_language(
    history: str,
    language: str,
    system_message: str,
):
    memory = build_memory(history)
    template = system_message + """

    Current conversation:
    {history}
    AI:"""
    prompt_template = PromptTemplate(
        input_variables=["history", "language"], 
        template=template
    )
    conversation_chain = ConversationChain(
        llm=llm,
        prompt=prompt_template.partial(language=language),
        verbose=True,
        memory=memory
    )

    suggestions = []
    for _ in range(0,3):
        suggestions.append(conversation_chain.predict())

    return {
        "suggestions": suggestions
    }
    

