# 🔐 Context Engine - Privacy Architecture PRD

> **文檔類型**: Product Requirements Document (Technical Spec)
> **目標讀者**: 工程團隊
> **狀態**: Draft - Discussion Phase
> **創建日期**: 2025-11-02
> **最後更新**: 2025-11-02
> **版本**: v0.1

---

## 📋 目錄

- [背景與目標](#背景與目標)
- [核心架構決策](#核心架構決策)
- [技術方案：混合匹配模式](#技術方案混合匹配模式)
- [開放技術問題](#開放技術問題)
- [實作優先級](#實作優先級)
- [參考資料](#參考資料)

---

## 🎯 背景與目標

### 產品願景

Context Engine 是 IrisGo.AI 的核心差異化功能，旨在：
1. **個人化 AI 體驗**: 基於用戶行為數據生成 System Prompt
2. **用戶數據資產化**: 讓用戶擁有並能從自己的數據獲益
3. **隱私優先變現**: 在保護隱私前提下實現數據市場化

### 核心挑戰

**挑戰 1: 規模化時間線不確定**
- IrisGo.AI 通過 OEM Pre-installation 目標達到 100M+ 用戶
- 但 GTM 速度存在不確定性（可能需要 2-3 年）
- Context Engine 需要在小規模時也能展示價值

**挑戰 2: 隱私與價值的平衡**
- 標籤越精準 → 廣告價值越高 → 但隱私風險越大
- 需要在不同用戶規模下動態調整隱私策略

**挑戰 3: 技術複雜度**
- 本地處理 vs 服務器效率
- K-Anonymity 保證 vs 標籤精準度
- 去中心化匹配 vs 實時競價

### 技術目標

本 PRD 專注於：
1. **定義混合匹配架構** - 平衡隱私和效率
2. **明確分層標籤策略** - Tier 1/2/3 的具體設計
3. **識別關鍵技術挑戰** - 需要工程團隊解決的問題
4. **建立實作路徑** - 從 MVP 到 Production 的演進

---

## ✅ 核心架構決策

### 決策 1: 採用混合匹配模式 (Hybrid Matching)

**日期**: 2025-11-02
**決策者**: Product Team
**理由**: 平衡隱私保護（本地處理）和系統效率（服務器匹配）

**架構概覽**:
```
┌─────────────────────────────────────┐
│     Context Engine Client           │
│        (用戶設備端)                  │
├─────────────────────────────────────┤
│ Tier 1 Tags (粗標籤)               │
│ → 上傳到服務器進行初步匹配          │
│                                      │
│ Tier 2 Tags (中等標籤)             │
│ → 混合策略（條件上傳或本地）        │
│                                      │
│ Tier 3 Tags (細標籤)               │
│ → 完全本地，絕不上傳                │
└─────────────────────────────────────┘
        ↓ Tier 1          ↓ Tier 2-3
   ┌──────────┐      ┌──────────────┐
   │ Server   │      │ Local        │
   │ Matcher  │      │ Matcher      │
   └──────────┘      └──────────────┘
```

### 決策 2: 每兩週更新標籤

**日期**: 2025-11-02
**決策者**: Product Team
**理由**: 人的行為模式不會快速變化，兩週是合理的平衡點

**更新策略**:
- **Regular Update**: 每兩週完整重新分析（週日和週三凌晨3點）
- **Rapid Decay**: 購買意圖等快速變化標籤每日衰減
- **Anomaly Detection**: 檢測行為劇變時觸發提前更新

---

## 🏗️ 技術方案：混合匹配模式

### 1. 分層標籤系統 (Tiered Tags)

#### Tier 1: 粗粒度標籤（服務器匹配）

**特性**:
- 單個標籤覆蓋 >100K 用戶
- 即使組合也有 >10K 用戶
- 低識別風險

**標籤示例**:
```javascript
tier1Tags = {
  // 基礎人口統計
  "region": "asia_pacific",
  "timezone": "UTC+8",
  "language": ["english", "chinese"],

  // 大類興趣
  "interest_category": ["technology", "business"],

  // 職業大類
  "professional_category": "knowledge_worker",

  // 設備類型
  "device_type": "desktop_windows"
}
```

**技術實現**:
```javascript
// 上傳到服務器
POST /api/v1/tags/tier1
{
  "user_id": "anonymous_uuid_550e8400",
  "tags": tier1Tags,
  "timestamp": "2025-11-02T03:00:00Z"
}

// 服務器進行粗匹配
const candidateAds = server.coarseMatch(tier1Tags);
// 返回：可能相關的 50-100 個廣告活動
```

#### Tier 2: 中等粒度標籤（混合策略）

**特性**:
- 單個標籤覆蓋 10K-100K 用戶
- 組合後可能縮小到 1K-10K 用戶
- 中等識別風險，需要用戶明確同意

**標籤示例**:
```javascript
tier2Tags = {
  // 具體興趣
  "interests": {
    "AI_automation": { score: 0.95, confidence: 0.90 },
    "productivity_tools": { score: 0.82, confidence: 0.88 }
  },

  // 專業技能
  "expertise": {
    "programming": { level: "expert", languages: ["javascript"] },
    "product_management": { level: "advanced" }
  },

  // 內容偏好
  "content_preferences": {
    "format": "long_form_technical",
    "tone": "practical_no_fluff"
  }
}
```

**混合策略選項**:

**選項 A: 條件上傳**
```javascript
// 默認本地存儲
// 只有當用戶同意特定廣告活動時，臨時上傳部分 Tier 2
if (user.hasConsent(campaign.id)) {
  const relevantTags = selectRelevantTags(tier2Tags, campaign.targeting);
  temporarilyUpload(campaign.id, relevantTags);
}
```

**選項 B: 兩階段匹配**
```javascript
// 階段 1: 服務器用 Tier 1 粗匹配，返回候選廣告
const candidateAds = await server.coarseMatch(tier1Tags);

// 階段 2: 本地用 Tier 2 精準匹配
const matchedAds = local.fineMatch(tier2Tags, candidateAds);
const topAd = local.selectByCPM(matchedAds);
```

**選項 C: 聚合上傳**
```javascript
// 不上傳個人標籤，只上傳統計聚合
// 用戶被分配到匿名群組
server.receives({
  cluster_id: "cluster_abc_1234",  // 包含 >1000 用戶
  aggregated_tags: {
    "AI_automation": { prevalence: 0.65 },  // 65% 用戶有此標籤
    "productivity_tools": { prevalence: 0.82 }
  }
})
```

#### Tier 3: 細粒度標籤（完全本地）

**特性**:
- 高度特定，可能識別個人
- 組合後範圍縮小到 <1K 用戶
- 高識別風險，絕不上傳

**標籤示例**:
```javascript
tier3Tags = {
  // 購買意圖
  "buying_intent": {
    "notion": {
      level: "very_high",
      consideration_set: ["notion", "linear", "height"],
      decision_timeline: "immediate"
    }
  },

  // 工作模式
  "work_patterns": {
    "peak_hours": "9am-12pm",
    "task_switching": "high_frequency",
    "focus_blocks": "short_intense"
  },

  // 當前項目
  "current_projects": {
    "working_on": "irisgo_ai",
    "tech_stack": ["node", "claude_api"],
    "team_size": "<10"
  }
}
```

**技術實現**:
```javascript
// 完全本地匹配
const localAdDB = await loadLocalAdDatabase();  // 從服務器同步廣告列表
const matchedAds = local.preciseMatch(tier3Tags, localAdDB);

// 本地決策，不回傳標籤內容
const result = {
  matched: true,
  ad_id: "notion_campaign_123",
  cpm: 45,
  // 不包含具體標籤內容
}
```

---

## ❓ 開放技術問題

以下問題需要工程團隊進一步討論和驗證：

### 問題 1: Tier 1/2/3 的分界標準

**問題描述**:
如何自動判斷一個標籤應該屬於哪個 Tier？

**方案 A: 基於統計覆蓋率**
```javascript
function assignTier(tag, userCount) {
  const coverage = countUsersWithTag(tag);

  if (coverage > 100000) return 'tier1';
  if (coverage > 10000) return 'tier2';
  return 'tier3';
}
```

**方案 B: 基於標籤類別**
```javascript
const tierMapping = {
  tier1: ['region', 'timezone', 'language', 'device_type'],
  tier2: ['interests', 'expertise', 'content_preferences'],
  tier3: ['buying_intent', 'work_patterns', 'current_projects']
}
```

**方案 C: 基於識別風險評分**
```javascript
function calculateIdentificationRisk(tag, userProfile) {
  let risk = 0;

  // 計算該標籤與其他標籤組合後的唯一性
  const combinationUniqueness = analyzeUniqueness(tag, userProfile);

  if (combinationUniqueness < 0.001) risk = 'high';  // < 1000 人
  else if (combinationUniqueness < 0.01) risk = 'medium';  // < 10K 人
  else risk = 'low';  // > 10K 人

  return risk;
}
```

**待決策**: 採用哪種方案？或組合使用？

---

### 問題 2: Tier 2 的「混合」具體實現

**問題描述**:
Tier 2 標籤的「混合策略」到底如何運作？

**子問題 2.1: 選擇哪種混合方案**

| 方案 | 優點 | 缺點 | 技術複雜度 |
|------|------|------|-----------|
| **條件上傳** | 靈活，按需上傳 | 需要管理臨時授權 | 中 |
| **兩階段匹配** | 隱私好，效率高 | 本地需要存儲廣告庫 | 中 |
| **聚合上傳** | 完全匿名 | 精準度降低 | 高 |

**子問題 2.2: 條件上傳的授權管理**
```javascript
// 用戶如何授權？
// 選項 A: 每次廣告都詢問
user.requestConsent({
  advertiser: "Notion",
  tags_requested: ["interests.productivity_tools", "expertise.programming"],
  benefit: "$0.04 earning",
  cpm: "$40"
});

// 選項 B: 預先授權類別
user.preAuthorizeTags({
  "interests": true,  // 所有興趣標籤都允許
  "expertise": true,
  "buying_intent": false  // 購買意圖不允許
});
```

**子問題 2.3: 兩階段匹配的廣告庫同步**
```javascript
// 本地廣告庫需要包含什麼？
localAdDatabase = [
  {
    id: "notion_123",
    targeting: {
      tier1: { region: "asia_pacific" },
      tier2: { interests: ["productivity_tools", "PKM"] },
      tier3: { buying_intent: ["notion", "productivity_saas"] }
    },
    cpm: 40,
    expires_at: "2025-12-01"
  },
  // ... 可能有數百個活動
]

// 問題：
// - 更新頻率？每小時？每天？
// - 如何防止用戶篡改 CPM 數據作弊？
// - 廣告庫大小限制？
```

**待決策**:
- 優先實現哪種混合方案？
- 授權流程的 UX 設計？
- 廣告庫同步機制？

---

### 問題 3: 服務器端隱私保護

**問題描述**:
即使只上傳 Tier 1 粗標籤，服務器仍可能通過長期追蹤識別用戶。

**風險分析**:
```javascript
// 服務器可以看到的信息
serverLogs = [
  {
    timestamp: "2025-11-02 09:30",
    uuid: "anonymous_550e8400",
    tier1_tags: ["asia_pacific", "technology", "knowledge_worker"],
    matched_ads: ["notion", "linear", "claude"]
  },
  {
    timestamp: "2025-11-16 09:35",
    uuid: "anonymous_550e8400",  // 同一個 UUID
    tier1_tags: ["asia_pacific", "technology", "knowledge_worker"],
    matched_ads: ["height", "superhuman"]
  },
  // ... 持續追蹤數月
]

// 風險：
// 1. 行為模式可能識別個人（活動時間、興趣變化軌跡）
// 2. 跨平台關聯（如果用戶在多個服務使用同一 UUID）
```

**緩解方案對比**:

**方案 A: 定期輪換 UUID**
```javascript
// 每月更換匿名 ID
monthly_uuid = hash(base_uuid + current_month)

// 優點：服務器無法長期追蹤
// 缺點：
// - 用戶的收益記錄如何保持連續性？
// - 需要本地維護 UUID 映射表
// - 廣告主無法進行頻次控制（同一用戶可能被多次展示）
```

**方案 B: 差分隱私噪音**
```javascript
// 上傳標籤時加入隨機噪音
function uploadWithNoise(tier1Tags, epsilon) {
  return {
    ...tier1Tags,
    interests: tier1Tags.interests.map(tag => ({
      ...tag,
      score: tag.score + laplaceNoise(epsilon)
    }))
  };
}

// 優點：數學上證明的隱私保護
// 缺點：
// - 降低匹配精準度
// - 需要調優 epsilon 參數
// - 用戶體驗可能受影響（收益降低）
```

**方案 C: 延遲批次上傳 (K-Shuffle)**
```javascript
// 不實時上傳，而是批次混淆上傳
class BatchUploader {
  constructor() {
    this.batch = [];
    this.batchSize = 100;
  }

  async queueUpload(userTags) {
    this.batch.push(userTags);

    if (this.batch.length >= this.batchSize) {
      shuffle(this.batch);  // 打亂順序
      await uploadBatch(this.batch);  // 服務器無法區分誰是誰
      this.batch = [];
    }
  }
}

// 優點：服務器無法實時追蹤
// 缺點：
// - 增加延遲（用戶可能需要等待湊齊批次）
// - 實時匹配受影響
// - 批次大小和延遲的權衡
```

**方案 D: 組合方案**
```javascript
// 結合多種技術
const privacyProtection = {
  uuid_rotation: {
    enabled: true,
    period: "monthly",
    keep_earnings_linked: true  // 通過加密映射維護收益連續性
  },

  differential_privacy: {
    enabled: true,
    epsilon: 1.5,  // 調優參數
    apply_to: ["tier1_scores"]  // 只對分數加噪，不對類別
  },

  batch_upload: {
    enabled: false,  // MVP 階段不啟用，避免複雜度
    batch_size: 50
  }
};
```

**待決策**:
- 採用哪種方案？
- 如何驗證隱私保護效果？
- 如何量化隱私 vs 收益的權衡？

---

### 問題 4: 本地匹配的技術挑戰

**問題描述**:
Tier 2-3 本地匹配需要解決多個技術問題。

**子問題 4.1: 本地廣告庫同步**

```javascript
// 需要設計的機制
class LocalAdDatabase {
  async sync() {
    // 從服務器下載廣告活動列表
    const ads = await fetchAdCampaigns();

    // 問題：
    // 1. 下載頻率？實時？每小時？
    // 2. 數據大小？如果有 1000 個活動，每個 5KB = 5MB
    // 3. 增量更新還是全量下載？
    // 4. 網絡失敗如何處理？

    this.store(ads);
  }

  async match(userTags) {
    // 本地匹配邏輯
    const ads = this.loadFromStorage();

    // 問題：
    // - 匹配算法複雜度？O(n) 還是可以優化？
    // - 如何處理複雜的 targeting 邏輯（AND/OR/NOT）？
    // - 如何排序（CPM vs 相關性）？
  }
}
```

**子問題 4.2: 防作弊機制**

```javascript
// 用戶可能的作弊手段
const cheatingVectors = [
  "修改本地廣告庫中的 CPM 值，總是匹配高價廣告",
  "偽造匹配結果，聲稱看了廣告但實際沒有",
  "修改標籤讓自己總是匹配高價值受眾",
  "頻繁重置 UUID 獲取新用戶獎勵"
];

// 緩解方案
const antiCheat = {
  // 廣告庫簽名
  ad_database_signature: {
    server_signs: true,
    client_verifies: true,
    tamper_detection: "cryptographic_hash"
  },

  // 匹配結果驗證
  match_verification: {
    method: "zero_knowledge_proof",  // 證明匹配成功但不透露標籤
    fallback: "server_revalidation"  // 抽樣驗證
  },

  // 行為異常檢測
  anomaly_detection: {
    track: ["match_frequency", "cpm_distribution", "ad_diversity"],
    flag_threshold: "statistical_outlier"
  }
};
```

**子問題 4.3: 性能和電池消耗**

```javascript
// 本地匹配的性能開銷
const performanceMetrics = {
  ad_database_size: "5MB",
  sync_frequency: "hourly",
  match_operation: "every_ad_impression",

  estimated_overhead: {
    cpu: "~50ms per match",
    memory: "~10MB resident",
    battery: "~0.5% per day",
    network: "~5MB download per day"
  }
};

// 優化策略
const optimizations = {
  indexing: "build local index for fast lookup",
  caching: "cache match results for 1 hour",
  lazy_loading: "only load relevant ad subset",
  background_sync: "sync during idle time"
};
```

**待決策**:
- 廣告庫同步頻率和策略？
- 採用哪種防作弊機制？
- 性能開銷是否可接受？
- 如何在低端設備上優化？

---

### 問題 5: 結算和收益證明

**問題描述**:
用戶聲稱「我匹配了廣告」，廣告主如何驗證而不洩露用戶標籤？

**傳統模式（不可行）**:
```javascript
// 服務器知道所有信息
server.knows({
  user_tags: tier3Tags,  // 知道用戶標籤
  ad_targeting: adTargeting,  // 知道廣告需求
  can_verify: true  // 可以驗證匹配
});

// 但這違反隱私原則（Tier 3 不上傳）
```

**零知識證明方案（理論）**:
```javascript
// 用戶生成證明
const proof = generateZKProof({
  statement: "我的標籤滿足這個廣告的 targeting 條件",
  public_input: adTargeting,  // 公開
  private_input: userTags,  // 不透露
  proof: "cryptographic_proof"
});

// 廣告主驗證
const isValid = verifyZKProof(proof, adTargeting);
// 返回 true/false，但不知道用戶的具體標籤

// 問題：
// - ZK-SNARK 實現複雜度高
// - 證明生成和驗證的性能開銷
// - 需要可信設置（Trusted Setup）
```

**簡化方案（實用）**:
```javascript
// 盲簽名 + 抽樣驗證
const simplifiedVerification = {
  step1: "本地匹配後，生成匹配憑證",
  step2: "服務器盲簽名（不知道內容）",
  step3: "用戶提交簽名憑證結算",
  step4: "服務器抽樣驗證（隨機驗證 5% 的匹配）",

  anti_cheat: "大規模作弊會被統計檢測發現"
};

// 示例代碼
class MatchVerification {
  // 用戶端：生成匹配憑證
  async generateMatchCert(userTags, adTargeting, timestamp) {
    const matchData = {
      ad_id: adTargeting.id,
      timestamp: timestamp,
      match_proof: hashTags(userTags)  // 不透露原始標籤
    };

    // 請求服務器盲簽名
    const signature = await server.blindSign(matchData);

    return { matchData, signature };
  }

  // 服務器端：驗證和結算
  async settlePayout(matchCert) {
    // 1. 驗證簽名是服務器發出的
    if (!this.verifySignature(matchCert.signature)) {
      throw new Error("Invalid signature");
    }

    // 2. 檢查是否已結算（防止重複）
    if (this.isAlreadySettled(matchCert)) {
      throw new Error("Already settled");
    }

    // 3. 抽樣驗證（5% 概率）
    if (Math.random() < 0.05) {
      await this.deepVerification(matchCert);
    }

    // 4. 結算
    await this.creditUser(matchCert.user_id, matchCert.earnings);
  }
}
```

**待決策**:
- 採用 ZK 證明還是簡化方案？
- 抽樣驗證的比例？
- 如何處理驗證失敗的情況？
- 是否需要第三方審計？

---

## 🎯 實作優先級

基於 MVP → Production 的演進路徑，建議優先級：

### P0 - MVP 必須（Month 1-2）

**目標**: 驗證核心價值（System Prompt generation），暫不涉及變現

```javascript
mvp_scope = {
  tags: "生成所有 Tier 標籤，但只用於 System Prompt",
  matching: "無需實現，不涉及廣告匹配",
  privacy: "本地處理，不上傳任何標籤",
  update: "手動觸發更新（無自動化）"
};
```

**技術任務**:
- [ ] 實現標籤生成算法（從 DayFlow 數據提取）
- [ ] 定義 Tier 1/2/3 標籤分類規則
- [ ] 實現 System Prompt 生成器
- [ ] 本地存儲標籤（加密）

**不實現**:
- ❌ 服務器匹配
- ❌ 廣告庫同步
- ❌ 結算系統
- ❌ 隱私保護高級特性

---

### P1 - Alpha 階段（Month 3-4）

**目標**: 小規模變現測試（B2B 市場研究），10K 用戶

```javascript
alpha_scope = {
  tags: "Tier 1 標籤上傳，Tier 2-3 本地",
  matching: "實現 Tier 1 服務器匹配（粗匹配）",
  privacy: "基礎 UUID 匿名化",
  monetization: "B2B 聚合洞察（不是個人廣告）"
};
```

**技術任務**:
- [ ] 實現 Tier 1 標籤上傳 API
- [ ] 服務器端粗匹配引擎
- [ ] UUID 生成和管理
- [ ] 聚合統計 API（群體洞察）

**開放問題需決策**:
- Tier 1/2/3 分界標準（問題 1）
- 服務器端隱私保護方案（問題 3 的選項）

---

### P2 - Beta 階段（Month 5-8）

**目標**: 個人變現測試（Data Marketplace），100K 用戶

```javascript
beta_scope = {
  tags: "完整 Tier 1/2/3 系統",
  matching: "混合匹配（Tier 1 服務器 + Tier 2-3 本地）",
  privacy: "差分隱私、UUID 輪換",
  monetization: "個人廣告收益"
};
```

**技術任務**:
- [ ] 實現 Tier 2 混合策略（決策問題 2 的方案）
- [ ] 本地廣告庫同步機制
- [ ] 本地匹配引擎
- [ ] 結算和收益證明系統（問題 5 的方案）
- [ ] 差分隱私實現（問題 3 方案 B）

**開放問題需決策**:
- Tier 2 混合方案選擇（問題 2）
- 本地匹配技術細節（問題 4）
- 結算驗證機制（問題 5）

---

### P3 - Production 階段（Month 9-12）

**目標**: 規模化到 1M+ 用戶，完整功能

```javascript
production_scope = {
  tags: "動態 K-Anonymity 調整",
  matching: "優化的混合引擎",
  privacy: "所有高級隱私特性",
  monetization: "完整 Data Marketplace"
};
```

**技術任務**:
- [ ] K-Anonymity 動態計算和泛化
- [ ] 零知識證明（如果需要）
- [ ] 性能優化（低端設備）
- [ ] 防作弊完整系統
- [ ] 監控和審計系統

---

## 📚 參考資料

### 技術論文
- [Differential Privacy](https://en.wikipedia.org/wiki/Differential_privacy)
- [K-Anonymity in Data Mining](https://en.wikipedia.org/wiki/K-anonymity)
- [Zero-Knowledge Proofs](https://en.wikipedia.org/wiki/Zero-knowledge_proof)
- [Federated Learning (Google AI)](https://ai.google/research/pubs/pub45648)

### 實現參考
- [Google's Privacy Sandbox](https://privacysandbox.com/)
- [Apple's Differential Privacy](https://www.apple.com/privacy/docs/Differential_Privacy_Overview.pdf)
- [Brave Ads (Privacy-First Advertising)](https://brave.com/brave-ads/)

### 相關文檔
- `Context-Aware-AI-Engine-Design.md` - 產品整體設計
- `Context-Engine-VLM-Complete-Solution.md` - VLM 視覺分析方案
- `Context-Engine-Data-Sources-Comprehensive.md` - 數據源詳細說明

---

## 📝 變更記錄

### v0.1 - 2025-11-02
- 初版 PRD
- 定義混合匹配架構
- 識別 5 個核心技術問題
- 制定實作優先級（P0-P3）

---

## 👥 貢獻者

**Product Team**:
- Lman (Co-founder, Product)
- Claude (AI Assistant, Technical Analysis)

**待參與**:
- Engineering Team (技術可行性驗證)
- Security Team (隱私方案審查)
- Legal Team (GDPR/隱私法規合規)

---

## ✅ 下一步行動

### For Product Team:
1. 審查並確認核心架構決策
2. 針對 5 個開放問題做出決策
3. 與 Engineering Team 討論技術可行性

### For Engineering Team:
1. 評估各方案的技術複雜度
2. 提供性能和資源開銷估算
3. 識別額外的技術風險

### For All:
1. 安排技術設計評審會議
2. 建立 POC (Proof of Concept) 驗證關鍵技術
3. 更新 PRD 基於討論結果

---

**文檔狀態**: 🟡 Draft - 等待團隊評審
**下次更新**: 待技術設計會議後

---

*🤖 Generated by Iris AI Butler System*
*Powered by Claude Code via [Happy Engineering](https://happy.engineering)*
*Last Updated: 2025-11-02*
