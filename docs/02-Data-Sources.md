# 🔍 Context Engine - 數據源完整分析

> **目標**: 系統化評估所有可能的洞察來源，聚焦可行性和 ROI
> **創建日期**: 2025-11-02
> **當前版本**: v1.0 (Merged Edition)

---

## 📝 版本歷史

### v1.0 - 2025-11-02 (Current)
- 合併兩份數據源分析文檔
- 核心洞察：DayFlow 錄影作為萬能數據源
- 完整的可行性評估矩陣
- 明確的優先級建議

### v0.2 - 2025-11-02
- 可行性聚焦版本
- 強調 DayFlow + VLM 方案
- 實作路徑規劃

### v0.1 - 2025-11-02
- 初版數據源全景分析
- 五層分類框架

---

## 💡 核心洞察：DayFlow 作為萬能數據源

### 革命性發現

DayFlow 錄影本質上是 **視覺化的行為日誌**，可以替代多個傳統數據源：

```
DayFlow 錄影 =
  Browser History +
  App Usage +
  Screen Time +
  Reading Patterns +
  Work Flow +
  Social Media Activity +
  Content Consumption +
  Communication Patterns +
  ... 幾乎所有屏幕上的行為
```

### 傳統方式 vs DayFlow + VLM

| 維度 | 傳統方式 | DayFlow + VLM | 優勢 |
|-----|---------|--------------|------|
| **數據源數量** | 需整合 10+ API | 1 個錄影系統 | 🔥 簡化 90% |
| **Browser** | 只有 URL 列表 | 看到實際閱讀內容 | 🔥 更深刻 |
| **App Usage** | 只知道用了 Slack | 知道在讀還是在寫 | 🔥 更細緻 |
| **Reading** | 只有收藏列表 | 知道讀完並實操了 | 🔥 更真實 |
| **Communication** | 只有發送記錄 | 看到 triage 模式 | 🔥 更全面 |
| **實作複雜度** | 每個 API 單獨處理 | 統一 VLM 流程 | 🔥 更簡單 |
| **維護成本** | API 變更頻繁 | 不依賴外部 API | 🔥 更穩定 |
| **隱私控制** | 數據分散多處 | 本地 VLM 統一處理 | 🔥 更安全 |

### 關鍵優勢

#### ✅ 1. 一個系統，多重洞察
- DayFlow **已經在錄影** - 零額外成本
- 一套 VLM 分析流程 - 統一處理
- 跨平台通用 - 所有應用都適用

#### ✅ 2. 捕捉真實行為
不只是 API 數據：
- **實際閱讀**了什麼（不只瀏覽了）
- **停留時間** - 真實興趣指標
- **操作序列** - 工作流程洞察
- **視覺內容** - 圖片、影片理解

#### ✅ 3. 跨平台通用
不需要個別 API：
- Twitter, LinkedIn, Instagram - 全適用
- 任何網站、任何應用 - 無需整合
- 平台更新不影響 - 永續可用

---

## 🎯 數據源評估框架

### 評估維度

我們用五個維度評估每個數據源：

1. **ROI (投資回報)** - ⭐×1-5 - 洞察價值
2. **可行性** - ✅×1-3 - 實作難度
3. **隱私敏感度** - 🟢🟡🔴 - 隱私風險
4. **更新頻率** - Real-time / Daily / Weekly
5. **推薦優先級** - 🔴P0 / 🟡P1 / 🟢P2 / ⚪P3

---

## 📊 第一優先級：立即可用

### 🔴 P0 - 本週必做

#### 1. ✅ DayFlow Intelligence (已完成)

**狀態**: 已完成
**數據**: 時間分配、專注度、工具使用、工作節奏

**輸出範例**：
```json
{
  "focus_score": 81,
  "work_time_ratio": 0.704,
  "top_tools": ["GitHub", "Slack", "Twitter"],
  "peak_hours": "6-9am",
  "avg_activity_duration": "17min"
}
```

**價值**: ⭐⭐⭐⭐⭐
**可行性**: ✅✅✅ (已完成)
**隱私**: 🟢 Low

---

#### 2. ⌨️ Terminal/Shell History

**實作方式**: 直接讀取 `.zsh_history`

```bash
# 超簡單！
cat ~/.zsh_history | tail -1000
```

**可獲得的洞察**：
```json
{
  "tech_stack": {
    "languages": ["javascript", "python"],
    "tools": ["docker", "git", "npm"],
    "platforms": ["node", "aws"]
  },
  "workflow_patterns": {
    "version_control": "git_flow",
    "testing": "frequent",
    "deployment": "docker_based"
  },
  "automation_level": "medium",
  "exploration": "high"  // 常用 --help, man
}
```

**詳細分析**：
- **Top Commands** → 技術棧識別
- **Command Sequences** → 工作流程
- **Alias Usage** → 自動化程度
- **Help/Man Usage** → 學習模式
- **Error Patterns** → 問題解決方式

**價值**: ⭐⭐⭐⭐
**可行性**: ✅✅✅ (10 行代碼)
**隱私**: 🟢 Low
**推薦**: **本週立即實作**

---

#### 3. 🌐 DayFlow → Browser Activity

**實作方式**: VLM 分析錄影畫面

**vs 傳統 Browser History**：

| 傳統方式 | DayFlow + VLM |
|---------|--------------|
| 讀取 Chrome SQLite DB | 分析錄影畫面 |
| 只有 URL + 時間戳 | 有視覺內容 + 行為 |
| 不知道實際看了什麼 | 知道閱讀了哪些內容 |
| 無滾動深度 | 有滾動模式、停留時間 |

**可獲得的洞察**：
```json
{
  "session": {
    "url": "twitter.com",
    "duration": "15min",
    "content_consumed": [
      {
        "type": "thread",
        "topic": "AI agents",
        "time_spent": "8min",
        "engagement": "bookmarked"
      },
      {
        "type": "single_tweet",
        "topic": "productivity",
        "time_spent": "2min",
        "engagement": "liked"
      }
    ],
    "reading_pattern": "deep",  // 從滾動速度
    "multitasking": false
  },
  "interest_signals": {
    "high": ["AI automation", "system design"],
    "medium": ["productivity tools"],
    "low": ["politics", "entertainment"]
  }
}
```

**價值**: ⭐⭐⭐⭐⭐ (比傳統方式更好)
**可行性**: ✅✅ (需要 VLM PoC)
**隱私**: 🟡 Medium (本地 VLM 處理)
**推薦**: **本週 PoC**

---

#### 4. 📊 GitHub Activity

**實作方式**: GitHub GraphQL API

```javascript
const query = `{
  user(login: "username") {
    contributionsCollection(from: "2025-10-01") {
      commitContributionsByRepository {
        repository {
          name
          primaryLanguage { name }
        }
        contributions { totalCount }
      }
    }
  }
}`;
```

**可獲得的洞察**：
```json
{
  "coding_patterns": {
    "peak_time": "evening",  // 晚上 commit 多
    "frequency": "daily",
    "commit_message_style": "conventional_commits"
  },
  "tech_stack": {
    "primary": "JavaScript (60%)",
    "secondary": "Python (30%)",
    "learning": "Rust (10%)"
  },
  "project_types": [
    "automation_tools",
    "personal_productivity",
    "api_integration"
  ],
  "collaboration": {
    "solo_ratio": 0.7,
    "pr_review_frequency": "high",
    "open_source_contributions": 5
  }
}
```

**價值**: ⭐⭐⭐⭐⭐
**可行性**: ✅✅ (API 成熟)
**隱私**: 🟢 Low (公開數據)
**推薦**: **本週實作**

---

## 🎯 第二優先級：Phase 2

### 🟡 P1 - 2-4 週內

#### 5. 📱 DayFlow → App Usage Patterns

**透過 VLM 可以看到**：

```json
{
  "slack": {
    "channels": ["#engineering", "#product"],
    "activity": "reading",  // VLM 判斷
    "participation": "lurking",
    "topics": ["deployment", "code review"],
    "urgency": "low"
  },
  "vscode": {
    "language": "javascript",
    "activity": "writing_code",
    "focus_level": "high",  // 畫面穩定
    "context": "API endpoint development"
  },
  "notion": {
    "activity": "documentation",
    "writing_speed": "steady",
    "structure": "outline_first"
  }
}
```

**vs 傳統 App Usage**：
- 傳統只知道 "用了 Slack 30 分鐘"
- DayFlow 知道 "在 #engineering 讀了 deployment 討論"

**價值**: ⭐⭐⭐⭐⭐
**可行性**: ✅✅
**隱私**: 🟡 Medium

---

#### 6. 📖 DayFlow → Reading & Learning

**可獲得的洞察**：

```json
{
  "article": {
    "source": "Medium",
    "title": "Building AI Agents",
    "reading_time": "8min",
    "reading_pattern": "thorough",
    "highlights": true,  // 看到選取文字
    "follow_up": [
      "opened_github_repo",
      "started_terminal",
      "searched_related"
    ],
    "learning_intent": "immediate_application"
  },
  "vs_traditional": {
    "readwise": "只知道收藏了",
    "dayflow": "知道讀完並實操了"
  }
}
```

**價值**: ⭐⭐⭐⭐⭐
**可行性**: ✅✅
**隱私**: 🟢 Low

---

#### 7. 📅 Calendar Patterns

**實作方式**: Google Calendar API (已有 MCP)

**可獲得的洞察**：
```json
{
  "meeting_density": {
    "avg_per_day": 4,
    "peak_days": ["Tuesday", "Thursday"],
    "meeting_free_days": ["Monday_AM", "Friday"]
  },
  "time_blocks": {
    "focus_time": ["6-9am", "8-10pm"],
    "meeting_time": "10am-5pm",
    "admin_time": "5-6pm"
  },
  "meeting_types": {
    "1_on_1": 30,
    "team": 20,
    "external": 10,
    "avg_duration": "45min"
  },
  "calendar_discipline": "high"
}
```

**價值**: ⭐⭐⭐⭐
**可行性**: ✅✅ (MCP 已有)
**隱私**: 🟢 Low

---

#### 8. 📝 PKM System Analysis

**實作方式**: 分析 Obsidian Vault

**可獲得的洞察**：
```json
{
  "vault_stats": {
    "total_notes": 1500,
    "daily_notes": 500,
    "permanent_notes": 800,
    "project_notes": 200
  },
  "knowledge_structure": {
    "top_tags": ["ai", "productivity", "system-design"],
    "orphan_notes": 50,
    "highly_linked": [
      "Context Engine Design",
      "Personal Knowledge Management"
    ]
  },
  "thinking_mode": "zettelkasten",
  "output_input_ratio": 0.6,  // 原創 vs 摘錄
  "update_frequency": "daily"
}
```

**價值**: ⭐⭐⭐⭐
**可行性**: ✅ (需要開發 vault analyzer)
**隱私**: 🟡 Medium

---

## 🟢 第三優先級：Phase 3+

### 🟢 P2 - 選擇性實作

#### 9. 💬 DayFlow → Communication Patterns

**注意**: 隱私敏感，需特別小心

**可獲得的洞察**：
```json
{
  "email_triage": {
    "emails_scanned": 15,
    "emails_read": 3,
    "emails_replied": 1,
    "response_speed": "fast",
    "triage_efficiency": "high"
  },
  "slack_patterns": {
    "channels_checked": 5,
    "messages_read": 45,
    "messages_sent": 3,
    "communication_style": "concise",
    "response_pattern": "selective"
  },
  "note": "不提取具體內容，只分析模式"
}
```

**價值**: ⭐⭐⭐⭐
**可行性**: ✅✅
**隱私**: 🔴 High (需嚴格保護)

---

#### 10. 🎨 DayFlow → Creative Work

**可獲得的洞察**：
```json
{
  "writing": {
    "tool": "Notion",
    "type": "technical_doc",
    "writing_speed": "steady",
    "editing_ratio": "high",
    "structure": "outline_first"
  },
  "coding": {
    "language": "javascript",
    "activity": "feature_dev",
    "testing_frequency": "high",
    "focus_duration": "45min_blocks",
    "stackoverflow_usage": "moderate"
  }
}
```

**價值**: ⭐⭐⭐⭐
**可行性**: ✅✅
**隱私**: 🟢 Low

---

#### 11. 🐦 Social Media Deep Analysis

**實作方式**: Twitter API + DayFlow VLM

**混合策略**：
- Twitter API: 發文、互動數據（結構化）
- DayFlow VLM: 閱讀行為、興趣洞察（視覺化）

**可獲得的洞察**：
```json
{
  "posting_behavior": {
    "frequency": "2-3/day",
    "topics": ["AI", "productivity", "building"],
    "engagement_rate": "high"
  },
  "reading_behavior": {
    "time_spent": "30min/day",
    "content_preference": "threads_over_singles",
    "engagement_type": "curator"  // 精選式
  },
  "network": {
    "community": "AI builders, indie hackers",
    "interaction_style": "thoughtful",
    "content_sharing": "practical_insights"
  }
}
```

**價值**: ⭐⭐⭐
**可行性**: ✅ (API + VLM)
**隱私**: 🟡 Medium

---

#### 12. 📁 File System Activity

**實作方式**: `find` 命令掃描

```bash
find ~/Projects ~/Documents ~/Dropbox \
  -type f -mtime -7 \
  -not -path "*/node_modules/*"
```

**可獲得的洞察**：
```json
{
  "active_projects": [
    {
      "path": "~/iris-system",
      "files_modified": 45,
      "activity_type": "heavy_development"
    }
  ],
  "file_types": {
    "code": 60,
    "markdown": 30,
    "json": 10
  },
  "organization": "project_based"
}
```

**價值**: ⭐⭐
**可行性**: ✅✅✅
**隱私**: 🟢 Low

---

## ⚪ 第四優先級：可選

### ⚪ P3 - 按需實作

#### 13. 📧 Gmail (統計層面)

**推薦策略**: 只做統計，不分析內容

```json
{
  "volume": {
    "received": 50,
    "sent": 10,
    "avg_per_day": 15
  },
  "correspondents": {
    "top_contacts": ["colleague1", "colleague2"],
    "domains": ["work.com", "personal.com"]
  },
  "note": "不分析郵件內容，只統計模式"
}
```

**價值**: ⭐⭐⭐
**可行性**: ✅ (MCP 已有)
**隱私**: 🔴 High

---

#### 14. 🎵 Music/Podcast

**實作方式**: Spotify API 或 DayFlow

**價值**: ⭐⭐ (錦上添花)
**可行性**: 🟡
**隱私**: 🟢 Low

---

## 🚫 明確不推薦

### ❌ Health/Fitness Data

**原因**：
- 隱私極度敏感
- 與 AI Prompt 個性化關聯弱
- 可能引起用戶不適

**例外**: 如用戶明確要求，只用 "睡眠質量 → 能量預測"

---

### ❌ Location Data

**原因**：
- 隱私紅線
- 對 Context Engine 價值有限
- 地理位置與 AI 理解關聯弱

**例外**: 只用 "Home vs Office" 粗略位置可接受

---

### ❌ Financial/Purchase Data

**原因**：
- 隱私紅線
- 整合極度困難
- ROI 極低

---

## 📊 完整評估矩陣

| # | 數據源 | ROI | 可行性 | 隱私 | 優先級 | 實作方式 | 時間估算 |
|---|--------|-----|--------|------|--------|---------|---------|
| 1 | **DayFlow Intelligence** | ⭐⭐⭐⭐⭐ | ✅✅✅ | 🟢 | 🔴 P0 | 已完成 | - |
| 2 | **Terminal History** | ⭐⭐⭐⭐ | ✅✅✅ | 🟢 | 🔴 P0 | 文件讀取 | 30min |
| 3 | **DayFlow → Browser** | ⭐⭐⭐⭐⭐ | ✅✅ | 🟡 | 🔴 P0 | VLM | 2-3h |
| 4 | **GitHub Activity** | ⭐⭐⭐⭐⭐ | ✅✅ | 🟢 | 🔴 P0 | API | 30min |
| 5 | **Calendar Patterns** | ⭐⭐⭐⭐ | ✅✅ | 🟢 | 🟡 P1 | MCP (已有) | 30min |
| 6 | **DayFlow → Apps** | ⭐⭐⭐⭐⭐ | ✅✅ | 🟡 | 🟡 P1 | VLM | 1-2h |
| 7 | **DayFlow → Reading** | ⭐⭐⭐⭐ | ✅✅ | 🟢 | 🟡 P1 | VLM | 1-2h |
| 8 | **PKM Analysis** | ⭐⭐⭐⭐ | ✅ | 🟡 | 🟢 P2 | Vault scan | 3-4h |
| 9 | **DayFlow → Creative** | ⭐⭐⭐⭐ | ✅✅ | 🟢 | 🟢 P2 | VLM | 1-2h |
| 10 | **DayFlow → Comms** | ⭐⭐⭐⭐ | ✅✅ | 🔴 | 🟢 P2 | VLM | 1-2h |
| 11 | **Social Media** | ⭐⭐⭐ | ✅ | 🟡 | 🟢 P2 | API + VLM | 2-3h |
| 12 | **File System** | ⭐⭐ | ✅✅✅ | 🟢 | ⚪ P3 | find command | 1h |
| 13 | **Gmail (統計)** | ⭐⭐⭐ | ✅ | 🔴 | ⚪ P3 | MCP (已有) | 1h |
| 14 | **Music/Podcast** | ⭐⭐ | 🟡 | 🟢 | ⚪ P3 | API | 2h |

---

## 🚀 分階段實作計劃

### Phase 1: MVP - Week 1 (本週)

**目標**: 快速驗證價值，生成第一版 System Prompt

```
✅ DayFlow Intelligence (已完成)
🔲 Terminal History Analyzer (30min)
🔲 GitHub Activity Script (30min)
🔲 DayFlow VLM PoC - Browser (2-3h)
🔲 整合生成 System Prompt v0.1 (1h)

總時間: 4-5 小時
交付物: 可用的 System Prompt
```

**本週末檢查點**：
- [ ] 能在 ChatGPT/Claude 測試 System Prompt
- [ ] 獲得初步反饋
- [ ] 決定是否繼續 Phase 2

---

### Phase 2: 深度整合 - Week 2-4

**目標**: 提升洞察深度，多維度分析

```
🔲 Calendar Patterns (30min)
🔲 DayFlow → App Usage (VLM, 1-2h)
🔲 DayFlow → Reading (VLM, 1-2h)
🔲 完善 VLM Pipeline 自動化 (4-6h)
🔲 System Prompt v0.2 (動態更新)

總時間: 8-12 小時
交付物: 多維度 System Prompt，自動更新
```

---

### Phase 3: 精細優化 - Week 5-8

**目標**: 洞察質量提升，邊緣場景覆蓋

```
🔲 PKM System Analysis (3-4h)
🔲 DayFlow → Creative Work (1-2h)
🔲 DayFlow → Communication (小心隱私, 1-2h)
🔲 Social Media (Twitter API + VLM, 2-3h)
🔲 隱私控制 UI (3-4h)

總時間: 10-15 小時
交付物: 完整 Context Engine
```

---

### Phase 4: 選擇性擴展 - 按需

根據 Phase 1-3 的反饋決定：
- File System Activity
- Gmail 統計
- Music/Podcast
- 其他特殊需求

---

## 💡 立即行動：本週 Quick Wins

### 1. Terminal History (5 分鐘)

```bash
# 直接運行，立即看結果
cat ~/.zsh_history | grep -v "^#" | \
  awk '{print $1}' | sort | uniq -c | sort -rn | head -20
```

### 2. GitHub Activity (10 分鐘)

```javascript
// 快速腳本
const token = 'YOUR_GITHUB_TOKEN';
fetch('https://api.github.com/users/USERNAME/events', {
  headers: { 'Authorization': `token ${token}` }
})
.then(r => r.json())
.then(events => {
  // 分析 commit, PR, issues
  console.log(events);
});
```

### 3. Calendar Quick Check (5 分鐘)

```javascript
// 使用現有 Google Calendar MCP
mcp__google-calendar__getEvents({
  timeMin: "2025-10-26T00:00:00Z",
  timeMax: "2025-11-02T23:59:59Z",
  maxResults: 50
})
```

### 4. DayFlow VLM PoC (1-2 小時)

```bash
# 測試 Ollama + LLaVA
ollama pull llava:13b

# 手動分析 5-10 個社交媒體畫面
# 評估質量和可行性
```

---

## 🎯 成功指標

### Phase 1 完成標準

- [ ] 4 個數據源成功整合
- [ ] 生成第一版 System Prompt
- [ ] 在 ChatGPT/Claude 測試
- [ ] 感受到個性化差異
- [ ] 決定是否繼續投資

### Phase 2 完成標準

- [ ] 7+ 個數據源整合
- [ ] 自動化 VLM Pipeline
- [ ] System Prompt 動態更新
- [ ] 洞察質量明顯提升

### Phase 3 完成標準

- [ ] 完整 Context Engine 運行
- [ ] 隱私控制完善
- [ ] 用戶可審查所有數據
- [ ] 產品化準備完成

---

## 📚 附錄

### 工具清單

**已有工具**：
- DayFlow - 畫面錄製
- Ollama - Local VLM
- Google Calendar MCP
- Gmail MCP
- Gemini MCP
- GitHub (personal access)

**需要安裝**：
- LLaVA 13B model (ollama pull)
- ffmpeg (影片處理)

**可選工具**：
- Tesseract OCR (預處理)
- OpenCV (進階影像分析)

---

### 參考資料

**Local VLM**:
- LLaVA: https://github.com/haotian-liu/LLaVA
- Ollama: https://ollama.ai

**APIs**:
- GitHub GraphQL: https://docs.github.com/graphql
- Google Calendar: https://developers.google.com/calendar
- Twitter API: https://developer.twitter.com

**Context Engine**:
- 完整設計文檔: `Context-Aware-AI-Engine-Design.md`
- VLM 方案: `Context-Engine-VLM-Analysis-Approach.md`
- Local VLM: `Context-Engine-Local-VLM-Solution.md`

---

## 🤔 開放問題

### 待決策

1. **VLM PoC 要用哪個？**
   - Option A: 直接用 Local VLM (隱私優先)
   - Option B: 先用 Gemini 快速驗證 (效率優先)

2. **分析頻率？**
   - 每日 (新鮮但耗時)
   - 每週 (平衡)
   - 按需 (用戶觸發)

3. **隱私控制粒度？**
   - 完全自動 (便利)
   - 人工審查 (安全)
   - 混合 (實用)

### 需要驗證

- [ ] Local VLM 質量是否足夠
- [ ] DayFlow 錄影檔案位置和格式
- [ ] VLM 分析成本（時間和電費）
- [ ] System Prompt 實際效果

---

## ✅ 下一步

### 立即行動（今天）

1. **Terminal History** - 5 分鐘看結果
2. **GitHub Activity** - 10 分鐘腳本
3. **決定 VLM PoC 策略** - Local 還是 Cloud first?

### 本週目標

- [ ] 完成 Phase 1 所有數據源
- [ ] 生成第一版 System Prompt
- [ ] 在 AI 工具中測試
- [ ] 準備 Phase 2 規劃

### 下週計劃

根據 Phase 1 結果決定：
- 繼續深化還是調整策略
- 選擇 Phase 2 優先級
- 開始自動化開發

---

*🤖 Generated by Iris AI Butler System*
*Powered by Claude Code via [Happy Engineering](https://happy.engineering)*

**Last Updated**: 2025-11-02 18:30
**Version**: v1.0 (Merged Edition)
