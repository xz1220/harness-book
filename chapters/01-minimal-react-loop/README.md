# Chapter 1 — 最简 ReAct loop

配套书的章节：[第 1 章](../../docs/01-minimal-react-loop.md)

## 状态

已填入第一个可运行版本：`agent.py`。

## 运行

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_api_key
python agent.py "用 bash 看看当前目录里有什么"
```

可选环境变量：

- `ANTHROPIC_MODEL`：默认 `claude-sonnet-4-5`
- `MAX_STEPS`：默认 `5`

## 这个版本故意只做三件事

- 调模型，让模型输出 `Thought / Action / Command` 或 `Final`
- 解析 `Action: bash`
- 执行命令，把 `Observation` 回喂给模型

这里还没有 permission、sandbox、工具 schema、并行工具调用和上下文压缩。这些会放到后续章节。
