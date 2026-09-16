# Planr

**Status:** Live on the App Store · v1.1 in preparation
**Health:** 🟢 Shipping
**Updated:** 2026-09-16

React Native / Expo fitness app — athlete-first, with a coaching layer on top. Supabase, RevenueCat, Anthropic API, Sentry, Resend.

## Live now
- v1.0 / v1.0.1 approved and on the App Store (id6761987757)
- Blocking system with RLS enforcement
- JWT-hardened Supabase Edge Functions
- Server-side AI usage limits (per-feature daily caps)
- Rebuilt password reset flow (fragment-token implicit flow)
- Per-user theme storage
- Sentry crash reporting with symbolication

## Shipped this cycle (in v1.1, not yet submitted)
- Video Stage 1 — coach demo videos: record once, attach to any exercise
- Video Stage 2 — client form-check videos: upload from a logged set, coach views and replies on that set, notification unread trail, camera-roll save, 14-day retention with automated daily cleanup, moderation/reporting
- Coach pricing tiers — Coach 5 / 20 / 50 by client count, priced under TrueCoach; first client free
  - RevenueCat webhook to users.coach_tier; server-side client-cap trigger (SECURITY DEFINER)
  - Count-aware paywall, activation poll for webhook delay
  - Free coach gated out of Pro features; free coach AI limited to 1 program generation/day
- Share Planr + coach "Invite a client" (App Store link + coach code)
- App Store review prompt (expo-store-review, positive moments only)
- Debug-log sweep before submission

## Next — before submitting v1.1
- [ ] Raise form-video quality (bitrate 1.5 to 4 Mbps; bucket + trigger limits to 20 MB)
- [ ] Update App Store description (add tier structure)
- [ ] Review notes: explain free first client
- [ ] Confirm privacy declarations (camera-roll save)
- [ ] Version bump to 1.1.0
- [ ] Build, verify, Transporter; submit app + 6 new subscription products

## Backlog (deferred)
- Theme migration (13 screens), keyboard double-tap, programs white flash
- Sign-out to account-type routing bug
- Tutorial walkthrough; social layer as post-launch fast-follow

## Workflow notes
- Build: eas build --local --platform ios then verify then Transporter
- SQL: manual in Supabase editor; read live pg_proc before editing any function/trigger
- Debug: npx expo run:ios --device
