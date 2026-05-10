# 第 5 章 上下文与记忆

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

给 harness 加上工程实践中最被低估的两件事：**上下文管理**（怎么塞进窗口）和**持久记忆**（跨会话）。

## 读完这一章，你会有

- 一份 context 预算的计算方法（system / messages / tools / cache）
- Compaction（自动压缩历史对话）的最简实现
- 文件型持久记忆：what / when / where to write
- prompt cache 的命中策略（每多一次 cache miss 是一次实打实的钱和延迟）

## 章节大纲（占位）

- 5.1 上下文不是无限的：算清你的预算
- 5.2 Compaction：什么时候压、怎么压、压完丢什么
- 5.3 文件型记忆：什么写、什么不写
- 5.4 Prompt cache 的命中点
- 5.5 让 harness 自己维护自己的记忆

## 配套代码

[`chapters/05-context-memory/`](https://github.com/xz1220/harness-book/tree/main/chapters/05-context-memory)
