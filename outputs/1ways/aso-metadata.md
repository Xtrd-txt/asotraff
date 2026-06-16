# 1ways — ASO Metadata Package (Apple App Store, en-US)

App: **1ways** — offline multi-stop route planner.
Features: point-to-point planning; Drive / Cycle / Walk modes; add stops 4 ways
(GPS, tap on map, manual coordinates, favorites); interactive canvas with points,
lines, live location and auto-zoom; stop list with drag-to-reorder, swipe-to-delete,
clear-all; total distance, time estimate, and per-segment breakdown.
Date: 2026-06-16. Platform: iOS. Locale: en-US.
**Description: intentionally omitted (per request).**

> Apple publishes no official search-volume data. Validate this keyword set against
> Apple Search Ads keyword popularity (5–100) in App Store Connect before submitting.
> Locale note: this is the en-US set. A separate Russian (ru) set would need
> different keywords — ask if you want it.

---

## Title (limit 30)

**Recommended:** `1ways: Route Planner` — 20/30

The brand name "1ways" has zero search value on its own, so adding "Route Planner"
to the title captures your single most important keyword phrase in the
highest-weighted field. Alternative: `1ways – Multi-Stop Routes` (25/30).

Indexed title tokens: route, planner.

---

## Subtitle (limit 30)

**Recommended:** `Offline multi-stop trip maps` — 28/30

Indexed tokens add: offline, multi, stop, trip, maps. "Offline" is a real
differentiator for a route planner and a genuine search term — worth the slot.

Alternatives:
- `Plan trips: drive, bike, walk` — 29/30 (captures the 3 travel modes instead)
- `Multi-stop trip & mileage maps` — 30/30

---

## Keywords (limit 100, comma-separated, NO spaces)

```
distance,mileage,gps,waypoint,itinerary,cycling,walking,driving,navigation,travel,stops,hiking,car
```
98/100. No spaces after commas, singular forms, no duplicates of title
("route", "planner") or subtitle ("offline", "multi", "stop", "trip", "maps").

Token strategy:
- **Output terms** (distance, mileage) — match "distance calculator" / "mileage" intent.
- **Mechanics** (gps, waypoint, stops, navigation) — core route-planner vocabulary.
- **Travel modes** (cycling, walking, driving, hiking, car) — cover Drive/Cycle/Walk
  searches; combine with subtitle into "cycling route", "walking trip", "driving distance".
- **Use cases** (itinerary, travel) — broaden into trip-planning searches.

Long-tail generated across fields: "multi-stop route planner", "offline route planner",
"trip distance calculator", "cycling route planner", "walking distance map",
"driving mileage", "waypoint navigation".

If ASA shows low popularity for any token, swap candidates: `commute,delivery,
courier,roadtrip,tracker,map distance,plan,journey,bike,walk run`.

---

## Promotional text (limit 170, editable anytime without app update)

```
Plan multi-stop routes offline — drive, cycle or walk. Add stops, reorder them, and get total distance, time and a segment-by-segment breakdown. No ads, no signup, free.
```
169/170. Not keyword-indexed — written to convert. Leads with the offline +
multi-stop + multimodal hooks, closes with the no-ads/free trust line.

---

## Notes for App Review (App Store Connect → App Review Information → Notes)

```
Thank you for reviewing 1ways.

1ways is an offline multi-stop route planner. Users add stops on a map and the app draws the route, calculates total distance and estimated time, and shows a per-segment breakdown for Drive, Cycle, or Walk modes.

KEY FACTS FOR REVIEW:

1. NO DATA COLLECTION — The app does not collect, store, or transmit any user information. There is no account, login, registration, or analytics/tracking SDK. The privacy nutrition label is "Data Not Collected." All routes and stops are stored locally on the device only.

2. LOCATION USE — The app requests location ("While Using") only to show the user's current position on the map and to add the current location as a stop. Location data is used on-device only and is never collected, stored off-device, or transmitted to any server.

3. OFFLINE — The app works fully offline. It does not require an internet connection to plan routes or calculate distance/time.

4. NO ADVERTISING — The app shows no ads and includes no advertising SDKs or ad networks.

5. COMPLETELY FREE — No paid subscriptions, no in-app purchases, and no locked or premium content.

6. NO ACCOUNT NEEDED TO TEST — No demo credentials required. All functionality is accessible on first launch.

HOW TO TEST:
- Add stops: use GPS, tap on the map, enter coordinates manually, or pick from favorites.
- Choose a mode: Drive, Cycle, or Walk.
- Reorder stops by dragging; swipe to delete a stop.
- View total distance, estimated time, and the per-segment breakdown.

Please contact us at the support email on file with any questions. Thank you!
```

Consistency requirements (these claims must match the rest of the submission):
- **Location string:** add a clear `NSLocationWhenInUseUsageDescription` in Info.plist
  (e.g., "1ways uses your location to show your position and add it as a stop"). A
  missing/vague purpose string is a common rejection.
- **Privacy label:** you can still answer **"Data Not Collected"** even though the app
  uses location — Apple counts data as "collected" only if it leaves the device. Since
  location is on-device only, "Not Collected" is correct. Make sure no bundled SDK
  (maps, crash, analytics) sends location off-device, or this becomes inaccurate.
- **Privacy policy URL** is mandatory regardless — a one-page "collects no data" note is fine.

---

## Category & quick notes
- **Primary: Navigation** (best keyword/browse fit for a route planner).
- **Secondary: Travel.**
- Screenshots (first 3 carry most weight): 1) canvas with a multi-stop route drawn +
  caption "Plan multi-stop routes"; 2) Drive/Cycle/Walk mode selector + "Drive, cycle
  or walk"; 3) distance/time + segment breakdown + "Distance, time, every segment";
  4) the 4 ways to add a stop; 5) "Works fully offline".
- When you're ready for the description, I'll write the conversion copy to match these fields.
