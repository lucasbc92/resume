# Resume Social Preview Meta Tags Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Open Graph and Twitter Card meta tags to index.html so the resume displays a professional thumbnail with title, description, and headshot when shared on LinkedIn, Twitter, Slack, and other platforms.

**Architecture:** Single-file modification. Insert semantic meta tags into the `<head>` section of index.html after existing charset and viewport declarations. No content or styling changes; purely metadata layer.

**Tech Stack:** HTML5, Open Graph protocol, Twitter Card protocol

## Global Constraints

- Language: Portuguese (pt-BR)
- Image URL: `https://i.imgur.com/kmzS276.jpeg` (absolute, public HTTPS)
- Resume URL: `https://lucasbc92.github.io/resume/`
- No changes to resume body, styling, or bilingual toggle functionality
- All meta tags must be valid and properly formatted

---

### Task 1: Add Open Graph and Twitter Card Meta Tags

**Files:**
- Modify: `index.html:1-10` (head section)

**Interfaces:**
- Consumes: Existing `<head>` structure
- Produces: Valid OG and Twitter Card meta tags in head; no new function/component interfaces

---

#### Step 1: Locate the head section in index.html

Open `index.html` and find the `<head>` opening tag. You'll see:
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LINKEDIN_RESUME_2026_07_LUCAS_BUENO_CESARIO</title>
    <style>
```

We'll insert the new meta tags **after the viewport meta tag and before the title tag**.

#### Step 2: Write the meta tags

Insert the following block of code between the viewport meta tag and the `<title>` tag:

```html
    <!-- Open Graph Meta Tags (Facebook, LinkedIn, Slack, Discord, etc.) -->
    <meta property="og:title" content="Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP">
    <meta property="og:description" content="6+ anos desenvolvendo microsserviços financeiros em Java Spring Boot, React e Angular. Processamento de milhões de transações, Machine Learning, automação -60%. AWS (EC2, S3, RDS), GCP, Docker, Kubernetes, Spec Driven Development com IA.">
    <meta property="og:image" content="https://i.imgur.com/kmzS276.jpeg">
    <meta property="og:url" content="https://lucasbc92.github.io/resume/">
    <meta property="og:type" content="profile">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP">
    <meta name="twitter:description" content="6+ anos desenvolvendo microsserviços financeiros em Java Spring Boot, React e Angular. Processamento de milhões de transações, Machine Learning, automação -60%. AWS (EC2, S3, RDS), GCP, Docker, Kubernetes, Spec Driven Development com IA.">
    <meta name="twitter:image" content="https://i.imgur.com/kmzS276.jpeg">
```

After insertion, your head should look like:
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Open Graph Meta Tags (Facebook, LinkedIn, Slack, Discord, etc.) -->
    <meta property="og:title" content="Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP">
    <meta property="og:description" content="6+ anos desenvolvendo microsserviços financeiros em Java Spring Boot, React e Angular. Processamento de milhões de transações, Machine Learning, automação -60%. AWS (EC2, S3, RDS), GCP, Docker, Kubernetes, Spec Driven Development com IA.">
    <meta property="og:image" content="https://i.imgur.com/kmzS276.jpeg">
    <meta property="og:url" content="https://lucasbc92.github.io/resume/">
    <meta property="og:type" content="profile">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP">
    <meta name="twitter:description" content="6+ anos desenvolvendo microsserviços financeiros em Java Spring Boot, React e Angular. Processamento de milhões de transações, Machine Learning, automação -60%. AWS (EC2, S3, RDS), GCP, Docker, Kubernetes, Spec Driven Development com IA.">
    <meta name="twitter:image" content="https://i.imgur.com/kmzS276.jpeg">
    <title>LINKEDIN_RESUME_2026_07_LUCAS_BUENO_CESARIO</title>
    <style>
```

#### Step 3: Verify HTML validity

Run an HTML validator to ensure syntax is correct:
```bash
# Using Node.js html-validate (if installed):
npx html-validate index.html

# OR check manually: open index.html in a browser and check browser console for errors
# Expected: No HTML errors in console
```

If using a browser, press F12 to open Developer Tools → Console tab. You should see no errors or warnings related to meta tags.

#### Step 4: Test with OG Debugger (manual verification)

Use the [Facebook OG Debugger](https://www.opengraph.xyz/) or [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/):

1. Go to https://www.opengraph.xyz/
2. Paste: `https://lucasbc92.github.io/resume/`
3. Click "Generate" or "Preview"
4. **Expected output:**
   - Title: "Desenvolvedor Full Stack Java | Spring Boot · React · Microservices · AWS/GCP"
   - Description: "6+ anos desenvolvendo microsserviços financeiros..."
   - Image: Thumbnail of lucas.jpeg headshot displays correctly
   - URL: Shows as `https://lucasbc92.github.io/resume/`

#### Step 5: Commit changes

```bash
git add index.html
git commit -m "feat: add Open Graph and Twitter Card meta tags for social preview

- Add og:title, og:description, og:image, og:url, og:type for LinkedIn, Facebook, Slack
- Add twitter:card (summary_large_image) with matching title, description, image
- Portuguese language content optimized for recruiter keyword search
- Image: https://i.imgur.com/kmzS276.jpeg (lucas.jpeg headshot)
- No changes to resume content or styling"
```

---

## Success Criteria

✓ All 9 meta tags present in `<head>` section  
✓ No HTML validation errors  
✓ OG Debugger shows correct title, description, image  
✓ Changes committed to git  

## Testing Notes

- **LinkedIn caching:** If you're testing on LinkedIn, it may cache the old preview. Use [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/) to force refresh and see the updated preview.
- **Slack:** Share the resume URL in a Slack message — the preview should auto-fetch and display the new thumbnail + title + description.
- **Twitter:** Retweets or quoted tweets will show the `twitter:card` variant with large image.
- **GitHub Pages deployment:** Changes will be live once pushed to the GitHub Pages branch.
