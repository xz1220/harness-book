# 第 3 章 自举：harness 改自己

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

让前两章的 harness 跨过那个临界点 —— **自己修改自己的代码**。

这是这本书最核心的一章。从这里开始，后续章节的功能都不再由你手写，而是由 harness 自己迭代出来。

## 读完这一章，你会有

- 一个能读自己代码、能 edit 自己代码、能重启自己的 harness
- 关于"agent 自我修改" 的工程边界（什么改、什么不改、改坏了怎么回滚）
- 一份"自举 commit log"：harness 真实写下的每一次自我升级

## 章节大纲（占位）

- 3.1 自举的最小可用形态：read self → edit self → restart
- 3.2 防止把自己改死：版本快照 / git 兜底
- 3.3 让 harness 给自己加一个新工具
- 3.4 让 harness 重构自己的某个模块
- 3.5 边界：哪些事永远不交给自举

## 配套代码

[`chapters/03-self-bootstrap/`](https://github.com/xz1220/harness-book/tree/main/chapters/03-self-bootstrap)
