# Harness Book

讲解 agent harness 工程的开源书。从零手写最简 ReAct loop，逐步加入工具、MCP、Skill、上下文、记忆和多 Agent 系统，演化出一个完整的 agent harness。

## 这本书的不同

市面上讲 agent 的内容大多围绕 framework（LangChain / LlamaIndex / Autogen）展开。本书走相反路径：

1. **从零手写最简 ReAct loop** —— 不依赖任何 agent 框架，几十行代码跑通 `thought → action → observation` 三步循环。
2. **逐步加能力** —— 先把第一章写扎实，再一章一章加入工具系统、MCP、Skill、上下文管理、记忆系统和多 Agent 协作。

读完之后，你不仅理解了 Claude Code / Codex 这类 harness 是怎么工作的，还能动手写一个属于自己的。

## 阅读方式

每一章对应一个可独立运行的代码课程。建议一边读、一边在 `chapters/0X-*/` 目录跑代码。

- [第 1 章 最简 ReAct loop](01-minimal-react-loop.md)

## 当前状态

当前正文和代码先只保留第 1 章，后续章节会按这个路线图逐步加入：

1. 最简 ReAct loop
2. 工具系统设计
3. MCP 集成
4. Skill 系统集成
5. 运行时上下文管理
6. 记忆系统设计
7. 多 Agent 系统（子 Agent、同级 Agent）
