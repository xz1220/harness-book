# Harness Book

讲解 agent harness 工程的开源书。从零手写最简 ReAct loop，再让它自举更新自己，逐步演化出一个完整的 agent harness。

## 这本书的不同

市面上讲 agent 的内容大多围绕 framework（LangChain / LlamaIndex / Autogen）展开。本书走相反路径：

1. **从零手写最简 ReAct loop** —— 不依赖任何 agent 框架，几十行代码跑通 `thought → action → observation` 三步循环。
2. **自举（self-bootstrapping）** —— 让最简 harness 开始更新自己的代码，迭代出后续能力。
3. **演化到完整 harness** —— 工具系统、permission、上下文管理、子代理、hooks 等机制按需逐层加进来，最终拼成一个真正可用的 harness。

读完之后，你不仅理解了 Claude Code / Codex 这类 harness 是怎么工作的，还能动手写一个属于自己的。

## 阅读方式

每一章对应一个可独立运行的代码课程。建议一边读、一边在 `chapters/0X-*/` 目录跑代码。

- [第 1 章 最简 ReAct loop](01-minimal-react-loop.md)
- [第 2 章 工具系统](02-tool-system.md)
- [第 3 章 自举：harness 改自己](03-self-bootstrap.md)
- [第 4 章 Permission 与 sandbox](04-permission-sandbox.md)
- [第 5 章 上下文与记忆](05-context-memory.md)
- [第 6 章 完整 harness](06-complete-harness.md)

## 当前状态

立项骨架阶段。章节正文与代码均为 TBD。
