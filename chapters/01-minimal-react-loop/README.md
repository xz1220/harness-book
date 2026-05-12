# Chapter 1 — 最简 ReAct loop

配套书的章节：[第 1 章](../../docs/01-minimal-react-loop.md)

## 状态

已填入第一个可运行版本：`agent.py`。

## 运行

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export KIMI_API_KEY=your_kimi_code_api_key
python agent.py "用 bash 看看当前目录里有什么"
```

可选环境变量：

- `KIMI_BASE_URL`：默认 `https://api.kimi.com/coding/`
- `KIMI_MODEL`：默认 `kimi-for-coding`
- `MAX_STEPS`：默认 `5`

这个示例走 Kimi For Coding 的 Anthropic 兼容端点，用 `anthropic` SDK 调用。需要在 Kimi Code Console 里创建 API Key（`sk-kimi-...`）。注意 Kimi Code 和 Kimi 开放平台不是同一套 key：开放平台的 key 走 `https://api.moonshot.ai/v1`，跟这里默认的 endpoint 不通。

> 为什么是 Anthropic SDK 而不是 OpenAI SDK：Kimi For Coding 的 `coding/v1` OpenAI 兼容路径会按客户端做白名单，普通 `openai` SDK 会被 403 拦掉；它的 Anthropic 兼容路径 (`coding/`) 则在官方文档列出的"其他 Coding Agent"接入方式里，`anthropic` SDK 自带的 UA 不会被拦。

## 这个版本故意只做三件事

- 调模型，让模型输出 `Thought / Action / Command` 或 `Final`
- 解析 `Action: bash`
- 执行命令，把 `Observation` 回喂给模型

这里还没有 permission、sandbox、工具 schema、并行工具调用和上下文压缩。这些会放到后续章节。
