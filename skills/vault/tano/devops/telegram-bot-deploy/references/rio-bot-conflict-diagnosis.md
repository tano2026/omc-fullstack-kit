# RIO Bot Conflict Diagnosis History (2026-07-17)

## Timeline

1. Bot `@Tano_research_pro_bot` (token `8157027188:***`) — ran OK for weeks
2. First ConflictError appeared → user revoked token → replaced with `8925653808:***`
3. New token ran for ~40 min (11:09-11:48) then got Conflict again
4. Subsequent launches of `8925653808:***` immediately conflicted — even though old token was revoked
5. Created brand new bot `@Tano_research_bot` (token `8300648617:***`) — launched successfully, no Conflict

## Key Diagnostic Observations

- **Token revocation alone did NOT fix the problem** — new token was immediately contested by another instance within 40 min
- **New bot with fresh token DID work** — proves Conflict was token-based, not infrastructure-based
- **Rogue instance likely on another machine** — could be VPS OpenClaw (100.64.173.75 — SSH dead), old laptop, or some panel/web service that had the token stored

## Lessons Learned

1. **Token revocation is insufficient when you don't control where the token is used** — rogue instances can grab the new token too
2. **Create a brand new bot = nuclear option** — always works because Telegram assigns a completely new bot ID + token pair
3. **Name convention for new bot**: `@Tano_research_bot` replaced `@Tano_research_pro_bot`
4. **Checklist before revoking**: identify ALL places using the old token first

## Recommended Future Steps

- Store all bot tokens in a central inventory (e.g. PROJECT-MAP.md)
- Document which machine/environment has which token
- Consider switching to webhook mode for production bots to avoid polling conflicts
