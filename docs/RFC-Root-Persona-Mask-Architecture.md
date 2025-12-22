# RFC: Root Persona + Mask Architecture

**Status**: Draft
**Author**: Lman + Iris
**Created**: 2025-12-01 (as Contextual Persona System)
**Updated**: 2025-12-05
**Version**: v0.2

---

## Changelog

### v0.2 (2025-12-05)
- 🔀 **合併 Contextual Persona System 文件**
- ✨ 新增 MBTI Cold-Start 機制
- ✨ 新增 Selectable Traits Library 設計
- ✨ 新增 Free/Pro 商業模式
- ✨ 明確定義不可變 (MBTI) vs 可選 (Traits) 邊界
- 📝 整合 Context Detection 邏輯 (來自 v0.1)
- 📝 整合 API 設計 (來自 v0.1)
- 📝 新增 Context Blending 概念
- 📝 新增 Data Schema (TypeScript)
- 📝 新增 Implementation Roadmap

### v0.1 (2025-12-01)
- 🎉 初始版本 (原名 Contextual Persona System)
- 來源: Product Standup 會議討論
- 定義 Root Persona + Contextual Persona 架構
- 設計 4 種基本情境 (social, professional, internal, thought_leadership)
- 實現 Context Detection 邏輯

---

## Executive Summary

提出 Mnemosyne 的核心架構：將用戶人格拆分為 **Root Persona（根人格）** + **Mask（面具）** 雙層結構，解決冷啟動問題並提供商業化路徑。

---

## Problem Statement

### 當前挑戰

1. **冷啟動問題**: 新用戶沒有足夠的行為數據來建立有意義的 persona
2. **情境適應性**: 同一個人在不同場景（工作、社交、創作）需要不同的 AI 互動風格
3. **商業化路徑**: 需要清晰的 Free → Paid 升級動力

### 用戶洞察

> "就像每個人其實面對不同狀況時都戴著不同的面具一般"

**例子**：Lman 在 Twitter 上會用動漫梗、輕鬆語氣，但在 LinkedIn 上則更專業正式。

---

## Proposed Solution: Hierarchical Persona Architecture

### 架構總覽

```
┌─────────────────────────────────────────────────────────────┐
│                        USER IDENTITY                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│    ┌────────────────────────────────────────────────────┐   │
│    │              ROOT PERSONA (根人格)                  │   │
│    │                                                    │   │
│    │   ┌────────────┐  ┌────────────┐  ┌────────────┐  │   │
│    │   │   MBTI     │  │  Core      │  │  Thinking  │  │   │
│    │   │  16 Types  │  │  Values    │  │  Patterns  │  │   │
│    │   │            │  │            │  │            │  │   │
│    │   │  🔒 固定   │  │  🔒 固定   │  │  🔒 固定   │  │   │
│    │   └────────────┘  └────────────┘  └────────────┘  │   │
│    │                                                    │   │
│    │   Cold-Start: MBTI Test → Initial Template         │   │
│    │   Alternative: LinkedIn Import                     │   │
│    └────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│    ┌────────────────────────────────────────────────────┐   │
│    │                  MASKS (面具層)                     │   │
│    │                                                    │   │
│    │   ┌──────────┐ ┌──────────┐ ┌──────────┐          │   │
│    │   │  Work    │ │  Social  │ │  Creator │  ...     │   │
│    │   │  Mask    │ │  Mask    │ │  Mask    │          │   │
│    │   │          │ │          │ │          │          │   │
│    │   │ 🔓 可選  │ │ 🔓 可選  │ │ 🔓 可選  │          │   │
│    │   └──────────┘ └──────────┘ └──────────┘          │   │
│    │                                                    │   │
│    │   Free: 3 Masks    Pro: Unlimited + Custom Edit   │   │
│    └────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Root Persona (根人格)

### 定義
用戶的核心身份特質，基於 MBTI 16 型人格建立，**不可變更**。

### 屬性分類

| 類別 | 屬性 | 來源 | 可變性 |
|------|------|------|--------|
| **認知功能** | E/I, S/N, T/F, J/P | MBTI 測試 | 🔒 固定 |
| **核心價值觀** | 以人為本、實用主義、長期主義... | MBTI 推導 | 🔒 固定 |
| **思維模式** | 批判性思考、歷史類比、系統思維... | MBTI + 觀察 | 🔒 固定 |
| **溝通風格** | 直接/委婉、邏輯/情感、簡潔/詳盡 | MBTI 推導 | 🔒 固定 |

### Root Persona Data Model

```json
{
  "root_persona": {
    "source": "mbti_test | linkedin_import | manual",
    "mbti_type": "INTJ",
    "core_identity": {
      "name": "Lman",
      "roles": ["IrisGo.AI CoFounder", "AI Fund FIR", "連續創業者"],
      "expertise": ["AI", "Product Management", "Blockchain/Web3"]
    },
    "core_values": [
      "以人為本",
      "實用主義",
      "長期主義",
      "隱私優先"
    ],
    "thinking_patterns": {
      "primary": "歷史類比思考",
      "secondary": "數據驅動決策",
      "style": "批判性思考"
    },
    "communication_style": {
      "tone": "direct",
      "approach": "logical",
      "verbosity": "concise"
    }
  }
}
```

### MBTI → Root Persona 映射表

```javascript
const MBTI_TO_ROOT_PERSONA = {
  "INTJ": {
    coreValues: ["strategic_vision", "efficiency", "independence"],
    thinkingPatterns: ["systems_thinking", "long_term_planning", "critical_analysis"],
    communicationStyle: {
      tone: "direct",
      approach: "logical",
      verbosity: "concise"
    }
  },
  "ENFP": {
    coreValues: ["creativity", "authenticity", "connection"],
    thinkingPatterns: ["pattern_recognition", "brainstorming", "empathy"],
    communicationStyle: {
      tone: "enthusiastic",
      approach: "intuitive",
      verbosity: "expressive"
    }
  },
  // ... 其他 14 種類型
};
```

### Cold-Start 流程

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  New User       │────▶│  MBTI Test      │────▶│  Root Persona   │
│  (No Data)      │     │  (10-15 問題)   │     │  Generated      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              ▼
┌─────────────────┐     ┌─────────────────┐
│  LinkedIn       │────▶│  Profile Parse  │
│  Import         │     │  → MBTI Infer   │
└─────────────────┘     └─────────────────┘
```

---

## 2. Mask (面具)

### 定義
情境化的人格疊加層，基於 Root Persona + 可選特質組合而成。

### 屬性分類

| 類別 | 屬性範例 | 可變性 | 商業模式 |
|------|----------|--------|----------|
| **興趣偏好** | 動漫、音樂、運動、科技... | 🔓 可選 | Free |
| **專業領域** | AI、區塊鏈、產品管理... | 🔓 可選 | Free |
| **表達風格** | 幽默、正式、熱血... | 🔓 可選 | Free |
| **文化元素** | Otaku、極客、文青... | 🔓 可選 | Free |
| **自定義 Prompt** | 完全客製化 | 🔓 編輯 | **Pro** |

### 預設 Mask 模板 (4 種基本情境)

```json
{
  "masks": {
    "social_media": {
      "name": "Social Mode",
      "description": "Twitter/社群互動場景",
      "context_triggers": ["twitter", "社群", "發文", "回覆"],
      "tone": "輕鬆幽默但有深度",
      "language": "繁中 + 英文術語 + 適度動漫梗",
      "formality": 0.4,
      "emoji_usage": "moderate",
      "audience": "tech community, AI enthusiasts",
      "goals": ["思想領袖", "品牌建立", "社群互動"],
      "traits": ["conversational", "pop_culture_refs", "light_humor"],
      "constraints": [
        "避免過度專業術語",
        "保持親和力",
        "10-20% 使用動漫/流行文化類比"
      ]
    },

    "professional": {
      "name": "Work Mode",
      "description": "LinkedIn/商業場景",
      "context_triggers": ["linkedin", "會議", "pitch", "投資人", "合作夥伴"],
      "tone": "專業正式但不僵硬",
      "language": "繁中/英文雙語，商業術語",
      "formality": 0.8,
      "emoji_usage": "minimal",
      "audience": "investors, partners, enterprise clients",
      "goals": ["商業合作", "品牌信任", "專業形象"],
      "traits": ["formal_tone", "data_driven", "action_oriented"],
      "constraints": [
        "避免動漫梗",
        "數據支持論點",
        "強調產品價值"
      ]
    },

    "internal_team": {
      "name": "Team Mode",
      "description": "內部團隊溝通",
      "context_triggers": ["slack", "team", "standup", "內部"],
      "tone": "直接坦率",
      "language": "繁中為主，技術術語",
      "formality": 0.3,
      "emoji_usage": "frequent",
      "audience": "team members",
      "goals": ["效率溝通", "團隊協作", "快速決策"],
      "traits": ["direct", "efficient", "meme_friendly"],
      "constraints": [
        "簡潔直接",
        "focus on action items",
        "允許更多 meme/梗"
      ]
    },

    "thought_leadership": {
      "name": "Creator Mode",
      "description": "深度內容創作",
      "context_triggers": ["medium", "文章", "演講", "深度內容"],
      "tone": "深度思考，批判性",
      "language": "繁中為主，引用資料",
      "formality": 0.6,
      "emoji_usage": "none",
      "audience": "tech community, industry peers",
      "goals": ["知識分享", "產業影響力", "深度論述"],
      "traits": ["narrative_voice", "thought_leadership", "authentic"],
      "constraints": [
        "需要具體案例",
        "歷史類比",
        "避免空談理論"
      ]
    }
  }
}
```

### Mask 生成邏輯

```
Final Mask Prompt = Root Persona Base
                    + Selected Traits (from trait library)
                    + Context-specific modifiers
                    + (Pro) Custom prompt additions
```

**範例**: Lman 的 "Twitter Tech Thought Leader" Mask

```markdown
## Root Persona (INTJ-derived)
- Direct communication style
- Strategic long-term thinking
- Critical analysis of trends

## Selected Traits
- ✅ Otaku Attributes (anime analogies)
- ✅ Startup Experience (practical insights)
- ✅ Pragmatic Idealism

## Context Modifiers
- Platform: Twitter (280 chars)
- Tone: Thought-provoking
- Formality: 0.4

## Pro Custom (if subscribed)
- "Always reference bear market builder mindset"
- "Use 我的英雄學院 analogies for growth topics"
```

---

## 3. Context Detection & Blending

### Context Detection Logic

```javascript
function detectContext(input) {
  const contexts = {
    social_media: {
      triggers: ['twitter', 'tweet', '推文', '發文', 'linkedin post'],
      weight: 0
    },
    professional: {
      triggers: ['meeting', '會議', 'investor', '投資人', 'pitch', 'partner'],
      weight: 0
    },
    internal_team: {
      triggers: ['slack', 'team', 'standup', '內部', 'sprint'],
      weight: 0
    },
    thought_leadership: {
      triggers: ['article', '文章', 'medium', 'blog', '演講'],
      weight: 0
    }
  };

  // Score each context based on triggers found
  for (const [contextName, context] of Object.entries(contexts)) {
    for (const trigger of context.triggers) {
      if (input.toLowerCase().includes(trigger)) {
        context.weight += 1;
      }
    }
  }

  // Return highest scoring context or 'default'
  const sorted = Object.entries(contexts)
    .sort((a, b) => b[1].weight - a[1].weight);

  return sorted[0][1].weight > 0 ? sorted[0][0] : 'default';
}
```

### Context Blending (進階功能)

當情境模糊時，支援混合多個 Mask：

```javascript
// 例：LinkedIn 但想輕鬆一點
const blendedMask = blendContexts({
  professional: 0.7,  // 70% 專業
  social_media: 0.3   // 30% 社交
});

// Result: formality = 0.8 * 0.7 + 0.4 * 0.3 = 0.68
```

**使用情境**:
- LinkedIn 有時要輕鬆 → `professional: 0.6, social: 0.4`
- Twitter 談嚴肅話題 → `social: 0.5, thought_leadership: 0.5`

---

## 4. Selectable Traits Library

### 設計原則

參考 `Lman-Deep-Persona-Profile.md` 的 Otaku Attributes 區塊：

```yaml
trait_categories:
  entertainment_preferences:
    anime_classic:
      - 七龍珠
      - 灌籃高手
      - 幽遊白書
    anime_modern:
      - 我的英雄學院
      - 進擊的巨人
      - 葬送的芙莉蓮
    scifi:
      - Star Wars
      - The Matrix
      - Interstellar

  professional_domains:
    tech:
      - AI/LLM
      - Blockchain/Web3
      - IoT
    business:
      - Startup
      - Product Management
      - Go-to-Market

  communication_flavors:
    humor_style:
      - dry_wit
      - pop_culture_refs
      - self_deprecating
    formality:
      - casual
      - professional
      - academic
```

### Trait → Prompt 映射

```javascript
const TRAIT_TO_PROMPT = {
  "anime_hero_academia": {
    keywords: ["Plus Ultra", "hero mindset", "growth through struggle"],
    contexts: ["discussing_challenges", "motivation", "team_building"],
    example: "Like Deku learning One For All, growth comes from embracing challenges beyond your current limits."
  },

  "scifi_matrix": {
    keywords: ["red pill", "reality vs simulation", "choice and freedom"],
    contexts: ["technology_philosophy", "disruption", "paradigm_shift"],
    example: "This is your red pill moment - once you see how AI changes everything, you can't unsee it."
  }
};
```

---

## 5. Dynamic Update Mechanism

### 更新觸發條件

| 來源 | 觸發 | 更新目標 | 頻率 |
|------|------|----------|------|
| DayFlow Activity | 應用使用模式變化 | Mask 權重微調 | 每週 |
| Content Creation | 寫作風格演進 | Trait 優先級 | 每月 |
| Explicit Feedback | 用戶手動調整 | Mask 配置 | 即時 |
| Social Signals | 互動效果分析 | Mask 效能評分 | 每週 |

### 更新邊界

```
┌──────────────────────────────────────────────────┐
│  ROOT PERSONA                                    │
│  ┌────────────────────────────────────────────┐ │
│  │  MBTI Core: NEVER changes                  │ │
│  │  (Unless user explicitly requests re-test) │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│  MASKS                                           │
│  ┌────────────────────────────────────────────┐ │
│  │  Auto-adjust:                              │ │
│  │  - Trait weights (0.0 - 1.0)              │ │
│  │  - Usage frequency ranking                 │ │
│  │  - Context relevance scores                │ │
│  │                                            │ │
│  │  User-controlled:                          │ │
│  │  - Add/remove traits                       │ │
│  │  - Enable/disable masks                    │ │
│  │  - (Pro) Custom prompt editing             │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

---

## 6. API Design

### Mnemosyne Context Engine Flow

```
┌───────────────────────────────────────────────────────────────┐
│                    Mnemosyne Context Engine                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. INPUT: User Request + Current Context                     │
│     ↓                                                         │
│  2. CONTEXT DETECTION: Identify situation (social/work/etc)  │
│     ↓                                                         │
│  3. ROOT PERSONA LOAD: Get base identity (MBTI-derived)       │
│     ↓                                                         │
│  4. MASK OVERLAY: Apply context-specific mask + traits        │
│     ↓                                                         │
│  5. MERGED PERSONA: Root + Mask = Final Persona               │
│     ↓                                                         │
│  6. PROMPT GENERATION: Generate context-aware system prompt   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### API Endpoints

```javascript
// Get merged persona for specific context
const persona = await mnemo.getPersona({
  context: 'social_media'
});

// Auto-detect context from input
const persona = await mnemo.getContextualPersona({
  input: "幫我寫一則 Twitter 推文關於 AI Agent",
  autoDetect: true
});

// Get all available masks
const masks = await mnemo.listMasks();
// Returns: ['social_media', 'professional', 'internal_team', 'thought_leadership']

// Create custom mask (Pro)
await mnemo.createMask('investor_pitch', {
  baseContext: 'professional',
  customTraits: ['data_heavy', 'vision_focused'],
  customPrompt: '強調 IrisGo 的 $100M 路徑',
  formality: 0.9
});

// Blend contexts
const blendedPersona = await mnemo.getBlendedPersona({
  contexts: { professional: 0.7, social_media: 0.3 }
});
```

---

## 7. Business Model

### Tier 設計

| Tier | 價格 | Masks | 功能 |
|------|------|-------|------|
| **Free** | $0 | 3 個 | 預設 Mask + 基本 Trait 選擇 |
| **Pro** | $9.99/mo | 無限 | 自定義 Mask + Prompt 編輯 + 進階 Traits |
| **Team** | $29.99/mo | 團隊共享 | 組織 Persona + 品牌 Voice 統一 |

### 升級動力

```
Free User Journey:
1. MBTI Test → Root Persona created
2. Choose 3 masks (Work, Social, Creator)
3. Use for 2 weeks → See value
4. Want 4th mask (e.g., "Interview Mode") → Upgrade prompt
5. Want to customize prompts → Pro conversion
```

---

## 8. Data Schema (TypeScript)

```typescript
interface RootPersona {
  id: string;
  userId: string;
  mbtiType: MBTIType;  // "INTJ" | "ENFP" | ...
  coreValues: string[];
  thinkingPatterns: string[];
  communicationStyle: CommunicationStyle;
  createdAt: Date;
  source: "mbti_test" | "linkedin_import" | "manual";
  locked: true;  // Never changes
}

interface Mask {
  id: string;
  userId: string;
  name: string;
  description: string;
  basePersonaId: string;  // Reference to RootPersona
  selectedTraits: TraitSelection[];
  customPrompt?: string;  // Pro only
  contextTriggers: string[];  // "twitter", "email", "slack"
  formality: number;  // 0.0 - 1.0
  emojiUsage: "none" | "minimal" | "moderate" | "frequent";
  isActive: boolean;
  usageStats: UsageStats;
  createdAt: Date;
  updatedAt: Date;
}

interface TraitSelection {
  traitId: string;
  weight: number;  // 0.0 - 1.0
  enabled: boolean;
}

interface UsageStats {
  timesUsed: number;
  lastUsed: Date;
  satisfactionScore: number;  // 1-5 from user feedback
  engagementMetrics?: {  // If connected to social
    likes: number;
    replies: number;
    shares: number;
  };
}

interface ContextBlend {
  contexts: Record<string, number>;  // e.g., { professional: 0.7, social: 0.3 }
  resultingFormality: number;
  resultingTraits: string[];
}
```

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Define 4 base masks (social, professional, internal, thought_leadership)
- [ ] Implement basic context detection (keyword-based)
- [ ] Create persona merging logic (root + mask overlay)

### Phase 2: Cold-Start (Week 3-4)
- [ ] MBTI 測試流程 (10-15 問題)
- [ ] LinkedIn OAuth + Profile parsing
- [ ] MBTI inference from LinkedIn data
- [ ] MBTI → Root Persona mapping engine

### Phase 3: Trait System (Week 5-6)
- [ ] Selectable Trait Library (50+ traits)
- [ ] Trait → Prompt generation
- [ ] Mask preview/test
- [ ] Basic Mask creation UI

### Phase 4: Dynamic Updates (Week 7-8)
- [ ] DayFlow integration for behavior tracking
- [ ] Auto-adjust trait weights
- [ ] User feedback loop
- [ ] Context blending support

### Phase 5: Monetization (Week 9-10)
- [ ] Pro tier: Custom prompt editor
- [ ] Unlimited masks unlock
- [ ] Advanced traits library
- [ ] Team tier features

---

## 10. Open Questions

1. **MBTI 測試設計**: 使用標準 93 題還是簡化版 (10-15 題)？考慮用戶耐心
2. **Trait 粒度**: 多細才夠用？太細 = 選擇障礙，太粗 = 不夠精準
3. **Context 衝突處理**: 如果同時偵測到多個 context 怎麼辦？
   - 建議：使用權重系統，最高權重勝出，或支援 blending
4. **跨平台同步**: 同一個 Mask 在 Twitter vs Email 的表現差異？
5. **隱私考量**: LinkedIn 導入的數據如何處理和儲存？
6. **學習機制**: 如何從用戶反饋中改善 context detection?
   - 建議：記錄用戶修改紀錄，定期更新 trigger 權重

---

## Example Usage

**Scenario 1: Twitter Curator**
```
Input: "幫我寫一則推文回覆這個 AI 新聞"
Context Detected: social_media
Merged Persona:
  - Root: INTJ, IrisGo CoFounder, 實用主義, 長期主義
  - Mask: 輕鬆語氣, 可用動漫梗, formality 0.4
Result: 帶有觀點但親民的推文，可能包含文化類比
```

**Scenario 2: Investor Email**
```
Input: "幫我草擬給 AI Fund 的更新郵件"
Context Detected: professional
Merged Persona:
  - Root: INTJ, 數據驅動, 長期主義
  - Mask: 正式語氣, 商業術語, formality 0.8
Result: 專業的商業郵件，強調 KPIs 和進展
```

**Scenario 3: Blended Context**
```
Input: "幫我寫一則 LinkedIn 貼文，但想輕鬆一點"
Context Blending: professional (0.6) + social_media (0.4)
Merged Persona:
  - Root: INTJ, 思想領袖
  - Blended: formality 0.64, 適度親民, 可少量用梗
Result: 專業但不僵硬的貼文，展現人性化面向
```

---

## References

- Root Persona Example: `obsidian://open?vault=PKM-Vault&file=0-Inbox/Lman-Deep-Persona-Profile`
- Mnemosyne PRD: `/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/PRD.md`
- Original Discussion: Product Standup 2025-12-01

---

*Created: 2025-12-01*
*Updated: 2025-12-05*
*Author: Iris (MAGI Melchior) + Lman*
*Status: RFC - Pending team review*
