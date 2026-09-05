# CyLab Security & Privacy Institute

## Business Context
- **Type/Industry:** University research institute (Carnegie Mellon University)
- **What they do:** Coordinate security and privacy research and education across all CMU departments.
- **Target audience:** Researchers, students, industry partners, policy makers, prospective faculty/students.
- **Page goal:** Establish authority, showcase research impact, surface news, and funnel to deeper content (research, education, partnerships).

---

# Page Layout & Structure

### Hero
Orange full-width banner (34% of surface coverage) with left-aligned text. H1 "CyLab is the university-wide security and privacy institute at Carnegie Mellon University" in near-black with tight letter-spacing; subtitle paragraph in near-black below. Right edge of banner contains a single orange badge (#1 ranking callout) positioned asymmetrically. Primary interaction: "Learn about CyLab's impact" link (blue underline) embedded in closing sentence. No image; type-forward, institutional tone.

### Header / Navigation
Horizontal sticky navigation bar on near-black background. Left: CyLab logo (orange + near-black). Center: 6 primary links (Research, Education, Partnerships, News, Events, About) + "More…" button (dropdown for Directory). Right: "Subscribe ✉" link in orange + Search icon (opens inline search box with placeholder "Search the CyLab Security and Privacy Institute site"). No hamburger; 15 total nav links. Orange used sparingly as link accent.

### Primary CTA / Input
Search box: top-right corner of header, inline text input with "Search" button. Secondary CTA: "Subscribe ✉" link (orange text) to /about/mailsignup.html, positioned left of search in header.

### Alert Banner
Full-width orange bar at page top. Text: "Save the Date! CyLab Partners Conference October 20-21, 2026." Dismissible or static; near-black text, orange background.

### Main Content Region (ID: maincontent)
**Purpose:** House all hero copy, news feed, stats, video section, and social links.
**Layout:** Vertical stack; white background below hero.

### News Section
**Purpose:** Surface 3 latest stories with publication dates and excerpt text.
**Layout:** H2 "News" in near-black, left-aligned. Vertical card stack: 3 news items, each = date (Sep 01, Aug 31, Aug 28) in dark gray + H3 link headline (near-black) + excerpt paragraph (dark gray). Cards have 1.24:1 aspect ratio thumbnail images placed to the left of text on larger viewports (stacked on mobile). Each card links to full article. Bottom: "More news from CyLab" link in orange.

### Stats / Impact Grid ×4 (uniform)
**Purpose:** Highlight institutional achievements and scale.
**Layout:** 4 equal cells, orange background (#1 icon + label + stat text), arranged left-to-right. Cells: "#1 Top-ranked programs" + "World-class faculty" + "Prolific researchers" + "Champions" (DEF CON, DARPA wins). Icons in orange badges. Text in near-black.

### What is CyLab? Section
**Purpose:** Video explainer with context.
**Layout:** Near-black full-width background. Left: H2 "What is CyLab?" (white text) + underline accent in orange (lightly rounded). Right: embedded iframe (video). Asymmetric layout; video takes ~50% width on desktop.

### Social Media Links Section
**Purpose:** Encourage social follows.
**Layout:** H2 "Social Media Links" (near-black). Horizontal line beneath heading (orange accent). 5 social icon circles (dark gray background, white icons: Facebook, YouTube, LinkedIn, Bluesky, X) arranged inline, each linked to respective platform (opens in new window).

### Action Links Region
**Purpose:** Secondary CTA bar with 3 directional links.
**Layout:** Light gray background, 3 equal cells: "Follow us on LinkedIn" + "Follow us on X" + "Subscribe to our YouTube channel" (each with arrow indicator, near-black text). Left-aligned stack on mobile.

### Footer
**Purpose:** Contact info, legal, social repeat, and institutional branding.
**Layout:** Near-black background (background 15.5% coverage). White text: CyLab address (4720 Forbes Avenue, Pittsburgh, PA 15213) + phone (+1 412 268 5715). Social icon links repeated (X, Facebook, YouTube, LinkedIn) in near-black circles. Carnegie Mellon logo (right-aligned). Blockquote from Lorrie Cranor (white text on near-black) with tight leading. Copyright line + "Legal" link in light gray. Lightly rounded corners on all interactive elements.

---

## Notable Patterns

- **Color dominance:** Orange used for CTAs, badges, alert bar, stats grid background, accent lines, and icon fills (34% of surface). Near-black dominates text (50 instances) and backgrounds.
- **Grid types:** Stats grid is **uniform** (4 equal orange cells); News stack is **uniform** height on mobile, mixed aspect on desktop.
- **Image ratios:** Thumbnails 1.24:1 (news cards) and 1.58:1 (impact imagery). All corners lightly rounded.
- **Asymmetry:** Hero banner with badge offset right; "What is CyLab?" text left, video right.
- **Sticky:** Header navigation remains fixed at top.
- **Accessibility:** Skip-to-Content link present; :focus-visible styling active; prefers-reduced-motion honored.
- **Interaction:** Search inline-opens in header; all CTAs use orange accent; social links open in new window.