# 第 2 章 工具系统

> 状态：立项骨架，正文 TBD

## 这一章你会做什么

把第 1 章的"单工具 loop"升级成可注册任意工具的工具系统。

## 读完这一章，你会有

- 一个工具注册器，新工具用一个装饰器就能加入
- 标准化的 tool schema（name / description / params）
- 多工具并行调用的处理
- 工具调用失败时的错误回喂机制

## 章节大纲（占位）

- 2.1 工具的形状：name / schema / handler
- 2.2 注册机制：装饰器还是显式列表
- 2.3 并行 tool call 处理
- 2.4 错误如何回喂给模型
- 2.5 内置工具集：read / write / edit / bash / glob / grep

## 配套代码

[`chapters/02-tool-system/`](https://github.com/xz1220/harness-book/tree/main/chapters/02-tool-system)
