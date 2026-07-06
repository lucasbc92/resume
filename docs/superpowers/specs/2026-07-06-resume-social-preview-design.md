# Resume Social Preview Meta Tags Design
**Date:** 2026-07-06  
**Scope:** Add Open Graph and Twitter Card meta tags to index.html for professional social media previews

## Overview
When Lucas's resume is shared on LinkedIn, Twitter, Slack, or via link preview (e.g., Discord), the default preview is generic or missing. This design adds semantic meta tags to present a professional, keyword-optimized thumbnail that appeals to technical recruiters and hiring managers.

## Goals
1. **Visual impact:** Display the professional headshot (lucas.jpeg via imgur) when shared
2. **Keyword optimization:** Pack primary tech stack and measurable achievements into title and description for discoverability
3. **Professional credibility:** Present a polished, intentional preview across all platforms
4. **Bilingual support (future):** Structure supports easy pivot to Portuguese/English variants

## Design Approach: Keywords-Heavy

### Title Strategy
**Text:** `Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP`

- Leads with role + name context ("Desenvolvedor Full Stack Java")
- Uses bullet separators (·) for visual scannability
- Prioritizes technologies with highest recruiter search volume: Spring Boot, React, Microservices, AWS/GCP
- ~80 characters (fits all platform displays without truncation)

### Description Strategy
**Text:** `6+ anos desenvolvendo microsserviços financeiros em Java Spring Boot, React e Angular. Processamento de milhões de transações, Machine Learning, automação -60%. AWS (EC2, S3, RDS), GCP, Docker, Kubernetes, Spec Driven Development com IA.`

- Opens with seniority claim (6+ years) and domain expertise (financial microservices)
- Primary stack: Java Spring Boot, React, Angular, AWS, GCP
- Measurable impact: millions of daily transactions, 60% automation gain, Machine Learning
- Secondary keywords: Docker, Kubernetes, Spec Driven Development, AI
- ~255 characters (Twitter/LinkedIn display limit before truncation)

### Image
**URL:** `https://i.imgur.com/kmzS276.jpeg`

- Professional headshot via imgur (user-provided, hosted externally)
- Absolute HTTPS URL (required by social platforms)
- ~1:1 square crop (platform standard for profile images)

### URL
**Base:** `https://lucasbc92.github.io/resume/`

- GitHub Pages domain for lucasbc92 account
- Required by Open Graph; must match where resume is hosted

## Meta Tags Structure

### Open Graph (OG) Tags
Used by Facebook, LinkedIn, Slack, Discord, and most social platforms:
- `og:title` — primary title
- `og:description` — preview text
- `og:image` — thumbnail URL
- `og:url` — canonical resume URL
- `og:type` — set to "profile" (indicates personal profile)

### Twitter Card
Used by Twitter/X specifically:
- `twitter:card` — set to "summary_large_image" (large headshot variant)
- `twitter:title` — same as og:title
- `twitter:description` — same as og:description
- `twitter:image` — same image URL

## Implementation Details

### Location in HTML
Meta tags insert into `<head>` section of index.html, after existing `<meta charset>` and `<meta viewport>` tags, before `<title>`.

### Character Encoding
All text is Portuguese; no special encoding required (UTF-8 already declared).

### No Content Changes
- Resume body remains unchanged
- Bilingual toggle and styling untouched
- Only metadata layer added

## Testing & Verification

**Manual verification:**
1. Share resume URL on LinkedIn — preview should show title, description, and headshot
2. Share on Twitter — verify "summary_large_image" layout with large photo
3. Share on Slack — confirm thumbnail displays
4. Use [OG Tag Debugger](https://www.opengraph.xyz/) to validate syntax

**Edge cases:**
- Platform caching: LinkedIn/Slack may cache old previews; use debug tools to force refresh
- Image accessibility: imgur link is public; no auth required

## Success Criteria
✓ Thumbnail displays correctly across LinkedIn, Twitter, Slack  
✓ Title and description are keyword-rich and recruiter-friendly  
✓ No changes to resume content or interactivity  
✓ All platforms fall back gracefully if image URL becomes unavailable  

## Future Enhancements (Out of Scope)
- Bilingual variants (separate meta tags for PT/EN versions)
- Branded og:image with gradient/branding (currently using plain headshot)
- Schema.org structured data (Resume schema for richer SEO)
