# Turning on live Google reviews

The homepage rating, review count and quotes can come straight from the Google
Business Profile instead of being typed in by hand. It needs one thing from
you: a Google API key. About five minutes.

Nothing here can be done from a Claude session. It is your Google account, it
needs a card on file, and an API key is a credential. So this is the one part
you do.

## Why it needs a key at all

Google does not publish reviews in any form a website can just read. The only
supported route is the Places API, and that needs an authenticated key.

## What it costs

Effectively nothing. The fetch runs **once a week**, so about four calls a
month. Google bills Places API Place Details per call, with a free monthly
allowance far above four. You still have to put a card on the Cloud account
before it will issue a key, which is normal and is not a charge.

If you would rather not attach a card at all, do nothing. The site keeps
showing the figures committed in `tools/build_pages.py`, which is what it is
doing today. Nothing is broken; it just has to be updated by hand.

## The five minutes

1. Go to <https://console.cloud.google.com> signed in as the account that owns
   the Pink Accounting Business Profile.
2. Create a project. Any name. "Pink Website" is fine.
3. Search the top bar for **Places API (New)** and press Enable. Enabling asks
   for billing if the project has none.
4. Go to **APIs and services**, then **Credentials**, then **Create
   credentials**, then **API key**.
5. Press **Edit API key** on the one it just made and set two restrictions:
   - **API restrictions**: Restrict key, and tick only **Places API (New)**.
   - **Application restrictions**: leave as None. The key is used by a GitHub
     Action from a changing IP, not by a browser.
6. Copy the key.

## Where the key goes

**Not into a chat window, and not into the site.** This site is static, so a
key in a page would be readable by anyone who opened developer tools. It goes
into GitHub, where it stays encrypted and is only visible to the workflow.

1. Open <https://github.com/Pinkypinkyyy/jobprofit/settings/secrets/actions>
2. **New repository secret**
3. Name: `GOOGLE_PLACES_API_KEY`
4. Value: the key
5. Add secret

## Then run it once

1. Open <https://github.com/Pinkypinkyyy/jobprofit/actions>
2. Pick **Refresh Google reviews** on the left
3. **Run workflow**

It will find the Business Profile from the firm name and address, and print a
line in the log like `GOOGLE_PLACE_ID=ChIJ...`. Save that value as a repository
*variable* named `GOOGLE_PLACE_ID` at
<https://github.com/Pinkypinkyyy/jobprofit/settings/variables/actions> so it
does not have to look it up again. Optional but tidier and slightly cheaper.

## What happens after that

- It runs Monday mornings Brisbane time.
- When the rating, count or reviews have changed it **opens a pull request**.
  It does not publish by itself, because merging to `main` publishes the live
  site and that stays your decision.
- Reviews under four stars are not shown. Each quote carries the reviewer's
  name and a link back to the review, which the Places API terms require.
- If the API is down or the key is wrong, the site falls back to the committed
  figures. It cannot blank the homepage.
- If the secret is missing the workflow does nothing and stays green, so you
  will not get a red build every Monday.

## If it goes wrong

The workflow log says which step failed.

| What the log says | What it means |
|---|---|
| `REQUEST_DENIED` or 403 | The key is restricted to the wrong API, or Places API (New) is not enabled on that project |
| `INVALID_ARGUMENT` or 400 | `GOOGLE_PLACE_ID` is set to something that is not a Place ID. Clear the variable and let it resolve again |
| `No place matched` | The firm name or address in `tools/fetch_reviews.py` no longer matches the Business Profile |
| Billing errors | The project has no billing account attached |

Paste the failing log into a Claude session and it can be read from there.
