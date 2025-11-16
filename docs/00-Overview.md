# 🧠 Context-Aware AI Engine - 設計文檔

> **核心定位**: 用戶數據資產管理系統 - 讓用戶掌握自己的數位洞察資產
> **核心功能**: 多源數據分析 → 標籤資產 → System Prompt + 雙重變現
> **狀態**: 設計階段
> **創建日期**: 2025-11-02
> **當前版本**: v0.3

---

## 📝 版本歷史

### v0.3 - 2025-11-02 (Current)
- **新變現路徑**: System Prompt as a Service (B2B API)
- 加入 B2B API 變現模式設計
- 4 個 vertical app use cases (Gamma AI, Notion, Linear, Superhuman)
- 完整 API 設計 (認證、響應格式、webhook)
- 雙重定價模型 (per-user vs revenue share)
- GTM 策略與技術路線圖
- 與廣告模式對比分析
- **戰略轉變**: 短期優先 API 模式（更快變現）

### v0.2 - 2025-11-02
- **革命性升級**: 從 System Prompt 工具升級為用戶資產管理系統
- 加入標籤資產系統 (Tag Asset System)
- 加入隱私優先變現模式 (Privacy-First Monetization)
- 加入同意管理系統 (Consent Management)
- 重新定位商業模式：用戶獲益 > 平台獲益

### v0.1 - 2025-11-02
- 初版設計：System Prompt 生成器
- 多源數據整合架構
- 分層 Prompt 設計

---

## 📋 目錄

- [核心概念](#核心概念)
- [用戶資產系統](#用戶資產系統)
- [標籤資產設計](#標籤資產設計)
- [隱私優先變現](#隱私優先變現)
- [B2B API 變現：System Prompt as a Service](#b2b-api-變現system-prompt-as-a-service)
- [數據源與洞察層級](#數據源與洞察層級)
- [系統架構](#系統架構)
- [System Prompt 設計](#system-prompt-設計)
- [同意管理系統](#同意管理系統)
- [實作計劃](#實作計劃)
- [產品化路徑](#產品化路徑)

---

## 🎯 核心概念

### 問題陳述 1: AI 缺乏用戶理解

當前 AI Agent (ChatGPT, Claude, Gemini) 缺乏對用戶的深度理解：
- 不知道用戶的工作風格和偏好
- 無法適應用戶的溝通方式
- 無法基於用戶當前狀態調整回應

### 問題陳述 2: 用戶數據資產被平台壟斷

**傳統模式 (Google/Facebook/平台時代)**:
```
用戶行為 → 平台收集 → 平台分析 → 平台獲利 → 平台壟斷
         ↓
      用戶 = 產品
      用戶 = 被剝削者
```

**問題**：
- ❌ 用戶創造價值，平台獲得收益
- ❌ 隱私被侵犯，cookies 被追蹤
- ❌ 數據被鎖在平台內，無法遷移
- ❌ Google 通過掌握你的瀏覽記錄建立帝國，用戶一無所得

### 革命性解決方案

**新模式 (AI 時代 - 用戶主權時代)**:
```
用戶行為 → 本地分析 → 標籤資產 → 用戶控制 → 用戶獲益
         ↓                    ↓             ↓
   用戶 = 資產擁有者      System Prompt   變現收益
                         個人化 AI        或更好服務
```

**核心理念**：
✅ **用戶洞察 = 用戶資產** - 不是平台的資產
✅ **隱私優先** - 本地處理，標籤化後不洩露個資
✅ **Consent-Based** - 用戶明確同意才分享
✅ **用戶獲益** - 變現收益或換取更好服務

### 雙重價值主張

#### 價值 1: 個人化 AI (System Prompt)

**多層數據融合 → 深度洞察 → System Prompt → 個人化 AI**

```
Raw Data          Insights              AI Enhancement
────────          ─────────             ──────────────
DayFlow    ──→    工作模式      ──→     更符合工作習慣的建議
Gmail      ──→    溝通風格      ──→     更契合表達方式的回應
Calendar   ──→    時間管理      ──→     更合理的優先級建議
Twitter    ──→    興趣領域      ──→     更相關的話題連結
```

**用戶獲得**：
- 更懂你的 AI 助手
- 更準確的建議和回應
- 節省溝通成本

#### 價值 2: 數據資產變現 (革命性)

**洞察標籤化 → 匿名資產 → 市場交易 → 用戶收益**

```
用戶行為分析
    ↓
標籤資產 (Tags)
├── "AI_automation" (興趣: 0.95)
├── "technical_decision_maker" (角色)
├── "evaluating_project_tools" (購買意圖)
└── "prefers_technical_content" (內容偏好)
    ↓
匿名 Profile (無個資)
    ↓
廣告主/服務商願意付費訪問
    ↓
用戶獲得收益 ($10-50/月)
```

**用戶獲得**：
- 💰 被動收入 ($10-50/月)
- 🎁 服務折扣或升級
- 🔒 完全控制權
- 📊 透明度 (知道誰訪問了什麼)

### 核心原則

1. **基於真實行為** - 不是問卷，是實際數據
2. **持續進化** - 隨時間自動更新
3. **隱私優先** - 本地處理，用戶完全控制
4. **標籤 ≠ 個資** - 有價值但不洩露隱私
5. **Consent-Based** - 明確同意才分享
6. **用戶獲益優先** - 用戶賺錢 > 平台賺錢
7. **透明可審計** - 用戶隨時知道發生什麼
8. **即插即用** - 標準格式，跨平台通用

---

## 💎 用戶資產系統

### 核心概念：資產積累

**用戶行為 → 洞察提取 → 標籤資產 → 資產組合**

```javascript
// 用戶的數位資產賬戶
const userAssetProfile = {
  user_id: "anonymous_uuid_550e8400",  // 匿名 ID，無個資

  // 標籤資產組合
  tag_portfolio: {
    interests: {
      "AI_automation": { score: 0.95, confidence: 0.90, trend: "increasing" },
      "system_design": { score: 0.88, confidence: 0.85, trend: "stable" },
      "productivity_tools": { score: 0.82, confidence: 0.88, trend: "increasing" }
    },

    expertise: {
      "programming": { level: "expert", languages: ["javascript", "python"] },
      "product_management": { level: "advanced", focus: "technical_products" },
      "system_architecture": { level: "expert", specialization: "automation" }
    },

    buying_intent: {
      "SaaS_tools": {
        level: "high",
        category: "productivity",
        budget_range: "$20-100/mo",
        decision_timeline: "1-3_months"
      },
      "AI_APIs": {
        level: "very_high",
        category: "infrastructure",
        budget_range: "$100-500/mo",
        decision_timeline: "immediate"
      }
    },

    professional_profile: {
      "role": "technical_founder",
      "team_size": "startup_<10",
      "decision_maker": true,
      "budget_authority": "enterprise_level",
      "tech_stack": ["node", "ai_apis", "macos_automation"]
    },

    content_preferences: {
      "format": "long_form_technical",
      "tone": "practical_no_fluff",
      "engagement_style": "deep_reader_curator",
      "languages": ["english", "traditional_chinese"]
    }
  },

  // 資產價值評分
  asset_value: {
    total_score: 850,           // 總價值評分 (0-1000)
    tier: "premium",             // bronze/silver/gold/premium
    estimated_monthly_value: {
      min: 15,
      max: 25,
      currency: "USD"
    }
  },

  // 資產質量指標
  quality_metrics: {
    data_richness: 0.88,       // 數據豐富度
    confidence_level: 0.85,     // 標籤置信度
    freshness: 0.92,            // 新鮮度（最近更新）
    consistency: 0.90           // 跨時間一致性
  },

  // 生命週期
  lifecycle: {
    created_at: "2025-11-02",
    last_updated: "2025-11-02",
    data_points: 1250,          // 累積數據點
    analysis_runs: 42           // 分析次數
  }
};
```

### 資產價值計算模型

```javascript
function calculateAssetValue(userProfile) {
  let score = 0;

  // 1. 專業角色價值（B2B 高價值）
  const roleScores = {
    'technical_founder': 200,
    'engineering_manager': 180,
    'product_manager': 150,
    'developer': 100,
    'student': 30
  };
  score += roleScores[userProfile.professional.role] || 50;

  // 2. 決策權溢價
  if (userProfile.professional.decision_maker) score += 150;
  if (userProfile.professional.budget_authority === 'enterprise') score += 100;

  // 3. 購買意圖價值（最高價值）
  Object.values(userProfile.buying_intent).forEach(intent => {
    const intentScores = {
      'very_high': 100,
      'high': 60,
      'medium': 30,
      'low': 10
    };
    score += intentScores[intent.level] || 0;
  });

  // 4. 專業技能價值（技術人才溢價）
  const expertCount = Object.values(userProfile.expertise)
    .filter(skill => skill.level === 'expert').length;
  score += expertCount * 30;

  // 5. 興趣深度
  const highInterests = Object.values(userProfile.interests)
    .filter(interest => interest.score > 0.8).length;
  score += highInterests * 20;

  // 6. 數據質量加成（乘數效果）
  score *= userProfile.quality_metrics.confidence_level;
  score *= userProfile.quality_metrics.freshness;

  return {
    score: Math.round(score),
    tier: getTier(score),
    estimated_monthly_value: estimateMonthlyValue(score)
  };
}

function getTier(score) {
  if (score >= 800) return 'premium';
  if (score >= 600) return 'gold';
  if (score >= 400) return 'silver';
  return 'bronze';
}

function estimateMonthlyValue(score) {
  // 基於市場 CPM (Cost Per Mille - 每千次曝光成本)
  // Premium audience: $20-50 CPM
  // 假設用戶每月參與 500-1000 次匹配
  const cpm = score / 1000 * 50;  // $0-$50 CPM
  const monthly_impressions = 750;  // 平均
  return {
    min: Math.round(cpm * monthly_impressions / 1000 * 0.8),
    max: Math.round(cpm * monthly_impressions / 1000 * 1.2),
    currency: 'USD'
  };
}
```

---

## 🏷️ 標籤資產設計

### 標籤 vs 個資：關鍵區別

**核心原則：有價值 + 不洩露隱私**

| 類型 | 傳統個資 (❌) | 標籤資產 (✅) |
|------|------------|------------|
| **識別性** | 可識別個人 | 匿名、不可逆 |
| **例子** | "Lman, lman@example.com" | "technical_founder_uuid_xxx" |
| **瀏覽記錄** | 具體 URL 列表 | 興趣標籤 "AI_automation: 0.95" |
| **購買行為** | "買了 iPhone" | "高購買意圖: 電子產品" |
| **社交關係** | 朋友列表、對話內容 | "professional_network_type" |
| **位置** | GPS 座標 | "timezone: UTC+8" |

```javascript
// ❌ 個資範例（隱私風險）
{
  "name": "Lman",
  "email": "lman@example.com",
  "browsing_history": [
    "https://github.com/anthropics/claude-code",
    "https://twitter.com/elonmusk/status/12345"
  ],
  "contacts": ["friend1@email.com", "colleague@company.com"]
}

// ✅ 標籤資產範例（隱私安全）
{
  "profile_id": "uuid_550e8400_anonymous",
  "interests": {
    "AI_automation": { score: 0.95, confidence: 0.90 },
    "system_design": { score: 0.88, confidence: 0.85 }
  },
  "expertise": {
    "programming": "expert"
  },
  "buying_intent": {
    "SaaS_tools": { level: "high", category: "productivity" }
  },
  "professional_profile": {
    "role": "technical_founder",  // 不是具體公司名
    "decision_maker": true
  },
  "network_type": "professional_technical"  // 不是具體聯絡人
}
```

### 標籤分類系統

#### Category 1: Interest Tags (興趣標籤)
**價值**: 💰💰 (內容推薦、廣告定向)
**隱私風險**: 🟢 低

```javascript
{
  "AI_automation": { score: 0.95, confidence: 0.90, trend: "increasing" },
  "productivity_tools": { score: 0.82, confidence: 0.88, trend: "stable" },
  "system_design": { score: 0.88, confidence: 0.85, trend: "stable" },
  "indie_hacking": { score: 0.75, confidence: 0.80, trend: "new" }
}
```

#### Category 2: Expertise Tags (專業技能)
**價值**: 💰💰💰 (教育、工具、招聘)
**隱私風險**: 🟢 低

```javascript
{
  "programming": {
    level: "expert",
    languages: ["javascript", "python"],
    frameworks: ["node", "react"]
  },
  "product_management": {
    level: "advanced",
    focus: "technical_products"
  },
  "system_architecture": {
    level: "expert",
    specialization: ["automation", "AI_integration"]
  }
}
```

#### Category 3: Buying Intent Tags (購買意圖)
**價值**: 💰💰💰💰💰 (最高價值 - 廣告主願意高價付費)
**隱私風險**: 🟡 中等

```javascript
{
  "SaaS_tools": {
    level: "high",             // very_high/high/medium/low
    category: "productivity",
    budget_range: "$20-100/mo",
    decision_timeline: "1-3_months",
    consideration_set: ["notion", "linear", "height"]  // 不是具體使用記錄
  },
  "AI_APIs": {
    level: "very_high",
    category: "infrastructure",
    budget_range: "$100-500/mo",
    decision_timeline: "immediate"
  }
}
```

#### Category 4: Professional Profile (專業檔案)
**價值**: 💰💰💰💰 (B2B 高價值)
**隱私風險**: 🟡 中等

```javascript
{
  "role": "technical_founder",     // 不是具體公司和職位
  "team_size": "startup_<10",
  "decision_maker": true,
  "budget_authority": "enterprise_level",  // 預算權限等級
  "tech_stack": ["node", "ai_apis", "macos"],  // 技術棧
  "industry": "tech_productivity"  // 行業類別
}
```

#### Category 5: Content Preferences (內容偏好)
**價值**: 💰💰💰 (內容平台、媒體)
**隱私風險**: 🟢 低

```javascript
{
  "format": "long_form_technical",    // vs short_form, visual, audio
  "tone": "practical_no_fluff",       // vs academic, casual, entertaining
  "engagement_style": "deep_reader",  // vs skimmer, lurker, contributor
  "content_depth": "expert_level",    // vs beginner, intermediate
  "reading_speed": "fast",
  "languages": ["english", "traditional_chinese"]
}
```

#### Category 6: Behavioral Patterns (行為模式)
**價值**: 💰💰 (產品優化、UX 設計)
**隱私風險**: 🟢 低

```javascript
{
  "work_schedule": {
    "peak_hours": "6-9am",
    "timezone": "UTC+8",
    "work_days": ["mon", "tue", "wed", "thu", "fri"]
  },
  "productivity_style": {
    "task_switching": "high_frequency",  // 高頻切換
    "focus_blocks": "short_intense",     // 短時間高強度
    "break_pattern": "micro_breaks"
  },
  "tool_adoption": {
    "early_adopter": true,
    "power_user": true,
    "customization_level": "high"
  }
}
```

### 標籤價值分級

| 標籤類型 | 市場價值 (CPM) | 需求方 | 變現方式 |
|---------|---------------|--------|---------|
| **Purchase Intent (高意圖)** | $30-50 | 廣告主 | 精準廣告 |
| **Professional Role (決策者)** | $20-40 | B2B SaaS | 企業銷售 |
| **Expertise (專家)** | $15-30 | 教育/工具 | 內容推薦 |
| **Content Preference** | $10-20 | 內容平台 | 個人化推薦 |
| **Interest (興趣)** | $5-15 | 內容/廣告 | 通用廣告 |
| **Behavioral Pattern** | $5-10 | 產品團隊 | UX 研究 |

---

## 💰 隱私優先變現

### 變現模式對比

| 模式 | 傳統廣告 (Google/FB) | Context Engine |
|------|---------------------|----------------|
| **追蹤方式** | ❌ Cookies, 跨站追蹤 | ✅ 本地分析，標籤化 |
| **個資洩露** | ❌ 高風險 | ✅ 零風險 (只有標籤) |
| **用戶收益** | ❌ $0 | ✅ $10-50/月 |
| **廣告精準度** | 🟡 中等 | ✅ 極高 |
| **用戶控制** | ❌ 無 | ✅ 完全控制 |
| **透明度** | ❌ 黑盒 | ✅ 完全透明 |
| **GDPR 合規** | 🟡 複雜 | ✅ 原生支持 |

### 模式 1: Anonymous Data Marketplace

**運作流程**：

```
1. 用戶註冊匿名 Profile
   ↓
2. 本地生成標籤資產
   ↓
3. 廣告主發布需求 + 出價
   ↓
4. Context Engine 本地匹配（不上傳數據）
   ↓
5. 匹配成功 → 用戶明確同意
   ↓
6. 展示廣告/內容
   ↓
7. 結算收益 → 用戶錢包
```

**具體例子**：

```javascript
// 廣告主發布需求
{
  "campaign_id": "camp_notion_123",
  "advertiser": "Notion",
  "targeting": {
    "interests": ["productivity_tools", "PKM"],
    "professional_role": ["product_manager", "founder", "developer"],
    "buying_intent": {
      "category": "productivity_SaaS",
      "level": ["high", "very_high"]
    }
  },
  "budget": {
    "cpm": 40,  // $40 per 1000 impressions
    "total": 10000,
    "currency": "USD"
  },
  "consent_required": true,
  "duration": "30_days"
}

// Context Engine 本地匹配
const matched = localMatch(userTags, campaignTargeting);

if (matched && userConsent) {
  // 展示廣告
  showAd(campaign);

  // 結算
  earnings = campaign.cpm / 1000;  // $0.04 per impression
  userWallet.credit(earnings);
}
```

**收益計算**：

```
假設用戶檔案：Premium tier (score 850)
每月匹配：500 次
平均 CPM：$35

月收益 = 500 × ($35 / 1000) = $17.50
平台手續費 20% = $3.50
用戶實得 = $14.00/月
```

### 模式 2: Consent-Based Service Enhancement

**用戶選擇性分享標籤，換取更好服務**

```javascript
// 用戶同意 Notion 訪問部分標籤
{
  "service": "notion.so",
  "consent_id": "consent_uuid_xxx",
  "consent_scope": {
    "interests": true,           // ✅ 允許
    "expertise": true,           // ✅ 允許
    "buying_intent": false,      // ❌ 不允許（太敏感）
    "work_patterns": true,       // ✅ 允許
    "professional_profile": true // ✅ 允許
  },
  "purpose": "personalized_templates_and_features",
  "benefit": {
    "type": "discount",
    "value": "30%_off_annual_plan",  // 或 "free_upgrade_to_pro"
    "equivalent_value": "$48/year"
  },
  "duration": "1_year",
  "revokable": true,
  "audit": true  // 用戶可查看 Notion 訪問了什麼
}
```

**Notion 獲得什麼**：
- 興趣標籤 → 推薦相關模板
- 專業技能 → 推薦進階功能
- 工作模式 → 優化介面和通知時機

**用戶獲得什麼**：
- 💰 30% 折扣 (價值 $48/年)
- 🎁 更好的個人化體驗
- 🔒 完全控制權（隨時撤銷）
- 📊 審計日誌（知道 Notion 看了什麼）

### 模式 3: First-Party Data Alliance

**願景：建立隱私優先的開放標準**

```
Context Engine ←→ DayFlow ←→ Notion ←→ Linear ←→ [更多服務]
       ↓              ↓          ↓          ↓
    統一標籤格式 (Open Standard)
       ↓
   用戶完全控制
       ↓
   跨服務無縫體驗
```

**標準化標籤協議**：

```json
{
  "protocol": "OpenUserTags v1.0",
  "spec": "https://openusertagsorg/spec/v1",
  "user_profile": {
    "anonymous_id": "uuid_xxx",
    "tags": {
      "interests": [...],
      "expertise": [...],
      // 標準化格式
    }
  },
  "consent_management": {
    "granular_control": true,
    "revokable": true,
    "portable": true  // 可跨服務遷移
  }
}
```

**生態系統效應**：
- 用戶一次建立 Profile，到處使用
- 服務商獲得更準確的用戶理解
- 用戶收益最大化（多方競價）
- 形成新的數據經濟範式

---

## 💼 B2B API 變現：System Prompt as a Service

### 核心概念：API 化的用戶理解

**發現的新變現路徑** (2025-11-02):

> "撇開廣告，光 system prompt 這部份，面向的就有可能是一些 vertical market 的 agent 例如 Gamma AI 這一類做簡報或者類似服務的業者，因為他們不太可能一下子就理解用戶，但在我的假想中，他們可以透過對用戶的 context aware engine 來串接獲得用戶授權後就有機會一次性或者連續性的得到最新的用戶 insight 或者是相關的 system prompt"

**為什麼這個重要**：
- ✅ **更快變現**：不需要等到 100K+ 用戶（廣告模式門檻）
- ✅ **更簡單實現**：只需 API，不需要廣告匹配系統
- ✅ **B2B 收入穩定**：按月訂閱，可預測
- ✅ **獨立於 IrisGo GTM**：不依賴 OEM pre-install 速度

### 目標客戶與價值主張

#### Vertical App 1: Gamma AI (AI 簡報生成)

**痛點**：
- 用戶第一次使用 Gamma 時，AI 不了解用戶風格
- 生成的簡報需要多次調整才符合需求
- 缺少用戶專業背景和內容偏好

**Context Engine API 解決**：
```javascript
// Gamma 調用 Context Engine API
const userContext = await contextEngine.getSystemPrompt({
  user_id: "gamma_user_12345",
  modules: [
    "professional_profile",  // 了解用戶角色（創業者/PM/工程師）
    "communication_style",    // 了解簡報風格偏好（數據驅動/視覺化）
    "expertise",              // 了解專業領域（AI/產品/商業）
    "content_preferences"     // 了解內容深度偏好（技術細節/高層概覽）
  ],
  format: "structured_json"
});

// Gamma 使用 context 生成個人化簡報
const presentation = await gammaAI.generate({
  topic: "Q4 Product Roadmap",
  user_context: userContext,  // 注入用戶理解
  style: userContext.communication_style.presentation_format  // "data_driven_concise"
});
```

**價值**：
- 用戶獲得：首次使用就產生高度個人化的簡報
- Gamma 獲得：更高的用戶滿意度和留存率
- Context Engine：$2-5 per active user/month

---

#### Vertical App 2: Notion (筆記與知識管理)

**痛點**：
- Notion AI 不了解用戶的 PKM 系統和思維方式
- 推薦的模板和功能不符合用戶需求
- 缺少個人化的內容組織建議

**Context Engine API 解決**：
```javascript
const userContext = await contextEngine.getSystemPrompt({
  user_id: "notion_user_67890",
  modules: [
    "work_patterns",          // 了解任務管理風格（GTD/時間區塊）
    "interests",              // 了解知識領域和興趣
    "decision_framework",     // 了解決策邏輯
    "tool_usage"              // 了解現有工具棧
  ]
});

// Notion 推薦個人化模板
const recommendations = notion.ai.recommend({
  context: userContext,
  type: "templates"
});
// → 推薦「技術產品經理專用模板」而非「通用任務管理」
```

**價值**：
- 用戶獲得：Notion 立即"懂你"，減少設置時間
- Notion 獲得：更高的付費轉化率
- Context Engine：$1-3 per active user/month

---

#### Vertical App 3: Linear (項目管理)

**痛點**：
- 不了解團隊成員的工作風格和溝通偏好
- Issue 分配和優先級建議不夠精準
- Workflow 設置需要大量手動配置

**Context Engine API 解決**：
```javascript
const teamContext = await contextEngine.getTeamProfiles({
  team_id: "linear_team_123",
  members: ["user_a", "user_b", "user_c"],
  modules: [
    "work_patterns",
    "communication_style",
    "decision_framework",
    "expertise"
  ]
});

// Linear 智能分配 Issues
const assignment = linear.ai.assignIssue({
  issue: "Implement OAuth flow",
  team_context: teamContext,
  criteria: "match_expertise_and_availability"
});
// → 分配給技術專家 + 當前工作負載低的成員
```

**價值**：
- 用戶獲得：更智能的任務分配和協作
- Linear 獲得：差異化功能，提高企業客戶 ARR
- Context Engine：$3-5 per active user/month

---

#### Vertical App 4: Superhuman (Email 客戶端)

**痛點**：
- 不了解用戶的溝通風格和回覆模式
- AI 草稿不符合用戶語氣
- 郵件優先級排序不夠精準

**Context Engine API 解決**：
```javascript
const userContext = await contextEngine.getSystemPrompt({
  user_id: "superhuman_user_456",
  modules: [
    "communication_style",     // 簡潔/詳細、正式/輕鬆
    "relationship_network",    // 核心聯絡人
    "response_patterns",       // 回覆速度和優先級
    "professional_context"     // 角色和職責
  ]
});

// Superhuman 生成符合用戶風格的 Email 草稿
const draft = superhuman.ai.draftReply({
  email: incomingEmail,
  user_context: userContext
});
// → 自動匹配用戶的「簡潔、數據驅動、解決方案導向」風格
```

**價值**：
- 用戶獲得：AI 草稿幾乎不需修改
- Superhuman 獲得：核心差異化功能
- Context Engine：$2-4 per active user/month

---

### API 設計

#### 認證與授權流程

```javascript
// Step 1: 用戶在 Vertical App 中授權
// Gamma/Notion/Linear 顯示授權請求
const authRequest = {
  app: "gamma.app",
  requested_modules: [
    "professional_profile",
    "communication_style",
    "expertise"
  ],
  purpose: "Personalize AI presentation generation",
  benefit: "Get presentations that match your style from first use",
  duration: "ongoing",  // 或 "one_time"
  revokable: true
};

// Step 2: 用戶同意後，Context Engine 生成 API token
const apiToken = contextEngine.authorize({
  user_id: "user_uuid_xxx",
  app_id: "gamma.app",
  scope: authRequest.requested_modules,
  expires_in: "1_year"
});

// Step 3: Vertical App 使用 API token 訪問
const response = await fetch('https://api.context-engine.io/v1/system-prompt', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_id: "user_uuid_xxx",
    modules: ["professional_profile", "communication_style"],
    format: "structured_json"  // or "text", "markdown"
  })
});
```

#### API 響應格式

```json
{
  "user_id": "anonymous_uuid_xxx",
  "generated_at": "2025-11-02T15:30:00+08:00",
  "confidence_score": 0.88,
  "data_sources": ["dayflow", "gmail", "calendar"],
  "modules": {
    "professional_profile": {
      "role": "technical_founder",
      "decision_maker": true,
      "team_size": "startup_<10",
      "industry": "tech_productivity",
      "tech_stack": ["node", "ai_apis", "macos"]
    },
    "communication_style": {
      "tone": "concise_data_driven",
      "format_preference": "bullet_points_and_code",
      "language": ["english", "traditional_chinese"],
      "response_speed": "prefer_quick_iterations"
    },
    "expertise": {
      "programming": {
        "level": "expert",
        "languages": ["javascript", "python"]
      },
      "product_management": {
        "level": "advanced",
        "focus": "technical_products"
      }
    }
  },
  "system_prompt": {
    "text": "You're assisting a technical founder who values concise, data-driven communication...",
    "length": 450,
    "format": "markdown"
  }
}
```

#### Webhook 更新機制

```javascript
// Vertical App 可以訂閱用戶 context 更新
const webhook = contextEngine.subscribe({
  app_id: "gamma.app",
  user_id: "user_uuid_xxx",
  events: ["context_updated", "consent_revoked"],
  webhook_url: "https://gamma.app/webhooks/context-engine"
});

// 當用戶的 Context 有顯著變化時（例如新項目、角色變化）
// Context Engine 發送 webhook
POST https://gamma.app/webhooks/context-engine
{
  "event": "context_updated",
  "user_id": "user_uuid_xxx",
  "timestamp": "2025-11-15T10:00:00+08:00",
  "changes": {
    "professional_profile.current_projects": {
      "added": ["IrisGo AI v2.0"],
      "removed": []
    },
    "interests": {
      "added": ["voice_AI"],
      "trending_up": ["automation"]
    }
  },
  "action": "fetch_updated_context"
}
```

---

### 商業模式

#### 定價策略

**Model 1: Per Active User Pricing (推薦)**

```javascript
const pricing = {
  tier_1_basic: {
    price_per_active_user_per_month: 1.00,  // $1/user/month
    included_modules: ["professional_profile", "interests"],
    update_frequency: "monthly",
    api_calls: "unlimited",
    suitable_for: "內容推薦類 App"
  },

  tier_2_standard: {
    price_per_active_user_per_month: 2.50,  // $2.5/user/month
    included_modules: [
      "professional_profile",
      "interests",
      "communication_style",
      "expertise"
    ],
    update_frequency: "bi-weekly",
    webhook_updates: true,
    suitable_for: "Gamma, Notion"
  },

  tier_3_premium: {
    price_per_active_user_per_month: 5.00,  // $5/user/month
    included_modules: "all",
    update_frequency: "weekly",
    webhook_updates: true,
    real_time_insights: true,
    suitable_for: "Superhuman, Linear (企業級)"
  }
};

// 計費示例：Gamma 有 10,000 個活躍用戶使用 Context Engine
// 月費 = 10,000 × $2.50 = $25,000/month
// Gamma 年成本 = $300,000
```

**Model 2: Revenue Share (替代方案)**

```javascript
const revenueShare = {
  model: "Context Engine 從 Vertical App 的增量收入中分成",
  calculation: {
    baseline: "用戶未使用 Context Engine 的平均 LTV",
    incremental: "使用 Context Engine 後的 LTV 增長",
    share: "Context Engine 獲得增量的 20-30%"
  },
  example: {
    app: "Notion",
    baseline_annual_revenue_per_user: 100,  // $100/year
    with_context_engine_revenue_per_user: 130,  // +30% due to better retention
    incremental_revenue: 30,
    context_engine_share_30_percent: 9,  // $9/user/year
    context_engine_monthly: 0.75  // $0.75/user/month
  },
  advantage: "對 Vertical App 風險更低，只在證明價值後付費",
  challenge: "需要追蹤和證明因果關係"
};
```

---

### 價值計算：為什麼 Vertical Apps 願意付費？

#### Case Study: Gamma AI

```javascript
const gammaBusinessCase = {
  // 當前狀況（無 Context Engine）
  without_context_engine: {
    user_onboarding: {
      first_presentation_satisfaction: "60%",  // 需要多次調整
      time_to_first_value: "20 minutes",
      onboarding_completion_rate: "65%"
    },
    user_retention: {
      day_7_retention: "40%",
      day_30_retention: "25%",
      annual_churn: "60%"
    },
    revenue: {
      free_to_paid_conversion: "5%",
      annual_revenue_per_user: "$80",
      ltv: "$150"
    }
  },

  // 整合 Context Engine 後
  with_context_engine: {
    user_onboarding: {
      first_presentation_satisfaction: "85%",  // ↑ 25%
      time_to_first_value: "5 minutes",        // ↓ 75%
      onboarding_completion_rate: "85%"        // ↑ 20%
    },
    user_retention: {
      day_7_retention: "55%",   // ↑ 15%
      day_30_retention: "35%",  // ↑ 10%
      annual_churn: "45%"       // ↓ 15%
    },
    revenue: {
      free_to_paid_conversion: "7%",     // ↑ 2%
      annual_revenue_per_user: "$95",    // ↑ $15 (better retention)
      ltv: "$210"                         // ↑ $60
    }
  },

  // ROI 計算
  roi_calculation: {
    incremental_ltv_per_user: 60,  // $210 - $150
    context_engine_cost_per_user_annual: 30,  // $2.5/month × 12
    net_gain_per_user: 30,  // $60 - $30
    roi: "100%",  // 每花 $1 賺回 $2

    // 對 Gamma 而言：即使付 $2.5/user/month，仍然有 $30 淨增益
    // 絕對值得投資
  },

  scale_impact: {
    gamma_monthly_active_users: 50000,
    context_engine_adoption_rate: "20%",  // 10,000 users 使用
    monthly_cost: "$25,000",  // 10k × $2.5
    annual_cost: "$300,000",
    annual_incremental_revenue: "$600,000",  // 10k × $60
    net_annual_gain: "$300,000"
  }
};
```

**結論**：即使 Gamma 每月支付 $25K，他們仍然獲得 $300K 年淨增益（100% ROI）

---

### 與廣告模式的對比

| 維度 | 廣告模式 (Data Marketplace) | API 模式 (System Prompt as a Service) |
|------|---------------------------|---------------------------------------|
| **用戶門檻** | 需要 100K+ 用戶才有規模效應 | 1K-10K 用戶就可啟動 |
| **變現速度** | 慢（需要建立雙邊市場） | 快（直接 B2B 銷售） |
| **收入穩定性** | 波動（依賴廣告主需求） | 穩定（按月訂閱） |
| **技術複雜度** | 高（匹配引擎、隱私保護、結算） | 中（API + Auth） |
| **用戶體驗** | 需要用戶主動同意每次廣告 | 一次授權，長期使用 |
| **單用戶收益** | $10-50/月 (長期) | $1-5/月 (但 B2B 穩定) |
| **依賴 IrisGo GTM** | 高（需要大量用戶） | 低（獨立銷售） |
| **首個收益時間** | 6-12 個月 | 1-3 個月 |

**戰略建議**：
1. **短期（M1-6）**：優先 API 模式
   - 更快驗證商業模式
   - 建立 B2B 客戶關係
   - 獨立於 IrisGo 的 GTM 進度

2. **中期（M6-12）**：並行發展
   - API 模式提供穩定現金流
   - 廣告模式在用戶規模達到後啟動

3. **長期（Y2+）**：雙引擎驅動
   - B2B API: 穩定收入 + 企業客戶
   - B2C Marketplace: 規模化收入 + 用戶獲益

---

### Go-to-Market 策略

#### Phase 1: Pilot Partners (M1-3)

**目標**：驗證 API 價值，優化產品

```javascript
const pilotProgram = {
  partners: [
    {
      name: "Gamma AI",
      reason: "AI-powered vertical, high value proposition",
      deal: "Free for 3 months, 1000 users cap",
      success_metrics: [
        "First presentation satisfaction ↑ 20%",
        "Onboarding completion ↑ 15%",
        "Day 7 retention ↑ 10%"
      ]
    },
    {
      name: "Notion",
      reason: "Large user base, strong PKM fit",
      deal: "Free for 3 months, 2000 users cap",
      success_metrics: [
        "Template recommendation click-through ↑ 25%",
        "AI feature usage ↑ 30%",
        "Premium conversion ↑ 5%"
      ]
    }
  ],
  deliverables: [
    "API integration guide",
    "SDKs (JavaScript, Python)",
    "Dedicated support",
    "Co-marketing case study"
  ],
  timeline: "M1-M3",
  kpi: "2 pilots successfully deployed, positive ROI demonstrated"
};
```

#### Phase 2: Paid Beta (M3-6)

**目標**：擴展到 5-10 個付費客戶

```javascript
const paidBeta = {
  pricing: {
    early_adopter_discount: "50% off for first year",
    tier_2_standard: "$1.25/user/month (normally $2.50)",
    minimum_commitment: "6 months"
  },
  target_customers: [
    "Superhuman (email)",
    "Linear (project management)",
    "Height (collaboration)",
    "Cron (calendar)",
    "Raycast (launcher + AI)"
  ],
  sales_approach: {
    method: "Direct outreach to founders/product leads",
    pitch: "API demo + pilot success case studies",
    close_rate_target: "30%"
  },
  revenue_target: {
    customers: 5,
    avg_active_users_per_customer: 5000,
    price_per_user: 1.25,
    mrr: "$31,250",  // 5 × 5000 × $1.25
    arr: "$375,000"
  }
};
```

#### Phase 3: Platform Launch (M6-12)

**目標**：建立 self-service platform，規模化

```javascript
const platformLaunch = {
  features: [
    "Self-service signup and API key generation",
    "Usage dashboard and analytics",
    "Billing automation",
    "Developer docs and sandbox",
    "Marketplace listing (expose to long-tail apps)"
  ],
  go_to_market: {
    channels: [
      "Product Hunt launch",
      "Developer community (Hacker News, Reddit)",
      "Content marketing (case studies, API guides)",
      "Conference presence (AI engineer summit)"
    ]
  },
  revenue_target: {
    tier_1_apps: 3,      // Large apps (50K+ users)
    tier_2_apps: 10,     // Mid-size (5K-50K users)
    tier_3_apps: 30,     // Small apps (500-5K users)
    total_users: 200000, // 加總
    avg_price: 2.00,     // 混合價格
    mrr: "$400,000",
    arr: "$4.8M"
  }
};
```

---

### 技術路線圖

#### M1-2: MVP API

```javascript
const mvpAPI = {
  endpoints: [
    "POST /v1/auth/authorize - 用戶授權",
    "GET /v1/system-prompt - 獲取 System Prompt",
    "GET /v1/modules/{module_name} - 獲取單一模組",
    "POST /v1/webhooks/subscribe - 訂閱更新"
  ],
  modules: [
    "professional_profile",
    "communication_style",
    "interests",
    "expertise"
  ],
  auth: "OAuth 2.0 + API tokens",
  format: "JSON + Markdown text",
  rate_limit: "1000 requests/day per app"
};
```

#### M3-6: Enhanced API

```javascript
const enhancedAPI = {
  new_modules: [
    "work_patterns",
    "decision_framework",
    "relationship_network",
    "temporal_context"
  ],
  new_features: [
    "Real-time webhooks on context change",
    "Batch API for multiple users",
    "Custom module composition",
    "Confidence scores per insight"
  ],
  sdks: [
    "JavaScript/TypeScript SDK",
    "Python SDK",
    "Ruby SDK",
    "REST API"
  ]
};
```

#### M6-12: Platform Scale

```javascript
const platformScale = {
  infrastructure: [
    "Horizontal scaling (handle 1M+ users)",
    "Global CDN for low latency",
    "99.9% SLA",
    "SOC 2 compliance"
  ],
  advanced_features: [
    "Team/organization APIs (for Linear, Notion workspace)",
    "White-label embedding",
    "Custom data source connectors",
    "Advanced analytics and attribution"
  ]
};
```

---

### 風險與緩解

#### Risk 1: Vertical Apps 不願意整合

**緩解**：
- 提供極其簡單的 API（5 行代碼整合）
- 免費 pilot 證明 ROI
- Co-marketing 帶來額外曝光

#### Risk 2: 用戶不願意授權

**緩解**：
- 清楚說明價值交換（更好的個人化體驗）
- 細粒度控制（用戶選擇分享哪些模組）
- 透明審計日誌
- 支持一次性授權（vs 持續訪問）

#### Risk 3: API 競爭者

**緩解**：
- 先發優勢 + 深度整合
- 持續更新的數據（competitor 很難複製）
- 多數據源融合（不只是單一來源）
- 建立 Network effect（更多 apps → 更多用戶 → 更多 data → 更好 insights）

---

### 成功指標

#### M3 Milestones
- [ ] 2 個 pilot partners 簽約
- [ ] API 文檔完成
- [ ] 首個成功整合（Gamma or Notion）

#### M6 Milestones
- [ ] 5 個付費客戶
- [ ] $30K+ MRR
- [ ] 平均 API uptime > 99%
- [ ] Pilot partners report positive ROI

#### M12 Milestones
- [ ] 20+ 付費客戶
- [ ] $400K+ MRR
- [ ] Self-service platform 上線
- [ ] 首個企業級客戶 (50K+ users)

---

## 📊 數據源與洞察層級

### 數據源矩陣

| 數據源 | 已完成 | 提供洞察 | 更新頻率 | 優先級 |
|--------|--------|----------|----------|--------|
| **DayFlow** | ✅ | 時間分配、專注度、工具使用、高效時段 | 每 2 天 | 🔴 High |
| **Gmail** | ⬜ | 溝通風格、關係網絡、回應速度、主題分佈 | 每日 | 🟡 Medium |
| **Calendar** | ⬜ | 會議密度、時間區塊、協作模式 | 每日 | 🟡 Medium |
| **Twitter** | ⬜ | 興趣話題、社交風格、內容偏好 | 每週 | 🟢 Low |

### 洞察層級

#### Layer 1: Raw Metrics (原始指標)
- DayFlow: 82 activities, 70.4% work time, 81/100 focus score
- Gmail: 50 emails/day, avg response time 2h
- Calendar: 4 meetings/day, 2h total

#### Layer 2: Behavioral Patterns (行為模式)
- 工作模式: 高強度任務切換 (27 tasks/day, 17min avg)
- 溝通偏好: 簡潔、數據驅動、解決方案導向
- 時間管理: 早晨 6-9am 最高效 (65% efficiency)

#### Layer 3: Cognitive Traits (認知特質)
- 決策風格: 多源資訊合成、實用主義
- 學習方式: 應用導向、動手實踐
- 思維模式: 系統思考、架構設計

#### Layer 4: Identity & Values (身份與價值觀)
- 核心身份: 務實的願景家、系統建造者
- 價值觀: 效率、影響力、知識應用
- 職涯定位: 技術 × 商業 × 人際的交會點

---

## 🏗️ 系統架構

### 整體架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                      Data Collection Layer                   │
├─────────────────────────────────────────────────────────────┤
│  DayFlow      Gmail       Calendar      Twitter      [More]  │
│  Collector    Collector   Collector     Collector            │
└────────┬──────────┬───────────┬─────────────┬────────────────┘
         │          │           │             │
         └──────────┴───────────┴─────────────┘
                         │
         ┌───────────────▼───────────────┐
         │     Analysis & Synthesis      │
         ├───────────────────────────────┤
         │  • Work Pattern Analyzer      │
         │  • Communication Analyzer     │
         │  • Interest Analyzer          │
         │  • Relationship Analyzer      │
         │  • Persona Synthesizer        │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │     Prompt Generation         │
         ├───────────────────────────────┤
         │  • Core Identity Module       │
         │  • Working Style Module       │
         │  • Communication Module       │
         │  • Temporal Context Module    │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │     Output & Distribution     │
         ├───────────────────────────────┤
         │  ChatGPT Prompt               │
         │  Claude Prompt                │
         │  Gemini Prompt                │
         │  API Endpoint                 │
         └───────────────────────────────┘
```

### 目錄結構

```
~/iris-system/context-engine/
│
├── collectors/                    # 數據收集器
│   ├── dayflow-collector.js      # ✅ 已存在 (dayflow-intelligence.js)
│   ├── gmail-collector.js         # ⬜ 待開發
│   ├── calendar-collector.js      # ⬜ 待開發
│   ├── twitter-collector.js       # ⬜ 待開發
│   └── base-collector.js          # 通用收集器基類
│
├── analyzers/                     # 數據分析器
│   ├── work-pattern-analyzer.js   # 分析工作模式
│   ├── communication-analyzer.js  # 分析溝通風格
│   ├── interest-analyzer.js       # 分析興趣領域
│   ├── relationship-analyzer.js   # 分析社交關係
│   └── temporal-analyzer.js       # 分析時間模式
│
├── synthesizers/                  # 洞察合成器
│   ├── persona-synthesizer.js     # 生成 Persona
│   ├── prompt-generator.js        # 生成 System Prompt
│   ├── context-updater.js         # 更新動態上下文
│   └── insights-merger.js         # 合併多源洞察
│
├── templates/                     # Prompt 模板
│   ├── core-identity.md           # 核心身份模板
│   ├── working-style.md           # 工作風格模板
│   ├── communication.md           # 溝通偏好模板
│   ├── decision-framework.md      # 決策框架模板
│   └── specialized/               # 專門模組
│       ├── technical.md
│       ├── creative.md
│       └── leadership.md
│
├── output/                        # 生成輸出
│   ├── prompts/                   # System Prompts
│   │   ├── chatgpt-full.txt
│   │   ├── chatgpt-compact.txt
│   │   ├── claude-full.txt
│   │   ├── claude-compact.txt
│   │   ├── gemini-full.txt
│   │   └── gemini-compact.txt
│   │
│   ├── personas/                  # Persona 檔案
│   │   ├── current-persona.json
│   │   ├── persona-history/
│   │   └── persona-diff.md
│   │
│   └── api/                       # API 格式
│       ├── context.json
│       └── modules/
│
├── config/                        # 配置檔案
│   ├── data-sources.json          # 數據源配置
│   ├── prompt-templates.json      # 模板配置
│   ├── privacy-settings.json      # 隱私設定
│   └── update-schedule.json       # 更新排程
│
├── scripts/                       # 執行腳本
│   ├── generate-prompt.js         # 生成 Prompt
│   ├── update-context.js          # 更新上下文
│   ├── compare-personas.js        # 比較 Persona 變化
│   └── export-to-ai.js            # 導出到 AI 工具
│
├── tests/                         # 測試
│   ├── collectors.test.js
│   ├── analyzers.test.js
│   └── generators.test.js
│
├── docs/                          # 文檔
│   ├── API.md
│   ├── DATA-SCHEMA.md
│   └── USER-GUIDE.md
│
├── package.json
├── README.md
└── context-engine.js              # 主程序
```

---

## 📝 System Prompt 設計

### 分層架構

#### 🔴 Core Identity (100-200 tokens)
**必須包含** - 最核心的特質和價值觀

```markdown
# Core Identity

You're a systems thinker and builder operating at the intersection of
technology, business, and people. You value practical application over
theory and prioritize efficiency to free cognitive bandwidth for complex
problems.

**Key Traits:**
- Pragmatic visionary
- Application-oriented learner
- High-bandwidth synthesizer
- Ruthless prioritizer
```

#### 🟡 Extended Context (300-500 tokens)
**常用場景** - 工作風格、溝通偏好、決策框架

```markdown
# Working Style

**Productivity Pattern:**
- Peak hours: 6-9am (65% efficiency)
- Task switching: ~27 activities/day, 17min avg
- Focus score: 81/100 (excellent)
- Work time: 70.4% of tracked time

**Primary Tools:**
- GitHub (24x/2days), Slack (21x), Twitter (16x)
- Terminal, Meet, Obsidian for PKM

**Communication Preferences:**
- Concise, data-driven, solution-oriented
- Direct approach, minimal ambiguity
- Bilingual (EN/ZH) seamless switching

**Decision Framework:**
- Multi-source synthesis (tech + product + market)
- Impact & urgency prioritization
- "What NOT to do" equally important
```

#### 🟢 Specialized Modules (可選)
**特定場景** - 技術、創意、領導力等專門模組

```markdown
# Technical Context

**Active Projects:**
- IrisGo AI: Intelligent personal assistant
- Investment Analyst: Automated news analysis
- Context Engine: Personalized AI prompts

**Tech Stack Familiarity:**
- Node.js, AI APIs (Claude, Gemini, OpenAI)
- macOS automation, LaunchAgents, shell scripting
- PKM systems (Obsidian), API integration

**Learning Mode:**
- Hands-on, build-to-learn
- API documentation → immediate implementation
- System design → practical application
```

#### 🔵 Temporal Context (動態更新)
**實時狀態** - 當前關注、近期活動、心智狀態

```markdown
# Current Context (Updated: 2025-11-02)

**Recent Focus:**
- Building context-aware AI engine
- Investment analysis automation with N8N
- Iris Vision system PKM integration

**Active Interests:**
- Claude Code, BrowserOS, DayFlow intelligence
- AI-powered productivity tools
- System architecture and automation

**Current Time Zone:** UTC+8 (Taiwan)
**Current Energy Level:** High (morning peak hours)
```

### 版本變體

#### Compact Version (適用 token 限制場景)
- 只包含 Core Identity + 關鍵工作風格
- 約 300-400 tokens

#### Full Version (適用高 token 限制)
- Core + Extended + 1-2 Specialized Modules + Temporal
- 約 800-1200 tokens

#### API Version (JSON 格式)
```json
{
  "core_identity": {...},
  "working_style": {...},
  "communication": {...},
  "decision_framework": {...},
  "technical_context": {...},
  "temporal_context": {...},
  "meta": {
    "version": "0.1.0",
    "generated_at": "2025-11-02T15:00:00+08:00",
    "data_sources": ["dayflow", "persona"],
    "confidence_score": 0.85
  }
}
```

---

## 🔒 同意管理系統

### 核心原則：用戶完全控制

**用戶數據 = 用戶資產 = 用戶決定**

```
數據收集 → 標籤生成 → 用戶審查 → 明確同意 → 才能分享
         ↓            ↓           ↓           ↓
     本地處理      可查看      可編輯      可撤銷
```

### 細粒度控制介面設計

```javascript
// Consent Management Dashboard
const userConsentSettings = {
  // 全局主開關
  master_switch: {
    anonymous_sharing: true,  // 總開關
    description: "允許匿名分享標籤資產以獲取收益或更好服務"
  },

  // 分類控制（細粒度）
  category_controls: {
    interests: {
      enabled: true,
      sub_controls: {
        "AI_automation": true,       // ✅ 允許分享
        "productivity_tools": true,  // ✅ 允許分享
        "entertainment": false,      // ❌ 不分享娛樂興趣
        "politics": false            // ❌ 不分享政治興趣
      },
      sensitivity_level: "low"
    },

    expertise: {
      enabled: true,
      sub_controls: {
        "programming": true,
        "product_management": true
      },
      sensitivity_level: "low"
    },

    buying_intent: {
      enabled: true,
      min_cpm_threshold: "$30",  // 只有高價值廣告才能訪問
      sensitivity_level: "high"
    },

    professional_profile: {
      enabled: true,
      exclude_fields: ["team_size"],  // 不透露團隊規模
      sensitivity_level: "medium"
    },

    work_patterns: {
      enabled: false,  // 工作模式完全不分享
      reason: "too_personal",
      sensitivity_level: "high"
    },

    content_preferences: {
      enabled: true,
      sensitivity_level: "low"
    }
  },

  // 行業/類別過濾
  industry_filters: {
    whitelist: [
      "SaaS",
      "productivity_tools",
      "AI_services",
      "developer_tools"
    ],
    blacklist: [
      "gambling",
      "dating",
      "politics",
      "adult_content",
      "alcohol",
      "tobacco"
    ]
  },

  // 頻率限制
  sharing_limits: {
    max_campaigns_per_day: 10,
    max_services_simultaneously: 5,
    cool_down_period: "24h"  // 同一廣告主24小時內只能訪問一次
  },

  // 變現設定
  monetization: {
    enabled: true,
    min_payout: "$5.00",
    payout_method: "crypto_wallet",  // 保持匿名
    payout_frequency: "monthly",
    platform_fee: 0.20  // 20% 平台手續費
  },

  // 服務商白名單（Consent-Based Service Enhancement）
  trusted_services: [
    {
      service: "notion.so",
      consent_id: "consent_uuid_123",
      allowed_categories: ["interests", "expertise", "work_patterns"],
      benefit: "30%_discount",
      expires_at: "2026-11-02",
      revokable: true
    }
  ]
};
```

### 透明度儀表板

**用戶可以實時查看所有訪問記錄**

```javascript
// Audit Log 審計日誌
const auditLog = [
  {
    timestamp: "2025-11-02 14:30:05",
    event_type: "tag_access",
    accessor: {
      type: "advertiser",
      id: "anonymous_advertiser_notion_123",
      name: "Notion"  // 不是完全匿名，用戶知道是誰訪問
    },
    tags_accessed: [
      "interests.productivity_tools",
      "expertise.programming",
      "professional_profile.role"
    ],
    purpose: "personalized_ad_campaign",
    user_earnings: "$0.04",
    user_action: "approved",  // 用戶明確同意
    cpm: "$40"
  },
  {
    timestamp: "2025-11-02 10:15:22",
    event_type: "service_access",
    accessor: {
      type: "service",
      id: "notion.so",
      name: "Notion"
    },
    tags_accessed: [
      "interests",
      "expertise",
      "work_patterns"
    ],
    purpose: "personalized_templates",
    benefit_received: "30%_discount ($48/year value)",
    user_action: "pre_approved",  // 長期授權
    consent_id: "consent_uuid_123"
  },
  {
    timestamp: "2025-11-02 09:00:15",
    event_type: "access_denied",
    accessor: {
      type: "advertiser",
      id: "anonymous_advertiser_dating_456"
    },
    reason: "industry_blacklist",
    tags_requested: ["interests", "professional_profile"],
    user_action: "auto_blocked"  // 自動封鎖
  }
];
```

### 同意流程設計

#### 流程 1: 即時廣告匹配

```
1. 廣告主發布需求
   ↓
2. Context Engine 本地匹配
   ↓
3. 匹配成功 → 彈出通知
   ┌─────────────────────────────────────┐
   │ 💰 收益機會                          │
   │                                     │
   │ Notion 想要訪問你的標籤:            │
   │ ✅ Interests: productivity_tools    │
   │ ✅ Expertise: programming           │
   │ ✅ Professional: founder            │
   │                                     │
   │ 目的: 個人化廣告推薦                │
   │ 收益: $0.04                         │
   │ CPM: $40 (Premium tier)             │
   │                                     │
   │ [同意] [拒絕] [永久封鎖 Notion]    │
   └─────────────────────────────────────┘
   ↓
4. 用戶決定
   ↓
5a. 同意 → 展示廣告 → 結算收益
5b. 拒絕 → 跳過此廣告
5c. 封鎖 → 永久封鎖該廣告主
```

#### 流程 2: 服務整合授權

```
1. 用戶想要使用 Notion 個人化功能
   ↓
2. Notion 請求訪問標籤
   ┌─────────────────────────────────────┐
   │ Notion 整合請求                      │
   │                                     │
   │ Notion 想要訪問以下標籤來提供      │
   │ 個人化模板和功能：                  │
   │                                     │
   │ ☑ Interests (推薦相關模板)         │
   │ ☑ Expertise (推薦進階功能)         │
   │ ☐ Buying Intent (不需要)           │
   │ ☑ Work Patterns (優化通知時機)     │
   │                                     │
   │ 你將獲得:                           │
   │ 🎁 30% 年度折扣 (價值 $48/year)    │
   │ 🎁 更好的個人化體驗                │
   │                                     │
   │ 有效期: 1 年 (可隨時撤銷)          │
   │                                     │
   │ [授權] [自定義範圍] [拒絕]        │
   └─────────────────────────────────────┘
   ↓
3. 用戶授權
   ↓
4. 生成 consent_id 記錄
   ↓
5. Notion 獲得訪問權限
```

### 撤銷機制

**用戶可以隨時撤銷授權**

```javascript
// 撤銷單一服務
function revokeConsent(consentId) {
  const consent = findConsent(consentId);

  // 立即撤銷
  consent.status = 'revoked';
  consent.revoked_at = Date.now();

  // 通知服務商
  notifyService(consent.service, {
    event: 'consent_revoked',
    consent_id: consentId,
    reason: 'user_requested'
  });

  // 清除該服務的快取標籤數據
  clearServiceCache(consent.service);

  return {
    success: true,
    message: `已撤銷 ${consent.service} 的訪問權限`
  };
}

// 撤銷所有授權（緊急按鈕）
function revokeAllConsents() {
  const allConsents = getUserConsents();

  allConsents.forEach(consent => {
    revokeConsent(consent.id);
  });

  // 清空所有分享歷史
  clearAllAuditLogs();

  // 重新生成匿名 UUID
  regenerateAnonymousId();

  return {
    success: true,
    message: '已撤銷所有授權並重置匿名 ID'
  };
}
```

### 數據可攜性 (Data Portability)

**用戶可以導出或遷移自己的標籤資產**

```javascript
// 導出標籤資產
function exportUserAssets() {
  const assets = {
    profile_id: user.anonymous_id,
    export_date: Date.now(),
    format_version: "1.0",

    tag_portfolio: user.tag_portfolio,
    asset_value: user.asset_value,
    quality_metrics: user.quality_metrics,

    consent_history: user.consent_history,
    audit_logs: user.audit_logs,
    monetization_summary: {
      total_earnings: user.total_earnings,
      transactions: user.transactions
    }
  };

  // 加密導出
  const encrypted = encryptWithUserKey(assets);

  return {
    filename: `context-engine-assets-${Date.now()}.json.enc`,
    data: encrypted,
    instructions: "Use your master key to decrypt"
  };
}

// 導入到另一個系統
function importUserAssets(encryptedData, userKey) {
  const assets = decryptWithUserKey(encryptedData, userKey);

  // 驗證格式
  if (assets.format_version !== "1.0") {
    throw new Error("Incompatible format version");
  }

  // 導入標籤
  mergeTagPortfolio(assets.tag_portfolio);

  // 重新計算資產價值
  recalculateAssetValue();

  return {
    success: true,
    imported_tags: Object.keys(assets.tag_portfolio).length,
    asset_value: user.asset_value
  };
}
```

### 隱私保護增強

#### 差分隱私 (Differential Privacy)

```javascript
// 在分享標籤時加入噪音，保護隱私
function shareTagsWithPrivacy(tags, epsilonmodels) {
  const noisyTags = {};

  Object.keys(tags).forEach(category => {
    noisyTags[category] = {};

    Object.keys(tags[category]).forEach(tag => {
      const originalScore = tags[category][tag].score;

      // 加入拉普拉斯噪音
      const noise = laplaceNoise(epsilon);
      const noisyScore = Math.max(0, Math.min(1, originalScore + noise));

      noisyTags[category][tag] = {
        score: noisyScore,
        confidence: tags[category][tag].confidence * 0.95  // 略降信心度
      };
    });
  });

  return noisyTags;
}
```

#### 最小權限原則

```javascript
// 廣告主只能訪問必要的標籤
function minimizeTagExposure(requestedTags, campaign) {
  const necessaryTags = determinessaryTags(campaign.targeting);

  // 只返回必要的標籤
  const exposedTags = filterTags(requestedTags, necessaryTags);

  // 記錄審計
  logTagExposure({
    campaign: campaign.id,
    requested: Object.keys(requestedTags).length,
    exposed: Object.keys(exposedTags).length,
    reduction: `${((1 - Object.keys(exposedTags).length / Object.keys(requestedTags).length) * 100).toFixed(0)}%`
  });

  return exposedTags;
}
```

---

## 🚀 實作計劃

### Phase 1: MVP Foundation (Week 1-2)

**目標**: 基於現有數據生成第一版可用的 System Prompt

#### Week 1: Data Integration
- [x] DayFlow intelligence (已完成)
- [x] Deep Persona Profile (已完成)
- [ ] 設計 prompt-generator.js 架構
- [ ] 創建基礎模板 (core-identity, working-style)
- [ ] 生成第一版 ChatGPT/Claude/Gemini prompts

**Deliverable**:
- 3 個可直接複製貼上的 System Prompt 文件
- 用戶測試反饋表單

#### Week 2: Gmail Integration
- [ ] 開發 gmail-collector.js (使用現有 MCP Gmail server)
- [ ] 分析溝通風格 (回應速度、郵件長度、用語)
- [ ] 分析關係網絡 (核心聯絡人、互動頻率)
- [ ] 整合 Gmail 洞察到 Extended Context
- [ ] 生成 v0.2 Prompt

**Deliverable**:
- Communication Module 完整實作
- v0.2 System Prompt (包含溝通風格)

### Phase 2: Multi-Source Enhancement (Week 3-4)

#### Week 3: Calendar Integration
- [ ] 開發 calendar-collector.js (使用現有 Google Calendar MCP)
- [ ] 分析會議模式、時間區塊
- [ ] 識別高協作/獨立工作時段
- [ ] 生成時間管理建議

#### Week 4: Social Media Integration
- [ ] Twitter/X data collection (如果有 API access)
- [ ] 分析興趣話題、內容偏好
- [ ] 提取社交風格和表達模式
- [ ] 生成 Interest & Social Module

**Deliverable**:
- 完整的 4 源數據整合
- v0.3 System Prompt (完整版)

### Phase 3: Product Polish (Week 5-6)

#### Week 5: User Experience
- [ ] 創建 CLI 工具 (一鍵生成 prompt)
- [ ] 版本管理系統 (追蹤 Persona 變化)
- [ ] Diff 工具 (比較不同時期的 Persona)
- [ ] 導出功能 (markdown, JSON, API)

#### Week 6: Automation & Distribution
- [ ] LaunchAgent 自動更新 (每週)
- [ ] Slack 命令 (/context-update)
- [ ] API endpoint (供其他應用調用)
- [ ] 文檔完善

**Deliverable**:
- 完整的 CLI 工具
- 自動化更新系統
- 用戶手冊

---

## 🎁 產品化路徑

### Stage 1: Personal Tool + MVP Monetization (Month 1-2)

**核心功能**：
- ✅ 本地運行 System Prompt 生成
- ✅ 標籤資產生成
- 🆕 簡單的資產儀表板（查看資產價值）
- 🆕 同意管理 CLI

**變現**: 無（專注驗證）

**用戶**: 自己 + 5-10 個 beta 用戶

**目標**:
- 驗證 System Prompt 有效性
- 驗證標籤資產概念
- 收集用戶反饋

---

### Stage 2: Power User Tool + PoC Marketplace (Month 3-4)

**核心功能**：
- Chrome Extension (一鍵注入 prompt)
- 支援 ChatGPT, Claude, Gemini, Poe
- 自動更新機制
- 🆕 基礎 Consent Management UI
- 🆕 PoC Data Marketplace (限量測試)

**變現 PoC**：
- 邀請 2-3 個 SaaS 廣告主測試
- 用戶可獲得 $5-15/月收益
- 平台手續費 20%

**用戶**: 技術愛好者、PKM 用戶 (100-500人)

**目標**:
- 驗證變現可行性
- 優化同意流程
- 建立廣告主關係

---

### Stage 3: SaaS Product + Full Marketplace (Month 5-8)

**核心功能**：
- Web Dashboard (完整 UI)
- OAuth 安全連接數據源
- 🆕 Anonymous Data Marketplace (正式上線)
- 🆕 Consent-Based Service Enhancement
- AI Prompt Marketplace (分享/購買 Persona 模板)
- 團隊版 (公司 Persona)

**變現模式**：
```
收入來源:
1. 廣告主 Data Marketplace 費用
   - 用戶收益: $10-50/月
   - 平台手續費: 20%
   - 平台月收入 = (用戶數 × 平均收益 × 0.20)

2. 服務商整合費用
   - 服務商支付 API 訪問費
   - 用戶獲得服務折扣

3. Premium 功能訂閱 (可選)
   - Basic: 免費 (含變現功能)
   - Pro: $5/月 (更多數據源、更高收益分成)
   - Team: $20/月/用戶
```

**用戶**: 知識工作者、創業者、管理者 (5K-50K)

**商業目標**:
- 建立雙邊市場（用戶 vs 廣告主）
- 平台收入 > $50K/月
- 用戶平均收益 $15-30/月

---

### Stage 4: Platform + Open Data Alliance (Month 9-12)

**核心功能**：
- API for developers
- Integrations (Notion, Obsidian, Roam, Linear...)
- 🆕 OpenUserTags Standard (開源標準)
- 🆕 Data Alliance Ecosystem
- AI Agent Ecosystem (自動選擇最佳 AI 工具)
- Enterprise solutions

**變現模式**：
```
收入來源:
1. 核心 Marketplace (持續)
2. Enterprise API ($1K-10K/月)
3. Alliance Partner Fees (服務商加盟費)
4. Data Licensing (B2B 數據洞察)
```

**戰略目標**：
- 成為用戶數據資產的標準協議
- 建立 Privacy-First Advertising 新範式
- 與 Google/Facebook 競爭的另一種選擇

**用戶**:
- 個人用戶: 100K+
- 企業客戶: 500+
- 生態夥伴: 50+

---

### Stage 5: Data Economy Revolution (Year 2+)

**願景**：重新定義數據經濟

```
傳統模式:
用戶 → 平台收集 → 平台獲利 → 用戶被剝削

新模式:
用戶 → 自己擁有資產 → 用戶獲益 → 平台協助變現
```

**生態系統**：
- Context Engine 作為基礎設施
- 標籤標準被廣泛採用
- 用戶真正擁有自己的數據資產
- 形成新的 Privacy-First Data Economy

**影響**：
- 用戶集體年收益 > $100M
- 打破 Google/Facebook 壟斷
- 建立新的數據倫理標準
- AI 時代的用戶主權運動

---

### 各階段對比

| 階段 | 時間 | 用戶規模 | 核心價值 | 變現模式 | 平台月收入 |
|-----|------|---------|---------|---------|-----------|
| **Stage 1** | M1-2 | 10 | System Prompt | 無 | $0 |
| **Stage 2** | M3-4 | 500 | Prompt + PoC | PoC 測試 | $1K |
| **Stage 3** | M5-8 | 50K | 完整 Marketplace | 雙邊市場 | $50K-100K |
| **Stage 4** | M9-12 | 100K+ | Platform + Alliance | 多元化 | $200K-500K |
| **Stage 5** | Y2+ | 1M+ | Data Economy | 生態系統 | $1M+ |

---

### 關鍵里程碑

**M2 - MVP Launch**:
- [ ] System Prompt v1.0 發布
- [ ] 10 個 beta 用戶測試
- [ ] 標籤資產生成驗證

**M4 - Marketplace PoC**:
- [ ] 2-3 個廣告主合作
- [ ] 100 個用戶參與測試
- [ ] 首位用戶收益 > $10

**M6 - Product-Market Fit**:
- [ ] 1000 個活躍用戶
- [ ] 用戶平均收益 > $15/月
- [ ] NPS > 50

**M12 - Platform Launch**:
- [ ] 50K+ 用戶
- [ ] 20+ 生態夥伴
- [ ] 平台月收入 > $200K

**Y2 - Industry Impact**:
- [ ] 100K+ 用戶
- [ ] OpenUserTags 被採用
- [ ] 媒體報導和行業認可

---

## 🔐 隱私與安全

### 設計原則

1. **本地優先**: 所有分析在本地進行
2. **用戶控制**: 明確同意每個數據源
3. **透明化**: 清楚顯示使用哪些數據
4. **可刪除**: 隨時停用/刪除數據

### 數據處理流程

```
Raw Data (本地)
    ↓
Analysis (本地)
    ↓
Insights (本地儲存)
    ↓
Prompt (用戶決定是否分享)
    ↓
AI Tool (用戶手動複製 or API 加密傳輸)
```

### 安全措施

- 敏感資訊自動過濾 (email addresses, phone numbers)
- 加密儲存 (如需雲端同步)
- 無追蹤、無遙測
- 開源核心引擎

---

## 📊 成功指標

### 定性指標
- [ ] AI 回應更符合個人風格
- [ ] 減少需要澄清/重新解釋的次數
- [ ] 建議更可行、更貼近實際情況
- [ ] 感覺 AI "更懂我"

### 定量指標
- [ ] Prompt 使用頻率
- [ ] 對話輪數減少 (更快達成目標)
- [ ] 採納建議的比例提高
- [ ] NPS (Net Promoter Score)

### A/B 測試
- 使用 Context Prompt vs. 不使用
- 比較回應質量、準確性、相關性

---

## 🤔 待解決的問題

### 技術挑戰
1. **Prompt 長度優化**: 如何在有限 token 內最大化資訊?
2. **動態更新**: 如何平衡即時性和穩定性?
3. **多 AI 適配**: 不同 AI 對 System Prompt 的理解差異?

### 產品挑戰
1. **效果驗證**: 如何量化"更個人化"?
2. **用戶教育**: 如何讓用戶理解價值?
3. **隱私顧慮**: 如何建立信任?

### 商業挑戰
1. **定價模式**: 免費 vs. 訂閱 vs. 一次性付費?
2. **市場定位**: vs. ChatGPT Custom Instructions?
3. **競爭優勢**: 多源數據整合 + 持續更新

---

## 📚 相關資源

### 現有系統
- DayFlow Intelligence: `/Users/lman/dayflow-intelligence.js`
- Deep Persona: `~/Dropbox/PKM-Vault/0-Inbox/My-Deep-Persona-Profile.md`
- Iris System: `/Users/lman/iris-system/`

### API & Tools
- Gmail MCP: `mcp__gmail__*`
- Google Calendar MCP: `mcp__google-calendar__*`
- Gemini MCP: `mcp__gemini__*`

### 參考文獻
- ChatGPT Custom Instructions
- Claude Projects
- Prompt Engineering Guide
- Personal Knowledge Management Systems

---

## ✅ Next Steps

### 立即行動 (本週)
1. [ ] 生成 v0.1 System Prompt (基於現有 DayFlow + Persona)
2. [ ] 在 ChatGPT/Claude/Gemini 測試
3. [ ] 收集使用反饋
4. [ ] 確定最有價值的 Module

### 短期目標 (本月)
1. [ ] 設置 context-engine 目錄結構
2. [ ] 開發 prompt-generator.js
3. [ ] Gmail collector 實作
4. [ ] v0.2 發布

### 中期目標 (下季)
1. [ ] 完整 4 源整合
2. [ ] CLI 工具完成
3. [ ] Chrome Extension alpha
4. [ ] 5-10 個 beta 用戶測試

---

## 🤖 協作記錄

### Session 1 - 2025-11-02 (v0.1)
**參與者**: Lman (User), Iris (AI Assistant)

**核心決策**:
- 採用分層 System Prompt 架構 (Core, Extended, Specialized, Temporal)
- 優先完成 MVP 驗證價值
- 隱私本地優先，用戶完全控制
- 產品化路徑: Personal → Power User → SaaS → Platform

---

### Session 2 - 2025-11-02 (v0.2) - 革命性升級

**參與者**: Lman (User), Iris (AI Assistant)

**重大洞察** (來自 Lman):
> "在 Google 透過掌握你的瀏覽記錄和 cookies 建立了巨大的帝國的時代，我認為在 AI 時代這些資產用戶更該有掌控權。這些有用的資產怎麼變成具體有用？是否有機會透過建立標籤的方式建構出用戶的數位樣貌但又不揭露了隱私個資，而用戶就有機會在 consent 的前提下透過我們的 context aware engine 提供給這些 service provider 或者揭露給廣告主賺取可能的費用"

**核心決策**:
- 🔥 **範式轉移**: 從 System Prompt 工具 → 用戶資產管理系統
- 🔥 **用戶洞察 = 用戶資產** - 不是平台的資產
- 🔥 **標籤 vs 個資**: 有價值但不洩露隱私的標籤系統
- 🔥 **三種變現模式**:
  1. Anonymous Data Marketplace
  2. Consent-Based Service Enhancement
  3. First-Party Data Alliance
- 🔥 **同意管理系統**: 細粒度控制 + 完全透明
- 🔥 **新商業模式**: 用戶獲益 > 平台獲益

**新增內容**:
- 💎 用戶資產系統
- 🏷️ 標籤資產設計 (6 大類標籤)
- 💰 隱私優先變現模式
- 🔒 同意管理系統
- 📊 資產價值計算模型
- 🎁 更新產品化路徑 (5 階段)

**願景**:
- 打破 Google/Facebook 數據壟斷
- 建立 Privacy-First Data Economy
- AI 時代的用戶主權運動

**下一步**:
- 完成 v0.1 System Prompt (驗證基礎價值)
- 設計標籤生成算法
- 原型同意管理介面
- 接觸潛在廣告主/服務商

---

### Session 3 - 2025-11-02 (v0.3) - System Prompt API 變現路徑

**參與者**: Lman (User), Claude (AI Assistant via Happy)

**新發現的變現路徑** (來自 Lman):
> "撇開廣告，光 system prompt 這部份，面向的就有可能是一些 vertical market 的 agent 例如 Gamma AI 這一類做簡報或者類似服務的業者，因為他們不太可能一下子就理解用戶，但在我的假想中，他們可以透過對用戶的 context aware engine 來串接獲得用戶授權後就有機會一次性或者連續性的得到最新的用戶 insight 或者是相關的 system prompt"

**核心決策**:
- 💡 **新變現模式**: System Prompt as a Service (SPaaS)
- 🎯 **目標客戶**: Gamma AI, Notion, Linear, Superhuman 等 vertical SaaS
- 💰 **定價**: $1-5 per active user/month
- 🚀 **優勢**:
  - 更快變現（1-3 個月 vs 6-12 個月）
  - 更低用戶門檻（1K-10K vs 100K+）
  - B2B 穩定收入
  - 獨立於 IrisGo GTM 進度

**新增內容**:
- 💼 B2B API 變現完整設計
- 🎯 4 個 vertical app 詳細 use cases (Gamma, Notion, Linear, Superhuman)
- 📊 ROI 計算 (Gamma case study: 100% ROI)
- 🔗 API 設計 (認證、響應格式、webhook)
- 💵 兩種定價模型 (per-user vs revenue share)
- 🗺️ GTM 策略 (Pilot → Paid Beta → Platform)
- 🛠️ 技術路線圖 (MVP → Enhanced → Scale)
- ⚖️ 與廣告模式對比分析

**戰略意義**:
- **短期策略**: API 模式優先（快速驗證商業模式）
- **中期策略**: API + 廣告並行發展
- **長期策略**: 雙引擎驅動（B2B API + B2C Marketplace）

**預期收入**:
- M6: $30K MRR (5 付費客戶)
- M12: $400K MRR (20+ 客戶, 200K 用戶)
- Y2: $1M+ MRR (平台規模化)

---

*🤖 Generated by Iris AI Butler System*
*Powered by Claude Code via [Happy Engineering](https://happy.engineering)*

**Last Updated**: 2025-11-02 21:30
**Version**: v0.3 - System Prompt API & Dual Monetization Strategy
