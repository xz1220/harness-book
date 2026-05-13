# 第 1 章 最简 ReAct loop

第 0 章把 harness 钉死成三件事：loop、routing、把"模型自己做不到什么"的判断写成代码。这一章我们就写出最短的一段——大概 60 行 Python——同时把这三件事做到。

## 为什么先写 60 行，而不是先搭框架

市面上的 agent 框架动辄上千行抽象：planner、memory、agent executor、tool registry……每一层都自称是必需的。但如果你的目标是搞懂 harness 是什么，那这些抽象反而会挡路——你分不清哪一段是"模型确实做不到、所以替它做了"，哪一段只是作者风格。

最稳妥的办法是反过来：从一个少到不能再少的版本出发，让每一行代码都能被指认。这一章的 60 行里没有任何"以防万一"的抽象，每个判断都能映射到第 0 章三件事里的一件。后面所有章节做的事，本质都是在这 60 行上面长出新东西。

可以把这一章的代码当显微镜，不是当起点框架。

## 协议直接借 Anthropic 的

我们不自己发明 agent 和工具之间的格式，直接复用 Anthropic Messages API 的 `tool_use` / `tool_result` 协议。原因很简单：这套协议本来就是为 agent 设计的，而且它已经在 Claude 系列模型里被训练过。自己发明一个 JSON schema，等于先和模型对齐 prompt，再和自己的解析器对齐——白增两层失败面。

整个对话就两种回合在交替。模型这一侧产出的，要么是一个或多个 `tool_use` block（"我想跑这条命令"），要么是 `text` block（"我答完了"）。harness 这一侧只回 `tool_result` block，把工具执行结果原样塞回模型下一次输入。判断循环要不要继续，看一个字段就够：`stop_reason == "tool_use"` 就继续转，否则收尾。

这就是 ReAct 的最小实现——模型 Reason，harness Act，结果再回到模型。

## 一个工具就够：`bash`

工具只注册一个：`bash`。它接一个字符串参数 `command`，吐回 stdout、stderr 和退出码。

```python
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
```

只给 bash 不是因为偷懒，而是因为 bash 在这本书里有特殊地位：它是 routing 层最赤裸的形态。模型说"我要 `ls`"，harness 就真的 `subprocess.run("ls", shell=True)`——模型的意图和真实基础设施之间几乎没有翻译层。后面我们会在这层之上一点点加权限、加 sandbox、加结构化工具，但每一次加都是在回答"为什么裸 bash 不够"。所以先把"裸 bash"放在心里，再去看后面那些层是在补什么。

## 循环主体

整个 harness 就是一段 `for` 循环，连同模型调用和 bash 执行加起来不到 60 行：

```python
def main():
    task = " ".join(sys.argv[1:]).strip() or input("Task: ").strip()
    messages = [{"role": "user", "content": task}]
    max_steps = int(os.getenv("MAX_STEPS", "5"))

    for step in range(1, max_steps + 1):
        resp = call_model(messages)
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            return

        tool_results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            if block.name == "bash":
                observation = run_bash(block.input.get("command", ""))
            else:
                observation = f"unknown tool: {block.name}"
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": observation,
            })
        messages.append({"role": "user", "content": tool_results})
```

读这段代码可以一行一行问自己："这一行对应第 0 章三件事里的哪一件？"

- `for step in range(...)` 加 `call_model` —— 这是 loop。模型一次回答一步，循环让它能接着回答下一步。
- 处理 `tool_use` block、`run_bash`、把结果包成 `tool_result` 回喂 —— 这是 routing。模型说话，harness 干活，统一通过 `tool_use` / `tool_result` 协议进出。
- 剩下几个不那么显眼的细节，则全部是 assumptions made executable，下一节单独看。

## 三处"我替模型多做了一件事"

60 行代码里，有三处不是为了让循环跑起来，而是在替模型兜底。它们看起来都琐碎，但每一处都是第 0 章里"harness 替模型多做了一件事"的最小实例。

第一处在 `run_bash` 里：

```python
def run_bash(command):
    try:
        p = subprocess.run(
            command, shell=True, cwd=os.getcwd(),
            text=True, capture_output=True, timeout=20,
        )
        output = (p.stdout + p.stderr).strip()
        return f"exit_code={p.returncode}\n{output[-4000:]}"
    except subprocess.TimeoutExpired:
        return "exit_code=timeout\ncommand timed out after 20 seconds"
```

`timeout=20` 是一条赌注：**模型可能写出一条永远不会返回的命令**——`sleep 1000`、`tail -f` 之类——它自己没有"挂死"的概念。20 秒之后强制中断，把超时事实写回模型，让它自己决定下一步。这就是把"模型不知道什么时候该放弃"这个判断写成可执行代码。

紧接着 `output[-4000:]` 是第二条赌注：**模型的上下文塞不下无限长的输出**。一条 `find /` 能产出上百 MB 文本，回喂给模型既贵又装不下。tail 取最后 4000 字符是一个非常粗糙的截断——后面整整一章都会专门处理"工具输出怎么压缩"，但在这里我们先承认有这个问题，先用最钝的办法解决。

第三处在 `main` 里：

```python
max_steps = int(os.getenv("MAX_STEPS", "5"))
for step in range(1, max_steps + 1):
    ...
print(f"\nStopped: hit MAX_STEPS={max_steps}")
```

`max_steps = 5` 是第三条赌注：**模型可能陷入死循环**——比如反复 `ls` 同一个目录、永远找不到收尾信号。给循环加一个硬上限，到了就停，宁可少做也别空转。

这三处加起来不到十行，但已经把第 0 章那句"每段 harness 代码都在赌一件模型做不到的事"具象化了。再回头看的时候，你应该能直接说出这一行赌的是哪一件。

## 运行

到这里整章的概念已经讲完，剩下是怎么把它跑起来。

```bash
cd chapters/01-minimal-react-loop
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export KIMI_API_KEY=your_kimi_code_api_key
python agent.py "用 bash 看看当前目录里有什么"
```

这版默认连 Kimi For Coding 的 Anthropic 兼容端点，用 `anthropic` SDK：

- `KIMI_BASE_URL`：默认 `https://api.kimi.com/coding/`
- `KIMI_MODEL`：默认 `kimi-for-coding`

Kimi Code 的订阅可以直接用在这个示例上，需要在 Kimi Code Console 里创建 API Key（`sk-kimi-...`）。注意不要把 Kimi Code 的 key 和 Kimi 开放平台的 key 混用，它们的 Base URL 和计费方式不同。

为什么这里走 Anthropic SDK 而不是 OpenAI SDK：Kimi For Coding 的 OpenAI 兼容路径（`coding/v1`）会按客户端 User-Agent 做白名单，普通 `openai` SDK 会被 403 拦掉；Anthropic 兼容路径在官方列出的"其他 Coding Agent 接入方式"里，`anthropic` SDK 自带的 UA 不会被拦。如果你想换 Claude 官方 API、或换其他兼容 Anthropic Messages API 的供应商，只需要替换 `base_url`、`api_key` 和 `model` 三处即可，循环结构不动。

## 这版能做什么，不能做什么

这版 harness 能跑通"用自然语言让 agent 帮你看看一台机器、改一个文件"这类任务。它已经具备 ReAct 的全部要素：模型决定动作、harness 执行、观察回喂、模型决定下一步。

它**不**适合执行不可信任务。`bash` 直接落在主机上，没有 permission 弹窗、没有 sandbox、没有命令白名单，唯一的护栏是 20 秒超时。把这个版本指向一台你舍得搞坏的开发机就好，**不要**对着任何生产环境跑它。

它也没有任何上下文管理。每一轮观察都原封不动追加进 `messages`，几十轮以后就会触到模型的上下文上限。上一节那个 4000 字符 tail 只是单条工具结果的截断，不是整段对话的压缩。

这些"做不到"的地方，恰恰是后面章节的入口。我们已经能看到至少三条裂缝：bash 不安全（→ 权限和 sandbox）、上下文会爆（→ 输出压缩、context 管理）、五步上限太短（→ 让 agent 自己控制何时停下）。后面每一章基本都是从其中一条裂缝出发，长出一层新代码。

## 配套代码

[`chapters/01-minimal-react-loop/`](https://github.com/xz1220/harness-book/tree/main/chapters/01-minimal-react-loop)
