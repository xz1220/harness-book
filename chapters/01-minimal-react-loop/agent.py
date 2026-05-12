import os
import subprocess
import sys

from anthropic import Anthropic

SYSTEM = """You are a tiny ReAct agent.
You have one tool: `bash`. Call it to inspect or act on the system.
When you have enough information to answer the user, stop calling tools and reply with plain text.
Only run bash commands that are necessary for the task.
"""

BASH_TOOL = {
    "name": "bash",
    "description": "Run a shell command. Returns combined stdout+stderr (tail-truncated) and the exit code.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Shell command to run."},
        },
        "required": ["command"],
    },
}


def call_model(messages):
    client = Anthropic(
        api_key=os.environ["KIMI_API_KEY"],
        base_url=os.getenv("KIMI_BASE_URL", "https://api.kimi.com/coding/"),
    )
    return client.messages.create(
        model=os.getenv("KIMI_MODEL", "kimi-for-coding"),
        max_tokens=1000,
        system=SYSTEM,
        tools=[BASH_TOOL],
        messages=messages,
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
    messages = [{"role": "user", "content": task}]
    max_steps = int(os.getenv("MAX_STEPS", "5"))

    for step in range(1, max_steps + 1):
        resp = call_model(messages)
        print(f"\n--- assistant step {step} (stop_reason={resp.stop_reason}) ---")
        for block in resp.content:
            if block.type == "text" and block.text.strip():
                print(block.text)
            elif block.type == "tool_use":
                print(f"[tool_use {block.name}] {block.input}")

        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            return

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            if block.name == "bash":
                command = block.input.get("command", "")
                print(f"\n$ {command}")
                observation = run_bash(command)
            else:
                observation = f"unknown tool: {block.name}"
            print(observation)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": observation,
            })
        messages.append({"role": "user", "content": tool_results})

    print(f"\nStopped: hit MAX_STEPS={max_steps}")


if __name__ == "__main__":
    main()
