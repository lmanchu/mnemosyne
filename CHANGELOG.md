# Changelog

All notable changes to Mnemosyne will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.5.0] - 2025-12-15

### Added
- **Root Persona + Mask Architecture**: Evolution from Contextual Persona System
  - **Cold-Start Solution**: MBTI test (10-15 questions) for rapid Root Persona generation
  - **LinkedIn Import**: Alternative onboarding via OAuth profile parsing
  - **MBTI → Root Persona Mapping Engine**: 16 personality types mapped to core attributes

- **Root Persona (Immutable Layer)**:
  - MBTI 16 Types as foundation
  - Core Values (derived from MBTI)
  - Thinking Patterns
  - Communication Style
  - Source tracking: `mbti_test | linkedin_import | manual`

- **Mask System (Customizable Layer)**:
  - 4 base masks: `social_media`, `professional`, `internal_team`, `thought_leadership`
  - **Selectable Traits Library**: 50+ traits organized by category
  - **Context Blending**: Mix multiple masks with weights (e.g., professional: 0.7, social: 0.3)
  - Trait → Prompt mapping for dynamic generation

- **TypeScript Data Schema**:
  - `RootPersona` interface (locked: true, never changes)
  - `Mask` interface (selectedTraits, customPrompt for Pro)
  - `TraitSelection`, `UsageStats`, `ContextBlend` interfaces

- **Implementation Roadmap** (10 weeks):
  - Phase 1: Foundation (4 masks + context detection)
  - Phase 2: Cold-Start (MBTI + LinkedIn)
  - Phase 3: Trait System (50+ traits)
  - Phase 4: Dynamic Updates (DayFlow integration)
  - Phase 5: Monetization (Pro tier features)

### Changed
- **Business Model Updated**:
  - Free Tier: 3 Masks + basic traits
  - Pro Tier ($9.99/mo): Unlimited Masks + Custom Prompt editing + Advanced traits
  - Team Tier ($29.99/mo): Organizational Persona + Brand Voice unification

### Documentation
- New RFC document: `docs/RFC-Root-Persona-Mask-Architecture.md` (v0.2)
- Merged content from original Contextual Persona System (v0.1)

### Source
- RFC-Root-Persona-Mask-Architecture.md v0.2 (2025-12-05)
- Internal architecture discussions

---

## [1.4.0] - 2025-12-01

### Added
- **Contextual Persona System**: New hierarchical persona architecture
  - Root Persona + Contextual Persona splitting concept
  - 4 base contextual personas: social_media, professional, internal_team, thought_leadership
  - Context detection logic (keyword-based)
  - Persona merging system (root + context overlay)
- New design document: `docs/contextual-persona-system.md`

### Changed
- Persona Analyzer now supports context-aware persona generation
- System Prompt Generator can apply contextual overlays

### Documentation
- Added RFC for Contextual Persona System
- Updated architecture diagrams with new persona hierarchy

### Source
- Product Standup meeting discussion (2025-12-01)
- Meeting notes: `Meetings/2025-12-01-Product-Standup-Skills-Strategy-Pricing.md`

---

## [1.3.0] - 2025-11-16

### Added
- Complete PRD documentation
- 6-week MVP implementation plan
- Privacy architecture design
- VLM solution documentation

### Changed
- Updated data source weights (DayFlow 40%, Gmail 30%, Calendar 20%, Stats 10%)
- Refined Tier 1/2/3 privacy tag system

---

## [1.2.0] - 2025-11-14

### Added
- Collaboration workflow documentation
- Quick Start guide for team onboarding

---

## [1.1.0] - 2025-11-12

### Added
- Initial project structure
- Basic README and project overview

---

## [1.0.0] - 2025-11-10

### Added
- Project inception
- Initial concept and naming (Mnemosyne - Memory Goddess)
- Core value proposition defined

---

## Upcoming (Planned)

### [1.6.0] - TBD
- [ ] ML-based context detection (upgrade from keyword-based)
- [ ] User-customizable mask definitions
- [ ] Real-time context switching
- [ ] Mask performance analytics

### [2.0.0] - TBD
- [ ] Cross-context learning
- [ ] Context history and analytics
- [ ] Full monetization integration
- [ ] Data Marketplace launch
