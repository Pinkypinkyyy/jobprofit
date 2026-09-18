# Service Profit photography direction

Written 18 September 2026. The site is the shopfront for a registered tax agent
charging $1,650 + GST a month. The imagery has to carry that. Cheap or obviously
generated photography costs more in credibility than it saves in time.

## Why the current photos are soft

The trade photos are 838px wide at source. The build was scaling them to 1200px,
so a retina phone was shown invented detail. That upscale is now blocked by
`test_no_photo_variant_is_wider_than_its_source`. The remaining fix is source
material at a real size.

**Minimum source width: 2400px.** That gives an honest 480 / 864 / 1200 / 1600
ladder with room to crop.

## Rules that protect the premium position

- Photoreal. No illustration, no 3D, no obvious render.
- Australian context: AU switchboards and outlets, AU hi-vis, AU vans, hard
  Queensland daylight. American gear reads wrong to this audience immediately.
- No text, signage, logos or brand marks anywhere in frame. Invented text is the
  fastest way for a viewer to spot a generated image.
- Faces: prefer three-quarter, over-shoulder, or working-hands framing. A face
  staring down the lens competes with the headline and is where generation
  artefacts show first.
- Hands near tools get scrutinised. Keep hands mid-action and partly occluded.
- No stock-cliche poses: no folded arms in front of a van, no hard hat and
  clipboard grin, no thumbs up.

## The stories, one per placement

Each photo does a job. If it does not carry the story, it is decoration and it
goes.

### 1. Hero, homepage — "the job ran long"
Landscape 2400x1350. Rooftop or plant-deck air conditioning unit, late
afternoon, long shadows. One technician still working, seen from behind or in
three-quarter, phone or worksheet in the free hand. The light says the day has
gone past where the quote said it would.
Not: a smiling portrait. The headline is the message; the photo is the weather.

### 2. Air con page — "the quote did not include the access"
Portrait 2400x3000. Rooftop changeover. The unit is the subject, the access
problem is the story: height, plant deck, awkward lift. Technician small in
frame.

### 3. Electrical page — "the variation nobody billed"
Portrait 2400x3000. Switchboard upgrade in progress, board open, AU-style
breakers, test leads in shot. Mid-distance, technician working, face turned to
the work.

### 4. Construction services page — "fit-out, not head contracting"
Portrait 2400x3000. Commercial fit-out at second-fix stage: ceiling grid, new
services, a trade van or gear staged. Deliberately not a house frame and not a
site full of head-contractor signage, because the page exists to tell those two
apart.

## Keep as-is

`pink-home.jpg` and `pink-meet.jpg` are real photographs of Huong and are the
highest-quality, most differentiating assets on the site. They stay. On a
professional services site the practitioner is the product.

## How to install new sources

Drop the full-size files into a folder and run:

    python tools/import_photos.py <source-folder>

It maps by filename, writes the JPEG at full size into `assets/`, rebuilds the
WebP ladder honestly, and refuses anything under 1600px so a small source cannot
quietly become another upscale.
