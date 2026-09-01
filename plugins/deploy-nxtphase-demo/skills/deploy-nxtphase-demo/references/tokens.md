# Tokens

This skill ships without credentials. It reads two values from a `.env` file in the root of
the app being deployed, and it never stores them anywhere else.

```
RAILWAY_API_TOKEN=<railway account token>
CLOUDFLARE_TOKEN=<cloudflare api token>
```

There is a template at `assets/env.example` next to this file. Copy it into the app
directory as `.env` and fill in the two values.

## Where to get the values

**Ask a developer on the team.** Both tokens belong to shared infrastructure: the
"Nxtphase AI demos" workspace on Railway and the `nxtphase.ai` zone on Cloudflare. Whoever
set those up already has working tokens and can hand them over.

Ask for them through a password manager, an encrypted note, or another secure channel.
Not through chat, not in a ticket, not in a Notion page, and not in a screenshot. A token
that has been posted somewhere readable is a token that needs rotating.

If you would rather mint your own, both are self-service:

### RAILWAY_API_TOKEN

A Railway **account token**, not a project token.

1. Railway dashboard, Account Settings, Tokens.
2. Create a token scoped to the **Nxtphase AI demos** workspace.
3. Copy the value once; Railway will not show it again.

The account token is what creates projects, services, per-project deploy tokens, variables,
and custom domains. The skill generates a separate project token per app for the CLI,
because the CLI does not accept account tokens.

### CLOUDFLARE_TOKEN

A Cloudflare **API token**, not the Global API Key. Never use the Global API Key: it grants
everything on the account and cannot be scoped.

1. Cloudflare dashboard, My Profile, API Tokens, Create Token, Custom token.
2. Permissions: **Zone, DNS, Edit**.
3. Zone Resources: **Include, Specific zone, nxtphase.ai**.
4. Create and copy the value once.

That is the minimum the skill needs. It creates and deletes CNAME and TXT records under
`demo.nxtphase.ai` and reads them back to verify.

## Rules for handling them

- `.env` is never committed. Make sure `.gitignore` covers it before you write it.
- `.railway-deploy.json` holds a generated Railway project token, so it is a secret too and
  belongs in `.gitignore` as well.
- Load them with `set -a; . ./.env; set +a` and reference them as `$RAILWAY_API_TOKEN` and
  `$CLOUDFLARE_TOKEN`. Do not paste literal values into commands, where they end up in
  shell history and in the session transcript.
- Do not set them as Railway service variables. They deploy the app; the app does not need
  them.
- If a token leaks, revoke it at the source (Railway Account Settings, Tokens; Cloudflare
  My Profile, API Tokens) and issue a new one. Rotating is cheap; a live token in a git
  history is not.

## Verifying a token works

Railway:

```bash
curl -sf https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{"query":"{ me { id name } }"}'
```

Returns the account name. Anything else means the token is wrong, expired, or revoked.

Cloudflare:

```bash
curl -sf "https://api.cloudflare.com/client/v4/zones/e40778c5acc095d398219f0cb955b9b3" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN"
```

Returns the `nxtphase.ai` zone with `"success": true`. A 403 means the token is missing the
DNS Edit permission, or is not scoped to this zone.
