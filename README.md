# Mnemosyne

> **The Memory Goddess of Your Digital Life**
>
> Privacy-first context engine that remembers who you truly are.
> Generate personalized AI System Prompts from your real behavior data while maintaining complete privacy control.

**Project Code Name**: Mnemosyne (Mnemo)
**Greek Origin**: Μνημοσύνη - Goddess of Memory, Mother of the Muses

---

## 🤝 Team Collaboration

**New to this project?** Start here:
- 📘 **[Quick Start Guide](./QUICK_START.md)** - 5-minute onboarding (推薦給同事)
- 📚 **[Collaboration Guide](./COLLABORATION.md)** - Complete Git workflow documentation

**Current Version**: v1.4.0 (2025-12-01)

---

## 📋 Project Overview

Mnemosyne is the context-aware engine at the heart of IrisGo.AI that:

1. **Personalizes AI Experience**: Generates custom System Prompts based on user behavior data
2. **Monetizes User Data**: Enables users to own and profit from their digital behavioral assets
3. **Privacy-First Design**: All sensitive data processing happens on-premise, never leaving user's device

### Key Innovation

Unlike traditional context systems that rely on cloud APIs and third-party data aggregation, Mnemosyne:

- ✅ Processes all data **locally** on user's hardware
- ✅ Uses **DayFlow screen recordings** + **Local VLM** for universal data extraction
- ✅ Implements **tiered privacy architecture** (Tier 1/2/3 tags)
- ✅ Enables **opt-in data monetization** without compromising privacy

---

## 🎯 Target Users (ICP)

**Knowledge Workers + Content Creators + Business Professionals**

Common characteristics:
- ✅ Heavy text-based work (emails, documents, presentations, articles)
- ✅ Value communication efficiency and professional image
- ✅ Need time management and prioritization
- ✅ Continuous learning of industry trends
- ✅ Digital native, familiar with various tools
- ❌ Not necessarily developers (no coding required)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Data Collection (MVP)                   │
├─────────────────────────────────────────────────────────┤
│  DayFlow VLM (40%) → Gmail Sent (30%) → Calendar (20%) │
│  DayFlow Stats (10%)                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                  Data Analysis (Local)                   │
├─────────────────────────────────────────────────────────┤
│  Persona Analyzer → Communication Analyzer              │
│  Time Analyzer → Interest Analyzer → Asset Manager      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│                    Output Generation                     │
├─────────────────────────────────────────────────────────┤
│  System Prompt (for AI chat) → Tag Assets (monetizable)│
│  Privacy-Protected Insights → User Analytics Dashboard  │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
mnemosyne/
├── docs/                          # Complete documentation
│   ├── 00-Overview.md            # Overall design and vision
│   ├── 01-MVP-Plan.md            # 6-week MVP implementation plan
│   ├── 02-Data-Sources.md        # Comprehensive data source analysis
│   ├── 03-Privacy-Architecture.md # Privacy-first technical design
│   └── 04-VLM-Solution.md        # Local VLM implementation details
│
├── src/
│   ├── collectors/               # Data collection modules
│   │   ├── dayflow-vlm-collector.js  # DayFlow + VLM analysis
│   │   ├── gmail-sent-collector.js   # Gmail Sent Mail via IMAP
│   │   ├── calendar-collector.js     # Google Calendar
│   │   └── dayflow-stats-collector.js # DayFlow Intelligence
│   │
│   ├── analyzers/               # Data analysis modules
│   │   ├── persona-analyzer.js
│   │   ├── communication-analyzer.js
│   │   ├── time-analyzer.js
│   │   └── interest-analyzer.js
│   │
│   ├── generators/              # Output generators
│   │   ├── prompt-generator.js
│   │   └── templates/
│   │       ├── core-identity.md
│   │       ├── working-style.md
│   │       ├── communication.md
│   │       └── expertise.md
│   │
│   ├── assets/                  # Tag asset system
│   │   ├── tag-extractor.js
│   │   ├── asset-manager.js
│   │   └── value-calculator.js
│   │
│   └── cli/                     # CLI interface
│       └── context-cli.js
│
├── tests/                       # Test suites
├── config/                      # Configuration files
├── package.json
└── README.md
```

---

## 🎯 Key Features

### 1. Multi-Source Data Collection (MVP - 4 Core Sources)

**1. DayFlow + VLM (40% weight)** - Interest & Content Preferences
- Analyze DayFlow screen recordings with local VLM
- Extract reading content topics (LinkedIn, Medium, YouTube)
- Identify work tool usage patterns (Notion, Figma, browser)
- Understand learning patterns (deep reading vs scanning)
- Social media behavior (platforms, engagement style)

**2. Gmail Sent Mail (30% weight)** - Communication Style
- Analyze outgoing emails via IMAP (read-only)
- Extract writing style (concise/detailed, formal/friendly)
- Identify email structure preferences (bullet points, paragraphs)
- Understand response patterns and timing
- Common openings and closings

**3. Calendar (20% weight)** - Time Management
- Meeting density and preferred time slots
- Deep work time blocks identification
- Meeting type distribution (1:1, team, external)
- Work/life balance patterns

**4. DayFlow Intelligence (10% weight)** - Basic Behavior
- Application usage time allocation
- Daily working hours
- Focus score and patterns
- Multitasking behavior

**Future Sources (Phase 2 - Month 3-4)**:

**5. Slack/Teams (補充即時溝通風格)**
- 只分析用戶發送的訊息
- 提取即時溝通模式和協作習慣
- 識別工作關係網絡
- 頻道黑名單保護隱私

**6. Notion/Obsidian (知識結構與學習模式)**
- Notion API 或 Obsidian 本地檔案
- 分析筆記主題和組織方式
- 識別學習興趣和內容創作模式
- 對內容創作者特別有價值

**7. Browser History (輕量級興趣追蹤)**
- 讀取 Chrome/Safari 歷史記錄
- 作為 DayFlow VLM 的補充或 fallback
- 捕捉搜尋意圖和瀏覽模式
- 敏感網站黑名單過濾

### 2. Privacy-First Architecture

**Tiered Tag System**:
- **Tier 1 Tags** (Coarse): Region, timezone, broad interests → May upload to server
- **Tier 2 Tags** (Medium): Specific interests, expertise → Hybrid strategy
- **Tier 3 Tags** (Fine): Purchase intent, work patterns → Never leaves device

**Privacy Protection**:
- All VLM analysis happens **locally** (Ollama + LLaVA)
- Sensitive content detection and filtering
- User-controlled data審查 UI
- Encrypted local storage
- Complete audit logging

### 3. System Prompt Generation

Generate personalized AI prompts that include:
- Core Identity (role, expertise, working style)
- Communication Style (tone, length, formality)
- Time Management (peak hours, meeting patterns)
- Interests & Expertise (topics, skill levels)

**Example Output**:
```markdown
You are talking to Lman, a founder and product builder focused on AI automation.

## Working Style
- Peak productivity: 9am-12pm, 2pm-5pm
- Deep work preference: 75% solo, 25% collaboration
- Communication: Concise, data-driven, semi-formal
- Tech stack: JavaScript, Node.js, Python, Claude API

## Current Focus
- Building IrisGo (on-premise AI product)
- Exploring VLM applications and context engines
- Interest in productivity automation and system design

## Preferences
- Favors practical examples over theory
- Appreciates direct, no-fluff communication
- Values privacy and local-first solutions
```

### 4. Tag Asset System (Monetization)

Extract **monetizable but privacy-safe tags**:
- Interests: "AI automation" (confidence: 0.95)
- Expertise: "JavaScript programming" (level: expert)
- Professional: "Product manager" (seniority: senior)
- Content Preference: "Technical deep-dive articles"

**Value Estimation**: $50-100/month potential earnings from anonymized tag assets

---

## 🚀 Implementation Roadmap

### Phase 1: MVP (Week 1-6)

**Week 1-2**: DayFlow VLM Collector
- Integrate DayFlow recording API
- Implement frame sampling (every 5 min)
- Build sensitive site blacklist
- Integrate Ollama + LLaVA 13B
- Test interest extraction accuracy
- **Output**: Interest Analyzer v0.1

**Week 3-4**: Gmail Sent Mail Collector
- Implement IMAP connection (read-only)
- Gmail App Password integration
- Email parsing and PII filtering
- Integrate Ollama Llama 3.2 for style analysis
- **Output**: Communication Analyzer v0.1

**Week 5**: Calendar + Integration
- Google Calendar API integration
- Meeting pattern statistical analysis
- Integrate all analyzers
- Persona aggregation logic
- **Output**: Time Analyzer v0.1 + Persona Generator v0.5

**Week 6**: CLI Tool + Automation
- CLI interface development
- System Prompt template system
- Export functionality (ChatGPT/Claude/Gemini)
- LaunchAgent setup
- Complete testing and documentation
- **Output**: Mnemosyne MVP v1.0

**Deliverable**: Functional System Prompt generator with 4 data sources

### Phase 2: Alpha (Month 3-4)

**New Data Sources**:
- Slack/Teams Collector (即時溝通風格)
- Notion/Obsidian Collector (知識結構)
- Browser History Collector (VLM fallback)

**Monetization**:
- Tier 1 tag upload for B2B market research
- Server-side coarse matching
- Basic anonymization

**Target**: 10K users

### Phase 3: Beta (Month 5-8)

- Full Tier 1/2/3 system
- Hybrid matching (server + local)
- Data Marketplace integration
- 100K users target

### Phase 4: Production (Month 9-12)

- K-Anonymity dynamic adjustment
- Advanced privacy features
- 1M+ users scale

---

## 💰 Business Model

### Personal Use (Free)
- Generate System Prompts for your own AI interactions
- Privacy-protected local analysis
- No data sharing required

### Data Marketplace (Opt-In)
- Users choose to monetize Tier 1/2 tags
- Privacy-preserving matching
- Earnings: Estimated $50-100/month
- Complete transparency and control

### B2B Market Research
- Aggregated, anonymized audience insights
- No individual user identification
- Premium pricing for advertisers

---

## 🔐 Privacy & Security

### Multi-Layer Protection

1. **Recording Level**: Blacklist sensitive sites (banking, email, messages)
2. **Pre-Scan Level**: Filter sensitive keywords before analysis
3. **VLM Prompt**: Instruct model to skip PII and sensitive content
4. **Local Processing**: All analysis happens on-device
5. **User Control**: Manual review before any data sharing
6. **Audit Log**: Complete transparency of all operations

### Data Storage

- Raw data: Encrypted local storage only
- Insights: User-controlled sharing
- Server: Only anonymized Tier 1 tags (opt-in)

---

## 🛠️ Tech Stack

### Core Technologies
- **Local VLM**: Ollama + LLaVA 13B (privacy-safe vision analysis)
- **Runtime**: Node.js
- **Storage**: SQLite (encrypted)
- **OCR**: Apple Vision Framework / Tesseract
- **Video Processing**: ffmpeg

### Data Sources Integration
- DayFlow (already integrated)
- Ollama + LLaVA 13B (local VLM)
- Ollama + Llama 3.2 (local LLM)
- Gmail IMAP (node-imap + mailparser)
- Google Calendar API / MCP

### Privacy Technologies
- Differential Privacy
- K-Anonymity
- Zero-Knowledge Proofs (future)
- Encrypted local storage

---

## 📊 Success Metrics

### MVP Phase
- System Prompt quality: >90% user satisfaction
- Data collection success rate: >95%
- Processing time: <5 seconds
- Privacy incidents: 0

### Production Phase
- Active users: 1M+
- Data monetization opt-in rate: >30%
- Average user earnings: $50-100/month
- Privacy compliance: 100%

---

## 🤝 Contributing

This is an internal IrisGo project. For questions or suggestions, contact the team.

---

## 📚 Documentation

Complete documentation available in `docs/`:
1. [PRD (Product Requirements Document)](Mnemosyne%20PRD.md) - **Start here**: Complete product specification
2. [Overview & Design](./docs/00-Overview.md) - Product vision and architecture
3. [MVP Implementation Plan](./docs/01-MVP-Plan.md) - 6-week execution plan
4. [Data Sources Analysis](./docs/02-Data-Sources.md) - Comprehensive source evaluation
5. [Privacy Architecture](./docs/03-Privacy-Architecture.md) - Technical privacy design
6. [VLM Solution](./docs/04-VLM-Solution.md) - Local VLM implementation

---

## 📝 License

Proprietary - IrisGo.AI © 2025

---

**Project Name**: Mnemosyne (Mnemo)
**Status**: Planning Phase → Ready for MVP Implementation
**Last Updated**: 2025-12-01
**Version**: 1.4.0

---

*"Mnemosyne, the Greek goddess of memory, remembers all that has been and all that will be. Just as she gave birth to the nine Muses who inspire all art and science, Mnemosyne gives birth to your digital persona - a true reflection of who you are."*
