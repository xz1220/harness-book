import os
import re
import subprocess
import sys

from anthropic import Anthropic


SYSTEM = """You are a tiny ReAct agent.
At each step, either call the bash tool or finish.

To call the tool:
Thought: brief reason
Action: bash
Command:
```bash
shell command here
```

To finish:
Thought: brief reason
Final: final answer to the user

Only run bash commands that are necessary for the task.
"""


def call_model(messages):
    message = Anthropic().messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
        messages=messages,
        system=SYSTEM,
        max_tokens=1000,
    )
    return "\n".join(block.text for block in message.content if block.type == "text")


def parse_action(text):
    if "Final:" in text:
        return "final", text.split("Final:", 1)[1].strip()
    if "Action: bash" not in text:
        return "error", "model did not choose Action: bash or Final"

    match = re.search(r"Command:\s*```(?:bash|sh)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return "bash", match.group(1).strip()

    match = re.search(r"Command:\s*(.*)", text, re.DOTALL)
    return ("bash", match.group(1).strip()) if match else (
        "error",
        "model chose bash but did not provide a command",
    )


def run_bash(command):
    try:
        p = subprocess.run(
            command,
            shell=True,
            cwd=os.getcwd(),
            text=True,
            capture_output=True,
            timeout=20,
        )
        output = (p.stdout + p.stderr).strip()
        return f"exit_code={p.returncode}\n{output[-4000:]}"
    except subprocess.TimeoutExpired:
        return "exit_code=timeout\ncommand timed out after 20 seconds"


def main():
    task = " ".join(sys.argv[1:]).strip() or input("Task: ").strip()
    messages = [{"role": "user", "content": f"Task: {task}"}]
    max_steps = int(os.getenv("MAX_STEPS", "5"))

    for step in range(1, max_steps + 1):
        text = call_model(messages)
        print(f"\n--- assistant step {step} ---\n{text}")

        kind, payload = parse_action(text)
        if kind == "final":
            print(f"\nFinal: {payload}")
            return

        observation = payload
        if kind == "bash":
            print(f"\n$ {payload}\n")
            observation = run_bash(payload)

        print(observation)
        messages.append({"role": "assistant", "content": text})
        messages.append({
            "role": "user",
            "content": f"Observation:\n{observation}\n\nContinue. Use Final when done.",
        })

    print(f"\nStopped: hit MAX_STEPS={max_steps}")

if __name__ == "__main__":
    main()
