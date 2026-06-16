# 3Chillies — ASO Metadata Package (Apple App Store, en-US)

App: **3Chillies** — spicy/hot Mexican food recipe app.
Features: recipe browser, step-by-step guides, built-in cooking timer.
Date: 2026-06-16. Platform: iOS. Locale: en-US.

> Apple publishes no official search-volume data. Validate this keyword set against
> Apple Search Ads keyword popularity (5–100) in App Store Connect before submitting.

---

## Subtitle (limit 30)

**Recommended:** `Spicy Mexican recipes & more` — 28/30

Alternatives:
- `Spicy Mexican recipes & meals` — 29/30
- `Hot Mexican cookbook & timer` — 28/30 (leans into the "timer" feature + "cookbook" keyword)

Indexed subtitle tokens add: spicy, mexican, recipes, meals/cookbook/timer.
(Don't repeat any of these in the keyword field.)

---

## Keywords (limit 100, comma-separated, NO spaces)

```
taco,burrito,salsa,enchilada,fajita,chili,jalapeno,guacamole,nacho,dinner,easy,cooking,authentic,hot
```
100/100. Rules applied: singular forms, no spaces after commas, no duplicates of
title ("3Chillies") or subtitle words (spicy, mexican, recipes), no "app/free/cooking-app"
filler, no competitor brand names.

Token strategy:
- **Dish names** (taco, burrito, salsa, enchilada, fajita, guacamole, nacho) — high-intent,
  high-volume searches; how people actually look for Mexican food.
- **Heat words** (chili, jalapeno, hot) — reinforce the spicy niche and differentiate.
- **Modifiers** (dinner, easy, authentic, cooking) — combine into long-tail:
  "easy tacos", "authentic mexican dinner", "easy enchilada recipe".

If ASA shows low popularity for any token, swap candidates: `mole,quesadilla,tex mex,
salsa verde,spicy food,street food,carnitas,chipotle`.

---

## Promotional text (limit 170, editable anytime without app update)

```
Craving real Mexican heat? 3Chillies brings authentic spicy recipes to your kitchen with step-by-step guides and built-in timers. No ads, no signup, 100% free.
```
159/170. Not keyword-indexed — written to convert. Rotate it seasonally
(Cinco de Mayo in May, Taco Tuesday pushes, holiday gatherings).

---

## Description (limit 4,000; not keyword-indexed on iOS — written for conversion)

```
3Chillies is your pocket guide to bold, authentic Mexican cooking — the spicy way. From sizzling fajitas to fiery salsas, every recipe is built to bring real Mexican heat to your kitchen.

Whether you're a first-timer or a chili-head chasing the next level of spice, 3Chillies walks you through every dish with clear, foolproof steps.

BROWSE & DISCOVER
Flip through a vibrant recipe browser packed with tacos, burritos, enchiladas, salsas, fajitas and more. Find your next meal in seconds.

COOK STEP BY STEP
Every recipe is broken into clear, numbered steps. No confusing walls of text — just follow along from prep to plate and get it right the first time.

BUILT-IN COOKING TIMER
Nail the timing on every dish. Start the timer right inside a recipe so nothing burns while you're chopping, stirring, or grabbing the next ingredient.

PICK YOUR HEAT
From mild and family-friendly to three-chili scorchers, choose recipes that match your spice tolerance — or push your limits.

WHY 3CHILLIES
• Authentic, spicy Mexican recipes
• Easy-to-follow step-by-step guides
• Built-in cooking timer
• Fast, visual recipe browser
• No ads, no account, no data collection — 100% free

Spice up dinner tonight. Download 3Chillies and start cooking real Mexican food with confidence.
```
1,270/4,000 chars. Plenty of headroom to add feature sections (favorites, shopping
list, etc.) as the app grows.

---

## Notes for App Review (App Store Connect → App Review Information → Notes)

```
Thank you for reviewing 3Chillies.

3Chillies is a Mexican food recipe app. Users can browse recipes, follow step-by-step cooking guides, and use a built-in cooking timer.

KEY FACTS FOR REVIEW:

1. NO DATA COLLECTION — The app does not collect, store, or transmit any user information. There is no account, login, registration, or analytics/tracking SDK. The privacy nutrition label is "Data Not Collected." All app data stays on the device.

2. NO ADVERTISING — The app shows no ads and includes no advertising SDKs or ad networks.

3. COMPLETELY FREE — No paid subscriptions, no in-app purchases, and no locked or premium content. Every recipe and feature is available immediately after install.

4. NO ACCOUNT NEEDED TO TEST — No demo credentials required. All functionality is accessible on first launch.

HOW TO TEST:
- Recipe browser: scroll the main screen to browse recipes.
- Step-by-step guide: open any recipe and follow the numbered steps.
- Timer: start the cooking timer from within a recipe.

Please contact us at the support email on file with any questions. Thank you!
```

Consistency requirements (these claims must match the rest of the submission):
- Set the privacy nutrition label to **"Data Not Collected"** (answer "No" in the
  App Privacy questionnaire).
- A privacy policy URL is still **mandatory** even with zero data collection — a
  one-page "this app collects no data" statement satisfies it.
- Audit bundled SDKs — if any third-party library (crash reporter, analytics)
  collects data, the "Data Not Collected" label becomes inaccurate (rejection risk).

---

## Category & quick notes
- **Primary: Food & Drink** (correct + low-scrutiny → fast review).
- **Secondary: Lifestyle.**
- Title stays `3Chillies` (brand). If you ever want keyword lift in the title,
  `3Chillies: Mexican Recipes` (26/30) would help, but the brand-only name is fine.
- Screenshots: first frame = a finished spicy dish (appetite appeal); then step-by-step
  view, timer-in-recipe, heat-level picker. Captions large and top-aligned.
