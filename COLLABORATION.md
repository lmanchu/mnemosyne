# Mnemosyne 協作指南

> 給團隊成員的 Git 協作說明

---

## 📋 目錄

- [快速開始](#快速開始)
- [日常工作流程](#日常工作流程)
- [分支策略](#分支策略)
- [Commit 規範](#commit-規範)
- [常見問題](#常見問題)

---

## 🚀 快速開始

### 第一次設置（只需做一次）

```bash
# 1. Clone 專案（從 GitHub/GitLab）
git clone https://github.com/irisgo/mnemosyne.git
cd mnemosyne

# 2. 設定你的身份
git config user.name "你的名字"
git config user.email "your.email@irisgo.ai"

# 3. 完成！可以開始工作了
```

**如果使用 Dropbox 共享**：
```bash
# 直接進入 Dropbox 資料夾
cd ~/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne

# 確認 Git 狀態
git status
```

---

## 💼 日常工作流程

### 情境 1：我要編輯文件

```bash
# 1. 確保在 main 分支
git checkout main

# 2. 拉取最新版本
git pull

# 3. 編輯文件
# （用你喜歡的編輯器：VS Code, Notion, etc.）

# 4. 查看變更
git status
git diff

# 5. 加入變更
git add PRD.md
# 或加入所有變更：git add .

# 6. Commit（附上清楚的說明）
git commit -m "docs: Update market analysis section"

# 7. 推送到遠端
git push
```

---

### 情境 2：我要新增一個大功能（使用分支）

```bash
# 1. 從 main 創建新分支
git checkout main
git pull
git checkout -b feature/add-deployment-plan

# 2. 編輯文件
# ...

# 3. Commit（可以多次）
git add .
git commit -m "feat: Add Phase 1 deployment plan"
git commit -m "feat: Add infrastructure requirements"

# 4. 推送分支到遠端
git push -u origin feature/add-deployment-plan

# 5. 在 GitHub 上創建 Pull Request (PR)
# （瀏覽器打開，點擊 "Create Pull Request"）

# 6. 等待 Review 和 Merge
# （Lman 或其他成員 review 後會 merge）
```

---

### 情境 3：查看歷史和差異

```bash
# 查看最近的 commits
git log --oneline -10

# 查看某個文件的歷史
git log --oneline PRD.md

# 查看兩個版本的差異
git diff v1.2 v1.3

# 查看某次 commit 的內容
git show ba393a5
```

---

## 🌳 分支策略

我們使用簡化的 **Feature Branch Workflow**：

```
main ─────────────────────────────────────> (永遠穩定)
  │
  ├── feature/deployment-plan ────────────> (功能分支)
  │
  ├── feature/cost-analysis ──────────────> (功能分支)
  │
  ├── ai/claude-updates ──────────────────> (AI 協作分支)
  │
  └── draft/lman-brainstorm ──────────────> (草稿分支)
```

### 分支命名規則

| 類型 | 命名格式 | 範例 | 用途 |
|------|---------|------|------|
| **功能** | `feature/xxx` | `feature/add-vlm-analysis` | 新增功能或章節 |
| **修復** | `fix/xxx` | `fix/typo-in-prd` | 修正錯誤 |
| **文檔** | `docs/xxx` | `docs/update-privacy` | 更新文檔 |
| **AI** | `ai/xxx` | `ai/claude-section8` | Claude 協作 |
| **草稿** | `draft/xxx` | `draft/lman-ideas` | 個人草稿 |

---

## 📝 Commit 規範

使用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 類型

| Type | 說明 | 範例 |
|------|------|------|
| `feat` | 新功能 | `feat: Add competitive moat analysis` |
| `fix` | 修復錯誤 | `fix: Correct Year 3 valuation calculation` |
| `docs` | 文檔變更 | `docs: Update privacy architecture` |
| `refactor` | 重構 | `refactor: Reorganize data sources section` |
| `chore` | 雜項 | `chore: Update .gitignore` |

### 範例

```bash
# 簡單 commit
git commit -m "docs: Update market size analysis"

# 詳細 commit
git commit -m "feat(prd): Add Personal Tag Asset System

- Added tiered tag architecture (Tier 1/2/3)
- Added monetization mechanism with revenue estimates
- Added competitive moat analysis
- Added valuation model ($1.9B-$3.2B)

Closes #12"
```

---

## 🤝 團隊協作流程

### Pull Request (PR) 流程

1. **創建分支並開發**
   ```bash
   git checkout -b feature/my-feature
   # ... 編輯文件 ...
   git commit -m "feat: My feature"
   git push -u origin feature/my-feature
   ```

2. **在 GitHub 創建 PR**
   - 打開 GitHub repo
   - 點擊 "Pull requests" → "New pull request"
   - 選擇你的分支
   - 填寫 PR 描述
   - 指定 Reviewer（通常是 Lman）

3. **Code Review**
   - Reviewer 檢查變更
   - 可能要求修改
   - 討論和迭代

4. **Merge**
   - Reviewer 批准後 merge
   - 分支自動刪除（可選）

### Review 時的注意事項

✅ **應該檢查的**：
- 內容是否準確
- 格式是否一致
- 邏輯是否清晰
- 有無錯字或語法錯誤

❌ **不需要過度檢查的**：
- 完美的英文語法（中英混雜 OK）
- 絕對的格式統一（重要的是內容）

---

## 🔄 與 Claude (AI) 協作

### Claude 編輯時的流程

**由 Lman 操作**：
```bash
# 1. Claude 說：「我準備更新 section 8」

# 2. 創建 AI 分支
git checkout -b ai/claude-section8-$(date +%Y%m%d)

# 3. Claude 編輯文件
# （Claude 會直接修改文件）

# 4. 查看變更
git diff

# 5. 如果滿意，commit 並 merge
git add .
git commit -m "feat(prd): Add critical analysis by Claude

Co-authored-by: Claude <noreply@anthropic.com>"

git checkout main
git merge ai/claude-section8-20241116
git push

# 6. 如果不滿意，丟棄變更
git checkout main
git branch -D ai/claude-section8-20241116
```

---

## 🆘 常見問題

### Q1: 我不小心在 main 上改了文件，還沒 commit，怎麼辦？

```bash
# 方法 1：丟棄變更
git checkout PRD.md

# 方法 2：把變更移到新分支
git stash
git checkout -b my-changes
git stash pop
```

---

### Q2: 我 commit 了但還沒 push，想修改 commit message

```bash
git commit --amend -m "新的 commit message"
```

---

### Q3: 我 push 了但發現有錯，怎麼辦？

```bash
# 方法 1：如果只是小錯誤，直接修正再 commit
git add .
git commit -m "fix: Correct typo"
git push

# 方法 2：如果是大錯誤，revert 上一次 commit
git revert HEAD
git push
```

---

### Q4: 我的分支和 main 衝突了

```bash
# 1. 確保在你的分支
git checkout feature/my-feature

# 2. 拉取最新的 main
git fetch origin main

# 3. Merge main 到你的分支
git merge origin/main

# 4. 如果有衝突，Git 會告訴你哪些文件衝突
# 打開文件，手動解決衝突（找到 <<<<<<< 標記）

# 5. 解決後，commit
git add .
git commit -m "merge: Resolve conflicts with main"
git push
```

---

### Q5: 如何查看誰改了這行？

```bash
# Blame 命令（查看每一行的作者）
git blame PRD.md

# 查看特定行範圍
git blame -L 100,120 PRD.md
```

---

### Q6: 我想回到之前的某個版本

```bash
# 查看歷史
git log --oneline

# 臨時查看某個版本（不會改變 main）
git checkout <commit-hash>

# 回到 main
git checkout main

# 如果真的要恢復到某個版本
git revert <commit-hash>
```

---

## 📚 推薦資源

- [Git 官方文檔](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [為你自己學 Git](https://gitbook.tw/)

---

## 🔗 快速指令參考

```bash
# 查看狀態
git status

# 查看歷史
git log --oneline -10

# 查看差異
git diff

# 拉取更新
git pull

# 創建分支
git checkout -b feature/my-feature

# 切換分支
git checkout main

# Commit
git add .
git commit -m "feat: My changes"

# 推送
git push

# 合併分支
git merge feature/my-feature

# 刪除分支
git branch -D feature/my-feature
```

---

## 📞 需要幫助？

- **Slack**: #mnemosyne-dev
- **Email**: lman@irisgo.ai
- **GitHub Issues**: [創建 Issue](https://github.com/irisgo/mnemosyne/issues)

---

**最後更新**：2025-11-16
**維護者**：Lman (@lman)
