# 第 1 章 最简 ReAct loop

> 状态：第一个可运行版本已填入

## 这一章你会做什么

从一张白纸开始，用 100 行左右代码写出最简单的 agent loop：

- 一个 `while` 循环
- 一次模型调用 → 一次工具调用 → 一次观察结果回喂
- 一个最小 `bash` 工具
- 没有 agent 框架、没有复杂抽象、没有 wrapper

## 读完这一章，你会有

- 一个能跑的 `agent.py`，依赖只有 Anthropic Python SDK
- 对 ReAct（Reason + Act）三步循环的肌肉记忆
- 理解 "agent 不是魔法，agent 是 while loop + tool call"

## 最小协议

我们直接用 Anthropic 的官方 tool calling。给模型注册一个 `bash` 工具：

```python
BASH_TOOL = {
    "name": "bash",
    "description": "Run a shell command...",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Shell command to run."},
        },
        "required": ["command"],
    },
}
```

每轮模型的回复要么是 `tool_use` block（要 harness 帮它执行命令），要么是普通 `text` block（任务完成，输出答案）。harness 只需要做两件事：

1. 如果 `stop_reason == "tool_use"`，遍历返回里的 `tool_use` block，执行命令，把结果以 `tool_result` block 形式作为下一条 `user` message 回喂给模型。
2. 否则（一般是 `stop_reason == "end_turn"`），直接结束循环——模型已经给出最终答复。

完整循环：

1. 用户给任务
2. 模型决定下一条命令（或决定收尾）
3. harness 执行 bash，包成 `tool_result`
4. 模型看到 `tool_result` 决定下一步
5. 循环直到 `stop_reason != "tool_use"`

## 运行配套代码

```bash
cd chapters/01-minimal-react-loop
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export KIMI_API_KEY=your_kimi_code_api_key
python agent.py "用 bash 看看当前目录里有什么"
```

这个版本默认调用 Kimi For Coding 的 Anthropic 兼容端点，用 `anthropic` SDK：

- `KIMI_BASE_URL`：默认 `https://api.kimi.com/coding/`
- `KIMI_MODEL`：默认 `kimi-for-coding`

Kimi Code 订阅可以用于这个示例，需要在 Kimi Code Console 里创建 API Key（`sk-kimi-...`）。不要把 Kimi Code 的 key 和 Kimi 开放平台的 key 混用；它们的 Base URL 和计费方式不同。

之所以这里用 Anthropic SDK 而不是 OpenAI SDK：Kimi For Coding 的 OpenAI 兼容路径（`coding/v1`）会按客户端做白名单，普通 `openai` SDK 直接请求会被 403 拦掉；Anthropic 兼容路径在官方文档列出的"其他 Coding Agent"接入方式里，`anthropic` SDK 自带的 UA 不会被拦。

这个版本的 `bash` 工具没有 permission 和 sandbox，只加了 20 秒超时。它适合用来理解 harness 的最小闭环，不适合执行不可信任务。

## 配套代码

[`chapters/01-minimal-react-loop/`](https://github.com/xz1220/harness-book/tree/main/chapters/01-minimal-react-loop)
