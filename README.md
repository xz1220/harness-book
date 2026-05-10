# Harness Book

讲解 agent harness 工程的开源书。从零手写最简 ReAct loop，再让它自举更新自己，逐步演化出一个完整的 agent harness。

## 在线阅读

GitHub Pages：https://xz1220.github.io/harness-book/

如果该地址暂时无法访问，请先在 GitHub 仓库 `Settings` → `Pages` 中把
`Build and deployment` 的 `Source` 设置为 `GitHub Actions`，然后重新运行发布工作流。

## 这本书的不同

市面上讲 agent 的内容大多围绕 framework（LangChain / LlamaIndex / Autogen）展开。
本书走相反路径：

1. **从零手写最简 ReAct loop** —— 不依赖任何 agent 框架，几十行代码跑通 `thought → action → observation` 三步循环。
2. **自举（self-bootstrapping）** —— 让最简 harness 开始更新自己的代码，迭代出后续能力。
3. **演化到完整 harness** —— 工具系统、permission、上下文管理、子代理、hooks 等机制按需逐层加进来，最终拼成一个真正可用的 harness。

读完之后，你不仅理解了 Claude Code / Codex 这类 harness 是怎么工作的，还能动手写一个属于自己的。

## 内容结构

- `docs/`：书的正文（mkdocs Material）
- `chapters/`：每章对应的代码课程
  - `chapters/0X-<slug>/`：该章可独立运行的代码
- `mkdocs.yml`：站点配置
- `.github/workflows/deploy.yml`：GitHub Pages 自动发布

每一章的 `docs/0X-*.md` 与 `chapters/0X-*/` 一一对应。读者可以一边读、一边跑。

## 章节大纲

1. 最简 ReAct loop
2. 工具系统
3. 自举：harness 改自己
4. Permission 与 sandbox
5. 上下文与记忆
6. 完整 harness（子代理 / hooks / 收尾）

> 当前为立项骨架，章节正文 / 代码均为 TBD。

## 本地预览

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

## 协议

本仓库采用双协议：

- **代码部分**（`chapters/` 及其他源代码）：[MIT License](LICENSE-CODE)
- **书的正文**（`docs/` 下的 markdown 内容）：[CC BY 4.0](LICENSE-DOCS)

简单说：代码可以随便用、随便改、随便商用；书的内容可以随便分享和改编，但请署名。
