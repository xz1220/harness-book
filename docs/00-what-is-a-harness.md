# 第 0 章 什么是 harness

> 状态：v1，钉死 harness 这个词，给后续章节铺底

## 这一章不写代码

后面所有章节都在写一个 harness。但在动手前先把这个词钉死，否则你读第 1 章时心里会嘀咕：我做的这玩意儿到底是 agent 还是 harness 还是 framework？三者不是一回事。

## Anthropic 的最小定义

Anthropic 在 [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) 里给 `harness` 加了一个**括号注释**，是目前能找到的最贴近字典定义的一句：

> harness (the loop that calls Claude and routes Claude's tool calls to the relevant infrastructure)

去掉括号、翻成中文，harness 在做两件事：

1. **Loop** —— 反复调用模型
2. **Routing** —— 把模型说"我要调 X 工具"的意图，翻译成对真实基础设施的调用，再把结果塞回模型下一次输入

再加上 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) 里反复强调的那句：

> every component in a harness encodes an assumption about what the model can't do on its own

补上第三件：

3. **Assumptions made executable** —— 每段 harness 代码都是一条"我替模型多做了这件事"的假设，被写成可执行的形式

合起来就是本书会反复回到的最小定义：

**Harness = Loop + Routing + 把"模型自己做不到什么"的判断写成代码。**

## 三件事分别展开

### 1. Loop —— 模型不是函数，是被反复调用的状态机

模型一次调用只能回答一次。一个能"做完一件事"的 agent，需要反复调它：模型给一步动作 → harness 执行 → 把观察喂回去 → 模型给下一步。这就是 ReAct loop。

Anthropic 在 [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) 里把 "agent" 这个名词归到这种 loop 上：

> agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks

注意是 **LLM 控制流程**，不是"代码控制流程，LLM 只是节点"。后者 Anthropic 称为 workflow，不是 agent。这个区分决定 harness 后面所有取舍——把决策权交给模型，还是预先用代码框死。

第 1 章会用 60 行代码把这个 loop 写出来，让你拿到对它的肌肉记忆。

### 2. Routing —— 模型说话，harness 干活

模型不会真的执行 `bash`，它只会输出一个结构化的 `tool_use` block，说"我想跑 `ls /tmp`"。这个 block 到底变成 `subprocess.run`、变成一次 HTTP 调用、还是被拦下来弹个权限框，**全在 harness 里决定**。

[Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) 里把 Anthropic 自己的容器化执行环境也归到这一层：

> the harness no longer lived inside the container. It called the container the way it called any other tool

意思是：从模型视角，看到的永远只是 `tool_use` / `tool_result` 这套统一协议；至于背后是本机 subprocess 还是远端 sandbox 容器，是 harness 自己的实现选择，模型不需要知道。

后面章节出现的"工具系统、permission、sandbox、MCP、子 agent"，本质都是在丰富这条 routing 通路。

### 3. Assumptions made executable —— 每行 harness 代码都在赌一件模型做不到的事

这是 Anthropic 在 harness 相关文章里反复点名的一句（见 [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) 与 [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)）：

> harnesses encode assumptions about what Claude can't do on its own

举几个具体的"假设"：

- **上下文压缩**：假设模型不会主动忘掉过期的工具结果
- **进度文件**（如 Anthropic 用的 `claude-progress.txt`）：假设换一个新的上下文窗口后，模型想不起上轮做到哪了
- **权限确认弹窗**：假设模型可能执行用户不希望的危险命令
- **子 agent**：假设主 agent 的上下文装不下这么多搜索结果

这条定义带来两个会贯穿全书的推论：

**Harness ≠ framework。** 框架是别人替你做好的抽象选择；harness 是**你自己**对"模型差什么"的判断。同一段代码，在 GPT-3.5 时代是必要补丁，在 Claude 4.7 时代可能就成了多余包袱。所以这本书不教你"用某某框架"，教你怎么自己做这些判断。

**Harness 代码会过期。** 模型变强后，今天必须的某段 harness，明天可能就成了拖后腿的补丁。Harness 不是"写完就稳定"的工程产物，它是要随模型不断重审的活物。Anthropic 的工程师在多篇文章里反复提醒这一点。

## 关于 "agent = 模型 + harness"

社区常用这句话浓缩 Anthropic 的论述。它和 Anthropic 原文论点一致，但 Anthropic 自己没逐字这么说过，所以本书在引用时不打引号、不算 Anthropic 原话——它是个好用的口诀，不是出处。

## 下一步

第 1 章我们就写一个 60 行的 ReAct loop。它同时做到了上面三件事的最简版本：

- 一个 while 循环（Loop）
- 一个 `bash` 工具（Routing）
- 一个 20 秒 timeout（Assumption：模型可能让自己挂死）

进入 [第 1 章 最简 ReAct loop](01-minimal-react-loop.md)。

## 本章引用

- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Scaling Managed Agents: Decoupling the brain from the body](https://www.anthropic.com/engineering/managed-agents)
- [Building agents with the Claude Agent SDK](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
