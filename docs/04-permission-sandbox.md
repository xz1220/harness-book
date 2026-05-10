# 第 4 章 Permission 与 sandbox

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

让自举出来的 harness 长出"安全边界" —— 在它继续修改自己 / 修改用户文件之前，先建立 permission 和 sandbox 机制。

## 读完这一章，你会有

- 三档 permission 模型：自动允许 / 询问用户 / 完全拒绝
- 基于路径 / 命令 / 工具名的 allowlist 与 denylist
- 一个能跑命令但跑不出 sandbox 的执行环境
- 理解"agent 安全"不是机器学习问题，是工程问题

## 章节大纲（占位）

- 4.1 为什么 agent 需要 permission：来自真实事故
- 4.2 三档模型：always / ask / never
- 4.3 allowlist / denylist 的写法与匹配规则
- 4.4 sandbox：从 chroot 到容器再到 vm
- 4.5 让 harness 自己学会请求 permission

## 配套代码

[`chapters/04-permission-sandbox/`](https://github.com/xz1220/harness-book/tree/main/chapters/04-permission-sandbox)
