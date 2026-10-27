# Service Profit social artwork

Status: UPLOADED 27 October 2026 (Pinky approved: profiles + covers now,
posts after Nylon then scheduled). LinkedIn company 143802027: profile,
banner and Overview live. Facebook Service Profit Accounting
(61594432044788): profile and cover live. Google cover held - one Google
profile only, Pink Accounting. Nylon PASS records: captions.nylon.json,
overview-linkedin.nylon.json. Overview text: overview-linkedin.txt.

Rebuilt 27 October 2026. The old set was flat black rectangles with small
white text and no photography. This set is photo-led, built by
`tools/build_assets.py` (`build_social()` and `build_og()`).

## Files

| File | Size | Use |
|---|---|---|
| profile-1080.png | 1080 x 1080 | Master profile picture |
| profile-linkedin-300.png | 300 x 300 | LinkedIn company page logo |
| profile-facebook-720.png | 720 x 720 | Facebook page profile picture |
| profile-circle-preview.png | 1080 x 1080 | Check only: how the circle crop looks. Do not upload. |
| cover-linkedin.png | 1584 x 396 | LinkedIn company page cover |
| cover-facebook.png | 1640 x 624 | Facebook page cover |
| cover-google.png | 1200 x 675 | Google / general cover |
| post-quoted-hours.png | 1080 x 1350 | Feed post: quoted 6, did 9 |
| post-bank-not-yours.png | 1080 x 1350 | Feed post: bank is not all yours |
| post-first-monday.png | 1080 x 1350 | Feed post: know which jobs paid |

Site share image: `assets/og.png` (1200 x 630) uses the same system.

## Masters

Photographic masters sit in `masters/` (hvac-rooftop, electrical-switchboard,
construction-fitout). They are illustrative brand artwork, not photos of
Pink staff, clients or client jobs. Do not caption them as real people or
real jobs.

## Brand rules applied

- Service Profit is a service name. Every piece carries Pink Accounting.
- Pink #ED1651 is an accent line only, never a fill.
- Charcoal #0E0E12 panels, white type, Segoe UI.
- Registered Tax Agent 26284368 where the format allows it.
- Rebuild: `python -c "import sys; sys.path.insert(0,'tools'); import build_assets; build_assets.build_og(); build_assets.build_social()"`

## Upload order (after Pinky approval)

1. LinkedIn company page: profile-linkedin-300.png, then cover-linkedin.png.
2. Facebook page: profile-facebook-720.png, then cover-facebook.png.
3. Keep profile-1080.png as the master for any new surface.
