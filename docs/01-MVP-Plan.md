# 🚀 Mnemosyne - MVP 實踐計畫

> **專案名稱**: Mnemosyne (Context-Aware AI Engine)
> **基於**: Context-Aware-AI-Engine-Design.md v0.3
> **最後更新**: 2025-11-16
> **執行者**: Iris (Melchior) - MAGI System
> **目標**: 6 週完成可用 MVP
> **ICP**: 知識工作者、內容創作者、商務專業人士（白領）

---

## 🔄 更新說明 (2025-11-16)

**數據源策略調整**：
- ❌ 移除：Terminal History、GitHub Activity（不符合 ICP）
- ✅ 保留並加強：
  1. **DayFlow + VLM (40%)** - 興趣與內容偏好分析
  2. **Gmail Sent Mail (30%)** - 溝通風格與寫作習慣
  3. **Calendar (20%)** - 時間管理與會議模式
  4. **DayFlow Intelligence (10%)** - 基礎行為數據

**目標用戶**：非技術背景的知識工作者，無需程式碼相關數據源。

詳見：[PRD.md](Mnemosyne%20PRD.md) 和 [README.md](../README.md)

---

## 📊 現有能力盤點

### ✅ 已完成的基礎建設

1. **數據收集能力**
   - ✅ DayFlow Intelligence (`dayflow-intelligence.js`) - 每兩天 01:00 自動分析
   - ✅ PKM Intelligence (`pkm-intelligence.js`) - 每天 02:00 自動分析
   - ✅ Gmail MCP - 完整郵件訪問能力
   - ✅ Google Calendar MCP - 日曆數據訪問
   - ✅ Social Media Tracker (`social-media-tracker.js`) - Twitter/X 數據收集
   - ✅ Twitter Curator (`twitter-curator.js`) - 社交互動分析

2. **AI 處理能力**
   - ✅ Ollama 本地運行 (gpt-oss:20b, qwen2.5vl:3b)
   - ✅ Gemini AI API (via MCP & Direct API)
   - ✅ 多源數據聚合經驗（投資分析系統）

3. **自動化基礎設施**
   - ✅ macOS LaunchAgents 管理系統
   - ✅ 23 個定時任務正在運行
   - ✅ Dropbox 同步（跨設備數據共享）
   - ✅ 通知系統 (`~/Iris/scripts/notifier.js`)

4. **已有洞察系統**
   - ✅ Deep Persona Profile (基於 DayFlow)
   - ✅ 工作模式分析
   - ✅ 溝通網絡分析
   - ✅ 興趣話題追蹤

### 🆕 需要開發的組件

1. **Context Aggregator** - 整合所有數據源
2. **Prompt Generator** - 生成 System Prompt
3. **Tag Asset System** - 標籤資產管理
4. **Consent Manager** - 同意管理系統
5. **API Layer** - 對外 API（Stage 2+）

---

## 🎯 MVP 目標與範圍

### 核心目標

**6 週內完成**：
1. ✅ 自動生成高質量 System Prompt（可直接用於 ChatGPT/Claude/Gemini）
2. ✅ 基於 4 個數據源（DayFlow, Gmail, Calendar, Twitter）
3. ✅ 每週自動更新
4. ✅ 標籤資產系統 MVP（可視化用戶資產）
5. ✅ CLI 工具（一鍵生成、查看、導出）

### 非目標（Stage 2+）

- ❌ B2B API（先專注個人工具）
- ❌ Web Dashboard
- ❌ Chrome Extension
- ❌ Data Marketplace

---

## 📅 6 週實踐計畫

### Week 1: 架構設計 + DayFlow 深化

**目標**: 建立 Context Engine 基礎架構，深化 DayFlow 分析

#### Day 1-2: 系統設計
- [ ] 設計 Context Engine 整體架構
  ```
  ~/Iris/scripts/context-engine/
  ├── collectors/           # 數據收集器
  │   ├── dayflow-collector.js
  │   ├── gmail-collector.js
  │   ├── calendar-collector.js
  │   └── twitter-collector.js
  ├── analyzers/           # 數據分析器
  │   ├── persona-analyzer.js
  │   ├── communication-analyzer.js
  │   ├── time-analyzer.js
  │   └── interest-analyzer.js
  ├── generators/          # Prompt 生成器
  │   ├── prompt-generator.js
  │   └── templates/
  │       ├── core-identity.md
  │       ├── working-style.md
  │       ├── communication.md
  │       └── expertise.md
  ├── assets/              # 標籤資產系統
  │   ├── tag-extractor.js
  │   ├── asset-manager.js
  │   └── value-calculator.js
  └── cli/                 # CLI 工具
      └── context-cli.js
  ```
- [ ] 設計數據存儲結構
  ```
  ~/Dropbox/PKM-Vault/.context-engine/
  ├── raw-data/           # 原始數據（隱私敏感）
  ├── insights/           # 分析洞察
  ├── prompts/            # 生成的 System Prompts
  ├── assets/             # 標籤資產
  └── history/            # 版本歷史
  ```

#### Day 3-5: DayFlow Collector
- [ ] 重構 `dayflow-intelligence.js` 為模組化 collector
- [ ] 提取核心洞察：
  - 工作模式（獨立 vs 協作時段）
  - 生產力模式（最佳工作時間）
  - 工具使用習慣
  - 項目焦點
- [ ] 輸出標準化 JSON 格式
  ```json
  {
    "source": "dayflow",
    "updated_at": "2025-11-08T10:00:00+08:00",
    "insights": {
      "working_patterns": {
        "peak_hours": ["09:00-12:00", "14:00-17:00"],
        "deep_work_preference": 0.75,
        "collaboration_ratio": 0.30
      },
      "tool_stack": [
        {"tool": "vscode", "usage_score": 0.95},
        {"tool": "terminal", "usage_score": 0.88}
      ],
      "current_projects": [
        {"name": "IrisGo", "focus_score": 0.92},
        {"name": "Context Engine", "focus_score": 0.85}
      ]
    }
  }
  ```

#### Day 6-7: Persona Analyzer v1
- [ ] 開發 `persona-analyzer.js`
- [ ] 從 DayFlow 洞察生成基礎 Persona
- [ ] 生成第一版 System Prompt
  - Core Identity (角色、專業、工作風格)
  - Working Style (工具、時間管理、協作模式)
- [ ] 測試：用生成的 Prompt 與 ChatGPT/Claude 對話

**Week 1 交付物**:
- ✅ Context Engine 基礎架構
- ✅ DayFlow Collector 完成
- ✅ Persona Analyzer v0.1
- ✅ System Prompt v0.1 (基於 DayFlow)

---

### Week 2: Gmail Integration + Communication Style

**目標**: 整合 Gmail 數據，分析溝通風格

#### Day 1-3: Gmail Collector
- [ ] 開發 `gmail-collector.js`
  - 使用現有 Gmail MCP
  - 分析最近 30 天郵件（不儲存郵件內容，只提取洞察）
- [ ] 提取洞察：
  - **溝通風格**:
    - 郵件長度分布（簡潔 vs 詳細）
    - 回應速度（快速 vs 深思熟慮）
    - 語氣分析（正式 vs 非正式）
  - **關係網絡**:
    - 核心聯絡人（前 20 名）
    - 互動頻率
    - 關係類型（客戶、同事、合作夥伴）
  - **溝通模式**:
    - 主動發起 vs 被動回應比例
    - 郵件時段分布
    - CC 使用習慣

#### Day 4-5: Communication Analyzer
- [ ] 開發 `communication-analyzer.js`
- [ ] 整合 Gmail 洞察
- [ ] 生成溝通風格描述
  ```json
  {
    "source": "gmail",
    "insights": {
      "communication_style": {
        "tone": "concise_data_driven",
        "avg_email_length": 250,
        "response_speed": "within_2_hours",
        "formality": "semi_formal"
      },
      "network": {
        "core_contacts": 15,
        "interaction_frequency": "high",
        "relationship_types": ["client", "partner", "team"]
      }
    }
  }
  ```

#### Day 6-7: Prompt Generator v0.2
- [ ] 整合 DayFlow + Gmail 洞察
- [ ] 生成 System Prompt v0.2
  - 加入 Communication Style 模組
  - 加入關係網絡建議
- [ ] 測試：比較 v0.1 vs v0.2 效果

**Week 2 交付物**:
- ✅ Gmail Collector 完成
- ✅ Communication Analyzer 完成
- ✅ System Prompt v0.2 (含溝通風格)

---

### Week 3: Calendar Integration + Time Management

**目標**: 整合 Calendar 數據，優化時間管理建議

#### Day 1-3: Calendar Collector
- [ ] 開發 `calendar-collector.js`
  - 使用現有 Google Calendar MCP
  - 分析最近 30 天日曆數據
- [ ] 提取洞察：
  - **會議模式**:
    - 會議頻率
    - 平均會議時長
    - 會議類型（1-on-1, 團隊會議, 客戶會議）
  - **時間區塊**:
    - 專注工作時段
    - 協作時段
    - 空閒時段
  - **時間管理風格**:
    - 日曆使用習慣（嚴格 vs 彈性）
    - 緩衝時間習慣
    - 優先級模式

#### Day 4-5: Time Analyzer
- [ ] 開發 `time-analyzer.js`
- [ ] 交叉分析 DayFlow + Calendar
  - 實際工作模式 vs 計劃時間
  - 會議效率分析
  - 時間浪費熱點識別

#### Day 6-7: Prompt Generator v0.3
- [ ] 整合 Calendar 洞察
- [ ] 生成 System Prompt v0.3
  - 加入時間管理建議
  - 加入會議風格描述
- [ ] 測試：AI 能否給出更符合時間習慣的建議

**Week 3 交付物**:
- ✅ Calendar Collector 完成
- ✅ Time Analyzer 完成
- ✅ System Prompt v0.3 (含時間管理)

---

### Week 4: Social Media Integration + Interest Mapping

**目標**: 整合 Twitter/Social 數據，建立興趣地圖

#### Day 1-3: Twitter Collector (Enhanced)
- [ ] 重構現有 `twitter-curator.js`
- [ ] 提取洞察：
  - **興趣話題**:
    - 高頻關鍵字（AI, automation, productivity...）
    - 話題趨勢變化
    - 深度 vs 廣度（專注 vs 多元）
  - **內容偏好**:
    - 喜歡的內容類型（技術文章、產品評論、思想領袖）
    - 互動模式（轉發、點讚、評論）
  - **社交風格**:
    - 發文頻率
    - 表達方式（長文 vs 短句）
    - 態度傾向（樂觀、批判、中立）

#### Day 4-5: Interest Analyzer
- [ ] 開發 `interest-analyzer.js`
- [ ] 建立興趣知識圖譜
  ```json
  {
    "source": "twitter",
    "insights": {
      "interests": {
        "AI_automation": {
          "score": 0.95,
          "confidence": 0.90,
          "trend": "increasing",
          "subtopics": ["LLM", "agents", "workflow"]
        },
        "productivity": {
          "score": 0.88,
          "trend": "stable"
        }
      },
      "content_preference": "technical_deep_dive",
      "social_style": "thought_leader"
    }
  }
  ```

#### Day 6-7: Prompt Generator v1.0 (Complete)
- [ ] 整合所有 4 個數據源
- [ ] 生成完整 System Prompt v1.0
  - Core Identity
  - Working Style
  - Communication Style
  - Time Management
  - Interests & Expertise
- [ ] 全面測試：ChatGPT, Claude, Gemini

**Week 4 交付物**:
- ✅ Twitter Collector Enhanced
- ✅ Interest Analyzer 完成
- ✅ **System Prompt v1.0 (4 源完整版)** 🎉

---

### Week 5: Tag Asset System + CLI Tool

**目標**: 建立標籤資產系統，開發 CLI 工具

#### Day 1-3: Tag Asset System
- [ ] 開發 `tag-extractor.js`
  - 從洞察中提取可變現標籤
  - 標籤分類：
    - Interests (興趣話題)
    - Expertise (專業領域)
    - Buying Intent (購買意圖)
    - Professional Profile (職業角色)
- [ ] 開發 `asset-manager.js`
  - 標籤資產存儲
  - 資產價值評估
  - 資產變化追蹤
- [ ] 輸出標籤資產報告
  ```json
  {
    "user_id": "anonymous_uuid_xxx",
    "generated_at": "2025-11-08T10:00:00+08:00",
    "tag_portfolio": {
      "interests": {
        "AI_automation": {
          "score": 0.95,
          "market_value_estimate": "$15-25/month"
        }
      },
      "expertise": {
        "programming": {
          "level": "expert",
          "market_value_estimate": "$20-40/month"
        }
      },
      "total_estimated_value": "$50-100/month"
    }
  }
  ```

#### Day 4-7: CLI Tool
- [ ] 開發 `context-cli.js`
  - 命令：
    ```bash
    # 生成 Prompt
    context generate

    # 查看當前 Persona
    context show

    # 查看標籤資產
    context assets

    # 導出 Prompt
    context export --format json|markdown|txt

    # 查看歷史版本
    context history

    # 比較兩個版本
    context diff v0.1 v1.0
    ```
- [ ] 美化輸出（使用 chalk, cli-table3）
- [ ] 測試所有命令

**Week 5 交付物**:
- ✅ Tag Asset System 完成
- ✅ CLI Tool v1.0
- ✅ 資產價值評估報告

---

### Week 6: Automation + Polish + Documentation

**目標**: 自動化、優化、文檔化

#### Day 1-2: 自動化更新
- [ ] 創建 LaunchAgent: `com.lman.context-engine-update.plist`
  - 排程：每週日 01:00
  - 執行：`context generate --auto`
- [ ] 實作增量更新（只更新變化的洞察）
- [ ] 通知系統整合
  ```bash
  # 更新完成後通知
  notify.success(
    "Context Engine 更新完成",
    "Prompt v1.2 已生成，資產價值 +5%"
  )
  ```

#### Day 3-4: 質量優化
- [ ] Prompt 模板優化
  - 基於實際使用反饋調整
  - A/B 測試不同模板
- [ ] 性能優化
  - 減少重複分析
  - 快取機制
- [ ] 錯誤處理完善
  - 數據源不可用時的降級方案
  - 日誌記錄

#### Day 5-7: 文檔與發布
- [ ] 撰寫用戶手冊
  - 安裝指南
  - 使用教程
  - 常見問題
- [ ] 撰寫開發者文檔
  - 架構說明
  - API 文檔
  - 擴展指南
- [ ] 準備 Demo
  - 錄製演示視頻
  - 準備案例研究
- [ ] Beta 測試準備
  - 邀請 5-10 個測試用戶
  - 準備反饋表單

**Week 6 交付物**:
- ✅ 自動化更新系統
- ✅ CLI Tool v1.0 (polished)
- ✅ 完整文檔
- ✅ **MVP 完成！** 🎉

---

## 📦 MVP 最終交付清單

### 核心功能

- [x] **Context Engine Core**
  - 4 個數據源 Collectors (DayFlow, Gmail, Calendar, Twitter)
  - 4 個 Analyzers (Persona, Communication, Time, Interest)
  - Prompt Generator with templates
  - Tag Asset System

- [x] **System Prompt v1.0**
  - 基於真實行為數據
  - 4 層結構（Identity, Style, Time, Interests）
  - 可直接用於 ChatGPT/Claude/Gemini
  - 每週自動更新

- [x] **Tag Asset System**
  - 標籤提取與分類
  - 資產價值評估
  - 變化追蹤

- [x] **CLI Tool**
  - 一鍵生成 Prompt
  - 查看資產組合
  - 版本管理與比較
  - 多格式導出

- [x] **自動化系統**
  - LaunchAgent 每週自動更新
  - 通知系統整合
  - 增量更新機制

### 文檔

- [ ] User Guide (用戶手冊)
- [ ] Developer Documentation (開發者文檔)
- [ ] API Reference (API 參考)
- [ ] Case Studies (案例研究)

### 測試

- [ ] 功能測試（所有命令正常運作）
- [ ] 集成測試（4 個數據源正常收集）
- [ ] 用戶測試（5-10 個 beta 用戶）

---

## 🎯 成功標準

### 定量指標

1. ✅ System Prompt 可用性 >= 90%
   - 測試方法：與 ChatGPT/Claude/Gemini 對話 20 次，評估回應質量
2. ✅ 數據收集成功率 >= 95%
   - 4 個數據源都能穩定收集
3. ✅ 更新週期 <= 7 天
   - 自動化系統穩定運行
4. ✅ CLI 響應時間 < 5 秒
   - `context generate` 命令執行時間

### 定性指標

1. ✅ AI 回應明顯更個人化
   - 理解我的工作風格
   - 使用我偏好的溝通方式
   - 給出符合我時間習慣的建議
2. ✅ 標籤資產有價值
   - 能準確反映我的興趣和專業
   - 不洩露個人隱私
   - 市場價值評估合理
3. ✅ 使用體驗流暢
   - 一鍵生成，無需複雜配置
   - CLI 操作直觀
   - 錯誤提示清晰

---

## ⚠️ 風險與應對

### 技術風險

1. **數據源 API 限制**
   - 風險：Gmail/Calendar MCP 可能有速率限制
   - 應對：實作快取、增量更新、錯誤降級

2. **隱私數據處理**
   - 風險：處理敏感郵件內容
   - 應對：只提取洞察，不儲存原始郵件內容

3. **Ollama 模型性能**
   - 風險：本地模型可能不夠準確
   - 應對：可選擇使用 Gemini API（已整合）

### 產品風險

1. **Prompt 質量不穩定**
   - 風險：生成的 Prompt 質量參差不齊
   - 應對：建立評估機制、持續優化模板

2. **用戶數據不足**
   - 風險：新用戶數據不夠生成高質量 Prompt
   - 應對：設計冷啟動策略、漸進式 Persona 構建

---

## 📈 後續規劃 (Stage 2+)

### Month 3-4: Power User Tool

- Chrome Extension (一鍵注入 Prompt)
- 支援更多 AI 平台
- Consent Management UI

### Month 5-8: B2B API

- System Prompt as a Service
- 與 Gamma, Notion 等整合
- API 文檔與 SDK

### Month 9-12: Platform

- Web Dashboard
- Data Marketplace MVP
- Self-service API platform

---

## 📝 結語

這個 MVP 計畫的核心理念：

1. **利用現有能力** - 最大化利用 MAGI 系統已有的數據收集和自動化能力
2. **漸進式迭代** - 每週一個里程碑，持續交付價值
3. **實用優先** - 先做出能用的個人工具，再考慮商業化
4. **隱私優先** - 本地處理，用戶完全掌控

6 週後，我們將擁有一個真正懂你的 AI 助手，以及一套可變現的數位資產！🚀

---

*生成時間: 2025-11-08*
*執行者: Iris (Melchior) - MAGI System*
*版本: v1.0*
