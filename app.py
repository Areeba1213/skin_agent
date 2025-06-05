import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="Skincare Expert",
    instructions=(
        "You are a skincare assistant who remembers the full conversation. "
        "Help users based on their previous messages."
    ),
    model=model
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("  I'm your virtual skincare & makeup advisor. Tell me about your skin — any problems, skin type, or makeup goals?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    # Store message history in session
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": message.content})

# #  Reject unrelated questions
#     if not any(keyword in user_input for keyword in SKIN_KEYWORDS):
#         await cl.Message(
#             content=" I'm only trained to help with skincare and makeup-related topics. "
#                     "Please ask something about your skin, face, or beauty routine."
#         ).send()
#         return

    
    # Add history to instructions (primitive memory simulation)
    history_text = "\n".join([f"{h['role'].capitalize()}: {h['content']}" for h in history])
    agent.instructions += f"\n\nConversation history:\n{history_text}"
    
    cl.user_session.set("history", history)

    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )

    await cl.Message(content=result.final_output).send()

