# 001 — 用 baby agent 自举出工具注册器

第 1 章的最简 ReAct agent 跑通之后，我们没有手写第 2 章，而是让 v0 自己改自己，产出 v1：一个能挂任意工具的注册器骨架。这是 baby agent 演化的第一次拐点，也是自举范式的第一次实战——下一版 agent，由上一版自己写出来。

## 起点

把 `chapters/01-minimal-react-loop/agent.py`（基于 Anthropic `tool_use` 的最简 ReAct + 单 `bash` 工具）原样复制到 `chapters/02-tool-system/agent.py`，作为这次自举的起点。

为给自举留出余裕，起点上调了两个参数：

- `max_tokens`：1000 → 4000（模型一次性能吐完整段 Python）
- `MAX_STEPS`：5 → 12（改文件 + 自验证的步数）

其它一切不动。

## task

给起点 agent 起的任务大意如下：

> 重构当前目录下的 `agent.py`，从「一个 hardcoded bash 工具」升级成「工具注册器骨架」：
>
> 1. 全局字典 `TOOLS = {"bash": {"schema": ..., "description": ..., "handler": ...}}`
> 2. `call_model` 里 `tools=` 从 `TOOLS` 自动生成
> 3. 主循环 `handler = TOOLS[block.name]["handler"]; handler(**block.input)`，异常和未知工具都按 `tool_result is_error=True` 回喂
> 4. 这一轮**不加新工具**，只验证注册器骨架能跑
> 5. 跑 `python agent.py "..."` 自验证
>
> Hint：你只有 bash 工具，改文件要用 `cat > agent.py <<'PY' ... PY` 这种 heredoc 写法。

## 过程

5 个 step，外层完整轨迹：

| step | stop_reason | 干了什么 |
|------|-------------|----------|
| 1 | tool_use | `cat agent.py` 读起点代码 |
| 2 | tool_use | `cat > agent.py <<'PY' ... PY` 一次性重写整个文件 |
| 3 | tool_use | 自验证跑 `python agent.py "..."` → 挂在 `python: command not found` |
| 4 | tool_use | 改成 `python3 agent.py "..."`，**子进程跑新版自己成功** |
| 5 | end_turn | 总结，对照 task 5 条要求逐项验收 |

几个值得记一笔的瞬间：

- **Step 2 没炸**。这一步最赌——agent 要在一段 bash 字符串里塞一份完整 Python 源码，里面再嵌套 `"""docstring"""`、`f"exit_code={..}"`、`<<'PY'` heredoc。这次 Kimi 一次吐对了 4000 token，没踩到引号嵌套。**如果它哪里漏一个引号，文件就坏了**，下一轮启动直接 syntax error。这种「能跑通是因为这次运气好」是必须重视的脆弱点（见下文）。
- **Step 3 → Step 4 的自纠错**。这台机器只有 `python3`，没 `python`。模型自己看到 `exit_code=127 /bin/sh: python: command not found`，下一步换成 `python3` 重试。没有任何指令告诉它该这样做，是 ReAct loop 本身的产出。
- **Step 4 嵌套两层 ReAct**。外层 agent 起的子进程是「自己的新版本」，新版本接到 `用 bash 跑 echo hello && uname -a` 又跑了自己的 step1（`tool_use`）→ step2（`end_turn`）。两层 loop 都对了，新注册器骨架第一次实战通过。

完整 log 在 `/tmp/agent-bootstrap-run.log`，不入 repo。

## 产出

`chapters/02-tool-system/agent.py` v1，相对 v0 的差异：

- 多了 `TOOLS` 字典，目前只有 `bash` 一项，结构 `{schema, description, handler}`
- `call_model` 里 `tools=` 用列表推导从 `TOOLS` 生成，不再 hardcode `BASH_TOOL`
- 主循环按 `block.name` 在 `TOOLS` 查 handler，调用 `handler(**block.input)`：
  - handler 抛异常 → `tool_result` 加 `is_error=True`，content 是异常 message
  - 工具名不在注册器里 → 同样 `is_error=True`，content `"unknown tool: ..."`

跟「我手写一个注册器会怎么写」对比，质量在合理范围：结构干净、错误路径没炸、没有过度设计。模型没自作主张加 `read_file` / `write_file`——task 里明确说了不加新工具，它守住了。

## 留下的脆弱点

1. **`SYSTEM` prompt 还写着 `You have one tool: `bash``**。注册器已经能挂多工具了，措辞跟实现脱节。模型这次没被误导，但这是个会发酵的技术债。
2. **改自己的代码只能靠 bash heredoc**。这次没炸有运气成分；后面如果要重构 200 行以上、或在 Python 字符串里嵌 raw shell（含 `$`、反引号、单双引号嵌套），很可能炸。**下一轮自举的核心目标应该是让 baby agent 摆脱 shell heredoc**：给它加 `read_file` / `write_file` / `edit_file` 三件套工具。
3. **多工具并行没真正验证**。Anthropic `tool_use` 协议允许一轮 response 里出现多个 `tool_use` block，注册器主循环已经是 `for block in resp.content` 处理，但当前只注册一个工具，没真实压过多 tool 同轮场景。下一轮加新工具时顺手测一下。

## 下一步

baby agent v1 → v2：**加 `read_file` / `write_file` / `edit_file` 三件套**。自验证方式可以是「让 v2 用 `write_file` 把自己重写一遍」——产出与 v1 等价就算通过，证明 baby agent 已经能不靠 shell 改自己。

这条路走通后再决定要不要继续加 `glob` / `grep`，还是先转去做 permission / sandbox / context 压缩里某一个——视彼时 baby agent 的最弱点决定，不预先规划。
