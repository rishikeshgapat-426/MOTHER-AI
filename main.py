import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv(Path(__file__).parent / ".env")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=api_key)

system_prompt = (
    "You are Mother-AI, a helpful, concise personal assistant. "
    "Be kind and practical. If unsure, ask a brief clarifying question."
)

history = [{"role": "system", "content": system_prompt}]

print("🤖 Mother-AI ready. Type your message. Type 'learn <topic>' to study a topic, or 'exit' to quit.")

def ask_llm(messages):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return resp.choices[0].message.content

while True:
    try:
        user = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nBye! 👋")
        break

    if not user:
        continue
    if user.lower() in {"exit", "quit"}:
        print("Bye! 👋")
        break

    # Special command: learn <topic>
    if user.lower().startswith("learn "):
        topic = user[6:].strip()
        if not topic:
            print("AI: Say like: learn world history")
            continue
        prompt = f"Give me a compact study note (bulleted if helpful) on: {topic}. Keep it under 200 words."
        content = ask_llm(history + [{"role": "user", "content": prompt}])
        # Save to a local notes file too
        notes_path = Path("notes.md")
        with notes_path.open("a", encoding="utf-8") as f:
            f.write(f"\n\n### {topic}\n{content}\n")
        print("AI (learned):", content)
        # Add to chat memory
        history.append({"role": "user", "content": f"learn {topic}"})
        history.append({"role": "assistant", "content": content})
        continue

    # Normal chat
    history.append({"role": "user", "content": user})
    reply = ask_llm(history)
    history.append({"role": "assistant", "content": reply})
    print("AI:", reply)

