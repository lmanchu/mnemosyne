# Mnemosyne 快速開始 🚀

> 給同事的 5 分鐘快速上手指南

---

## 📍 你現在在哪裡？

這個專案已經設置好 Git 版本控制，你可以：
- ✅ 查看歷史變更
- ✅ 追蹤誰改了什麼
- ✅ 安全地實驗新想法（用分支）
- ✅ 與團隊和 AI (Claude) 協作

---

## 🎯 最簡單的使用方式（3 步驟）

### 1️⃣ 編輯文件
用你喜歡的方式編輯（Notion、VS Code、TextEdit 都可以）

### 2️⃣ 儲存變更
```bash
cd ~/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne
git add .
git commit -m "docs: 我做了什麼變更"
```

### 3️⃣ 完成！
就這麼簡單。Git 會自動記錄：
- 誰改的
- 什麼時候改的
- 改了什麼

---

## 📖 常用命令速查表

```bash
# 查看目前狀態（有什麼變更？）
git status

# 查看歷史（誰改過這個文件？）
git log --oneline PRD.md

# 查看最新的 5 次變更
git log --oneline -5

# 查看某次變更的內容
git show <commit-hash>

# 恢復到某個版本（查看，不會改變文件）
git checkout v1.3

# 回到最新版本
git checkout main
```

---

## 🌟 進階功能（當你需要時）

### 想要實驗新想法但不影響主文件？

```bash
# 1. 創建實驗分支
git checkout -b draft/my-experiment

# 2. 隨便改
# ...

# 3. 不喜歡？直接刪除
git checkout main
git branch -D draft/my-experiment

# 4. 喜歡？合併回主分支
git checkout main
git merge draft/my-experiment
```

---

## 📚 完整文檔在哪裡？

詳細的協作指南在這裡：
**[COLLABORATION.md](./COLLABORATION.md)**

包含：
- 分支策略
- Commit 規範
- Pull Request 流程
- 與 Claude 協作
- 常見問題 Q&A

---

## 🆘 遇到問題？

### 情境 1：我改錯了，還沒 commit

```bash
# 丟棄變更，恢復到上次 commit 的狀態
git checkout PRD.md
```

### 情境 2：我 commit 了但想修改 commit message

```bash
git commit --amend -m "新的 commit message"
```

### 情境 3：我不知道發生什麼事了

```bash
# 查看狀態
git status

# 如果真的不知道，直接問 Lman 或在 Slack #mnemosyne-dev
```

---

## 🤝 與 Claude 協作

**好消息**：Claude 也會使用 Git！

當 Claude 編輯文件時：
1. Claude 會告訴你「我準備編輯 XXX」
2. 你可以事後用 `git diff` 查看 Claude 改了什麼
3. 滿意就 commit，不滿意就 `git checkout` 恢復

---

## 💡 小技巧

### 快速查看誰改了這行
```bash
git blame PRD.md
```

### 搜尋歷史中的關鍵字
```bash
git log --all --grep="Tag Asset"
```

### 比較兩個版本
```bash
git diff v1.2 v1.3
```

---

## 📞 需要幫助？

- **Slack**: #mnemosyne-dev
- **直接問 Lman**: lman@irisgo.ai
- **完整文檔**: [COLLABORATION.md](./COLLABORATION.md)

---

## 🎉 你已經準備好了！

現在你可以：
- ✅ 安全地編輯文件
- ✅ 追蹤所有變更
- ✅ 與團隊協作
- ✅ 永遠不會「搞丟」東西

**開始編輯吧！** 🚀

---

**專案狀態**：v1.3 (2025-11-16)
**當前版本**：完整 PRD + 個人標籤資產系統 + 競爭護城河分析
