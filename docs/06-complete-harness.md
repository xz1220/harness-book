# 第 6 章 完整 harness

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

把前 5 章拼起来，再补齐工程上还差的那几块 —— 子代理、hooks、TODO 跟踪、scheduling、事件系统 —— 收尾出一个真正可用的 harness。

## 读完这一章，你会有

- 一个完整的 harness：能起子代理、能注册 hooks、能跑长任务
- 自己亲手完成（或者更准确地说：和 harness 一起完成）的一份工程作品
- 对 Claude Code / Codex 这类商业 harness 的"祛魅"理解

## 章节大纲（占位）

- 6.1 子代理（subagents）：什么时候 spawn、context 怎么隔离
- 6.2 Hooks：用户怎么自定义你的 harness 行为
- 6.3 TODO 系统与长任务跟踪
- 6.4 事件 / 调度：scheduled wakeup、background tasks
- 6.5 收尾：把整本书的 commit 历史拉出来看一遍
- 6.6 下一步：你的 harness 还能去哪里

## 配套代码

[`chapters/06-complete-harness/`](https://github.com/xz1220/harness-book/tree/main/chapters/06-complete-harness)
