# Fish'n Cook — ASO Plan (Apple App Store, en-US)

App: **Fish'n Cook** — fish & seafood cookbook with recipes.
Date: 2026-06-12. Platform: iOS. Locale: en-US.

> Note on data: Apple publishes no official search-volume numbers. Volume/competition
> ratings below are qualitative estimates based on live competitive research
> (App Store listings surfaced via web search) and category knowledge. Validate with
> Apple Search Ads popularity scores once you have an App Store Connect account —
> ASA keyword popularity (5–100) is the only first-party volume signal available.

---

## 1. Market position & strategy

The dedicated fish/seafood recipe niche on iOS is shallow:

| Competitor | Type | State |
|---|---|---|
| Fish Recipes for You! | direct | dated (~2017), thin content, weak metadata |
| Easy Fish – Healthy Sea Foods | direct | dated (~2017), low rating volume |
| Seafoodopedia | adjacent | species reference guide, not a cookbook |
| Tasty, BigOven, Paprika, Epicurious | indirect | own generic head terms ("recipes", "cookbook"), don't target fish keywords |
| FishAngler, Pro Angler | adjacent | fishing apps with zero cooking content |

**Strategy:** Don't fight the giants for "recipes"/"cookbook" head terms. Own the
fish/seafood mid-tail where competition is stale, and capture the **unserved
"catch and cook" angler crossover** — fishing apps have large audiences and none
of them help users cook what they catch. No iOS app currently owns that intent.

---

## 2. Keyword strategy

Apple indexes: title + subtitle + keyword field (and learns from ASA). Never
repeat a token across the three fields — every duplicate wastes a slot.

### Tier 1 — primary (in title/subtitle)
| Keyword | Est. volume | Competition | Why |
|---|---|---|---|
| fish recipes | medium | low | core intent; covered by "Fish'n" + "Recipes" tokens |
| seafood recipes | medium | low | second core intent; in title |
| fish cookbook / cookbook | medium | medium | in subtitle; giants rank but rarely for fish+cookbook combos |
| easy | high (modifier) | — | combines into "easy fish recipes", "easy seafood" |

### Tier 2 — keyword field (species + methods + occasions)
salmon, tuna, shrimp, trout, cod, halibut, tilapia — species searches are
high-intent and convert ("salmon recipes" is the single biggest fish-adjacent
query family); grill/bake/fry methods; dinner, healthy, meal, pescatarian.

### Tier 3 — angler crossover (differentiator)
fishing, angler, catch — near-zero cookbook competition; combos like
"cook your catch", "fishing recipes" are effectively uncontested.

### Long-tail combos the metadata generates
"easy fish recipes", "seafood cookbook", "grilled salmon recipes",
"easy seafood dinner", "cook fish", "healthy fish meals", "cook your catch",
"fishing cookbook", "pescatarian meals".

---

## 3. Metadata package (validated character counts)

### Recommended (Package 1 — broadest reach)

| Field | Value | Count / Limit |
|---|---|---|
| Title | `Fish'n Cook: Seafood Recipes` | 28/30 |
| Subtitle | `Easy cookbook: grill & bake` | 27/30 |
| Keywords | `salmon,tuna,shrimp,trout,cod,halibut,tilapia,fishing,angler,catch,dinner,healthy,pescatarian,meal` | 97/100 |
| Promo text | `New: 30+ grilled fish recipes for summer. From fresh catch to weeknight salmon dinners — step-by-step recipes any home cook can master.` | 135/170 |

Indexed token set: fish, cook, seafood, recipes, easy, cookbook, grill, bake,
salmon, tuna, shrimp, trout, cod, halibut, tilapia, fishing, angler, catch,
dinner, healthy, pescatarian, meal. Zero duplicates.

### Alternative (Package 2 — angler-positioned, for A/B test)

| Field | Value | Count / Limit |
|---|---|---|
| Title | `Fish'n Cook: Seafood Recipes` | 28/30 |
| Subtitle | `Cook your catch, easy cookbook` | 30/30 |
| Keywords | `salmon,tuna,shrimp,trout,cod,grilled,baked,fried,fishing,angler,dinner,healthy,pescatarian,meal` | 95/100 |

### Keyword-field rules applied
Singular forms only, no spaces after commas, no words already in title/subtitle,
no "app"/"free"/category name (wasted or disallowed), no competitor brand names
(rejection risk).

### Full description (1,900/4,000 chars; description is not keyword-indexed on iOS — written for conversion)

Based on the actual feature set: recipe book, search, cooking timer,
step-by-step guides, save favorites. Do not list features the app doesn't have.

```
Fish'n Cook is the easiest way to cook fish and seafood with confidence. One app, hundreds of fish recipes, and everything you need to get dinner right: search, step-by-step guides, a built-in cooking timer, and your own favorites collection.

Most recipe apps treat fish as an afterthought. Fish'n Cook is built for it — every recipe is written around the fish, with the timing and technique seafood actually needs. No more overcooked salmon or rubbery shrimp.

FIND THE RIGHT RECIPE FAST
Search the whole cookbook in seconds. Look up a species you bought (salmon, cod, shrimp, trout), a dish you're craving (chowder, fish tacos, grilled tuna), or whatever fits tonight — and start cooking.

FOLLOW ALONG, STEP BY STEP
Every recipe is broken into clear, numbered steps so you always know what to do next. No wall-of-text instructions, no scrolling back and forth with wet hands — one step at a time, from prep to plate.

NAIL THE TIMING
Fish is unforgiving — a minute too long makes the difference. The built-in cooking timer keeps you on track right inside the recipe, so you never overcook your fillet while hunting for the kitchen clock.

SAVE YOUR FAVORITES
Found a keeper? Save it to your favorites and build your personal go-to collection — weeknight staples, special-occasion dishes, and the recipes your family asks for again and again, always one tap away.

WHY FISH'N COOK
• A dedicated fish & seafood cookbook — not a generic recipe app
• Fast search across every recipe
• Step-by-step instructions anyone can follow
• Built-in timer for perfectly cooked fish
• Favorites — your personal recipe collection
• Recipes for grilling, baking, pan-frying and more

Fish is the healthiest protein most people are afraid to cook. Fish'n Cook removes the fear — clear steps, exact timing, perfect results from your very first try.

Download Fish'n Cook and never wonder what to do with fish again.
```

---

## 4. Category

- **Primary: Food & Drink** — correct browse placement, moderate competition.
- **Secondary: Lifestyle** — broad fallback. (Don't use Sports despite the angler
  angle; category must match core function or review may flag it.)

---

## 5. Visual assets

**Icon:** one fish silhouette + one cooking cue (pan/flame), 2 colors max,
readable at 60px. Avoid text in the icon. Test "fish on grill" vs "fish + fork".

**Screenshots (first 3 carry ~90% of weight):**
1. Hero: finished dish + caption "Perfect fish, every time"
2. Step-by-step view + caption "One clear step at a time"
3. Built-in timer in a recipe + caption "Never overcook fish again"
4. Search results + caption "Find any recipe in seconds"
5. Favorites screen + caption "Save the keepers"

Captions top-aligned, large type, device frame optional but consistent.

**Preview video (optional, high ROI here):** 15s, food-first: sizzling pan →
app timer → plated dish. Food content demos extremely well.

---

## 6. Ratings & reviews plan

- Trigger `SKStoreReviewController` after a positive moment: user completes a
  recipe (timer finished) for the 2nd time. Never on first launch.
- Respond to every review in the first 90 days within 48h.
- Seed initial ratings via TestFlight cohort → ask for honest App Store reviews
  at public launch (don't incentivize — policy violation).
- Target: 4.5+ average, 50+ ratings in the first month (enough to show stars in
  search results, which materially lifts tap-through).

---

## 7. Seasonality calendar (strong for this niche)

| Window | Hook | Action |
|---|---|---|
| Feb–Mar (Lent) | Fish Fridays | promo text + featured collection; biggest predictable spike for fish recipes |
| May–Aug | Grilling season + fishing season | "grilled" keyword emphasis, catch-and-cook push |
| Sep–Oct | Healthy reset | pescatarian/healthy angle |
| Dec | Feast of the Seven Fishes / NYE | Italian seafood collection, holiday promo text |
| Jan | New-year health | "healthy fish meals" promo text |

Promotional text is editable without an app update — rotate it for each window.

---

## 8. A/B testing plan (App Store Connect → Product Page Optimization)

1. **Test 1 — Icon** (highest leverage): fish-only vs fish+pan. Run ≥2 weeks or
   until ~9,000 impressions/variant for ~10% lift detection at 80% power.
2. **Test 2 — First screenshot**: finished-dish hero vs timer-in-recipe hero.
   Tests whether appetite appeal or the "never overcook fish" promise converts better.
3. **Test 3 — Subtitle** (requires app update): Package 1 vs Package 2 subtitle.
   Judge by impression→install conversion AND keyword ranking movement
   (catch/angler combos), not conversion alone.

One variable per test. Ship the winner, then iterate.

---

## 9. Launch checklist (condensed)

- [ ] All metadata fields filled to limits (validated above)
- [ ] 6.7", 6.1" screenshot sets (iPad set if supporting iPad — recipe apps get real iPad traffic)
- [ ] Privacy nutrition labels + privacy policy URL
- [ ] Age rating 4+, no unlock-content issues
- [ ] Demo account for review if any login exists
- [ ] `SKStoreReviewController` wired to post-recipe trigger
- [ ] ASA keyword popularity check to validate this keyword set pre-submission
- [ ] Soft-launch option: AU/NZ/CA first to tune conversion before US push
- [ ] Day 1–14: daily check of keyword ranks (fish recipes, seafood recipes, salmon recipes, fish cookbook, cook your catch), impressions, and conversion in App Analytics

## 10. KPIs (first 90 days)

| Metric | Target |
|---|---|
| Top-10 rank | "fish recipes", "seafood cookbook", "cook your catch" |
| Top-30 rank | "salmon recipes", "seafood recipes", "fish cooking" |
| Search impression → install | ≥ 3% (Food & Drink median ~2–3%) |
| Rating | ≥ 4.5 with 50+ ratings month 1 |
| Localization trigger | If non-US installs >20%, localize ES/FR/DE/JA metadata first (metadata-only localization is cheap and effective) |
