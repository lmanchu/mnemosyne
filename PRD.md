# Mnemosyne - 產品需求文件 (PRD)

> **你數位生活的記憶女神**
>
> 隱私優先的情境引擎，從真實行為數據生成個人化 AI System Prompts

---

## 📋 文件資訊

| 項目 | 內容 |
|------|------|
| **產品名稱** | Mnemosyne (簡稱 Mnemo) |
| **產品類型** | Privacy-First Context Engine |
| **目標市場** | 知識工作者、內容創作者、商務專業人士 |
| **開發狀態** | Planning Phase → MVP Implementation |
| **版本** | 1.3 |
| **最後更新** | 2025-11-16 |
| **負責人** | IrisGo.AI Product Team |

---

## 🎯 產品概述

### 產品定位

Mnemosyne 是一個**隱私優先的 AI 情境引擎**，透過分析用戶的真實數位行為，自動生成個人化的 AI System Prompts，讓 AI 助理（ChatGPT、Claude、Gemini）真正了解用戶的工作風格、溝通習慣、專業領域和興趣偏好。

### 核心價值主張

**For** 知識工作者、內容創作者和商務專業人士
**Who** 希望 AI 助理更了解他們的個人特質和工作風格
**Mnemosyne is** 一個隱私優先的情境引擎
**That** 自動從真實行為數據生成個人化 System Prompts
**Unlike** 需要手動填寫或依賴雲端 API 的競品
**Our product** 100% 本地處理、自動更新、保護隱私

### 產品願景

**短期（6 個月）**：成為 IrisGo.AI 生態系統的核心情境引擎，為 1 萬名 early adopters 提供個人化 AI 體驗

**中期（1 年）**：發展成獨立產品，擁有 10 萬活躍用戶，建立隱私安全的數據變現模式

**長期（3 年）**：成為全球領先的本地優先 AI 情境引擎，100 萬+ 用戶，定義個人數據主權的新標準

---

## 💡 問題與解決方案

### 問題陳述

當用戶與 AI 助理（ChatGPT、Claude、Gemini）對話時，AI 並不了解他們：

1. **工作風格不明**：不知道用戶是早上還是晚上工作、偏好深度工作還是協作
2. **專業領域未知**：不知道用戶的專業背景、技能水平、當前專注的項目
3. **興趣偏好缺失**：不知道用戶關注什麼主題、閱讀什麼內容、學習什麼技能
4. **溝通習慣不清**：不知道用戶偏好簡潔還是詳細的回答、正式還是輕鬆的語氣

**結果**：AI 給出的是通用、一體適用的回答，無法滿足個人化需求，降低了 AI 助理的實用價值。

### 現有解決方案的問題

| 方案 | 問題 |
|------|------|
| **手動設定 Custom Instructions** | 費時、不完整、需要持續更新 |
| **雲端 Profile 服務** | 隱私風險、數據上傳、依賴第三方 |
| **API 整合方案** | 成本高、API 變更頻繁、覆蓋範圍有限 |
| **問卷調查** | 不反映真實行為、用戶疲勞、數據過時 |

### Mnemosyne 的解決方案

**自動生成個人化 System Prompt**，透過分析真實行為數據：

```markdown
你正在與 Lman 對話，他是一位專注於 AI automation 的創業家。

## 工作風格
- 最佳工作時段：早上 9-12 點、下午 2-5 點
- 深度工作偏好：75% solo work、25% 協作
- 溝通風格：簡潔、數據驅動、半正式

## 當前專注
- 開發 IrisGo（本地優先的 AI 產品）
- 研究 VLM 應用和情境引擎
- 興趣：生產力自動化、系統設計

## 偏好
- 喜歡實用案例勝過純理論
- 重視隱私和本地優先方案
- 欣賞簡潔但完整的回答
```

**效果**：AI 的回答更個人化、更相關、更符合用戶當下的工作重點和溝通風格。

---

## 👥 目標用戶 (ICP)

### 主要用戶群

**1. 知識工作者 (Knowledge Workers)**
- **定義**：產品經理、UX 設計師、數據分析師、研究員
- **痛點**：需要 AI 協助研究、分析、決策，但通用回答不夠精準
- **使用場景**：
  - 產品研究和競品分析
  - 數據解讀和洞察提取
  - 文件撰寫和簡報準備
  - 學習新技能和工具
- **關鍵需求**：AI 了解其專業領域和當前專注的項目

**2. 內容創作者 (Content Creators)**
- **定義**：部落客、YouTuber、Newsletter 作者、社群媒體創作者
- **痛點**：需要 AI 協助創作，但希望保持個人風格和聲音
- **使用場景**：
  - 文章大綱和腳本生成
  - 標題和 hook 優化
  - SEO 和受眾分析
  - 內容點子發想
- **關鍵需求**：AI 理解其寫作風格和受眾偏好

**3. 商務專業人士 (Business Professionals)**
- **定義**：顧問、業務開發、企業主、高階主管
- **痛點**：需要 AI 協助商務溝通，但必須符合專業形象
- **使用場景**：
  - Email 和提案撰寫
  - 會議準備和簡報
  - 客戶溝通和談判
  - 策略規劃和決策
- **關鍵需求**：AI 掌握其溝通風格和時間管理模式

### 用戶特徵

**共同特徵**：
- ✅ 大量文字工作（Email、文件、簡報、文章）
- ✅ 重視溝通效率和專業形象
- ✅ 需要時間管理和優先級設定
- ✅ 持續學習行業趨勢
- ✅ 數位原生，熟悉各種工具和平台
- ❌ 不一定有技術背景（非開發者）

**數位行為模式**：
- 每天使用 AI 助理 2-5 次
- 活躍於 LinkedIn、Medium、Twitter 等平台
- 使用 Gmail、Google Calendar、Notion/Obsidian 等工具
- 重視隱私和數據安全
- 願意為個人化體驗付費

### 市場規模

**TAM (Total Addressable Market)**：
- 全球知識工作者：3 億人
- AI 工具活躍用戶：1 億人（ChatGPT、Claude、Gemini）

**SAM (Serviceable Addressable Market)**：
- 重視隱私的 AI 用戶：1000 萬人（10%）
- 願意使用本地處理方案：300 萬人（3%）

**SOM (Serviceable Obtainable Market)**：
- Year 1：1 萬用戶（0.3%）
- Year 2：10 萬用戶（3%）
- Year 3：100 萬用戶（30%）

---

## 🔧 產品功能

### 核心功能（MVP - 6 週）

#### 1. 數據收集系統

**1.1 DayFlow VLM Collector (40% 權重)**

**功能描述**：分析螢幕錄製內容，提取用戶的興趣和內容偏好

**技術實施**：

<details>
<summary><strong>macOS 實施</strong></summary>

- 使用現有 DayFlow 系統
- 螢幕錄製：1 frame/second
- 影片編碼：H.264, Metal 硬體加速
- 儲存：約 25 GB/週
- 分析：選擇性抽樣（每 5 分鐘抽取 1 幀，約 2000 幀/週）
- VLM：Ollama + LLaVA 13B (Metal)
</details>

<details>
<summary><strong>Windows 實施</strong></summary>

```csharp
// Windows Graphics Capture API
using Windows.Graphics.Capture;
using Windows.Media.MediaProperties;

public class DayFlowWindowsCapture {
    // 1 fps 螢幕錄製
    private GraphicsCaptureSession session;

    public async Task StartCapture() {
        var encoding = VideoEncodingProperties.CreateH264();
        encoding.Bitrate = 1000000;  // 1 Mbps
        encoding.FrameRate = new MediaRatio(1, 1);  // 1 fps

        // 使用 Intel Quick Sync / NVENC 硬體編碼
        var item = await GetPrimaryMonitor();
        session = new GraphicsCaptureSession(item);
    }
}
```

- 螢幕錄製：1 frame/second
- 影片編碼：H.264, Intel Quick Sync / NVENC 硬體加速
- 儲存：約 25 GB/週（與 macOS 相同）
- 分析：選擇性抽樣（每 5 分鐘抽取 1 幀）
- VLM：Ollama + LLaVA 13B (CUDA/DirectML)
- 部署：OEM 預裝 Windows Service
</details>

**共通設計**：
- 敏感網站黑名單過濾（銀行、郵件、訊息 app）
- 夜間批次處理（23:00 - 03:00）
- 用戶可配置保留天數（7/14/30 天）
- 分析後可選擇刪除原始影片（僅保留洞察）

**提取數據**：
```json
{
  "interests": {
    "ai_automation": 0.95,
    "productivity_tools": 0.88,
    "content_marketing": 0.75
  },
  "platforms": {
    "linkedin": 0.65,
    "medium": 0.25,
    "youtube": 0.10
  },
  "content_types": {
    "articles": 0.65,
    "videos": 0.25,
    "social": 0.10
  },
  "reading_depth": "deep_reader",
  "learning_style": "visual_learner"
}
```

**隱私保護**：
- 黑名單網站自動跳過
- OCR 預掃描敏感關鍵字
- VLM prompt 指示忽略 PII
- 100% 本地處理，不上傳雲端
- 用戶可審查所有待分析畫面

---

**1.2 Gmail Sent Mail Collector (30% 權重)**

**功能描述**：分析寄出的郵件，提取溝通風格和寫作習慣

**技術實施**（兩平台相同）：

<details>
<summary><strong>通用實施</strong>（macOS & Windows）</summary>

- **連線協議**：IMAP（唯讀模式，EXAMINE 指令）
- **目標資料夾**：`[Gmail]/Sent Mail`
- **抓取頻率**：每週一次，過去 7 天郵件（平均 20-50 封）
- **分析引擎**：Ollama + Llama 3.2（本地 LLM）
- **排程**：
  - **macOS**: LaunchAgent（每天 23:00）
  - **Windows**: Task Scheduler（每天 23:00）
- **技術棧**：
  - Node.js: `node-imap` + `mailparser`
  - OAuth2 或 App-Specific Password
  - PII 過濾：正則表達式 + 本地 LLM 檢測

</details>

**實施細節**：
- 平台無關性高（Node.js 跨平台）
- 憑證儲存：macOS Keychain（macOS）/ Windows Credential Manager（Windows）
- 記憶體占用：< 100 MB
- 處理時間：約 30-60 秒（50 封郵件）

**提取數據**：
```json
{
  "tone": "professional_friendly",
  "structure": {
    "bullet_points": 0.70,
    "paragraphs": 0.30
  },
  "avg_length": 180,
  "formality": "semi_formal",
  "common_openings": [
    "感謝回覆",
    "更新一下進度",
    "快速確認"
  ],
  "common_closings": [
    "請確認",
    "有問題隨時討論",
    "期待你的回覆"
  ],
  "response_pattern": {
    "avg_time": "2.5 hours",
    "batch_mode": "morning_replies"
  }
}
```

**隱私保護**：
- OAuth2 / App-Specific Password
- 唯讀模式（EXAMINE 指令）
- PII 自動過濾（email、電話、地址）
- 不儲存原文，只儲存風格特徵
- 用戶可設定黑名單（排除特定收件人）

---

**1.3 Calendar Collector (20% 權重)**

**功能描述**：分析行事曆，理解時間管理和工作模式

**技術實施**（兩平台相同）：

<details>
<summary><strong>通用實施</strong>（macOS & Windows）</summary>

- **連線方式**：Google Calendar API 或 MCP（Model Context Protocol）
- **資料範圍**：過去 30 天的行事曆事件
- **分析類型**：統計分析（無需 AI）
- **排程**：
  - **macOS**: LaunchAgent（每週一次）
  - **Windows**: Task Scheduler（每週一次）
- **技術棧**：
  - Node.js: `googleapis` 或 Google Calendar MCP
  - OAuth2 認證（Web flow）
  - 純 JavaScript 統計分析（無需 LLM）

</details>

**實施細節**：
- 平台無關性：100%（純 Web API）
- 憑證儲存：macOS Keychain（macOS）/ Windows Credential Manager（Windows）
- 記憶體占用：< 50 MB
- 處理時間：約 5-10 秒（100 個事件）
- 只讀取 metadata，不讀取事件描述內容

**提取數據**：
```json
{
  "meeting_density": "medium",
  "meetings_per_week": 8,
  "avg_meeting_duration": 30,
  "preferred_time": "afternoon",
  "meeting_types": {
    "one_on_one": 0.40,
    "team": 0.35,
    "external": 0.25
  },
  "focus_blocks": [
    {"time": "9-11am", "frequency": 0.90},
    {"time": "2-4pm", "frequency": 0.75}
  ],
  "work_life_balance": {
    "work_hours_per_week": 45,
    "weekend_work": 0.10
  }
}
```

**隱私保護**：
- 只讀取統計數據，不讀取事件內容
- 會議標題做 hash 處理
- 參與者資訊不保存

---

**1.4 DayFlow Intelligence / Activity Tracker (10% 權重)**

**功能描述**：追蹤應用使用和活動模式，提供基礎行為數據

**技術實施**：

<details>
<summary><strong>macOS 實施</strong></summary>

- 使用現有 DayFlow Intelligence 系統
- API 整合讀取應用使用統計
- 自動分析工作時段和專注度
</details>

<details>
<summary><strong>Windows 實施</strong> (自建 Activity Tracker)</summary>

```csharp
// Windows 活動追蹤服務
using System.Diagnostics;
using System.Runtime.InteropServices;

public class WindowsActivityTracker {
    [DllImport("user32.dll")]
    static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);

    // 每秒追蹤一次活動視窗
    public ActivitySnapshot CaptureActivity() {
        var hwnd = GetForegroundWindow();
        var process = GetProcessFromWindow(hwnd);

        return new ActivitySnapshot {
            Timestamp = DateTime.Now,
            AppName = process.ProcessName,
            WindowTitle = SanitizeTitle(GetWindowText(hwnd)),
            IsIdle = GetIdleTime() > 60,  // 60 秒無活動視為閒置
            KeyboardActive = IsKeyboardActive(),
            MouseActive = IsMouseActive()
        };
    }

    // 計算應用使用時間
    public Dictionary<string, TimeSpan> CalculateAppUsage(
        DateTime start, DateTime end)
    {
        var activities = GetActivities(start, end);
        return activities
            .GroupBy(a => a.AppName)
            .ToDictionary(
                g => g.Key,
                g => TimeSpan.FromSeconds(g.Count())
            );
    }
}
```

**實施細節**：
- 背景服務：每秒記錄活動視窗
- 使用 Windows API (user32.dll, kernel32.dll)
- 記憶體占用：< 50 MB
- CPU 占用：< 1%
- 儲存：約 10 MB/天（純 metadata）
- 部署：Windows Service (開機自動啟動)
</details>

**提取數據**（兩平台相同格式）：
```json
{
  "app_usage": {
    "browser": 0.45,
    "notion": 0.20,
    "slack": 0.15,
    "other": 0.20
  },
  "working_hours": {
    "peak": ["9-12am", "2-5pm"],
    "total_focused_hours": 6.5
  },
  "work_life_balance": {
    "work": 0.70,
    "personal": 0.30
  },
  "multitasking_score": 0.65
}
```

---

#### 2. 數據分析系統

**2.1 Persona Analyzer**

**功能**：聚合所有數據源，生成用戶 Persona

**輸出**：
```json
{
  "professional_identity": {
    "role": "Product Manager",
    "seniority": "Senior",
    "focus_areas": ["AI Automation", "Productivity Tools"]
  },
  "working_style": {
    "peak_hours": ["9-12am", "2-5pm"],
    "meeting_preference": "low_moderate",
    "collaboration_ratio": 0.25
  },
  "communication_style": {
    "tone": "professional_friendly",
    "structure": "bullet_point_heavy",
    "length": "concise",
    "formality": "semi_formal"
  },
  "interests": [
    {"topic": "AI Automation", "confidence": 0.95},
    {"topic": "Productivity", "confidence": 0.88},
    {"topic": "System Design", "confidence": 0.75}
  ],
  "content_preferences": {
    "type": "deep_technical_articles",
    "platforms": ["LinkedIn", "Medium"],
    "reading_speed": "fast_scanner"
  }
}
```

**2.2 Communication Analyzer**

**功能**：深度分析溝通模式和寫作風格

**2.3 Time Analyzer**

**功能**：分析時間管理和工作節奏

**2.4 Interest Analyzer**

**功能**：識別興趣主題和學習模式

---

#### 3. System Prompt 生成器

**3.1 Prompt Generator**

**功能**：根據 Persona 生成完整的 System Prompt

**模板**：
```markdown
# 你正在與 {{name}} 對話

## 👤 專業身份
- 職業：{{role}}
- 專長領域：{{expertise}}
- 當前專注：{{current_focus}}

## 💬 溝通風格
- 語氣：{{tone}}
- 結構偏好：{{structure}}
- 回應長度：{{length}}
- 正式程度：{{formality}}

## ⏰ 工作模式
- 最佳工作時段：{{peak_hours}}
- 會議習慣：{{meeting_pattern}}
- 深度工作時段：{{focus_blocks}}
- 回信習慣：{{email_pattern}}

## 📚 興趣與專業
- 主要關注：
  {{#interests}}
  - {{topic}}（{{confidence}}）
  {{/interests}}

- 內容偏好：
  - 喜歡：{{preferences_positive}}
  - 避免：{{preferences_negative}}

## 🎯 AI 互動偏好
{{interaction_guidelines}}
```

**輸出格式**：
- Markdown 文件（可直接複製）
- JSON 格式（程式化使用）
- 針對不同 AI 平台優化的版本：
  - ChatGPT Custom Instructions
  - Claude Project Instructions
  - Gemini Custom Instructions

---

#### 3.2 產出與價值交付

Mnemosyne 不只生成 System Prompt，更提供全方位的個人數位洞察和優化建議。

**核心產出（MVP）**：

<details>
<summary><strong>1. 個人化 AI System Prompts</strong>（核心功能）</summary>

**輸出內容**：
- 完整的 System Prompt（Markdown 格式）
- 針對不同 AI 平台的優化版本（ChatGPT/Claude/Gemini）
- 每週自動更新（檢測行為變化）

**價值**：
- AI 回答更精準、更相關
- 減少重複澄清需求的時間
- 保持個人風格和語氣一致性

**範例輸出**：
```markdown
你正在與 Lman 對話，他是專注於 AI automation 的創業家...
（完整 System Prompt 如前所示）
```

</details>

<details>
<summary><strong>2. 個人數位畫像儀表板</strong>（Self-Analytics）</summary>

**工作模式洞察**：
```bash
$ mnemo insights work
📊 工作模式分析（過去 30 天）

🕐 最佳專注時段：
  - 早上 9:00-12:00（專注度 92%）
  - 下午 2:00-5:00（專注度 85%）

⚡ 生產力趨勢：
  - 深度工作：6.5 小時/天（↑ 15% vs 上月）
  - 多工模式：35%（↓ 10% vs 上月）✨ 改善中

📅 會議模式：
  - 每週 8 小時會議（中等密度）
  - 建議：保護早上 9-12 點作為深度工作時段
```

**興趣演變時間線**：
```bash
$ mnemo insights interests
📈 興趣演變分析

當前熱門主題（本週）：
  🔥 VLM Applications (95% 信心度)
  🔥 Context Engines (88% 信心度)

興趣軌跡：
  3 個月前：Web3、區塊鏈
  1 個月前：AI Agents、自動化
  本週：VLM、個人化 AI

💡 洞察：你的興趣正在向「個人化 AI 系統」深化
```

**溝通風格分析**：
```bash
$ mnemo insights communication
💬 溝通風格報告

Email 特徵：
  - 語氣：專業友善（70% 正式、30% 輕鬆）
  - 結構：項目符號為主（70% bullet points）
  - 長度：簡潔（平均 180 字）
  - 回覆速度：2.5 小時（快速回應者）

趨勢變化：
  - 本月 Email 長度 -15%（更簡潔）✨
  - 回覆速度加快 20%
```

</details>

<details>
<summary><strong>3. 生產力優化建議</strong>（Actionable Insights）</summary>

**會議優化建議**：
```bash
$ mnemo optimize meetings
📊 會議分析與建議

當前狀況：
  - 每週 8 小時會議（中等密度）
  - 最常開會時間：下午 2-5pm

⚠️ 發現的問題：
  1. 下午 2-5pm 是你第二專注時段，但被會議占用 60%
  2. 早上 9-12pm 專注度最高，但仍有 3 個會議

✨ 優化建議：
  1. 將例行會議移到下午 5-6pm（非高效時段）
  2. 保護早上 9-12pm 為「深度工作專屬時段」
  3. 減少 1:1 會議 30%（目前占比 40%，略高）

💰 預估效果：
  - 深度工作時間 +2.5 小時/週
  - 生產力提升 25-30%
```

**精力管理洞察**：
```bash
$ mnemo insights energy
⚡ 精力管理分析

每週模式：
  週一：精力充沛（9/10）
  週二：高效（8/10）
  週三下午：明顯下降（5/10）⚠️
  週四：回升（7/10）
  週五下午：低效（4/10）⚠️

💡 建議：
  - 週三下午安排輕鬆任務（Admin work、Email）
  - 週五下午適合 brainstorming、學習新技能
  - 避免在這些時段安排重要決策或深度工作
```

</details>

---

**進階產出（Alpha 階段）**：

<details>
<summary><strong>4. AI 使用效果追蹤</strong></summary>

**Before/After 比較**：
```bash
$ mnemo analytics ai-impact
📊 AI 使用效果分析

使用 Mnemosyne 前（30 天）：
  - AI 對話次數：120 次
  - 平均澄清次數：3.5 次/對話
  - 滿意度：65%

使用 Mnemosyne 後（30 天）：
  - AI 對話次數：95 次（效率提升）
  - 平均澄清次數：1.2 次/對話（↓ 66%）✨
  - 滿意度：92%（↑ 42%）✨

💰 時間節省：
  - 每次對話節省 2.5 分鐘
  - 每月節省 4 小時
  - 年度 ROI：$2,400（以時薪 $50 計算）
```

</details>

<details>
<summary><strong>5. 個人化內容推薦</strong></summary>

**學習資源推薦**：
```bash
$ mnemo recommend learning
📚 個人化學習推薦

基於你的興趣（VLM Applications, Context Engines）：

🔥 高度推薦：
  1. "Building Production VLM Systems" (Andrej Karpathy)
     匹配度：95% | 深度：Advanced | 時長：2 小時

  2. "Context Window Optimization in LLMs" (OpenAI Research)
     匹配度：88% | 深度：Intermediate | 時長：45 分鐘

💡 內容創作靈感：
基於你過去 3 個月閱讀，以下主題適合你寫作：
  - "本地優先 VLM 的隱私優勢"（興趣重疊度 92%）
  - "AI Context Engine 的商業應用"（專業度匹配 85%）
```

</details>

<details>
<summary><strong>6. 週報 / 月報</strong>（Automated Insights）</summary>

**個人化週報**：
```markdown
# 📊 Mnemosyne 週報（2025-11-10 ~ 2025-11-16）

## 🎯 本週亮點

### 工作模式
- 深度工作：45 小時（↑ 20% vs 上週）✨
- 專注度評分：8.5/10（持平）
- 最佳時段：週二早上 9-12am（專注度 95%）

### 興趣演變
- **新興興趣**：VLM Applications（從 65% → 95%）🔥
- 持續關注：AI Automation（穩定 92%）
- 興趣深化：從「廣泛探索」轉向「深度研究」

### 溝通風格
- Email 平均長度：165 字（↓ 15%，更簡潔）✨
- 回覆速度：2.1 小時（加快 16%）
- 語氣變化：更偏向「直接、數據驅動」

## 📈 趨勢分析

你的工作模式正在優化：
- 深度工作時間持續增加
- 會議效率提升（平均時長 -10 分鐘）
- 溝通更簡潔高效

## 💡 下週建議

1. **保護早上時段**：繼續將深度工作安排在 9-12am
2. **新興趣探索**：你可能對「Multimodal AI」感興趣（基於最近搜尋）
3. **內容創作**：本週閱讀 VLM 相關文章 12 篇，適合撰寫技術總結

## 🎯 System Prompt 更新

檢測到以下變化，已自動更新 System Prompt：
- ✅ 新增興趣：VLM Applications
- ✅ 溝通風格：更新為「簡潔、直接」
- ✅ 當前專注：更新為「Context Engine 研究」
```

</details>

---

**未來產出（Beta/Enterprise）**：

<details>
<summary><strong>7. Personal API</strong>（開發者功能）</summary>

允許用戶的其他工具和自動化流程查詢 Mnemosyne 洞察：

```javascript
// Personal API 範例
const mnemo = require('@irisgo/mnemosyne-api');

// 取得當前 Persona
const persona = await mnemo.getPersona();
console.log(persona.interests); // ["AI Automation", "VLM Applications"]

// 取得最佳專注時段
const focusTime = await mnemo.getFocusTime();
console.log(focusTime.peak); // ["9-12am", "2-5pm"]

// 整合到自動化工作流（Zapier、Make.com）
if (persona.energy < 5) {
  // 精力低落時，自動調整 Calendar，減少會議
  calendar.blockDeepWork("9-12am");
}
```

**使用場景**：
- 自動調整 Calendar 深度工作時段
- 根據精力水平推薦任務優先級
- 整合到個人生產力系統（Notion、Todoist）

</details>

<details>
<summary><strong>8. 標籤資產組合</strong>（Data Monetization）</summary>

```bash
$ mnemo assets portfolio
💰 標籤資產組合（本月價值）

Tier 1 標籤（粗粒度）：
  - Region: Asia-Pacific
  - Industry: Tech
  - 預估價值：$15-25/月

Tier 2 標籤（中粒度）：
  - Expertise: AI Automation (Expert)
  - Interests: VLM Applications (95% confidence)
  - 預估價值：$35-50/月

總價值：$50-75/月

💡 優化建議：
  - 增加 LinkedIn AI 相關內容互動 → 可提升標籤價值 $10-15/月
  - 參與 VLM 相關討論 → 強化專業度信號
```

</details>

<details>
<summary><strong>9. 團隊協作洞察</strong>（Enterprise 版）</summary>

**團隊溝通模式**：
```bash
$ mnemo team insights
👥 團隊協作分析

你在團隊中的角色：
  - 溝通樞紐指數：8.5/10（高度連接者）
  - 跨部門協作：頻繁（與 5 個團隊互動）
  - 知識分享者：你是「AI Automation」領域的 go-to person

建議：
  - 可以主導 AI 相關的 knowledge sharing session
  - 減少低價值會議，保護深度工作時間
```

</details>

---

**產出摘要表**：

| 產出類型 | MVP | Alpha | Beta | Enterprise | 主要價值 |
|---------|-----|-------|------|------------|---------|
| System Prompt | ✅ | ✅ | ✅ | ✅ | 個人化 AI 體驗 |
| 工作模式洞察 | ✅ | ✅ | ✅ | ✅ | 生產力優化 |
| 興趣演變分析 | ✅ | ✅ | ✅ | ✅ | 自我認識 |
| 優化建議 | - | ✅ | ✅ | ✅ | 行動指引 |
| AI 效果追蹤 | - | ✅ | ✅ | ✅ | ROI 證明 |
| 內容推薦 | - | ✅ | ✅ | ✅ | 學習加速 |
| 週報/月報 | - | ✅ | ✅ | ✅ | 趨勢追蹤 |
| Personal API | - | - | ✅ | ✅ | 自動化整合 |
| 標籤資產組合 | - | - | ✅ | ✅ | 數據變現 |
| 團隊洞察 | - | - | - | ✅ | 協作優化 |

---

#### 4. CLI 工具

**4.1 命令列介面**（兩平台相同）

<details>
<summary><strong>平台實施</strong></summary>

**macOS / Linux**:
```bash
$ mnemo generate  # 使用 Node.js CLI
```

**Windows**:
```powershell
PS> mnemo generate  # 使用 Node.js CLI 或 C# 包裝器
```

**技術棧**：
- **核心**：Node.js (Commander.js, Inquirer.js, Chalk, Ora)
- **macOS**: 直接執行 Node.js
- **Windows 選項 1**：Node.js（需用戶安裝）
- **Windows 選項 2**：C# Console App 包裝 Node.js（OEM 預裝，對用戶透明）
- **Windows 選項 3**：pkg 打包成 .exe（獨立可執行檔，不需 Node.js）

**推薦方案（Windows OEM）**：使用 `pkg` 將 Node.js CLI 打包成獨立 .exe，用戶無需安裝 Node.js

</details>

```bash
# 生成 System Prompt
$ mnemo generate
🔍 收集數據...
  ✓ DayFlow VLM 分析 (40%)
  ✓ Gmail Sent 分析 (30%)
  ✓ Calendar 分析 (20%)
  ✓ DayFlow Stats (10%)
✨ System Prompt 已生成！

# 查看當前 Persona
$ mnemo show
👤 專業身份: Product Manager (Senior)
💬 溝通風格: 專業友善、簡潔、項目符號為主
⏰ 工作模式: 早上 9-12am 最專注
📚 主要興趣: AI Automation (95%), Productivity (88%)

# 導出到不同平台
$ mnemo export chatgpt
📋 已複製 ChatGPT Custom Instructions 到剪貼簿

$ mnemo export claude
📋 已複製 Claude Project Instructions 到剪貼簿

# 查看數據源狀態
$ mnemo stats
📊 數據源狀態：
  DayFlow VLM:  ✓ 最後更新 2 小時前（1,850 幀）
  Gmail Sent:   ✓ 最後更新 1 天前（45 封郵件）
  Calendar:     ✓ 最後更新 1 天前（23 個事件）
  DayFlow Stats:✓ 最後更新 2 小時前

# 更新 Persona
$ mnemo update
🔄 更新中...
✓ 已更新 System Prompt（檢測到新的興趣主題：VLM Applications）

# 查看標籤資產（未來功能）
$ mnemo assets
💰 標籤資產價值：
  Tier 1: $15-25/月（廣泛興趣標籤）
  Tier 2: $35-50/月（專業技能標籤）
  總計: $50-75/月
```

---

#### 5. 自動化排程

**5.1 平台自動化整合**

<details>
<summary><strong>macOS - LaunchAgent</strong></summary>

```xml
<!-- ~/Library/LaunchAgents/com.irisgo.mnemosyne.plist -->
<dict>
  <key>Label</key>
  <string>com.irisgo.mnemosyne</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/local/bin/node</string>
    <string>/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/src/cli/mnemo-cli.js</string>
    <string>update</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Weekday</key>
    <integer>0</integer>  <!-- 每週日 -->
    <key>Hour</key>
    <integer>1</integer>   <!-- 凌晨 1 點 -->
    <key>Minute</key>
    <integer>0</integer>
  </dict>
</dict>
```

**安裝**：
```bash
launchctl load ~/Library/LaunchAgents/com.irisgo.mnemosyne.plist
```

</details>

<details>
<summary><strong>Windows - Task Scheduler</strong></summary>

```xml
<!-- Mnemosyne_WeeklyUpdate.xml -->
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-01-01T01:00:00</StartBoundary>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Sunday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\Program Files\Mnemosyne\mnemo.exe</Command>
      <Arguments>update</Arguments>
    </Exec>
  </Actions>
  <Settings>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
  </Settings>
</Task>
```

**安裝**：
```powershell
schtasks /Create /XML "C:\Program Files\Mnemosyne\Mnemosyne_WeeklyUpdate.xml" /TN "Mnemosyne\WeeklyUpdate"
```

或使用 C# 程式化安裝：
```csharp
using Microsoft.Win32.TaskScheduler;

public void InstallScheduledTask() {
    using (TaskService ts = new TaskService()) {
        TaskDefinition td = ts.NewTask();
        td.Triggers.Add(new WeeklyTrigger {
            DaysOfWeek = DaysOfTheWeek.Sunday,
            StartBoundary = DateTime.Today + TimeSpan.FromHours(1)
        });
        td.Actions.Add(new ExecAction(
            @"C:\Program Files\Mnemosyne\mnemo.exe",
            "update",
            null
        ));
        ts.RootFolder.RegisterTaskDefinition(
            "Mnemosyne\\WeeklyUpdate",
            td
        );
    }
}
```

</details>

**執行時程**（兩平台相同）：
- **每週日凌晨 1:00**：完整更新 System Prompt
- **每天晚上 23:00**：收集當天數據（Gmail、DayFlow）
- **需要時手動**：`mnemo update` 立即更新

---

### 次要功能（Phase 2 - Month 3-4）

#### 5. Slack/Teams Collector

**功能描述**：分析團隊溝通工具中的訊息，補充即時溝通風格

**技術實施**：
- Slack API / Slack MCP
- Microsoft Teams Graph API
- 只分析用戶發送的訊息（不分析接收的訊息）
- 本地 LLM（Ollama Llama 3.2）分析

**提取數據**：
```json
{
  "communication_style": {
    "async_vs_sync": 0.70,
    "emoji_usage": 0.45,
    "response_time": "within_30min",
    "message_length": "concise",
    "thread_participation": "active_contributor"
  },
  "collaboration_patterns": {
    "channels": ["#product", "#ai-research", "#team"],
    "dm_ratio": 0.30,
    "peak_hours": ["10-12am", "3-5pm"],
    "weekday_vs_weekend": "95_5"
  },
  "work_relationships": {
    "frequent_contacts": 15,
    "cross_functional": true,
    "team_size_preference": "small_medium"
  }
}
```

**隱私保護**：
- ⚠️ 中等風險（工作溝通）
- 頻道黑名單（#confidential, #legal, #hr）
- 自動過濾 @mentions、URLs、附件名稱
- 不儲存原文，只儲存模式特徵

**價值**：
- 了解即時溝通風格（vs Email 的正式溝通）
- 識別協作偏好
- 補足 Email 無法覆蓋的團隊互動

---

#### 6. Notion/Obsidian Collector

**功能描述**：分析個人知識管理系統，了解思考結構和學習模式

**技術實施**：
- **Notion**: OAuth API 整合
- **Obsidian**: 本地 .md 檔案讀取（無需 API）
- 分析 metadata、標籤、連結
- 本地 LLM 提取主題

**提取數據**：
```json
{
  "knowledge_structure": {
    "top_topics": [
      {"topic": "AI Automation", "note_count": 45, "growth": "high"},
      {"topic": "Product Design", "note_count": 32, "growth": "medium"}
    ],
    "organization_style": "hierarchical",
    "note_taking_frequency": "daily",
    "total_notes": 850
  },
  "learning_patterns": {
    "avg_note_length": 350,
    "link_density": "high",
    "review_frequency": "weekly",
    "backlink_usage": "active",
    "learning_style": "structured_deep_dive"
  },
  "content_creation": {
    "drafts": 12,
    "published_notes": 8,
    "writing_style": "structured_long_form",
    "templates_used": ["meeting_notes", "book_summary"]
  }
}
```

**隱私保護**：
- ✅ 低風險（用戶自己的筆記）
- Notion: 用戶授權 OAuth，可撤銷
- Obsidian: 本地處理，不上傳
- 只分析結構和主題，不讀取完整內容

**價值**：
- 了解思考結構和知識體系
- 識別學習興趣和深度
- 補充 DayFlow VLM 看不到的私密學習內容
- 對內容創作者特別有價值

---

#### 7. Browser History Collector

**功能描述**：分析瀏覽器歷史記錄，作為 DayFlow VLM 的輕量級補充/替代

**技術實施**：
- 直接讀取 Chrome/Safari History SQLite 數據庫
- 無需 API，本地處理
- 與 DayFlow VLM 互補或作為 fallback

**提取數據**：
```json
{
  "browsing_patterns": {
    "top_domains": [
      {"domain": "linkedin.com", "visits": 450, "avg_time": "5min"},
      {"domain": "medium.com", "visits": 320, "avg_time": "8min"},
      {"domain": "github.com", "visits": 280, "avg_time": "3min"}
    ],
    "search_queries": [
      "AI automation tools 2025",
      "best productivity apps for Mac",
      "local-first software"
    ],
    "reading_time_distribution": {
      "skim": 0.60,
      "medium": 0.30,
      "deep": 0.10
    },
    "daily_pattern": "morning_research_afternoon_execution"
  },
  "interests_timeline": {
    "this_week": ["VLM applications", "Context engines"],
    "last_month": ["AI agents", "Local-first software"],
    "trend": "deepening_focus"
  }
}
```

**隱私保護**：
- ⚠️ 中等風險（包含所有網站）
- 敏感網站黑名單（銀行、郵件、成人內容、醫療）
- 只提取 domain + title，不提取 URL 參數
- 不儲存完整 URL

**價值**：
- **比 DayFlow VLM 更輕量**（不需要 VLM 處理）
- 提供精確的時間戳和訪問頻率
- 捕捉搜尋意圖（search queries）
- 作為 VLM 的 fallback（當 VLM 處理太慢或資源不足時）

**與 DayFlow VLM 的關係**：
- **互補模式**：VLM 看畫面內容，History 看 metadata
- **Fallback 模式**：若 VLM 無法運行，降級使用 History
- **權重調整**：根據用戶硬體能力動態調整

---

#### 8. 個人標籤資產系統與競爭護城河

**核心理念**：用戶數位行為標籤是可累積、可變現的個人資產

Mnemosyne 不只是生成 System Prompts 的工具，更是一個讓用戶**擁有並變現自己數位行為數據**的平台。透過分層標籤系統，用戶可以選擇性地分享隱私安全的標籤，同時獲得收益。

---

##### 8.1 分層標籤架構

**設計原則**：
- 用戶完全擁有所有標籤
- 標籤留在本地，只有用戶明確同意才上傳
- 分層設計確保隱私和變現的平衡

<details>
<summary><strong>Tier 1 標籤（粗粒度）</strong> - 可上傳變現</summary>

**特徵**：
- **K-Anonymity ≥ 100,000**（至少 10 萬用戶共享相同標籤）
- 覆蓋範圍廣，無法識別個人
- 可選擇性上傳到服務器

**範例標籤**：
```json
{
  "geo": {
    "region": "Asia-Pacific",
    "timezone": "UTC+8"
  },
  "broad_interests": [
    "Technology",
    "Business",
    "Productivity"
  ],
  "professional": {
    "industry": "Tech",
    "role_category": "Knowledge Worker"
  },
  "platform_usage": [
    "LinkedIn",
    "Email",
    "Calendar"
  ]
}
```

**變現價值**：$15-25/月

**隱私保護**：
- 極低風險（覆蓋 >10 萬用戶）
- 無法逆向識別個人
- 動態調整 K-Anonymity 閾值

</details>

<details>
<summary><strong>Tier 2 標籤（中粒度）</strong> - 用戶同意後可變現</summary>

**特徵**：
- **K-Anonymity ≥ 10,000**（至少 1 萬用戶共享）
- 較具體的興趣和專業度
- 需用戶明確同意（Opt-in）

**範例標籤**：
```json
{
  "specific_interests": {
    "AI_Automation": {"score": 0.95, "trend": "increasing"},
    "VLM_Applications": {"score": 0.88, "trend": "new"},
    "Productivity_Tools": {"score": 0.82, "trend": "stable"}
  },
  "expertise": {
    "JavaScript": {"level": "expert", "years": "5+"},
    "Product_Management": {"level": "advanced", "years": "3-5"}
  },
  "professional_seniority": "Senior",
  "content_preferences": {
    "format": "deep_technical_articles",
    "reading_depth": "deep_reader"
  }
}
```

**變現價值**：$35-50/月

**隱私保護**：
- 中等風險（需用戶同意）
- 可撤銷授權
- 持續監控 K-Anonymity

</details>

<details>
<summary><strong>Tier 3 標籤（細粒度）</strong> - 絕不離開設備</summary>

**特徵**：
- **100% 本地**，絕不上傳
- 高度個人化、可識別個人
- 僅用於本地 System Prompt 生成

**範例標籤**：
```json
{
  "purchase_intent": {
    "notion": {"score": 0.95, "urgency": "high"},
    "figma": {"score": 0.78, "urgency": "medium"}
  },
  "current_projects": [
    "irisgo_ai_development",
    "mnemosyne_mvp"
  ],
  "work_patterns": {
    "peak_hours": ["9-12am", "2-5pm"],
    "energy_dips": ["Wed_afternoon", "Fri_afternoon"]
  },
  "communication_network": {
    "frequent_contacts": ["john@company.com", "sarah@company.com"],
    "team_collaboration_score": 0.75
  },
  "personal_goals": [
    "launch_mvp_Q1",
    "raise_seed_round"
  ]
}
```

**變現價值**：$0（不可變現，僅本地使用）

**隱私保護**：
- 零風險（不上傳）
- 加密本地儲存
- 用戶完全控制

</details>

---

##### 8.2 標籤資產變現機制

**運作流程**：

```
用戶數位行為
    ↓
本地分析 → 生成 Tier 1/2/3 標籤
    ↓
用戶審查 & 選擇性同意 (Opt-in)
    ↓
Tier 1/2 標籤匿名上傳（加密 + K-Anonymity）
    ↓
Data Marketplace 匿名匹配
    ↓
廣告主/研究機構付費
    ↓
收益分配：70% 用戶、30% 平台
```

**收益估算**：

| 標籤層級 | 月均價值 | Opt-in 率（預估） | 用戶月收益 |
|---------|---------|-----------------|-----------|
| Tier 1  | $15-25  | 80%             | $10-20    |
| Tier 2  | $35-50  | 30%             | $25-35    |
| **總計** | **$50-75** | **混合** | **$35-55** |

**Year 1-3 收益增長**：
- **Year 1**: Opt-in 率 10%，月均 $30/用戶
- **Year 2**: Opt-in 率 30%，月均 $50/用戶
- **Year 3**: Opt-in 率 40%，月均 $75/用戶

**關鍵差異化**：
- ✅ 用戶擁有標籤，不是平台擁有
- ✅ 透明化收益分配（70/30）
- ✅ 可撤銷授權，隨時退出
- ✅ 完整審計日誌，用戶知道誰買了什麼

---

##### 8.3 競爭護城河：時間累積的數據資產

**核心洞察**：時間是最強的護城河，巨頭有錢但買不到時間。

**為什麼時間累積的標籤資產無法被競爭**：

<details>
<summary><strong>1. 冷啟動問題反轉為競爭優勢</strong></summary>

**傳統產品的冷啟動問題**：
- 新用戶剛加入時，沒有數據 → 無法提供價值 → 用戶流失

**Mnemosyne 的冷啟動反轉**：
- 新用戶剛加入時，Tier 3 標籤為 0 → **標籤資產價值 = $0**
- 使用 3 個月後，Tier 2/3 標籤豐富 → **標籤資產價值 = $35/月**
- 使用 12 個月後，高質量 Tier 2 標籤 → **標籤資產價值 = $95/月**

**切換成本**：
```
切換到競爭對手 = 損失 12 個月累積的標籤資產價值
                = 損失 $95/月 × 12 = $1,140/年收益
```

**結論**：用戶使用越久，切換成本越高，護城河越深

</details>

<details>
<summary><strong>2. 網路效應：數據質量 > 用戶數量</strong></summary>

**不是傳統的網路效應（Metcalfe's Law）**：
- 不是「用戶越多，價值越高」
- 而是「數據累積越久，價值越高」

**單用戶數據價值增長曲線**：
```
Month 1:  標籤質量 20%，變現價值 $10
Month 3:  標籤質量 50%，變現價值 $35
Month 6:  標籤質量 75%，變現價值 $65
Month 12: 標籤質量 95%，變現價值 $95
```

**複利效應**：
- 每個月的行為數據都累加到標籤資產
- 興趣演變、專業深化、溝通風格優化
- **時間 = 不可逆的競爭優勢**

</details>

<details>
<summary><strong>3. 巨頭無法用金錢複製的護城河</strong></summary>

**場景：Google/Meta 想要複製 Mnemosyne**

| 挑戰 | Mnemosyne (Year 3) | 巨頭從零開始 | 巨頭劣勢 |
|------|-------------------|------------|---------|
| **用戶數據** | 100 萬用戶 × 12 個月數據 | 0 個月數據 | ❌ 需要 12 個月追上 |
| **標籤質量** | 高質量 Tier 2/3 標籤 | Tier 1 基礎標籤 | ❌ 無法速成 |
| **用戶信任** | 隱私優先品牌 | 隱私疑慮（歷史紀錄） | ❌ 難以建立信任 |
| **切換成本** | 用戶有 $1,140/年資產 | $0 | ❌ 用戶不願切換 |
| **B2B 客戶** | 12 個月行為數據 = 準確洞察 | 淺層數據 = 低價值 | ❌ 廣告主不買單 |

**結論**：
- ✅ 巨頭可以用錢挖工程師 → **但買不到 12 個月用戶數據**
- ✅ 巨頭可以用錢買廣告獲客 → **但買不到用戶信任**
- ✅ 巨頭可以抄功能 → **但無法抄走用戶的標籤資產**

**唯一選項：收購 Mnemosyne**

</details>

<details>
<summary><strong>4. 時間累積的三層防禦</strong></summary>

**第一層防禦：用戶層（Switching Cost）**
```
用戶切換成本 = 12 個月標籤資產價值 + 重新建立個人檔案時間成本
             = $1,140/年 + 12 個月等待
             = 極高障礙
```

**第二層防禦：數據層（Data Moat）**
```
Mnemosyne Year 3: 100 萬用戶 × 12 個月 = 1,200 萬個月的行為數據
競爭對手 Day 1:   0 用戶 × 0 個月 = 0

數據差距 = 1,200 萬個月（無法用金錢彌補）
```

**第三層防禦：信任層（Brand Moat）**
```
Mnemosyne: 3 年隱私優先 + 0 隱私事件 + 用戶擁有數據
巨頭:      歷史隱私醜聞 + 雲端處理疑慮

信任差距 = 無法用金錢彌補（需要時間 + 行動證明）
```

</details>

---

##### 8.4 估值潛力與收購可能性

**基於標籤資產的估值模型**：

<details>
<summary><strong>Year 3 估值計算</strong></summary>

**假設**（Year 3）：
- 活躍用戶：100 萬
- Opt-in 率：40%
- 月均收益：$75/用戶
- 收益分配：70% 用戶、30% 平台

**平台年收益**：
```
100 萬用戶 × 40% × $75 × 12 個月 × 30% = $108M/年
```

**SaaS 估值倍數**：
- 成長型 SaaS：10-15x ARR
- 數據平台：15-25x ARR（更高倍數）
- **保守估值**：$108M × 15 = **$1.62B**
- **樂觀估值**：$108M × 25 = **$2.7B**

**加上 Pro/Enterprise 訂閱收益**：
```
Pro Tier (15% 轉換，10 萬用戶): $18M/年
Enterprise (500 企業): $1.2M/年
總 ARR = $108M + $18M + $1.2M = $127.2M

估值範圍：$1.9B - $3.2B
```

</details>

<details>
<summary><strong>收購邏輯：巨頭的唯一選擇</strong></summary>

**為什麼收購是唯一選項**：

**選項 1：自己做（Build）**
- 時間成本：3 年（Year 1 獲客 + Year 2 數據累積 + Year 3 達到品質）
- 金錢成本：$150M+（工程、獲客、營運）
- 風險：用戶不信任（隱私疑慮）、數據質量不如 Mnemosyne
- **預期成功率**：< 30%

**選項 2：收購 Mnemosyne（Buy）**
- 時間成本：6-12 個月（談判 + 整合）
- 金錢成本：$2-3B（Year 3 估值）
- 風險：低（已驗證產品、用戶基礎、數據資產）
- **預期成功率**：> 90%

**經濟比較**：
```
Build 選項 NPV = $150M 成本 + 3 年時間成本 - 70% 失敗風險
               = 負值或極低

Buy 選項 NPV  = $2-3B 成本 / 即時獲得 100 萬用戶 + 數據資產
               = 正值且確定性高
```

**結論**：收購是理性選擇

</details>

<details>
<summary><strong>潛在收購方</strong></summary>

**Tier 1 收購方**（估值 $2.5-4B）：
- **Google**：整合到 Gemini，強化個人化
- **Microsoft**：整合到 Copilot，補強隱私短板
- **Apple**：符合隱私優先策略，整合到 Apple Intelligence

**Tier 2 收購方**（估值 $1.5-2.5B）：
- **OpenAI**：強化 ChatGPT 個人化能力
- **Anthropic**：補強 Claude 的用戶情境理解
- **Notion**：擴展到個人 AI 助理領域

**Tier 3 收購方**（估值 $800M-1.5B）：
- **Salesforce**：整合到 Einstein，B2B 數據洞察
- **Adobe**：整合到 Creative Cloud，創作者工作流
- **Atlassian**：整合到 Confluence/Jira，團隊協作

</details>

---

##### 8.5 實施策略

**Phase 1（Year 1）：建立數據護城河**
- [ ] 實施 Tier 1/2/3 標籤系統
- [ ] 標籤自動生成和累積
- [ ] 用戶標籤資產儀表板
- [ ] **目標**：10K 用戶 × 3-6 個月數據

**Phase 2（Year 2）：啟動變現**
- [ ] Data Marketplace Alpha（Tier 1 標籤）
- [ ] B2B 市場研究平台
- [ ] 用戶收益分配系統
- [ ] **目標**：100K 用戶 × 10% Opt-in

**Phase 3（Year 3）：規模化與防禦**
- [ ] Data Marketplace Beta（Tier 1 + Tier 2）
- [ ] K-Anonymity 動態調整
- [ ] 標籤資產交易市場
- [ ] **目標**：1M 用戶 × 40% Opt-in

**防禦策略**：
- ✅ 專利保護（分層標籤架構、K-Anonymity 動態調整）
- ✅ 品牌建立（隱私優先、用戶擁有數據）
- ✅ 社群經營（早期用戶 = 品牌大使）
- ✅ 時間累積（每個月都在加深護城河）

---

##### 8.6 關鍵成功指標

**用戶層面**：
- 標籤資產累積速度：> 10 個新標籤/月/用戶
- 標籤質量評分：> 85%（Year 1）
- 用戶留存率：> 80%（12 個月）

**變現層面**：
- Opt-in 率：Year 1 (10%) → Year 2 (30%) → Year 3 (40%)
- 平均月收益：Year 1 ($30) → Year 2 ($50) → Year 3 ($75)
- B2B 客戶滿意度：> 90%

**護城河層面**：
- 切換成本：Year 1 ($360) → Year 2 ($720) → Year 3 ($1,140)
- 數據資產價值：Year 3 達到 $2-3B
- 競爭對手進入難度：Year 3 達到「極高」

---

#### 9. Data Marketplace 整合

**功能**：讓用戶透過安全、匿名的方式變現數據標籤

**技術架構**（詳見 8.2）

**預估收益**：每月 $50-100（個人）、$108M/年（平台，Year 3）

#### 10. 多語言支援

**功能**：支援中英文混合分析，生成雙語 System Prompt

---

## 🏗️ 技術架構

### 系統架構圖

```
┌─────────────────────────────────────────────────────────┐
│                    數據收集層                            │
├─────────────────────────────────────────────────────────┤
│  DayFlow VLM  │  Gmail IMAP  │  Calendar API  │ DayFlow │
│  (40%)        │  (30%)       │  (20%)         │ (10%)   │
└────────┬────────────┬────────────┬─────────────┬─────────┘
         │            │            │             │
         ↓            ↓            ↓             ↓
┌─────────────────────────────────────────────────────────┐
│                    數據處理層 (本地)                     │
├─────────────────────────────────────────────────────────┤
│  Persona      │  Communication │  Time        │ Interest│
│  Analyzer     │  Analyzer      │  Analyzer    │ Analyzer│
└────────┬────────────┬────────────┬─────────────┬─────────┘
         │            │            │             │
         └────────────┴────────────┴─────────────┘
                        │
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    輸出生成層                            │
├─────────────────────────────────────────────────────────┤
│  Prompt Generator  │  Tag Extractor  │  CLI Interface  │
└────────┬───────────────────┬─────────────────┬──────────┘
         │                   │                 │
         ↓                   ↓                 ↓
┌─────────────────────────────────────────────────────────┐
│                    儲存層 (加密)                         │
├─────────────────────────────────────────────────────────┤
│  SQLite (本地)  │  macOS Keychain  │  檔案系統 (加密) │
└─────────────────────────────────────────────────────────┘
```

### 技術棧

**核心技術**（跨平台）：
- **Runtime**: Node.js (≥18.0.0)
- **本地 VLM**: Ollama + LLaVA 13B
  - **macOS**: Metal 加速
  - **Windows**: CUDA (NVIDIA) / DirectML (AMD/Intel) 加速
- **本地 LLM**: Ollama + Llama 3.2
- **儲存**: SQLite (加密)
  - **macOS**: macOS Keychain（憑證）
  - **Windows**: Windows Credential Manager（憑證）
- **OCR**:
  - **macOS**: Apple Vision Framework
  - **Windows**: Tesseract OCR（開源）
- **影片處理**: ffmpeg（跨平台）

**平台特定技術**：

<details>
<summary><strong>macOS 專屬</strong></summary>

- **螢幕錄製**: DayFlow（現有系統）
- **活動追蹤**: DayFlow Intelligence API
- **硬體加速**: Metal (GPU)
- **排程**: LaunchAgent
- **憑證管理**: macOS Keychain
- **系統整合**: Cocoa APIs

</details>

<details>
<summary><strong>Windows 專屬</strong></summary>

- **螢幕錄製**: Windows Graphics Capture API (C#)
- **活動追蹤**: Win32 API (user32.dll, kernel32.dll)
- **硬體加速**:
  - Intel Quick Sync (Intel CPU)
  - NVENC (NVIDIA GPU)
  - DirectML (AMD/Intel GPU for VLM)
- **排程**: Task Scheduler
- **憑證管理**: Windows Credential Manager
- **系統整合**:
  - Windows Service（背景服務）
  - System Tray App（用戶控制）
  - WPF/WinUI（GUI，可選）
- **部署**:
  - MSI installer（企業）
  - OEM 預裝（主要策略）

</details>

**數據源整合**（跨平台）：
- **DayFlow VLM**:
  - **macOS**: 現有整合
  - **Windows**: 自建 Windows 版（C# + Node.js）
- **Gmail**: node-imap + mailparser（跨平台）
- **Calendar**: Google Calendar API / MCP（跨平台）
- **Activity Tracker**:
  - **macOS**: DayFlow Intelligence
  - **Windows**: 自建服務

**隱私技術**（跨平台）：
- Differential Privacy
- K-Anonymity
- Local-first encryption
- PII detection and filtering

**CLI 工具**（跨平台）：
- Commander.js (命令列框架)
- Inquirer.js (互動式 prompt)
- Chalk (終端機上色)
- Ora (載入動畫)
- cli-table3 (表格顯示)
- **Windows 打包**: pkg（打包成 .exe）

---

## 🔐 隱私與安全

### 隱私設計原則

1. **本地優先 (Local-First)**
   - 所有敏感數據處理在用戶設備上進行
   - 不上傳原始數據到雲端
   - 用戶完全掌控數據

2. **最小化收集 (Minimal Collection)**
   - 只收集生成 System Prompt 必要的數據
   - 不收集 PII（個人識別資訊）
   - 定期清理過期數據

3. **透明化 (Transparency)**
   - 完整的審計日誌
   - 用戶可審查所有待分析數據
   - 明確告知數據用途

4. **用戶控制 (User Control)**
   - Opt-in 機制（預設關閉）
   - 黑名單功能（排除特定網站/收件人）
   - 隨時刪除數據

### 多層隱私保護

**第 1 層：錄製層級**
- DayFlow 黑名單：銀行、郵件、訊息 app
- 敏感網站自動跳過

**第 2 層：預掃描**
- OCR 檢測敏感關鍵字（姓名、電話、地址、信用卡）
- 檢測到敏感資訊自動跳過該畫面

**第 3 層：VLM Prompt**
- 指示 VLM 跳過個人識別資訊
- 只提取主題標籤和行為模式

**第 4 層：本地處理**
- 所有 VLM/LLM 分析在本地進行
- 使用 Ollama（完全離線）

**第 5 層：用戶審查**
- 提供 UI 讓用戶審查待分析數據
- 可手動排除特定數據

**第 6 層：加密儲存**
- SQLite 數據庫加密（SQLCipher，兩平台相同）
- 憑證儲存：
  - **macOS**: macOS Keychain
  - **Windows**: Windows Credential Manager
- 檔案系統加密：
  - **macOS**: FileVault
  - **Windows**: BitLocker（OEM 預啟用建議）

### 數據分層策略

**Tier 1（粗標籤）**：
- 可選擇性上傳服務器
- K-Anonymity ≥ 100,000
- 範例：{"region": "Asia", "industry": "Tech"}

**Tier 2（中標籤）**：
- 需用戶明確同意
- K-Anonymity ≥ 10,000
- 範例：{"expertise": "JavaScript", "interests": ["AI", "Productivity"]}

**Tier 3（細標籤）**：
- 絕不離開設備
- 僅用於本地 System Prompt
- 範例：{"current_project": "irisgo_ai", "purchase_intent": {"notion": 0.95}}

### 合規性

- **GDPR**: 完全合規（本地處理、用戶控制、可刪除）
- **CCPA**: 完全合規（透明化、用戶權利）
- **Apple Privacy Policy**: 遵循 macOS 隱私最佳實踐

---

## 📅 開發計畫

### MVP 實施計畫（6 週）

**Week 1-2: DayFlow VLM Collector**
- [ ] **macOS**:
  - [ ] 整合現有 DayFlow 錄製 API
  - [ ] 實施畫面抽樣機制（每 5 分鐘 1 幀）
  - [ ] 建立敏感網站黑名單
- [ ] **Windows**:
  - [ ] 實施 Windows Graphics Capture API (C#)
  - [ ] Intel Quick Sync / NVENC 硬體編碼整合
  - [ ] 實施相同的抽樣機制和黑名單
- [ ] **共通**:
  - [ ] 整合 Ollama + LLaVA 13B
  - [ ] 建立 VLM 分析 pipeline
  - [ ] 測試興趣提取準確度（兩平台）
- **產出**：Interest Analyzer v0.1（macOS + Windows）

**Week 3-4: Gmail Sent Mail Collector**
- [ ] **跨平台**（Node.js，macOS + Windows 共用）:
  - [ ] 實施 IMAP 連線（唯讀）
  - [ ] Gmail App Password / OAuth2 整合
  - [ ] 郵件解析和 PII 過濾
  - [ ] 整合 Ollama Llama 3.2
  - [ ] 風格分析演算法
  - [ ] 憑證儲存整合（Keychain / Credential Manager）
  - [ ] 測試溝通風格提取（兩平台）
- **產出**：Communication Analyzer v0.1（跨平台）

**Week 5: Calendar Collector + Integration**
- [ ] **跨平台**（Google Calendar API，macOS + Windows 共用）:
  - [ ] Google Calendar API 整合
  - [ ] OAuth2 Web flow
  - [ ] 會議模式統計分析
  - [ ] 深度工作時段識別
  - [ ] 整合所有 analyzers
  - [ ] Persona 聚合邏輯
  - [ ] 測試兩平台的整合流程
- **產出**：Time Analyzer v0.1 + Persona Generator v0.5（跨平台）

**Week 6: CLI Tool + Automation**
- [ ] **CLI 開發**（Node.js，跨平台）:
  - [ ] CLI 介面開發（Commander.js）
  - [ ] System Prompt 模板系統
  - [ ] 導出功能（ChatGPT/Claude/Gemini）
  - [ ] **Windows**: pkg 打包成 mnemo.exe
- [ ] **自動化排程**:
  - [ ] **macOS**: LaunchAgent 設定和安裝腳本
  - [ ] **Windows**: Task Scheduler XML + C# 安裝器
- [ ] **系統整合**:
  - [ ] **macOS**: 整合測試
  - [ ] **Windows**: Windows Service + System Tray 開發
  - [ ] **Windows**: MSI installer（可選）
- [ ] **測試與文檔**:
  - [ ] 兩平台完整測試
  - [ ] 性能優化（VLM 速度、記憶體使用）
  - [ ] 文檔撰寫（雙平台安裝指南）
- **產出**：Mnemosyne MVP v1.0（macOS + Windows）

### Phase 2: Alpha（Month 3-4）

**目標**：10,000 用戶 + 3 個新數據源

**新增數據源**：

#### 5. Slack/Teams Collector
- [ ] 實施 Slack API / Slack MCP 整合
- [ ] 只分析用戶發送的訊息（類似 Gmail Sent Mail）
- [ ] 提取即時溝通風格和協作模式
- [ ] 頻道黑名單機制（排除機密頻道）
- [ ] 本地 LLM 分析溝通模式
- **提取洞察**：
  - 溝通風格（async vs sync, emoji usage, response time）
  - 協作模式（頻道參與、DM 比例）
  - 工作關係網絡（frequent contacts, cross-functional）

#### 6. Notion/Obsidian Collector
- [ ] Notion API OAuth 整合
- [ ] Obsidian 本地 .md 檔案讀取
- [ ] 分析筆記結構和主題
- [ ] 提取學習模式和興趣演變
- [ ] Frontmatter、標籤、連結分析
- **提取洞察**：
  - 知識結構（top topics, organization style, note frequency）
  - 學習模式（note length, link density, review frequency）
  - 內容創作（drafts, published, writing style）

#### 7. Browser History Collector
- [ ] Chrome/Safari History SQLite 讀取
- [ ] 敏感網站黑名單過濾
- [ ] 搜尋查詢提取
- [ ] 閱讀時間分布分析
- [ ] 作為 DayFlow VLM 的 fallback 機制
- **提取洞察**：
  - 瀏覽模式（top domains, visit frequency, avg time）
  - 搜尋意圖（search queries）
  - 興趣時間線（this week vs last month）
  - 閱讀深度（skim vs deep reading）

**標籤資產與變現**：
- [ ] Tier 1 標籤提取系統
- [ ] 標籤上傳機制（opt-in）
- [ ] 基礎 K-Anonymity 實施
- [ ] B2B 市場研究 dashboard

**產品優化**：
- [ ] 用戶反饋收集系統
- [ ] 性能優化
- [ ] 多數據源權重調整
- [ ] System Prompt 質量提升

### Phase 3: Beta（Month 5-8）

**目標**：100,000 用戶

- [ ] 完整 Tier 1/2/3 系統
- [ ] Data Marketplace 整合
- [ ] 混合匹配機制
- [ ] 進階隱私功能
- [ ] 多語言支援
- [ ] Web UI（可選）

### Phase 4: Production（Month 9-12）

**目標**：1,000,000+ 用戶

- [ ] K-Anonymity 動態調整
- [ ] Differential Privacy 優化
- [ ] Zero-Knowledge Proofs（探索）
- [ ] 跨平台支援（Windows, Linux）
- [ ] 企業版功能
- [ ] API for Developers

---

## 📊 成功指標

### MVP 階段（Month 1-2）

| 指標 | 目標 | 測量方式 |
|------|------|----------|
| **System Prompt 質量** | >90% 用戶滿意度 | 用戶調查（1-5 分） |
| **數據收集成功率** | >95% | 自動監控日誌 |
| **處理時間** | <5 秒 | 性能測試 |
| **隱私事件** | 0 | 審計日誌 |
| **CLI 使用率** | 每週 ≥3 次 | 使用統計 |

### Alpha 階段（Month 3-4）

| 指標 | 目標 | 測量方式 |
|------|------|----------|
| **活躍用戶** | 10,000 | 用戶註冊數 |
| **週留存率** | >60% | Cohort 分析 |
| **System Prompt 更新頻率** | 每週 1 次 | 自動統計 |
| **數據變現 opt-in** | >10% | 用戶設定 |
| **NPS** | >40 | 用戶調查 |

### Beta 階段（Month 5-8）

| 指標 | 目標 | 測量方式 |
|------|------|----------|
| **活躍用戶** | 100,000 | 用戶註冊數 |
| **週留存率** | >70% | Cohort 分析 |
| **數據變現 opt-in** | >30% | 用戶設定 |
| **平均收益** | $50-100/月 | 收益統計 |
| **NPS** | >50 | 用戶調查 |

### Production 階段（Month 9-12）

| 指標 | 目標 | 測量方式 |
|------|------|----------|
| **活躍用戶** | 1,000,000+ | 用戶註冊數 |
| **週留存率** | >80% | Cohort 分析 |
| **數據變現 opt-in** | >40% | 用戶設定 |
| **平均收益** | $75-150/月 | 收益統計 |
| **隱私合規** | 100% | 合規審計 |

---

## 💰 商業模式

### 收益模式

**1. 個人使用（免費 Tier）**
- 生成 System Prompts 供自己使用
- 基礎數據源（4 個）
- 每週自動更新
- 本地處理，完全隱私
- **收益**：0（獲客和品牌建立）

**2. Data Marketplace（選擇加入）**
- 用戶選擇分享 Tier 1/2 標籤
- 隱私保護的匹配機制
- **收益分享**：70% 給用戶，30% 給平台
- **預估用戶收益**：$50-100/月
- **平台收益**：$20-40/用戶/月

**3. Pro Tier（$9.99/月）**（未來）
- 更多數據源（Slack、Teams、Notion）
- 即時更新（不只週更新）
- 進階分析和洞察
- 團隊協作功能
- **目標轉換率**：10-15%

**4. Enterprise Tier（$99-499/月）**（未來）
- 團隊版（10-100 人）
- 管理員控制台
- SSO 整合
- 企業級隱私保護
- **目標客戶**：500-5000 人企業

**5. B2B 市場研究**
- 聚合、匿名化的受眾洞察
- 不識別個別用戶
- **定價**：$5,000-50,000/報告
- **目標客戶**：廣告主、市場研究公司

### 成本結構

**技術成本**（每用戶/月）：
- 伺服器（Tier 1 標籤儲存）：$0.05
- CDN（下載和更新）：$0.02
- 數據庫（用戶資料）：$0.01
- **總計**：$0.08/用戶/月

**本地處理成本**（用戶自付）：
- 電費：約 $0.50/月
- 硬體：Mac/PC（用戶已有）

**開發和營運成本**（年）：
- 工程師（2 人）：$300,000
- PM/設計（1 人）：$120,000
- 營運/客服（1 人）：$80,000
- 基礎設施：$50,000
- **總計**：$550,000/年

### 收益預測

**Year 1**（10,000 用戶）：
- Data Marketplace（10% opt-in）：1,000 × $30 × 12 = $360,000
- **總收益**：$360,000
- **成本**：$550,000 + (10,000 × $0.08 × 12) = $559,600
- **淨利**：-$199,600（投資期）

**Year 2**（100,000 用戶）：
- Data Marketplace（30% opt-in）：30,000 × $30 × 12 = $10,800,000
- Pro Tier（10% 轉換）：10,000 × $9.99 × 12 = $1,198,800
- **總收益**：$11,998,800
- **成本**：$850,000 + (100,000 × $0.08 × 12) = $946,000
- **淨利**：$11,052,800

**Year 3**（1,000,000 用戶）：
- Data Marketplace（40% opt-in）：400,000 × $30 × 12 = $144,000,000
- Pro Tier（15% 轉換）：150,000 × $9.99 × 12 = $17,982,000
- Enterprise（500 企業）：500 × $200 × 12 = $1,200,000
- **總收益**：$163,182,000
- **成本**：$1,500,000 + (1M × $0.08 × 12) = $2,460,000
- **淨利**：$160,722,000

---

## 🏆 競爭分析

### 競爭對手

| 產品 | 類型 | 優勢 | 劣勢 |
|------|------|------|------|
| **ChatGPT Custom Instructions** | 手動設定 | 官方功能 | 需手動填寫、不自動更新 |
| **Mem.ai** | AI 記憶系統 | 自動化、雲端同步 | 隱私風險、依賴雲端、$8-15/月 |
| **Rewind.ai** | 本地錄製 + 搜尋 | 本地處理、強大搜尋 | 只有搜尋、無 AI 整合、$19/月 |
| **Claude Projects** | 專案情境 | 官方功能、免費 | 需手動設定、單一平台 |
| **Personal.ai** | AI 個人助理 | 學習用戶風格 | 雲端處理、隱私疑慮、$40/月 |

### Mnemosyne 的差異化

| 功能 | Mnemosyne | 競爭對手 |
|------|-----------|----------|
| **隱私** | 100% 本地處理 | 大多雲端處理 |
| **成本** | 免費 + opt-in 變現 | $8-40/月訂閱 |
| **自動化** | 完全自動、週更新 | 需手動設定 |
| **覆蓋範圍** | 通用（VLM + 所有平台） | 依賴 API（有限） |
| **數據擁有權** | 用戶擁有、可變現 | 平台擁有 |
| **跨平台** | ChatGPT/Claude/Gemini | 通常單一平台 |

---

## ⚠️ 風險與緩解

### 技術風險

| 風險 | 影響 | 可能性 | 緩解措施 |
|------|------|--------|----------|
| **VLM 準確度不足** | 高 | 中 | 多模型測試、人工審查機制、持續訓練 |
| **處理速度太慢** | 中 | 中 | 優化抽樣頻率、批次處理、硬體加速 |
| **IMAP 連線失敗** | 中 | 低 | 重試機制、錯誤通知、降級處理 |
| **隱私漏洞** | 高 | 低 | 多層防護、安全審計、Bug Bounty |

### 產品風險

| 風險 | 影響 | 可能性 | 緩解措施 |
|------|------|--------|----------|
| **用戶不信任隱私** | 高 | 中 | 透明化、開源核心、第三方審計 |
| **System Prompt 質量低** | 高 | 中 | 持續優化、用戶反饋、A/B 測試 |
| **用戶不願授權 Gmail** | 中 | 高 | Opt-in、清楚說明、提供替代方案 |
| **數據不足** | 中 | 低 | 多數據源、降級模式、引導用戶 |

### 市場風險

| 風險 | 影響 | 可能性 | 緩解措施 |
|------|------|--------|----------|
| **AI 平台原生支援** | 高 | 中 | 快速迭代、差異化功能、生態系統 |
| **競爭對手抄襲** | 中 | 高 | 專利保護、品牌建立、社群經營 |
| **市場需求不足** | 高 | 低 | MVP 驗證、早期用戶訪談、迭代 |
| **法規變更** | 中 | 低 | 合規監控、法律顧問、彈性架構 |

---

## 📚 附錄

### A. 專業術語表

- **System Prompt**: AI 助理的系統指令，定義其行為和回應風格
- **VLM (Vision Language Model)**: 視覺語言模型，可同時處理圖像和文字
- **LLM (Large Language Model)**: 大型語言模型
- **ICP (Ideal Customer Profile)**: 理想客戶畫像
- **PII (Personally Identifiable Information)**: 個人識別資訊
- **K-Anonymity**: 隱私保護技術，確保每個用戶至少與 K-1 個其他用戶無法區分
- **Differential Privacy**: 差分隱私，通過添加噪音保護個人隱私
- **IMAP (Internet Message Access Protocol)**: 郵件存取協議

### B. 參考文檔

- [00-Overview.md](/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/docs/00-Overview.md) - 完整產品設計
- [01-MVP-Plan.md](/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/docs/01-MVP-Plan.md) - 6 週實施計畫
- [02-Data-Sources.md](/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/docs/02-Data-Sources.md) - 數據源分析
- [03-Privacy-Architecture.md](/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/docs/03-Privacy-Architecture.md) - 隱私架構
- [04-VLM-Solution.md](/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/docs/04-VLM-Solution.md) - VLM 實施方案

### C. 版本歷史

| 版本 | 日期 | 變更內容 | 作者 |
|------|------|----------|------|
| 1.0 | 2025-11-16 | 初版 PRD，定義 MVP 範圍和 ICP | IrisGo Product Team |
| 1.1 | 2025-11-16 | 新增 Windows/macOS 雙平台實施細節 | IrisGo Product Team |
| 1.2 | 2025-11-16 | 新增「產出與價值交付」章節，完整定義所有產出 | IrisGo Product Team |
| 1.3 | 2025-11-16 | 新增「個人標籤資產系統與競爭護城河」完整分析 | IrisGo Product Team |

**v1.3 更新摘要**：
- ✅ **大幅擴展第 8 節**：個人標籤資產系統與競爭護城河
- ✅ **8.1 分層標籤架構**：詳細定義 Tier 1/2/3 標籤特徵、範例、變現價值
- ✅ **8.2 標籤資產變現機制**：完整運作流程、收益估算、Year 1-3 增長預測
- ✅ **8.3 競爭護城河分析**：
  - 冷啟動問題反轉為競爭優勢
  - 網路效應（數據質量 > 用戶數量）
  - 巨頭無法用金錢複製的護城河（對比表）
  - 時間累積的三層防禦（用戶層、數據層、信任層）
- ✅ **8.4 估值潛力與收購可能性**：
  - Year 3 估值計算（$1.9B - $3.2B）
  - Build vs Buy 經濟分析
  - 潛在收購方分層（Tier 1/2/3）
- ✅ **8.5 實施策略**：Phase 1/2/3 時間表與防禦策略
- ✅ **8.6 關鍵成功指標**：用戶層面、變現層面、護城河層面
- ✅ 更新版本號至 1.3

**v1.2 更新摘要**：
- ✅ 新增「產出與價值交付」章節（section 3.2）
- ✅ 定義 9 大產出類型：
  1. 個人化 AI System Prompts（核心）
  2. 個人數位畫像儀表板（工作模式、興趣演變、溝通風格）
  3. 生產力優化建議（會議優化、精力管理）
  4. AI 使用效果追蹤（Before/After、ROI）
  5. 個人化內容推薦（學習資源、創作靈感）
  6. 週報/月報（自動化洞察）
  7. Personal API（開發者功能）
  8. 標籤資產組合（數據變現）
  9. 團隊協作洞察（Enterprise 版）
- ✅ 包含具體 CLI 指令範例和輸出格式
- ✅ 產出摘要表（MVP/Alpha/Beta/Enterprise 階段劃分）

**v1.1 更新摘要**：
- ✅ DayFlow VLM Collector：新增 Windows Graphics Capture API 實施（C#）
- ✅ Activity Tracker：新增 Windows 自建服務實施（Win32 API）
- ✅ Gmail & Calendar Collectors：標註為跨平台（Node.js）
- ✅ CLI 工具：新增 Windows pkg 打包策略
- ✅ 自動化排程：新增 Windows Task Scheduler 實施
- ✅ 技術棧：完整列出 macOS/Windows 平台差異
- ✅ 隱私架構：更新憑證儲存（Keychain vs Credential Manager）
- ✅ MVP 計畫：所有 6 週任務標註平台需求

**部署策略確認**：
- 🎯 **Windows 優先**：透過 OEM 合作夥伴（HP, Acer, Lenovo）預裝
- 🎯 **macOS 支援**：提供下載和手動安裝
- 🎯 **功能對等**：兩平台完全相同的功能和用戶體驗

---

## ✅ 批准與簽核

### 決策點

- [ ] **隱私架構批准**：確認多層隱私保護機制符合要求
- [ ] **數據源確認**：批准 4 大數據源（DayFlow VLM, Gmail, Calendar, DayFlow Stats）
- [ ] **MVP 範圍批准**：確認 6 週實施計畫可行
- [ ] **成功指標設定**：同意 MVP 階段成功指標
- [ ] **預算批准**：批准 Year 1 預算（$550K）

### 審查者

| 角色 | 姓名 | 簽核 | 日期 |
|------|------|------|------|
| Product Lead | | [ ] | |
| Tech Lead | | [ ] | |
| Privacy Officer | | [ ] | |
| CEO | | [ ] | |

---

**文件狀態**：Draft → Ready for Review
**下一步**：團隊審查會議，確認 MVP 範圍和時程

---

*Mnemosyne - 記住真實的你*
