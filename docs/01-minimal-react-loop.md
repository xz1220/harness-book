# 第 1 章 最简 ReAct loop

> 状态：第一个可运行版本已填入

## 这一章你会做什么

从一张白纸开始，用 100 行左右代码写出最简单的 agent loop：

- 一个 `while` 循环
- 一次模型调用 → 一次工具调用 → 一次观察结果回喂
- 一个最小 `bash` 工具
- 没有 agent 框架、没有复杂抽象、没有 wrapper

## 读完这一章，你会有

- 一个能跑的 `agent.py`，依赖只有 Anthropic SDK
- 对 ReAct（Reason + Act）三步循环的肌肉记忆
- 理解 "agent 不是魔法，agent 是 while loop + tool call"

## 最小协议

这一章先不用官方 tool calling。我们让模型按纯文本格式输出：

````text
Thought: 解释下一步
Action: bash
Command:
```bash
pwd && ls
```
````

如果任务完成，模型输出：

```text
Thought: 解释为什么完成
Final: 给用户的最终答案
```

这已经足够构成一个 ReAct loop：

1. 用户给任务
2. 模型决定下一条命令
3. harness 执行 bash
4. harness 把 observation 回喂给模型
5. 循环直到 `Final`

## 运行配套代码

```bash
cd chapters/01-minimal-react-loop
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_api_key
python agent.py "用 bash 看看当前目录里有什么"
```

这个版本的 `bash` 工具没有 permission 和 sandbox，只加了 20 秒超时。它适合用来理解 harness 的最小闭环，不适合执行不可信任务。

## 配套代码

[`chapters/01-minimal-react-loop/`](https://github.com/xz1220/harness-book/tree/main/chapters/01-minimal-react-loop)
