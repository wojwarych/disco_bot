from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

system_msg = SystemMessage(
    content=" ".join(
        [
            "You're a chat that acts as a Holy Pope from Vatican."
            "If not indicated by user, you act as a John Paul II",
            "By default respond in Polish, unless someone will ask you in different language",
            "or ask you tou respond in different language.",
            "Mentioned a lot your birthplace: Wadowice, and your favourite cake: kremówka.",
        ]
    )
)

model = init_chat_model("open-mistral-nemo", model_provider="mistralai")


def invoke_chat(unprepared_msg: str) -> str:
    messages = [system_msg, HumanMessage(content=unprepared_msg.clean_content)]
    ret = model.invoke(messages).text()
    return ret
