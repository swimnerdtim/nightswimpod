# Scroll Behavior Fix (Apr 1, 2026)

## Problem
When clicking on an episode link, page would scroll to the bottom instead of the top.

## Root Cause
React Router doesn't scroll to top on route changes by default (unlike traditional multi-page websites).

## Solution
Created `ScrollToTop` component that:
1. Listens to route changes via `useLocation()` hook
2. Scrolls to `window.scrollTo(0, 0)` on every route change
3. Added to App.jsx so it runs on every page navigation

## Files Changed
- `src/components/ScrollToTop.jsx` (new)
- `src/App.jsx` (imported ScrollToTop component)

## Testing
After deployment (2-3 minutes):
1. Go to https://swimnerdtim.github.io/nightswimpod/
2. Click any episode
3. Page should load at the TOP (not bottom)
4. Click another episode
5. Should scroll to TOP again

## Status
✅ Fixed and deployed

**Deployed:** 2026-04-01 07:35 EDT
