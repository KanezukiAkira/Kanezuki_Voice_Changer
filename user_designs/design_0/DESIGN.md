---
name: Aura Voice
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 20px
  container-max: 1440px
---

## Brand & Style

The design system is engineered for a high-performance, premium AI voice transformation environment. It targets professional content creators, streamers, and enthusiasts who require a sophisticated, low-latency interface. 

The aesthetic is rooted in **Futuristic Glassmorphism**. It leverages deep spatial layers, vibrant background blurs, and luminous accents to evoke a sense of advanced technology. The interface must feel like a precision instrument—fast, reliable, and cutting-edge. High-contrast neon accents provide clear visual feedback and highlight monetized features or premium actions within the desktop environment.

## Colors

The palette is anchored in deep, cinematic blues and slates to reduce eye strain during long production sessions.

- **Primary & Secondary:** A gradient of Neon Blue (#3b82f6) and Violet (#8b5cf6) is used for active states, primary CTAs, and brand-defining moments like AI processing indicators.
- **Backgrounds:** The foundation uses Deep Slate (#0f172a). Overlays and container surfaces utilize Navy (#1e293b) with 60-80% opacity to facilitate glassmorphic effects.
- **Accents:** Tertiary Emerald (#10b981) is reserved for success states and "Live" status indicators.
- **Ad Spaces:** Designated advertisement zones should utilize a slightly lifted slate background (#334155) to distinguish them from functional UI while maintaining visual harmony.

## Typography

This design system utilizes **Inter** exclusively to ensure maximum legibility and a clean, systematic appearance. 

- **Hierarchy:** Use `headline-xl` for main dashboard titles. `label-md` is intended for small technical metadata like "KHÔNG GIAN TÊN" or "TẦN SỐ LẤY MẪU".
- **Weight:** Use Semi-Bold (600) for interactive elements and Regular (400) for descriptive body text.
- **Localization:** Vietnamese diacritics must be carefully monitored for vertical alignment; Inter’s tall x-height and generous metrics handle these requirements effectively.

## Layout & Spacing

This design system follows a **12-column fluid grid** for the main dashboard content, with a fixed sidebar for primary navigation.

- **Sidebar:** Fixed width of 260px.
- **Margins:** Desktop views use 40px (lg) margins to allow the background gradients to breathe.
- **Rhythm:** An 8px linear scale is the standard. Use 16px (sm) for internal card padding and 24px (md) for spacing between major UI blocks.
- **Ad Integration:** Ad banners should be contained within standard grid widths (e.g., spanning 4 or 12 columns) and must respect the standard container padding to appear as integrated "sponsored" content rather than intrusive pop-ups.

## Elevation & Depth

Depth is achieved through **Glassmorphism** and luminosity rather than traditional drop shadows.

- **Surface Tiers:** Background is the lowest tier. Cards sit on Tier 1 with a `backdrop-filter: blur(12px)`.
- **Outlines:** Every elevated card or menu must have a 1px solid border using `rgba(255, 255, 255, 0.1)`. The top and left edges should use a slightly brighter stroke to simulate a light source.
- **Glows:** Active states (like a voice being "ON") should use an outer glow (`box-shadow`) matching the primary color with a 20px blur and 0.4 opacity.
- **Ad Separation:** Ad containers should have a 0px blur and a solid background to subtly signal they are external to the core AI utility.

## Shapes

The shape language is sophisticated and approachable. 

- **Standard Containers:** Cards, modals, and large panels use a 12px (`rounded-lg`) radius.
- **Inputs & Small Buttons:** Use an 8px radius to maintain a precise, technical feel.
- **Status Indicators:** Use circular (pill) shapes for "Live," "Recording," or "AI Ready" badges.

## Components

### Buttons & Controls
- **Primary Action:** Solid Neon Blue to Violet gradient background with white text. On hover, increase brightness and add a 15px glow.
- **Secondary Action:** Ghost style with a 1px border. On hover, fill with `rgba(255, 255, 255, 0.05)`.
- **Sliders:** The track should be a thin 4px dark line. The "thumb" should be a 16px glowing circle in the primary accent color.

### Input & Selection
- **Dropdowns:** Semi-transparent Navy background (#1e293b) with a 12px blur. List items should have a 4px radius hover state using Primary Blue at 15% opacity.
- **Input Fields:** Darker than the card background to create an "inset" feel, with an 8px radius.

### Voice Profile Cards
- Large glassmorphic panels displaying the AI model name, a waveform visualization, and a "Select" button. Include a subtle gradient mesh background for "Premium" models to distinguish them from standard ones.

### Ad Units
- **Sponsored Slot:** Standardized containers for 728x90 or 300x250 placements. They must be labeled with "Tài trợ" in `label-md` typography and use a distinct, non-blurred background to meet readability standards for third-party content.

### Audio Visualizers
- Real-time frequency bars using a vertical gradient from Primary Blue to Secondary Violet. Use rounded caps on the bars for a softer, more modern look.