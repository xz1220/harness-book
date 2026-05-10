# 第 1 章 最简 ReAct loop

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

从一张白纸开始，用几十行代码写出最简单的 agent loop：

- 一个 `while` 循环
- 一次模型调用 → 一次工具调用 → 一次观察结果回喂
- 没有框架、没有抽象、没有 wrapper

## 读完这一章，你会有

- 一个能跑的 `agent.py`，依赖只有 Anthropic SDK（或等价物）
- 对 ReAct（Reason + Act）三步循环的肌肉记忆
- 理解 "agent 不是魔法，agent 是 while loop + tool call"

## 章节大纲（占位）

- 1.1 `thought → action → observation` 是什么
- 1.2 模型 API 调用与消息格式
- 1.3 写第一个工具：read_file
- 1.4 把 loop 跑起来
- 1.5 为什么这就是一个 agent

## 配套代码

[`chapters/01-minimal-react-loop/`](https://github.com/xz1220/harness-book/tree/main/chapters/01-minimal-react-loop)
