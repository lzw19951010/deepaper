# Deepaper Roadmap — 从工具到爆款

**Created:** 2026-03-30
**Status:** Phase 1 部分完成（改名+License），待继续

---

## 已完成

- [x] 重命名: paper-manager → deepaper (包名、CLI、imports、tests 全部更新，73 tests passing)
- [x] AGPL-3.0 License
- [x] PyPI 元数据完善 (classifiers, keywords, urls, readme)
- [x] pypdfium2 加入 dependencies (之前遗漏)

## 待完成 — 按优先级排序

---

### Phase 1: 分发基础（传播前提）

**目标：** `pip install deepaper && deepaper add <arxiv-url>` 3 分钟内跑通

#### 1.1 GitHub 仓库重命名
- [ ] 手动操作: GitHub Settings → Rename → `deepaper`（GitHub 会自动 redirect 旧 URL）
- [ ] 更新 git remote: `git remote set-url origin https://github.com/lzw19951010/deepaper.git`

#### 1.2 PyPI 首次发布
- [ ] 注册 PyPI 账号（如没有）
- [ ] `pip install build twine`
- [ ] `python -m build && twine upload dist/*`
- [ ] 验证: `pip install deepaper` 从任意环境可用

#### 1.3 init 脱离仓库根目录
- [ ] `deepaper init` 在任意空目录可运行（不依赖 config.yaml.example）
- [ ] 内置默认 config.yaml 和 templates/default.md
- [ ] 自动检测 Claude Code CLI，给清晰错误提示
- **验收:** `mkdir test && cd test && deepaper init && deepaper add 2301.00001` 成功

---

### Phase 2: 引用分析 — 杀手级特性（核心差异化）

**目标：** "后代"从推测变为证据驱动，基于真实引用数据

#### 2.1 新模块 `src/deepaper/citations.py`
- [ ] Semantic Scholar API 集成
  - `GET https://api.semanticscholar.org/graph/v1/paper/ArXiv:{id}/citations`
  - Fields: `title,authors,year,citationCount,externalIds,url,isInfluential`
  - Rate limit: 100 req/5min，复用 downloader.py 的 `_rate_limit` 模式
- [ ] `fetch_citing_papers(arxiv_id, limit=50) -> list[dict]`
  - 按 citationCount 降序排列
  - 标记 isInfluential=True 的高影响力引用
  - API 失败时返回空列表（不阻断主流程）
- [ ] `format_descendants_section(citing_papers, total_citations) -> str`
  - 输出格式:
    ```markdown
    ### 后代 (Descendants) — 基于引用分析

    > 截至 2026-03-30，本文共被引用 **12,345** 次（Semantic Scholar）

    #### 高影响力后续工作
    | 论文 | 年份 | 引用数 | 关键继承/改进 |
    |------|------|--------|-------------|
    | BERT (Devlin et al.) | 2019 | 89,234 | 将Transformer encoder用于预训练 |

    #### 引用趋势
    - 2020: 1,234 篇 | 2021: 2,345 篇 | ...
    ```

#### 2.2 集成到分析流程
- [ ] `cli.py` 的 `add` 命令: 在 `analyze_paper()` 后调用 `fetch_citing_papers()`
- [ ] 用 Claude 合成引用数据 + 原始分析，生成更丰富的 Descendants 叙述
  - 输入: 原始 mechanism_transfer + citing papers 列表
  - 输出: 替换 mechanism_transfer 中的 Descendants 子节
- [ ] 在 YAML frontmatter 中添加: `citation_count`, `influential_citations`, `citation_date`

#### 2.3 独立命令 `deepaper cite`
- [ ] `deepaper cite <arxiv-id>` — 单独查看引用信息
- [ ] `deepaper cite --update <arxiv-id>` — 更新已有笔记的 Descendants 部分
- [ ] `deepaper cite --update-all` — 批量更新所有笔记

#### 2.4 测试
- [ ] Mock Semantic Scholar API 响应的单元测试
- [ ] 集成测试: 对 "Attention Is All You Need" 验证返回引用数据

---

### Phase 3: README & 演示（让人 10 秒内想 star）

**目标：** GitHub 页面让人一眼看懂价值，想分享

#### 3.1 README 重写
- [ ] Hero section: 一句话 pitch + demo GIF
  - Pitch: "一个 arxiv 链接 → 一份专家级深度分析笔记，存入 Obsidian"
- [ ] "为什么用 deepaper?" 对比表:
  | | Zotero | Semantic Scholar | 手动笔记 | deepaper |
  |---|---|---|---|---|
  | 深度分析 | ✗ | 摘要级 | 你自己写 | 7节AI深度剖析 |
  | 机制图谱 | ✗ | ✗ | ✗ | 自动生成引用族谱 |
  | Obsidian | 插件 | ✗ | 手动 | 原生 |
  | 语义搜索 | ✗ | 有 | ✗ | 本地RAG |
- [ ] 3 命令 Quick Start
- [ ] 示例分析截图（Obsidian 中打开的效果）
- [ ] Badge 行: PyPI version, Python, License, Stars

#### 3.2 Demo 录制
- [ ] 用 `vhs` (charmbracelet/vhs) 或 `asciinema` 录制终端演示
- [ ] 转换为 GIF 放在 README hero section

---

### Phase 4: 体验打磨

#### 4.1 Rich 终端输出
- [ ] 添加 `rich` 依赖
- [ ] PDF 下载进度条
- [ ] 分析中的 spinner + 实时 token 计数
- [ ] 完成后的 summary card (标题/分类/标签/耗时)

#### 4.2 实用命令补全
- [ ] `deepaper list` — 表格展示所有论文（标题/日期/分类/标签）
  - `--category llm/pretraining` 过滤
  - `--tag transformer` 过滤
  - `--sort date|title` 排序
- [ ] `deepaper stats` — 集合统计（总数/按分类/按月/热门标签）
- [ ] `deepaper open <query>` — 模糊搜索 + 用默认编辑器打开

---

### Phase 5: 社区传播

#### 5.1 自动索引
- [ ] `deepaper readme` — 在 `papers/README.md` 生成按分类组织的论文索引
- [ ] GitHub 仓库直接可浏览

#### 5.2 单篇导出
- [ ] `deepaper export <query> --format html` — 生成可分享的单页 HTML
- [ ] 好排版，适合发微信/Twitter

#### 5.3 批量导入
- [ ] `deepaper import reading-list.txt` — 从文件批量添加论文

---

### Phase 6: 国际化（扩大受众）

#### 6.1 英文支持
- [ ] `config.yaml` 添加 `language: zh|en`
- [ ] `templates/default_en.md` — 英文分析提示词
- [ ] `writer.py` 根据语言切换节标题

---

## 技术决策记录

### 引用 API 选择: Semantic Scholar
| API | 免费 | 引用数据 | 影响力标记 | 风险 |
|-----|------|---------|-----------|------|
| **Semantic Scholar** | 免费无需key | 优秀 | `isInfluential` | 低 |
| OpenAlex | 免费 | 好 | 无 | 低 |
| Google Scholar | 无API | 最全 | 无 | 高（封IP） |

**决策:** Semantic Scholar 作为主要来源。免费、稳定、有影响力评分。

### 引用合成方式
- **Phase 1 (Option A):** 直接格式化引用数据为 markdown，不额外调用 Claude（快、省）
- **Phase 2 (Option B):** 可选 `--deep-cite` 让 Claude 合成引用数据与原始分析的叙事（更丰富）

### 命名统一
- PyPI 包: `deepaper`
- CLI 命令: `deepaper`
- GitHub 仓库: `lzw19951010/deepaper`
- Python 包: `deepaper` (src/deepaper/)

---

## 执行顺序建议

| 阶段 | 内容 | 耗时估计 | 影响 |
|------|------|---------|------|
| Phase 1 | 仓库重命名 + PyPI 发布 + init 优化 | 当天 | 🔴 传播前提 |
| Phase 2 | 引用分析 (citations.py + cite 命令) | 1-2天 | 🔴 核心差异化 |
| Phase 3 | README 重写 + 演示录制 | 半天 | 🔴 第一印象 |
| Phase 4 | Rich UI + list/stats/open 命令 | 1天 | 🟡 体验打磨 |
| Phase 5 | 索引生成 + 导出 + 批量导入 | 1天 | 🟡 社区传播 |
| Phase 6 | 英文支持 | 半天 | 🟢 受众扩大 |
