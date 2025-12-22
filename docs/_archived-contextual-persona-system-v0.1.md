# Contextual Persona System - Design Document

> **來源**: 2025-12-01 Product Standup 會議討論
> **核心概念**: Root Persona + Contextual Persona 分割
> **狀態**: RFC (Request for Comments)

---

## Problem Statement

目前 Mnemosyne 的 Persona Analyzer 生成**單一固定 Persona**，但現實中：

1. 人在不同場合會展現不同「人設」
2. 社群媒體的「我」 vs 工作中的「我」 vs 私人生活的「我」
3. 單一 Persona 無法捕捉這種多面性

**例子**：Lman 在 Twitter 上會用動漫梗、輕鬆語氣，但在 LinkedIn 上則更專業正式。

---

## Proposed Solution: Hierarchical Persona Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ROOT PERSONA                         │
│  (Lman-Deep-Persona-Profile.md)                        │
│                                                         │
│  - Core Identity (不變的核心身份)                        │
│  - Core Values (核心價值觀)                              │
│  - Thinking Patterns (思維模式)                         │
│  - Expertise & Skills (專業能力)                        │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ SOCIAL PERSONA  │ │  WORK PERSONA   │ │ PERSONAL PERSONA│
│                 │ │                 │ │                 │
│ - Twitter 風格   │ │ - LinkedIn 專業  │ │ - 家人朋友互動   │
│ - 動漫梗/輕鬆    │ │ - 正式商業語氣   │ │ - 完全放鬆      │
│ - 思想領袖定位   │ │ - IrisGo CEO    │ │ - 真實自我      │
│ - 繁中+英文術語  │ │ - 產業洞察      │ │ - 生活話題      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Data Model

### 1. Root Persona (基礎 Persona)

```json
{
  "root_persona": {
    "source": "obsidian://open?vault=PKM-Vault&file=0-Inbox/Lman-Deep-Persona-Profile",
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
    }
  }
}
```

### 2. Contextual Personas (情境 Persona)

```json
{
  "contextual_personas": {
    "social_media": {
      "context_triggers": ["twitter", "社群", "發文", "回覆"],
      "tone": "輕鬆幽默但有深度",
      "language": "繁中 + 英文術語 + 適度動漫梗",
      "formality": 0.4,
      "emoji_usage": "moderate",
      "audience": "tech community, AI enthusiasts",
      "goals": ["思想領袖", "品牌建立", "社群互動"],
      "constraints": [
        "避免過度專業術語",
        "保持親和力",
        "10-20% 使用動漫/流行文化類比"
      ]
    },

    "professional": {
      "context_triggers": ["linkedin", "會議", "pitch", "投資人", "合作夥伴"],
      "tone": "專業正式但不僵硬",
      "language": "繁中/英文雙語，商業術語",
      "formality": 0.8,
      "emoji_usage": "minimal",
      "audience": "investors, partners, enterprise clients",
      "goals": ["商業合作", "品牌信任", "專業形象"],
      "constraints": [
        "避免動漫梗",
        "數據支持論點",
        "強調 IrisGo 產品價值"
      ]
    },

    "internal_team": {
      "context_triggers": ["slack", "team", "standup", "內部"],
      "tone": "直接坦率",
      "language": "繁中為主，技術術語",
      "formality": 0.3,
      "emoji_usage": "frequent",
      "audience": "IrisGo team members",
      "goals": ["效率溝通", "團隊協作", "快速決策"],
      "constraints": [
        "簡潔直接",
        "focus on action items",
        "允許更多 meme/梗"
      ]
    },

    "thought_leadership": {
      "context_triggers": ["medium", "文章", "演講", "深度內容"],
      "tone": "深度思考，批判性",
      "language": "繁中為主，引用資料",
      "formality": 0.6,
      "emoji_usage": "none",
      "audience": "tech community, industry peers",
      "goals": ["知識分享", "產業影響力", "深度論述"],
      "constraints": [
        "需要具體案例",
        "歷史類比",
        "避免空談理論"
      ]
    }
  }
}
```

---

## Context Detection Logic

```javascript
// Pseudocode for context detection
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

---

## Integration with Mnemosyne

### Modified Persona Analyzer Flow

```
┌───────────────────────────────────────────────────────────────┐
│                    Mnemosyne Context Engine                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. INPUT: User Request + Current Context                     │
│     ↓                                                         │
│  2. CONTEXT DETECTION: Identify situation (social/work/etc)  │
│     ↓                                                         │
│  3. ROOT PERSONA LOAD: Get base identity from Deep Profile    │
│     ↓                                                         │
│  4. CONTEXTUAL OVERLAY: Apply context-specific adjustments    │
│     ↓                                                         │
│  5. MERGED PERSONA: Root + Contextual = Final Persona         │
│     ↓                                                         │
│  6. PROMPT GENERATION: Generate context-aware system prompt   │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### API Design

```javascript
// New Mnemosyne API endpoints

// Get merged persona for specific context
const persona = await mnemo.getPersona({
  context: 'social_media'
});

// Auto-detect context from input
const persona = await mnemo.getContextualPersona({
  input: "幫我寫一則 Twitter 推文關於 AI Agent",
  autoDetect: true
});

// Get all available contexts
const contexts = await mnemo.listContexts();
// Returns: ['social_media', 'professional', 'internal_team', 'thought_leadership']

// Add/modify contextual persona
await mnemo.setContextualPersona('investor_meeting', {
  tone: '更正式，數據導向',
  formality: 0.9,
  // ...
});
```

---

## Implementation Phases

### Phase 1: Foundation (MVP)
- [ ] Define 4 base contextual personas (social, professional, internal, thought_leadership)
- [ ] Implement basic context detection (keyword-based)
- [ ] Create persona merging logic (root + context overlay)

### Phase 2: Enhancement
- [ ] Add more granular contexts (investor_pitch, customer_support, etc.)
- [ ] Implement ML-based context detection
- [ ] User-customizable context definitions

### Phase 3: Advanced
- [ ] Real-time context switching during conversation
- [ ] Cross-context learning (patterns that work in one context might apply to another)
- [ ] Context history and analytics

---

## Example Usage

**Scenario 1: Twitter Curator**
```
Input: "幫我寫一則推文回覆這個 AI 新聞"
Context Detected: social_media
Merged Persona:
  - Root: IrisGo CoFounder, 實用主義, 長期主義
  - Overlay: 輕鬆語氣, 可用動漫梗, formality 0.4
Result: 帶有觀點但親民的推文，可能包含文化類比
```

**Scenario 2: Investor Email**
```
Input: "幫我草擬給 AI Fund 的更新郵件"
Context Detected: professional
Merged Persona:
  - Root: IrisGo CoFounder, 數據驅動
  - Overlay: 正式語氣, 商業術語, formality 0.8
Result: 專業的商業郵件，強調 KPIs 和進展
```

---

## Open Questions

1. **Context 衝突處理**: 如果同時偵測到多個 context 怎麼辦？
   - 建議：使用權重系統，最高權重勝出

2. **Context 邊界模糊**: LinkedIn 有時要輕鬆，Twitter 有時要專業
   - 建議：允許 context blending (0.7 professional + 0.3 social)

3. **學習機制**: 如何從用戶反饋中改善 context detection?
   - 建議：記錄用戶修改紀錄，定期更新 trigger 權重

---

## References

- Root Persona: `obsidian://open?vault=PKM-Vault&file=0-Inbox/Lman-Deep-Persona-Profile`
- Mnemosyne PRD: `/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Mnemosyne/PRD.md`
- Meeting Notes: `/Users/lman/Dropbox/PKM-Vault/1-Projects/IrisGo/Meetings/2025-12-01-Product-Standup-Skills-Strategy-Pricing.md`

---

*Created: 2025-12-01*
*Author: Iris (Based on Product Standup discussion)*
*Status: RFC - Pending team review*
