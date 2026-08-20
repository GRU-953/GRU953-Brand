# GRU953 — the benchmark

GENERATED — do not hand-edit. Produced by `scripts/render_benchmark.py` from
`01_research/_data/criteria.json` and `01_research/findings.json`. To change a
verdict or add a finding, edit those files and re-run the script.

সহজ প্রযুক্তি। সবার জন্য। · Simple technology. For everyone.

**9 meets · 4 partial · 27 gap (including 4 not yet tested) · 10 not applicable yet — out of 50 criteria, frozen 20 August 2026, before this rebuild's own artefacts existed to test against.**

---

## 0. What this benchmark is, and is not

This compares GRU953 against **published guidance** from other organisations —
never against how well those organisations follow their own guidance, and never
against their private brand books, because neither Apple nor Google publishes
one. Every criterion below names the test that decides it, written and frozen
on **20 August 2026**, before the rebuilt kit existed — so a verdict
cannot be graded to an answer it already knew. `baseline_verdict` is scored
against the kit as it stood **before** this rebuild (13 August 2026); it exists
so the rebuild's own progress can be measured, not just claimed.

Research behind this benchmark: **141 findings**, each
carrying a primary source, a retrieval date, and — for any numeric claim — a
verbatim quote. **35 questions** could not be
verified from a primary source and are listed as such, not guessed at. Full data:
`01_research/findings.json`.

---

## A - Brand fundamentals

### A01 — Gap

**Claim:** GRU953's own architecture document states, in its own words, whether it is a design system, a brand book, or both, and does not claim to be one while actually being the other.

**Test:** grep 02_strategy/*.md and the guidebook for the words 'design system' and 'brand book' used with a stated definition

**Baseline:** BRAND-SPEC.md and DESIGN-RULES.md exist but neither states this distinction explicitly.


### A02 — Gap

**Claim:** The two-tier architecture (GRU953 governs developer-facing surfaces; products get their own identity with GRU953 as endorsement) is written down as a rule, with the endorsement form stated, before any product uses it.

**Test:** a committed 02_strategy/ARCHITECTURE.md exists and states the endorsement form

**Baseline:** BRAND-SPEC.md §9 states endorsement form for products under GRU953, but nothing states the two-tier split (GRU953 vs independently-branded consumer products) confirmed in this rebuild's interview.


### A03 — Meets

**Claim:** Design system and brand book are described as two different things, and neither Apple nor Google is cited as publishing a brand book they do not publish.

**Test:** grep the guidebook and BENCHMARK.md for phrases like "Apple's brand book" or "Google's brand guidelines" used to mean identity governance

**Baseline:** The old kit's RESEARCH.md and DESIGN-RULES.md make no such claim about Apple or Google. Verified this is still correct: Apple's HIG is a design system with no public brand book (only a trademark-permission policy); Google's Material is a design system, and its public brand page is likewise a trademark-usage guide, not identity governance.

> The HIG functions as a public engineering-facing design system: every page we read (App icons, Materials, Typography, Layout, Buttons, Motion, Accessibility) is structured around components, platform-by-platform specification tables, and direct cross-references to developer APIs (SwiftUI/UIKit/AppKit/WatchKit types and modifiers). It contains no brand-identity content — no logo/wordmark usage rules, no brand voice or tone guidance, no brand architecture. It is a design system, not a brand book.
> — Human Interface Guidelines pages (App icons, Materials, Typography, Layout, Buttons, Motion, Accessibility) - Apple Developer Documentation, https://developer.apple.com/design/human-interface-guidelines/, read 20 August 2026
>
> No. What is publicly available under Apple's 'marketing resources' / 'brand' materials is a trademark-permission and legal-usage policy for third parties (developers, resellers, licensees) — governing how they may reference Apple's product names, logo, and badges in their own marketing — not a governance brand book describing Apple's own mark meaning, voice, or brand architecture. The developer.apple.com page titled 'Marketing Resources and Identity Guidelines' is entirely composed of trademark/legal rules (badge specs, product-image rules, naming conventions, trademark symbols, a signed licensing agreement) with no content about brand meaning or voice.
> — *“Use only the badge artwork provided in these guidelines. Don't use icons, logos, graphics, or images from www.apple.com to promote your app.”* (Marketing Resources and Identity Guidelines - App Store - Apple Developer,
>   https://developer.apple.com/app-store/marketing/guidelines/, read 20 August 2026)
>
> Material Design 3's own homepage describes it explicitly as an engineering/design system, not a brand identity book.
> — *“Material Design 3 is Google's open-source design system for building beautiful, usable products.”* (Material Design 3 - Google's latest open source design system,
>   https://m3.material.io/, read 20 August 2026)
>
> Google's public brand page (about.google/brand-resource-center redirects to its Partner Marketing Hub 'Overview') is explicitly framed as a trademark/usage-permission guide for external parties naming or referencing Google — not an internal identity/voice governance brand book. The fuller internal 'Brand Standards' governance site exists but is gated to invited agencies via a Google contact, so its content could not be verified publicly.
> — *“If you want to name or refer to Google in your work, these are the guidelines for how to do it, whether you're a business owner, filmmaker, journalist, student, or otherwise. ... If you're part of an agency making work for Google, head to Google's Brand Standards site. If you need access, reach out to your Google contact.”* (Overview - Partner Marketing Hub,
>   https://partnermarketinghub.withgoogle.com, read 20 August 2026)
>

### A04 — N/A

**Claim:** Where GRU953 claims a company publishes both a design system and a brand book (as a model to follow), that claim is backed by a verified finding naming both artefacts.

**Test:** cross-reference every such claim against findings.json

**Baseline:** The old kit makes no such claim yet; criterion applies once the new guidebook cites these examples.

> Yes. Mozilla's own design-system homepage explicitly names and separates the two: Acorn is the public design system for the Firefox product (tokens, components, content, platform guidelines), while a distinct resource called 'Firefox Brand Guidelines' covers positioning, voice and tone, and visual elements (i.e. a brand book), and a third resource, Mozilla Protocol, is a separate design system for marketing websites.
> — *“Firefox Brand Guidelines — These guidelines document the Brand System as it applies to brand design and marketing applications. It includes positioning, voice and tone, and visual elements. Mozilla Protocol — Mozilla maintains a design system used for marketing websites.”* (Acorn – Acorn Design System (homepage),
>   https://acorn.firefox.com, read 20 August 2026)
>
> Yes. Codex (doc.wikimedia.org/codex) is Wikimedia's public design system (tokens, Vue/CSS components, icons). Separately, the Wikimedia Foundation Governance Wiki publishes a detailed public visual identity guide covering the Wikipedia puzzle globe, wordmark, construction rules and permitted variants — a genuine brand/mark book, distinct from Codex.
> — *“The distinctive Wikipedia identity has evolved over the years since it was introduced in 2003 [...] The hero version of the puzzle globe shows characters from 18 language sets: Armenian, Khmer, Japanese (Katakana), Geez, Guarani, Greek, Latin, Arabic, Devanagari, Traditional Chinese, Cyrillic, Korean, Georgian, Kannada, Hebrew, Thai, Tibetan, Tamil.”* (Legal:Visual identity guidelines – Wikimedia Foundation Governance Wiki,
>   https://foundation.wikimedia.org/wiki/Legal:Visual_identity_guidelines, read 20 August 2026)
>
> Yes, and they are hosted as clearly separate public sites. design-system.service.gov.uk is the design system (styles, components, patterns, code, MIT-licensed). brand.design-system.service.gov.uk is titled 'GOV.UK Brand Guidelines' and is a distinct brand book covering the graphic device (the dot), the logo system (wordmark + crown), colour, typography, data/chart branding, and 'brand in use', with assets downloadable from a separate GitHub repo.
> — *“How to use the GOV.UK brand. Help users find, understand and trust the GOV.UK brand. [...] Logo system: How the GOV.UK wordmark and crown work together in different contexts. [...] Get brand assets: You can find and download brand element and asset files in the govuk-brand-assets repository on GitHub.”* (GOV.UK Brand Guidelines (homepage),
>   https://brand.design-system.service.gov.uk, read 20 August 2026)
>

### A05 — Meets

**Claim:** The accepted 'GRU = Gated Recurrent Unit' reading risk is stated in the guidebook, with the mitigation rule (tagline always under the wordmark), not quietly dropped.

**Test:** grep the guidebook for 'Gated Recurrent Unit'

**Baseline:** BRAND-SPEC.md §7 and RESEARCH.md §1 both state this already, well.


### A06 — Gap

**Claim:** GRU953 states honestly that its own benchmark rests on published guidance, not on how well the benchmarked organisations follow their own guidance, and not on their private brand books.

**Test:** the benchmark document contains an explicit limits section saying this

**Baseline:** No such limits statement exists yet in the old kit.


---

## B - Mark and icons

### B01 — Gap

**Claim:** No corner radius, percentage or squircle value is attributed to Apple anywhere in the kit; where a radius is used, it is labelled a GRU953 house choice.

**Test:** grep the whole tree for 'squircle' or a radius number near the word 'Apple'

**Baseline:** 03_logo/GRU953-appicon.svg's own <desc> reads "at the squircle corner radius iOS and Android expect" and 02_strategy/DESIGN-RULES.md §2.3 repeats it. Confirmed invented: Apple's own HIG states only that masking 'precisely matches the curvature of other rounded interface elements ... and the bezel of the physical device itself' -- no number, ever.

> No. Apple's current HIG states only that the system's masking matches the curvature of other interface elements and the device bezel; it publishes no numeric radius, percentage, or squircle formula for designers to use, and explicitly tells designers to supply square, unmasked layers and let the system apply the mask.
> — *“In iOS, iPadOS, and macOS, icons are square, and the system applies masking to produce rounded corners that precisely match the curvature of other rounded interface elements throughout the system and the bezel of the physical device itself.”* (App icons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/app-icons, read 20 August 2026)
>

### B02 — Gap

**Claim:** The rebuilt mark's small-size floor (16px, per the owner's own stated floor) is proven by rasterising and checking counter survival, under at least two independent renderers.

**Test:** run the mark build's raster gate under resvg/Chromium and a second engine

**Baseline:** The old kit's marks.py checks only 24px, under one renderer (rsvg-convert, not present on this Mac).


### B03 — Gap

**Claim:** Every icon artefact ships rounded or circular, per the owner's instruction, except exactly one square unmasked master for Icon Composer -- and that exception is documented, not accidental.

**Test:** the asset manifest lists every icon artefact's shape; exactly one is 'square-unmasked'

**Baseline:** The old kit ships only a pre-rounded app-icon tile; there is no square unmasked master for Icon Composer at all.


### B04 — Gap

**Claim:** The kit states, in the owner's own words, that pre-rounding departs from Apple's current guidance, and quotes Apple's stated cost.

**Test:** the guidebook contains the exact Apple quote about pre-defined masking

**Baseline:** Verified quote to use: "Providing layers with pre-defined masking negatively impacts specular highlight effects and makes edges look jagged."

> Apple explicitly warns against pre-masking: supplying layers with their own corner/circle masking already applied harms the specular-highlight lighting effects the system draws and makes the icon's edges look jagged rather than crisp.
> — *“Providing layers with pre-defined masking negatively impacts specular highlight effects and makes edges look jagged.”* (App icons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/app-icons, read 20 August 2026)
>

### B05 — Gap

**Claim:** visionOS and watchOS icon artefacts are noted as the platforms where the departure costs nothing, because Apple's own system mask there is already circular.

**Test:** the guidebook states this platform-by-platform, not as a blanket claim

**Baseline:** watchOS canvas is 1088x1088, not 1024 -- confirmed; the old kit's watch asset, if any, must be checked against this, not assumed 1024.

> Confirmed: visionOS and watchOS are the two platforms where Apple's system masks the square icon layout into a circle; iOS, iPadOS, and macOS mask to a rounded rectangle, and tvOS masks a rectangular (landscape) layout to a rounded rectangle.
> — *“In visionOS and watchOS, icons are square and the system applies circular masking.”* (App icons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/app-icons, read 20 August 2026)
>
> Confirmed: watchOS uses a 1088x1088 px square layout canvas (not 1024), layered style, masked by the system into a circle.
> — *“watchOS | Square | Circular | 1088x1088 px | Layered | N/A”* (App icons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/app-icons, read 20 August 2026)
>
> visionOS uses a square 1024x1024 px layout canvas, style 'Layered (3D)', masked by the system into a circle.
> — *“visionOS | Square | Circular | 1024x1024 px | Layered (3D) | N/A”* (App icons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/app-icons, read 20 August 2026)
>

### B06 — Gap

**Claim:** The Android adaptive icon foreground is NOT pre-rounded; a full-bleed background layer plus an unrounded foreground is supplied so every OEM launcher mask still applies correctly.

**Test:** the Android asset set has a background layer sized 108x108dp with a foreground logo between 48x48dp and 66x66dp, unrounded

**Baseline:** No adaptive-icon-specific asset exists in the old kit at all -- confirmed dimensions to build to: 108dp canvas, 66dp inner safe zone, 18dp reserved margin per side, logo 48-66dp, monochrome layer for Android 13+ theming.

> Adaptive icon layers must be sized to a 108x108dp canvas, with a 66x66dp inner safe zone that is never clipped by an OEM mask, and an 18dp margin reserved on each side for masking/visual effects; the logo itself must be between 48x48dp and 66x66dp.
> — *“Size all layers to 108x108 dp. ... Use a logo that's at least 48x48 dp. It must not exceed 66x66 dp, because the inner 66x66 dp of the icon appears within the masked viewport. ... The outer 18 dp on each of the four sides of the layers is reserved for masking and to create visual effects such as parallax or pulsing.”* (Adaptive icons | Android Developers,
>   https://developer.android.com/develop/ui/views/launch/icon_design_adaptive, read 20 August 2026)
>
> A monochrome icon layer is not mandatory for the adaptive icon to function, but is required specifically to support Android's per-device icon theming feature introduced in Android 13 (API 33); from Android 16 QPR 2 onward, the OS auto-generates a themed icon for apps that don't supply their own monochrome layer.
> — *“starting with Android 13 (API level 33), users can theme their adaptive icons... for apps that have a monochrome layer in their adaptive icon. Starting with Android 16 QPR 2, Android automatically themes app icons for apps that don't provide their own.”* (Adaptive icons | Android Developers,
>   https://developer.android.com/develop/ui/views/launch/icon_design_adaptive, read 20 August 2026)
>

### B07 — Gap

**Claim:** Every rasteriser-dependent proof states which renderer(s) produced the figure, so the claim is never presented as renderer-independent fact.

**Test:** the mark/asset build scripts print their renderer name in the proof output

**Baseline:** marks.py's counter-survival check does not name its renderer in its output.


---

## C - Colour and contrast

### C01 — Partial

**Claim:** No colour role is named after a role Google's current Compose Material3 API marks Deprecated.

**Test:** cross-reference every --gru-* role name against the ColorScheme API's actual Deprecated annotations, not against a secondhand summary

**Baseline:** CORRECTED FINDING, important: background/onBackground/surfaceVariant are NOT marked Deprecated as properties in the current ColorScheme API -- only two constructor overloads that omit newer parameters are. The old kit's --gru-bg is therefore not importing a formally deprecated name, contrary to what this rebuild's own earlier planning assumed. The naming choice (bg vs surface) is still worth reconsidering for alignment with the newer, larger role vocabulary (10 surface-family roles among 26 total), but it must not be described in the guidebook as 'the deprecated name' -- that claim would itself fail criterion G01.

> In the current (checked today) Jetpack Compose Material3 API reference, the ColorScheme class's background, onBackground and surfaceVariant properties are listed as ordinary public properties with no 'Deprecated' tag on any of them individually.
> — *“background — The background color that appears behind scrollable content.”* (ColorScheme | API reference | Android Developers,
>   https://developer.android.com/reference/kotlin/androidx/compose/material3/ColorScheme, read 20 August 2026)
>
> Only two of the three public ColorScheme() constructor overloads are marked deprecated — the ones that omit the newer 'surfaceContainer' and 'fixed' accent-color parameters — not the color properties themselves, and not via the word 'removed'.
> — *“This function is deprecated. Use constructor with additional 'surfaceContainer' roles.”* (ColorScheme | API reference | Android Developers,
>   https://developer.android.com/reference/kotlin/androidx/compose/material3/ColorScheme, read 20 August 2026)
>

### C02 — Partial

**Claim:** Every text pair is proven at 4.5:1 normal / 3:1 large in every theme, with 'large' defined exactly as WCAG defines it (18pt, or 14pt bold) -- not a rounded approximation stated as the standard.

**Test:** the contrast engine's threshold table cites the exact WCAG definition

**Baseline:** DESIGN-RULES.md §5.1 states "3:1 large (24px, or 19px bold)" -- close but not the standard's own wording (18pt/14pt bold; 19px is this kit's own pixel conversion, not cited as such).

> SC 1.4.3 (Level AA) requires text and images of text to have a contrast ratio of at least 4.5:1, with large-scale text as the stated exception.
> — *“The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text”* (WCAG 2.2 — Success Criterion 1.4.3,
>   https://www.w3.org/TR/WCAG22/#contrast-minimum, read 20 August 2026)
>
> Large-scale text (and images of large-scale text) need only a 3:1 contrast ratio under SC 1.4.3.
> — *“Large-scale text and images of large-scale text have a contrast ratio of at least 3:1”* (WCAG 2.2 — Success Criterion 1.4.3,
>   https://www.w3.org/TR/WCAG22/#contrast-minimum, read 20 August 2026)
>
> WCAG 2.2's glossary defines large-scale text as at least 18 point, or 14 point bold, type (or the CJK equivalent size) — not simply '18pt or 14pt' without the bold qualifier on the smaller size.
> — *“large scale (text) with at least 18 point or 14 point bold or font size that would yield equivalent size for Chinese, Japanese and Korean (CJK) fonts”* (WCAG 2.2 — Glossary, definition of 'large scale (text)',
>   https://www.w3.org/TR/WCAG22/#dfn-large-scale, read 20 August 2026)
>

### C03 — Meets

**Claim:** No AAA claim is made for non-text contrast anywhere, because WCAG defines no AAA level for it.

**Test:** grep for 'AAA' within 15 words of 'border', 'focus', 'icon', 'non-text', 'target'

**Baseline:** Confirmed: SC 1.4.11 exists only at AA; the Level AAA criteria under Guideline 1.4 (1.4.6, 1.4.7, 1.4.8, 1.4.9) do not cover non-text contrast at all. The old kit makes no AAA-for-non-text claim currently.

> No. SC 1.4.11 Non-text Contrast exists only at Level AA. The Level AAA criteria grouped under Guideline 1.4 are 1.4.6 Contrast (Enhanced) — which covers TEXT contrast at 7:1, not non-text — plus 1.4.7 Low or No Background Audio, 1.4.8 Visual Presentation, and 1.4.9 Images of Text (No Exception); none of these addresses non-text/UI-component contrast, so WCAG 2.2 has no AAA equivalent of 1.4.11.
> — *“How to Meet Non-text Contrast (Level AA)”* (WCAG 2.2 (Success Criterion 1.4.11 heading) and WCAG 2.2 Quick Reference (full 1.4.x criteria/levels list),
>   https://www.w3.org/TR/WCAG22/#non-text-contrast, read 20 August 2026)
>

### C04 — N/A

**Claim:** Where the kit states a policy floor above WCAG's normative minimum (e.g. a 7:1 high-contrast-theme floor), it is labelled explicitly as GRU953 policy, not as a conformance claim.

**Test:** grep for '7:1' and confirm the word 'policy' appears in the same paragraph

**Baseline:** The old kit has no high-contrast theme yet.


### C05 — Untested (counts as a gap)

**Claim:** Non-text UI contrast is proven at 3:1 as WCAG's SC 1.4.11 actually states it -- against adjacent colours, not against an arbitrary reference.

**Test:** the contrast engine's non-text check compares against the actual adjacent colour in context

**Baseline:** Not directly checked against the old engine's implementation in this pass.

> SC 1.4.11 (Level AA) requires a contrast ratio of at least 3:1 against adjacent colours for user interface components and graphical objects.
> — *“The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s): User Interface Components”* (WCAG 2.2 — Success Criterion 1.4.11,
>   https://www.w3.org/TR/WCAG22/#non-text-contrast, read 20 August 2026)
>

### C06 — Gap

**Claim:** Every tonal surface step has a stated job (background, hover, border, text, etc.), the way Radix Colors' 12-step model and IBM Carbon's Core/Component tokens both do -- not a bare number a reader must look up.

**Test:** the token doc lists a one-line job for every step

**Baseline:** The old kit's ramps are numbered 50-950 with no stated per-step job.

> Yes — Radix Colors publishes an explicit use-case table assigning one primary job to each of the 12 steps: 1 App background, 2 Subtle background, 3 UI element background, 4 Hovered UI element background, 5 Active/Selected UI element background, 6 Subtle borders and separators, 7 UI element border and focus rings, 8 Hovered UI element border, 9 Solid backgrounds, 10 Hovered solid backgrounds, 11 Low-contrast text, 12 High-contrast text.
> — *“There are 12 steps in each scale. Each step was designed for at least one specific use case.”* (Radix Colors (WorkOS),
>   https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale, read 20 August 2026)
>
> Steps 3, 4 and 5 are explicitly assigned to a component's normal, hover, and pressed/selected background states respectively.
> — *“Step 3 is for normal states. Step 4 is for hover states. Step 5 is for pressed or selected states.”* (Radix Colors (WorkOS),
>   https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale, read 20 August 2026)
>
> For color specifically, Carbon's live docs name three layers: "Core Tokens" (global colors used across all components), "Component Tokens" (colors scoped to one component only and never reused elsewhere), and "AI Tokens" (a separate suite reserved for AI-styled UI). This is Carbon's actual current terminology, not the generic "global/alias/component" naming some third-party write-ups attribute to it.
> — *“Core tokens are global colors that are used across components... Some components have their own specific color tokens, known as component tokens... and should never be used for anything other than their own component.”* (IBM / Carbon Design System,
>   https://carbondesignsystem.com/elements/color/tokens/, read 20 August 2026)
>

### C07 — Untested (counts as a gap)

**Claim:** Contrast figures are published as the worst legal pairing in the set, not the best one, the way Radix's Lc 60/90 guarantee and USWDS's magic-number floor are both stated as guarantees, not highlights.

**Test:** CONTRAST.md (or its successor) states a single worst-pair headline figure

**Baseline:** Not directly checked in this pass whether the old CONTRAST.md states a worst-pair headline.

> Radix states that its text steps (11 and 12) are engineered to a specific measured contrast guarantee against a step-2 background from the same scale, using the APCA contrast metric — not just a subjective 'low/high contrast' label.
> — *“Steps 11 and 12—which are designed for text—are guaranteed to Lc 60 and Lc 90 APCA contrast ratio on top of a step 2 background from the same scale.”* (Radix Colors (WorkOS),
>   https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale, read 20 August 2026)
>
> USWDS ties its whole grade/magic-number system back to a specific legal contrast floor: Section 508 (which it says aligns with WCAG 2.0 Level AA) requiring 4.5:1 contrast for most text and 3:1 for large text.
> — *“The baseline AA contrast standard is 4.5:1 for most text and 3:1 for large text (19px+ bold or 24px+ normal text).”* (U.S. General Services Administration (USWDS),
>   https://designsystem.digital.gov/design-tokens/color/overview/, read 20 August 2026)
>

---

## D - Typography and script parity

### D01 — Gap

**Claim:** Every candidate typeface claimed as evaluated appears as a measured row in the type data; the stated count equals the row count.

**Test:** assert len(candidates measured) == the number claimed in prose

**Baseline:** 05_type/README.md claims 29 candidate families compared; only specimens for 5 (4 rejected + Sora) ship as evidence.


### D02 — N/A

**Claim:** Bengali shaping is described accurately: Bengali is shaped by its own dedicated OpenType specification (the Indic shaping engine), not blanket-described as shaped 'via the Universal Shaping Engine (USE)'.

**Test:** grep the kit for 'Universal Shaping Engine' near 'Bengali' and check it is not stated as the shaper actually used

**Baseline:** The old kit does not currently make a claim about which shaping spec governs Bengali; this criterion guards against introducing the imprecise claim during the rebuild.

> The Universal Shaping Engine (USE) is a real, actively documented OpenType shaping specification (Microsoft Typography, last updated September 2024) that defines syllable clustering, conjunct formation (the 'cjct' feature) and glyph reordering (e.g. 'rphf'/'pref' for reph and pre-base forms) for complex scripts. By its own stated scope, it covers scripts not already handled by a dedicated shaping engine — it is not a universal replacement for every complex-script shaper.
> — *“complex scripts included in the Unicode Standard 16.0, but not otherwise supported by a dedicated shaping engine”* (Creating and supporting OpenType fonts for the Universal Shaping Engine,
>   https://learn.microsoft.com/en-us/typography/script-development/use, read 20 August 2026)
>
> Correction to a common assumption: Microsoft's own typography documentation gives Bengali its own separate, dedicated page ('Developing OpenType Fonts for Bengali Script'), which explicitly invokes 'the Indic shaping engine' — a distinct, older specification from USE. This matches USE's own stated scope (only for scripts without a dedicated shaper). Both specs describe similar mechanics (conjuncts, reph/matra reordering) using shared OpenType feature tags, but they are formally separate documents, so 'Bengali is shaped by USE' is not accurate as a blanket statement per this primary source.
> — *“Once the Indic shaping engine has analyzed the cluster as described above, it creates and manages a buffer”* (Developing OpenType Fonts for Bengali Script,
>   https://learn.microsoft.com/en-us/typography/script-development/bengali, read 20 August 2026)
>

### D03 — Gap

**Claim:** Bengali digit usage follows CLDR's own bn-BD convention (native ০-৯ digits, not Western 0-9), and this is stated as sourced from CLDR, not assumed.

**Test:** grep guidebook for a citation to CLDR bn_BD.xml near any digit-usage rule

**Baseline:** No CLDR citation currently exists for digit choice; confirmed CLDR source: bn (and bn_BD specifically) defaults to native Bengali digits, while bn_IN (India) explicitly overrides to Western digits -- a genuine country-level distinction worth stating precisely.

> CLDR's root/base 'bn' locale file sets the default numbering system to 'beng' (native Bengali digits ০-৯), not Western digits.
> — *“<defaultNumberingSystem>beng</defaultNumberingSystem>”* (CLDR common/main/bn.xml,
>   https://github.com/unicode-org/cldr/blob/main/common/main/bn.xml, read 20 August 2026)
>
> CLDR's likelySubtags data maps bare 'bn' to 'bn_Beng_BD' (Bangladesh), and the dedicated bn_BD.xml locale file itself contains no numbering/date overrides at all — it inherits everything, including the native-Bengali-digit default, from the root 'bn' data. This confirms native Bengali digits (০-৯) are CLDR's convention specifically for Bengali as used in Bangladesh.
> — *“<likelySubtag from="bn" to="bn_Beng_BD"/>”* (CLDR common/supplemental/likelySubtags.xml and common/main/bn_BD.xml,
>   https://github.com/unicode-org/cldr/blob/main/common/supplemental/likelySubtags.xml, read 20 August 2026)
>
> Yes — CLDR's 'bn_IN' locale file (Bengali, India) explicitly overrides the default numbering system to 'latn' (Western 0-9 digits), unlike the Bangladesh-default 'beng' (native digits). This is a genuine, sourced country-level distinction within CLDR, not an assumption.
> — *“<defaultNumberingSystem>latn</defaultNumberingSystem>”* (CLDR common/main/bn_IN.xml,
>   https://github.com/unicode-org/cldr/blob/main/common/main/bn_IN.xml, read 20 August 2026)
>

### D04 — Gap

**Claim:** The Latin-to-Bangla apparent-size multiplier is a measured figure (from real rendered ink), not an assumed ratio, and is published with the method stated.

**Test:** the type data file has a measured column, not just an asserted ratio

**Baseline:** No such multiplier is currently measured or published in the old kit.


### D05 — Meets

**Claim:** Every font's OFL status is checked against the licence's actual current terms (1.1, no 1.2, Reserved Font Name clause worded precisely), not a secondhand paraphrase.

**Test:** cross-reference each shipped font's licence claim against openfontlicense.org's own text

**Baseline:** The old kit's font licences already correctly cite OFL 1.1 (confirmed: there is no 1.2) and each shipped OFL.txt travels with its font.

> The current and only version of the SIL Open Font License is 1.1, dated 26 February 2007. No version 1.2 exists — the license's own site states it has not changed since 2007, and no '1.2' appears anywhere on the page.
> — *“the OFL itself has remained unchanged since 2007”* (SIL Open Font License — official site,
>   https://openfontlicense.org, read 20 August 2026)
>
> Yes — the license's own official text names openfontlicense.org as its own canonical home, in the standard copyright-header template every OFL font is meant to carry.
> — *“This license is copied below, and is also available with a FAQ at: https://openfontlicense.org”* (SIL Open Font License 1.1 — official text,
>   https://openfontlicense.org/open-font-license-official-text/, read 20 August 2026)
>
> A 'Reserved Font Name' is any name the copyright holder declares as such after the copyright statement. A Modified Version of the font may not use that Reserved Font Name without the copyright holder's explicit written permission — but this restriction applies only to the font's primary, user-facing name, not to internal/technical naming.
> — *“No Modified Version of the Font Software may use the Reserved Font Name(s) unless explicit written permission is granted by the corresponding Copyright Holder.”* (SIL Open Font License 1.1 — official text,
>   https://openfontlicense.org/open-font-license-official-text/, read 20 August 2026)
>

### D06 — N/A

**Claim:** Where a font used for comparison (e.g. Nikosh) has a disputed or unverifiable licence, the kit states the dispute rather than picking one claim to repeat as fact.

**Test:** grep for 'Nikosh' and confirm the licence is described as disputed/unverified if cited

**Baseline:** The old kit does not currently reference Nikosh; guard for if the typography research phase does.

> Secondary sources disagree on both the body behind Nikosh and its licence. A specialised Bangla web-font catalogue states its designers are named individuals and that the organisation behind it is 'the Election Commission of Bangladesh' (not the Bangladesh Computer Council), releasing it under 'Creative Common License, v3' — attribution required, non-commercial use only, no derivatives — which would contradict the widespread separate claim that Nikosh is freely usable for commercial and government work. Neither claim could be checked against a true primary document (an official licence file or a BCC/Election Commission statement) today, since BCC's own page was empty and no official licence text was located.
> — Nikosh | Bangla Web Fonts, https://fonts.maateen.me/nikosh/, read 20 August 2026
>

---

## E - Accessibility beyond contrast

### E01 — Gap

**Claim:** Every accessibility floor states the exact WCAG success criterion number it derives from, and platform-specific figures (Apple/Android) are attributed to the platform, not folded into a WCAG citation.

**Test:** every row in the accessibility table carries an SC id or a named platform, never neither

**Baseline:** DESIGN-RULES.md §5.1's target-size row ("24x24px minimum, 44x44px preferred") cites neither SC 2.5.8 nor a platform by name. Confirmed correct figures to cite: WCAG SC 2.5.8 = 24x24 CSS px; Apple HIG = 44x44pt default / 28x28pt minimum (iOS); Android = 48dp minimum -- three different numbers from three different authorities, never to be conflated.

> SC 2.5.8 (Level AA) requires pointer-input targets to be at least 24 by 24 CSS pixels, subject to five named exceptions (Spacing, Equivalent, Inline, User Agent Control, Essential).
> — *“The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when: Spacing”* (WCAG 2.2 — Success Criterion 2.5.8,
>   https://www.w3.org/TR/WCAG22/#target-size-minimum, read 20 August 2026)
>
> Confirmed as expected: iOS/iPadOS default control (tap target) size is 44x44 pt, minimum is 28x28 pt. The same 44x44/28x28 figures apply to watchOS; macOS uses 28x28pt default/20x20pt minimum (pointer-based); tvOS 66x66pt/56x56pt; visionOS 60x60pt default/28x28pt minimum.
> — *“iOS, iPadOS 44x44 pt 28x28 pt”* (Accessibility - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/accessibility, read 20 August 2026)
>
> Android's current design guidance states a minimum touch target size of 48dp.
> — *“Ensure all touch targets are at least 48 dp, even if this extends past the UI element visual.”* (Accessibility | Mobile | Android Developers,
>   https://developer.android.com/design/ui/mobile/guides/foundations/accessibility, read 20 August 2026)
>

### E02 — Untested (counts as a gap)

**Claim:** Apple-platform components meet Apple's own stated default and minimum control sizes, cited from the current HIG, not a remembered figure.

**Test:** the component spec states 44x44pt default / 28x28pt minimum, matching the current Buttons and Accessibility HIG pages

**Baseline:** Not directly checked against the old kit's component specs in this pass.

> Confirmed as expected: iOS/iPadOS default control (tap target) size is 44x44 pt, minimum is 28x28 pt. The same 44x44/28x28 figures apply to watchOS; macOS uses 28x28pt default/20x20pt minimum (pointer-based); tvOS 66x66pt/56x56pt; visionOS 60x60pt default/28x28pt minimum.
> — *“iOS, iPadOS 44x44 pt 28x28 pt”* (Accessibility - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/accessibility, read 20 August 2026)
>
> The Buttons page independently corroborates the 44x44pt figure as a general-rule hit region for any platform, calling out visionOS's larger 60x60pt figure as the exception.
> — *“As a general rule, a button needs a hit region of at least 44x44 pt — in visionOS, 60x60 pt — to ensure that people can select it easily, whether they use a fingertip, a pointer, their eyes, or a remote.”* (Buttons - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/buttons, read 20 August 2026)
>

### E03 — N/A

**Claim:** Where the kit claims Apple 'defers to WCAG' for contrast, this is stated precisely: Apple's Accessibility Inspector tool uses WCAG AA figures (4.5:1 up to 17pt, 3:1 at 18pt+ or any bold) -- it is not stated as a blanket 'Apple publishes no contrast standard at all'.

**Test:** grep the guidebook for any claim that Apple publishes no contrast figures anywhere, and correct it if so

**Baseline:** Refines the earlier verified-design-standards memory's claim that Apple 'publishes no contrast ratio for text' -- true of the Materials page specifically, false of the Accessibility page, which does cite WCAG AA via Accessibility Inspector. The precise claim is: no PROPRIETARY Apple ratio and none for materials/Liquid Glass specifically, but WCAG AA is cited generally.

> Apple's Accessibility HIG page (a general page, not the Materials page) is where a numeric contrast standard actually appears, and it explicitly defers to the third-party WCAG Level AA standard (as implemented in Apple's own Accessibility Inspector tool) rather than defining a proprietary Apple ratio: minimum 4.5:1 for text up to 17pt, 3:1 for 18pt+ or any bold text.
> — *“Accessibility Inspector uses the following values from WCAG Level AA as guidance in determining whether your app's colors have an acceptable contrast.”* (Accessibility - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/accessibility, read 20 August 2026)
>
> The table Apple publishes gives 4.5:1 as the minimum ratio for text up to 17pt (any weight), and 3:1 for 18pt text or any bold text of any size.
> — *“Up to 17 pts All 4.5:1 18 pts All 3:1 All Bold 3:1”* (Accessibility - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/accessibility, read 20 August 2026)
>
> No. The Materials HIG page gives only qualitative guidance for text-over-material legibility (use vibrant colors, choose thicker materials for more opaque contrast, thinner for context-visibility) with no numeric contrast ratio anywhere on the page. It does not reference WCAG or any ratio at all in the materials context.
> — *“Help ensure legibility by using vibrant colors on top of materials. When you use system-defined vibrant colors, you don't need to worry about colors seeming too dark, bright, saturated, or low contrast in different contexts.”* (Materials - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/materials, read 20 August 2026)
>

### E04 — Meets

**Claim:** Reduced motion is honoured, and where a duration or curve is stated as a GRU953 choice, it is not attributed to Apple or Google, since neither publishes a duration or named curve.

**Test:** grep for a millisecond figure or curve name within 15 words of 'Apple' or 'HIG'

**Baseline:** DESIGN-RULES.md §4 states its durations as GRU953's own choice, correctly, and does not attribute them to Apple. Confirmed: Apple's Motion HIG page contains no ms duration and no named easing curve at all -- the only numeric values on the page are a 30-60fps game frame-rate note and a 0.2Hz vestibular-safety caution, neither an animation timing spec.

> No. As expected, the dedicated Motion HIG page contains no millisecond duration values and no named easing-curve terminology (e.g. no 'ease-in-out', no cubic-bezier values, no spring-constant numbers) anywhere in its text. The one place 'easing' is mentioned, it is described only as an automatic, non-configurable system behavior with no name or timing value given.
> — *“All layout- and appearance-based animations automatically include built-in easing that plays at the start and end of the animation. You can't turn off or customize easing.”* (Motion - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/motion, read 20 August 2026)
>
> The only two numeric values on the Motion page are: (1) a game frame-rate recommendation of 30-60 fps, which is a rendering-performance target, not an animation duration or curve; and (2) a vestibular-comfort caution against oscillation near 0.2 Hz in visionOS, which is a perceptual-safety threshold, not a UI-animation timing spec. Neither answers the 'duration/easing curve' question in the affirmative.
> — *“In most games, maintaining a consistent frame rate of 30 to 60 fps typically results in a smooth, visually appealing experience.”* (Motion - Apple Developer Documentation (Human Interface Guidelines),
>   https://developer.apple.com/design/human-interface-guidelines/motion, read 20 August 2026)
>

### E05 — N/A

**Claim:** Where GRU953 cites Material's motion springs as a model (damping/overshoot behaviour), the actual published parameter values are cited, not an approximate description.

**Test:** grep for 'spring' near 'Material' and check numeric parameters are cited from source

**Baseline:** The old kit makes no such claim; guard for the rebuild. Confirmed values if cited: expressive spatial springs 0.6-0.8 damping (underdamped/bouncy), expressive effects springs 1.0 damping (critically damped) at every speed.

> M3 Expressive's motion physics system defines two spring styles — 'spatial' (position/size/rotation, designed to overshoot and bounce) and 'effects' (color/opacity, designed with no overshoot) — each available at three speeds (fast, default, slow) under two schemes (standard, expressive).
> — *“Spatial spring tokens are used for animations that move something on screen... This spring overshoots the final value and bounces into place. ... Effects spring tokens are used to animate properties such as color and opacity animations, where there shouldn't be any overshoot.”* (Motion – Material Design 3,
>   https://m3.material.io/styles/motion/overview/how-it-works, read 20 August 2026)
>
> Google's own AndroidX source (androidx.compose.material3.tokens, generated version v0_14_0) confirms this exactly: expressive spatial springs use damping ratios of 0.8 (default), 0.6 (fast) and 0.8 (slow) — all below 1.0, i.e. underdamped/bouncy — while expressive effects springs use damping ratio 1.0 (critically damped, no overshoot) at every speed; the standard scheme uses 0.9 for all spatial speeds and 1.0 for all effects speeds, with stiffness values ranging 200–3800.
> — *“const val SpringDefaultSpatialDamping = 0.8f ... const val SpringDefaultEffectsDamping = 1.0f ... const val SpringFastSpatialDamping = 0.6f”* (ExpressiveMotionTokens.kt - Android Code Search,
>   https://cs.android.com/search?q=file:ExpressiveMotionTokens.kt&ss=androidx, read 20 August 2026)
>

### E06 — Untested (counts as a gap)

**Claim:** lang is declared on every Bangla passage inside an English page, and this is stated as the single highest-value accessibility line for a bilingual brand -- and it is actually true in the shipped markup, not just claimed.

**Test:** grep every HTML output for Bangla codepoints outside a lang="bn" scope

**Baseline:** DESIGN-RULES.md §5.3 claims this; not directly re-verified against the shipped guidebook markup in this pass.


---

## F - Voice, language and bilingual parity

### F01 — Gap

**Claim:** Every worked example in the voice guide uses real GRU953 artefacts (real error messages, real byte counts, real history) rather than an invented product and invented figures.

**Test:** grep 02_strategy/VERBAL-IDENTITY*.md for the word 'Ledger' or other invented-example markers

**Baseline:** VERBAL-IDENTITY.md sections 1, 2, 3 and 6 are built on an imaginary app 'Ledger' with invented figures, self-flagged in the document's own preamble but not marked inline at each occurrence.


### F02 — Gap

**Claim:** No example changelog or version history reads as real (no real-looking dated headings), matching the kit's own stated position that it has no changelog.

**Test:** grep for version-number-shaped headings with dates

**Baseline:** VERBAL-IDENTITY.md contains example headings '## 2.4.1 -- 8 August 2026' and '## 2.5.0 -- 3 September 2026' (the second in the future relative to the kit's own build date) that read as real history despite BRAND-SPEC.md stating the kit has none.


### F03 — Gap

**Claim:** Every sentence containing a number resolves to a computed source (tokens, measurements, findings) or is explicitly marked unverified -- no invented number anywhere.

**Test:** every numeric sentence in hand-written prose is cross-referenced against a data file

**Baseline:** The 22.46% squircle claim is the flagship instance; VERBAL-IDENTITY.md's invented figures are a second, broader instance of the same failure mode.


### F04 — Partial

**Claim:** Concrete, testable content rules exist underneath the voice principles (banned words, sentence patterns, numeric caps), the way Atlassian's and GOV.UK's do -- not principles alone.

**Test:** count concrete Do/Don't rules with a specific trigger (a word, a number, a construction) in the voice guide

**Baseline:** VERBAL-IDENTITY.md has some concrete rules (word lists) but fewer structural ones (sentence-length caps, list-length caps) than Atlassian's page has. Note: the widely-quoted GOV.UK 'reading age 9' figure could NOT be confirmed on GOV.UK's own current primary guidance -- do not cite it as a GOV.UK standard if referencing this model.

> Yes — underneath the principle layer, Atlassian's Style, grammar and punctuation page gives dozens of concrete, testable Do/Don't rules: mandatory sentence case (not Title Case) in headings/buttons, mandatory active voice, present tense preferred, no periods in headings, an Oxford comma requirement, exact keyboard shortcuts for curly quotes/em dashes, and banned constructions such as 'e.g.', 'i.e.', 'etc.' and '&'. This is the same operational register as GOV.UK's style guide, not just principles.
> — *“Don't use 'e.g.', 'i.e.', 'etc.', or '&' as they're not localization friendly and can be confusing for users of assistive technologies.”* (Atlassian,
>   https://atlassian.design/content/language-and-grammar/, read 20 August 2026)
>
> Atlassian mandates active voice as a hard rule tied explicitly back to brand voice, with a worked Do/Don't pair, not left as a vague preference.
> — *“Use active voice whenever possible as it improves readability and reflects Atlassian's voice and tone.”* (Atlassian,
>   https://atlassian.design/content/language-and-grammar/, read 20 August 2026)
>
> Atlassian caps list length as an explicit numeric rule rather than a vague guideline.
> — *“Try to limit lists to 6 items or less. If there are more items, make multiple lists.”* (Atlassian,
>   https://atlassian.design/content/language-and-grammar/, read 20 August 2026)
>
> The current (checked today) official GOV.UK content and publishing guidance page on plain language does NOT state a numeric target reading age. Instead it mandates plain English generally and gives concrete, quantified structural rules: paragraphs of no more than 5 sentences, and splitting sentences longer than 25 words. The widely-repeated 'reading age of 9' figure was not found on this current primary page — it appears mainly on secondary/derivative sources (see could_not_verify).
> — *“Plain English is mandatory for all of GOV.UK. [...] Paragraphs should have no more than 5 sentences each. Try to split up sentences that are over 25 words long.”* (Use clear language – GOV.UK content and publishing guidance,
>   https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/, read 20 August 2026)
>

### F05 — Gap

**Claim:** Bangla is written natively for every string that ships, verified against the actual Bangla Academy standard edition that can be dated and sourced (the 2012 revised edition, reprinted January 2015, is the most recent confirmed edition) -- not against an undated web summary.

**Test:** every cited spelling rule names the edition and, where possible, a page

**Baseline:** No edition citation currently exists in the old kit's Bangla content.

> An archival scan of the actual Bangla Academy publication (not a summary) shows its title page reading "পরিমার্জিত সংস্করণ ২০১২" (Revised Edition 2012), with this particular copy being the "পরিমার্জিত সংস্করণ প্রথম পুনর্মুদ্রণ" (first reprint of the revised edition), dated Magh 1421 of the Bengali calendar / January 2015.
> — *“বাংলা একাডেমি প্রমিত বাংলা বানানের নিয়ম (পরিমার্জিত সংস্করণ ২০১২) — পরিমার্জিত সংস্করণ প্রথম পুনর্মুদ্রণ — মাঘ ১৪২১/জানুয়ারি ২০১৫”* (বাংলা একাডেমি প্রমিত বাংলা বানানের নিয়ম (Internet Archive item page, viewed directly),
>   https://archive.org/details/bangla-academy-promito-bangla-bananer-niyom-2015, read 20 August 2026)
>
> A separate, distinct archive.org item titled "Bangla Academy Pramita Bangla Bananer Niyam" is dated 1992 and self-describes as "Standard Bengali spelling as laid out by the Bangla Academy, Dhaka." This is the earliest dated copy of the document I could directly access and read today; the page itself does not state whether 1992 was the very first edition or already a reprint of an earlier one.
> — *“Publication date 1992 ... Standard Bengali spelling as laid out by the Bangla Academy, Dhaka”* (Bangla Academy Pramita Bangla Bananer Niyam (Internet Archive item page, viewed directly),
>   https://archive.org/details/banglaacademybanan, read 20 August 2026)
>

### F06 — N/A

**Claim:** Every Bangla string's approval is dated after that string's last edit -- editing a string silently invalidates its prior approval.

**Test:** the Bangla review data has an approval timestamp newer than the string's edit timestamp for every entry

**Baseline:** No Bangla review mechanism exists yet in the old kit.


---

## G - Sourcing and verifiability

### G01 — Gap

**Claim:** Every numeric claim attributed to an external party carries a verbatim quoted line from a primary source read on a stated date.

**Test:** cross-reference every external numeric claim in the guidebook against findings.json

**Baseline:** This is the rule the 22.46% squircle claim violated -- no such cross-reference exists in the old kit at all.


### G02 — Partial

**Claim:** Every external URL cited in the kit returns 200 on the day of the build.

**Test:** a link-liveness check over every .md/.html/.py/.json file

**Baseline:** 01_research/RESEARCH.md's own PolyForm URL is correct (no trailing slash); the trailing-slash 404 form survives only in the _to_delete archive, now moved to the attic, not the shipping kit -- corrected finding from an earlier over-broad claim of mine.


### G03 — N/A

**Claim:** A claim of 'inferred' confidence (a structural observation with no formal spec, e.g. Meta's brand architecture) is labelled as such in the same sentence as the claim, never presented with the same certainty as a quoted standard.

**Test:** grep for Meta-attributed claims and confirm each carries an inferred/observed qualifier

**Baseline:** Guard for the Meta section of the new benchmark prose, once written.

> Meta operates a single 'Brand Resource Center' microsite that is explicitly organised product-by-product — Meta, Facebook, Instagram, WhatsApp and Threads each have their own separate named guidelines page for logo, colour and usage — read live today, confirming a 'house of brands' architecture (separately governed sub-brands) rather than one umbrella visual identity stamped across all products.
> — Meta brand resources and guidelines | Brand Resource Center, https://about.meta.com/brand/resources/meta/company-brand/, read 20 August 2026
>
> What Meta publishes for its own corporate logo, read live today, is a brand book — colour variants, minimum size, clear space, a gated internal 'Brand Review' approval process, and trademark legal terms — with no components, design tokens or code of any kind, i.e. the opposite of an engineering design system.
> — *“never be used below 12px/5mm”* (Meta brand resources and guidelines | Brand Resource Center,
>   https://about.meta.com/brand/resources/meta/company-brand/, read 20 August 2026)
>

### G04 — N/A

**Claim:** Where a widely-repeated secondary claim could not be confirmed on a primary source (e.g. GOV.UK's 'reading age of 9'), the kit says so explicitly rather than repeating the popular figure as fact.

**Test:** grep for 'reading age' near 'GOV.UK' and confirm it is marked unconfirmed if present

**Baseline:** Guard for if the plain-language chapter cites this figure.

> The current (checked today) official GOV.UK content and publishing guidance page on plain language does NOT state a numeric target reading age. Instead it mandates plain English generally and gives concrete, quantified structural rules: paragraphs of no more than 5 sentences, and splitting sentences longer than 25 words. The widely-repeated 'reading age of 9' figure was not found on this current primary page — it appears mainly on secondary/derivative sources (see could_not_verify).
> — *“Plain English is mandatory for all of GOV.UK. [...] Paragraphs should have no more than 5 sentences each. Try to split up sentences that are over 25 words long.”* (Use clear language – GOV.UK content and publishing guidance,
>   https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/, read 20 August 2026)
>

### G05 — N/A

**Claim:** A claim about Meta's design-system practice acknowledges Astryx (Meta's own newly public design system, beta since 18 June 2026) rather than asserting Meta publishes nothing comparable to Apple's or Google's design system.

**Test:** grep for any absolute claim that Meta publishes no design system

**Baseline:** IMPORTANT CORRECTION to this rebuild's own planning assumption: Meta DOES now publish a real, public, open-source design system (Astryx, 150-170+ components, in Beta since 18 June 2026). It is explicitly brand-neutral/white-label, not an expression of Facebook/Instagram/WhatsApp's own visible identity the way HIG/Material are -- so the comparison to Apple/Google must be nuanced (Meta has a design system now, but not one that codifies its own product brand identity), not simply asserted absent.

> Contrary to the assumption that Meta publishes nothing comparable, Meta does now publish a genuine public, open-source design system called Astryx (astryx.atmeta.com), which went into Beta on 18 June 2026 and, read live today, documents 150-170+ accessible React components, design tokens, themes, templates and a CLI — a real engineering-contract design system in the technical sense.
> — *“matured within Meta for the last eight years and powers over 13,000 apps”* (Introducing Astryx by Meta: an open source design system built for how we build now,
>   https://astryx.atmeta.com/blog/introducing-astryx, read 20 August 2026)
>
> Astryx's own launch post, read live today, explicitly frames itself as brand-neutral, white-label tooling and frames the alternative — adopting a 'big company' system — as the problem it was built to avoid; this means Astryx is not analogous to Apple's HIG or Google's Material as a public codification of the parent's own visible product identity, it is a generic engineering toolkit Meta happens to have open-sourced.
> — *“your app ends up looking like someone else's product”* (Introducing Astryx by Meta: an open source design system built for how we build now,
>   https://astryx.atmeta.com/blog/introducing-astryx, read 20 August 2026)
>

---

## H - Engineering and reproducibility

### H01 — Meets

**Claim:** Every mechanical gate runs to completion on the owner's own machine from a clean checkout.

**Test:** sh 00_sandbox/setup.sh && sh scripts/verify-all.sh exits 0

**Baseline:** As of this rebuild's Phase 1 (20 Aug 2026): sh 00_sandbox/setup.sh builds cleanly, smoke.py passes all 8 tools with a real job each, and scripts/no-system-path.sh proves no hidden dependency. Verified on this Mac and on GitHub's Ubuntu CI runner.


### H02 — Meets

**Claim:** design-system/check.mjs -- the only check that renders and measures the actual cards -- runs in CI on every push, not just locally by chance.

**Test:** CI job list includes a step calling design-system/check.mjs

**Baseline:** Fixed in this rebuild's Phase 1: wired into .github/workflows/brand.yml job 5. First-ever run: 27 cards, 4 widths x 2 schemes, 216 renders, no findings.


### H03 — Gap

**Claim:** No generated file contains an absolute path, a timestamp, or a random value.

**Test:** scan every generated file for date-shaped strings and absolute filesystem paths

**Baseline:** 03_logo/marks.py and lockups.py hardcoded /home/claude/GRU953_Branding/00_sandbox; 04_colour/engine.py hardcoded a GRU953_Build/ path. Fixed in this rebuild's Phase 0 (fork resolution) for the repo copy; root copy retired to the attic.


### H04 — Gap

**Claim:** Any figure produced by a single rasteriser is confirmed by a second, independent rasteriser before being published as fact.

**Test:** the mark/asset build runs under two renderers and diffs the result

**Baseline:** The old kit's counter-survival check runs under one renderer only.


### H05 — Meets

**Claim:** The build works with the system PATH stripped to the minimum needed, and with no fonts installed anywhere on the host, proving no hidden dependency on what merely happens to be on this machine.

**Test:** sh scripts/no-system-path.sh exits 0

**Baseline:** Built and verified in this rebuild's Phase 1, on both this Mac and GitHub's Ubuntu CI runner -- the hermetic gate caught a real CI configuration bug on its first run anywhere, which was then fixed.


---

## I - Honest limits

### I01 — Gap

**Claim:** The kit states plainly that it has had no user research, in contrast to Material 3 Expressive's stated 46 studies / 18,000+ participants, and that this is Google's own unaudited figure with no published methodology.

**Test:** the guidebook's limits chapter states both figures side by side

**Baseline:** No such comparison exists in the old kit yet.


### I02 — Meets

**Claim:** The kit never uses an unmeasurable superlative ("gold standard", "world-class", "industry-leading") about itself.

**Test:** grep the whole tree for these phrases applied to GRU953

**Baseline:** No such phrase currently appears in the old kit's own self-description.


---

## What could not be verified

Stated rather than silently dropped, grouped by research stream:

**apple-hig**
- Whether Apple maintains any non-public, internal brand governance book (identity/voice/architecture) cannot be verified either way from public sources — only its absence from Apple's public-facing pages was confirmed.
- The dedicated Icon Composer sub-page of the HIG (developer.apple.com/design/human-interface-guidelines/icon-composer) was not independently opened in this session; the Icon Composer findings above are sourced from its treatment on the App Icons overview page, which is a primary source but may not be the most detailed available page on that specific tool.
- No official Apple definition/formula for what distinguishes 'clear light' from 'clear dark' or 'tinted light' from 'tinted dark' beyond their listing in the App Icons specifications table was found in the pages read; the underlying rendering logic for each variant was not detailed on the pages retrieved.
- Whether any Apple developer-only (Apple ID/NDA-gated) documentation contains numeric animation durations or named easing curves could not be checked, since this research was limited to publicly accessible HIG pages.

**material-3**
- Could not access or verify the content of Google's gated internal 'Brand Standards' site (agency-only, requires a Google contact for access), so whether it constitutes a full identity/voice governance brand book beyond the public trademark-permission guidance could not be confirmed.
- Did not check whether background/onBackground/surfaceVariant carry a 'deprecated' tag in the older XML/View-based Material Components for Android (non-Compose) documentation — only the current Jetpack Compose Material3 ColorScheme API reference was checked and read.
- Could not find a GitHub Releases-based version/date for material-color-utilities beyond its raw commit history, since the repository does not use GitHub's Releases feature ('There aren't any releases here').
- Did not directly load the standalone web tool at material.io/theme-builder to confirm it is still functionally live (only its GitHub source, now archived, and its Figma plugin listing, still published, were checked).

**meta-architecture**
- Whether Astryx's 170+ components, or the Meta Horizon OS design-system components, are actually used to build Meta's own production consumer apps (Facebook, Instagram, WhatsApp) or are used only for internal tools and third-party/external adopters — no primary source found either confirming or denying this, so no claim is made about Astryx being 'the design system behind Facebook/Instagram/WhatsApp's own UI.'
- The detailed internal criteria and turnaround time of Meta's 'Brand Review' approval process for third-party use of the Meta or product logos — the Brand Resource Center references this process but gates the actual workflow behind an internal Meta contact, so its substance could not be verified from a public primary source.
- Whether there is a single dedicated Meta newsroom post explicitly announcing the exact date app-store/marketing copy switched wording from 'from Facebook' (2019 convention) to 'from Meta' (current convention) — the 2021 rename announcement and founder's letter cover the corporate rename narratively, but no primary source pinpointing the exact copy-change date was found.
- The explicit business rationale, in Meta's own words, for why Threads is credited to 'Instagram, Inc.' on app stores rather than to 'Meta Platforms, Inc.' or given a 'from Meta' tag — this tiering is an observed structural pattern, not one Meta has explained in a primary source.
- Whether Meta has published, anywhere, a single unified visual/brand-architecture diagram or policy document that names and ranks its own endorsement tiers (e.g. flagship vs. acquired vs. sub-product) — no such consolidated primary-source document was found; the tiering described in these findings is inferred from comparing several separate live listings and pages side by side.

**carbon-spectrum**
- Whether Carbon's DTCG migration is complete across every token package (e.g. spacing, typography, color-for-data-visualization) as of 20 August 2026 — I directly confirmed live DTCG-format files only for the motion package and the themes (color) package; other packages were not individually checked.
- Whether spectrum.adobe.com's public documentation site hosts a live, interactive preview of an actual Windows High Contrast theme (as opposed to the written guideline and the per-component visual references it promises) — no such interactive page appears among the 114 URLs in the site's own sitemap, but I could not rule out an unindexed or in-app-only preview.
- The exact current completion percentage or version number of Carbon's DTCG rollout (e.g. whether it is still labelled 'experimental' internally) — no versioned status page was found; status was inferred only from issue/PR open-closed states on GitHub.

**primer-atlassian-radix-uswds**
- Primer's dedicated 'design token naming guidelines' page (linked from the Color usage page) was not opened directly today, so the full formal naming-convention rulebook (beyond what the Color usage and Color/CSS-variables pages already state) is not independently confirmed.
- Atlassian's internal word list/glossary ('go/vocab') is explicitly restricted to Atlassian staff, so its actual banned/approved word content could not be checked from any public source today.
- Whether Radix Colors publishes any additional per-hue technical construction notes (e.g. exact APCA methodology or perceptual-uniformity math) beyond the use-case table was not fully explored — only the palette-composition/understanding-the-scale page was read in depth.
- The exact live URL path for the USWDS page read today could not be pinned down with certainty — the browser's reported address bar value stayed generic (designsystem.digital.gov root) even after navigating to a specific /design-tokens/color/overview/ path, though the returned page title and content ('Using color | U.S. Web Design System (USWDS)') match the intended primary source.
- Could not confirm whether USWDS has published any newer color-token naming scheme replacing 'grade' terminology beyond the 2022-06-03 and 2021-12-29 changelog entries shown on the page itself.

**mozilla-wikimedia-antdesign-govuk**
- Whether GOV.UK has ever officially stated, or currently states on any live page, a specific 'reading age of 9' standard. This figure is widely repeated by secondary/derivative sources (Home Office User-Centred Design Manual, ONS style guide, and a 2016 Government Digital Service blog post) but was not found today on GOV.UK's current core content-design guidance pages (guidance.publishing.service.gov.uk) that were checked directly, so it should not be attributed to GOV.UK's current primary standard as fact.
- Whether Codex genuinely ships two separate direction-specific stylesheets (codex.style.css and codex.style-rtl.css) as claimed in some secondary summaries — this was surfaced only via an AI-summarised web search result and was not confirmed by directly reading the exact sentence on a Wikimedia primary page today.
- Whether every component and pattern in the GOV.UK Design System (beyond the two checked — Accordion and Character count) carries a 'Research on this component' section in the same format; only a sample of two was directly verified today.
- Whether Ant Group (the parent company, as distinct from the open-source Ant Design project) maintains a separate, non-public corporate brand book; only public-facing sources were checked, so a private internal Ant Group brand book cannot be ruled out.
- Exact current version number and full page-by-page contents of the 'Voice & Tone' and 'Overview' documents inside Mozilla's brand.mozilla.com Firefox Brand portal — confirmed to exist and be public via the site's own API, but their prose content could not be read directly because the rendered page crashed in this browser session (a client-side JS bug in the Frontify-hosted portal), so only page titles/structure were confirmed, not the full guideline text.

**wcag-aria-iso-unicode-ofl**
- Which shaping engine current production text-rendering libraries (e.g. HarfBuzz) actually route Bengali through today — the legacy 'Indic' shaper or the Universal Shaping Engine (USE) — could not be confirmed from a primary source; harfbuzz.github.io returned a 404 today and no alternate primary HarfBuzz doc was checked.
- The full wording of ISO 24495-1:2023's guideline text under each of the four principles (the body of clause 5, sub-clauses 5.1-5.4) is behind ISO's paywall (CHF 135) and could not be read today; only the principle names and their order, visible in ISO's own free table-of-contents preview, were verified.
- Whether the WAI-ARIA Authoring Practices Guide carries any formal W3C document-status label (e.g. 'Working Group Note') could not be confirmed — no such label appeared on the About page or the Accordion pattern page fetched today; it presents as a continuously-updated, non-versioned WAI resource rather than a dated TR-track publication like WCAG.

**bangla-academy-standard**
- Whether any edition of প্রমিত বাংলা বানানের নিয়ম newer than the 'Revised Edition 2012' (reprinted January 2015) exists — I found no dated primary or archival source confirming a later revision despite searching Bangla Academy's own site, booksellers (Rokomari), and forums; absence of evidence is not proof none exists.
- Whether the 1992 archive.org copy of the rules is the actual first-ever edition, or itself a later printing of an earlier (commonly cited but unconfirmed) 1988 draft/workshop version — secondary sources mention a 1988 Cumilla workshop under Anisuzzaman's editorship as a precursor, but I could not verify this lineage from a primary document today.
- Which specific topics — খণ্ড ত (khanda-ta), চন্দ্রবিন্দু (chandrabindu), numeral conventions, or দাঁড়ি-vs-period punctuation — the 2012 revised edition's rules explicitly cover or omit. I could confirm the document's title, edition and date from its cover, but every attempt to retrieve its OCR'd full body text from archive.org (direct download of the _djvu.txt and _hocr_searchtext.txt.gz derivatives, via both curl and Python, following the site's own redirect chain) returned 404 errors today, so I could not read the actual rule content to answer this.
- The exact designation, scope and current status of the Bangladesh national Bengali keyboard standard, commonly cited in secondary sources as 'BDS 1738:2004' (developed by Bangladesh Computer Council, declared by the Bangladesh Standards and Testing Institution) and a later revision cited as 'BDS 1738:2018'. I could not confirm either designation from BCC's or BSTI's own site, since BCC's 'Standards Development' page returned no body content when I loaded it today, and I did not locate a BSTI primary document.
- The Nikosh font's true originating body (Bangladesh Computer Council vs. Election Commission of Bangladesh, per conflicting secondary sources) and its exact licence terms (variously claimed as SIL Open Font License, Creative Commons BY-NC-ND v3, or GPL v3 across different secondary sources) — no official licence file or government statement was accessible to resolve this.
- Whether BCC currently publishes any accessible technical specification document at all (a keyboard-layout diagram, font files with embedded licence metadata, or a formal standards register) — its own 'Standards Development' page was an empty stub when accessed today, so I cannot confirm what, if anything, BCC currently makes available in this area beyond its page's mere existence.

