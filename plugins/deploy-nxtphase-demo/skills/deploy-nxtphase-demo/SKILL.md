---
name: deploy-nxtphase-demo
description: >
  Deploy any app to our team's Railway workspace with a custom domain on
  demo.nxtphase.ai. Handles the full flow: explore the codebase, create a
  project, deploy to Railway, set up DNS via Cloudflare, and verify. Reads its
  two API tokens from a .env file in the app directory; it ships with no
  credentials of its own.
metadata:
  author: Kamiel
  tags: deploy, railway, cloudflare, dns, demo, nxtphase
---

# Deploy to Railway

Written by Kamiel. The deploy flow and the API calls below are his; this is his
skill packaged for the marketplace.

Deploy any app to the **Nxtphase AI demos** workspace on Railway with a custom domain on `demo.nxtphase.ai`. Each demo gets its own Railway project.

## Credentials

This skill contains no tokens, passwords, or keys, and it never will. Everything it needs
comes from a `.env` file that lives in the app you are deploying, outside this repository.

Read a token from `.env` at the moment you need it and pass it straight into the request.
Never echo a token to the terminal, never write one into a tracked file, a commit message,
or a chat message, and never copy one into another document.

## Architecture

This skill uses two tokens, both read from `.env`:

- **`RAILWAY_API_TOKEN`** (account token), used with the Railway GraphQL API (`https://backboard.railway.com/graphql/v2`) for all management operations: creating projects, services, tokens, variables, and domains.
- **`CLOUDFLARE_TOKEN`**, used with the Cloudflare API for DNS record management.

The Railway CLI is used only for `railway up` (deploying local source code) and `railway logs`. The CLI does not accept account tokens, so each project gets a **generated project token** created via the API at setup time.

**Important**: The CLI does not need to be linked to a project. Always `cd` into the app directory and pass `--service <name>` explicitly.

### State file

After the first deploy, the skill writes a `.railway-deploy.json` file in the app's root directory. This file links the app to its Railway project and contains everything needed for re-deploys:

```json
{
  "projectId": "...",
  "environmentId": "...",
  "serviceId": "...",
  "serviceName": "...",
  "projectToken": "...",
  "domain": "<name>.demo.nxtphase.ai"
}
```

`projectToken` is a live deploy credential. Treat `.railway-deploy.json` like `.env`: it
must be in `.gitignore` and it must never be committed.

The CLI commands further down load that token with `jq`. If `jq` is not installed (common
on Windows), use this instead, which needs nothing extra:

```bash
export RAILWAY_TOKEN="$(sed -n 's/.*"projectToken"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' .railway-deploy.json)"
```

Either way, pull the value out of the file rather than pasting it into the command, so it
stays out of shell history and out of the transcript.

On subsequent runs, if this file exists, skip straight to the deploy step (Step 6). All IDs and the deploy token are already known.

### Fixed IDs

These are account identifiers, not credentials. They are useless without the tokens above.

| Resource | ID |
|---|---|
| Workspace (Nxtphase AI demos) | `5ebe06e4-9353-4997-b43c-5f11d4795d2c` |
| Cloudflare zone (nxtphase.ai) | `e40778c5acc095d398219f0cb955b9b3` |

## Preflight

### 1. Tokens

Look for a `.env` file in the app's root directory containing `RAILWAY_API_TOKEN` and
`CLOUDFLARE_TOKEN`. If the file is missing, or either token is absent or still a
placeholder, stop and tell the user:

> I need two API tokens to deploy, and this skill does not ship with them. Create a `.env`
> file in this app's root directory:
>
> ```
> RAILWAY_API_TOKEN=<railway account token>
> CLOUDFLARE_TOKEN=<cloudflare api token>
> ```
>
> **Both values are in our shared password manager.** Look for the entries for the
> "Nxtphase AI demos" Railway workspace and the `nxtphase.ai` Cloudflare zone, and copy
> them straight into `.env`.
>
> If you cannot find them, or you do not have access to that vault yet, ask one of the
> developers on the team. Have them share the values through the password manager, not
> through chat, a ticket, or a Notion page.
>
> If you would rather mint your own tokens, `references/tokens.md` lists the exact
> permissions each one needs.

There is a template next to this file at `assets/env.example`. Copying it is the fastest
way to get the shape right:

```bash
cp <skill-dir>/assets/env.example .env
```

Do not proceed without both tokens. Do not guess them, do not reuse a token from another
project, and do not go looking for these values elsewhere on the machine.

### 2. Keep the secrets out of git

Before writing anything, make sure the app's `.gitignore` covers both `.env` and
`.railway-deploy.json`. Add the lines if they are missing:

```bash
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
grep -qxF '.railway-deploy.json' .gitignore || echo '.railway-deploy.json' >> .gitignore
```

If the app has no `.gitignore`, create one with those two lines. If `.env` is already
tracked by git (`git ls-files --error-unmatch .env`), say so and stop: that token has to be
rotated before anything else happens.

### 3. Railway CLI

Verify the Railway CLI is installed with `command -v railway`. If missing, install with `bash <(curl -fsSL cli.new)`, `brew install railway`, or `npm i -g @railway/cli`.

### 4. Verify access

Load the tokens into the environment once, from the file, rather than pasting values into
command lines where they land in shell history and in the transcript:

```bash
set -a; . ./.env; set +a
```

Then check the Railway token:

```bash
curl -sf https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{"query":"{ me { id name } }"}'
```

This should return the account name. If it fails, the token is invalid or expired: ask the
user to check with the colleague who supplied it.

### 5. Check for existing deployment

Check if the app directory contains a `.railway-deploy.json` file. If it does, this app has been deployed before, so read the file and skip to **Step 6, Deploy**. All IDs and the deploy token are in the file.

If the file does not exist, this is a first-time deploy. Continue with Step 1.

## First-time deploy flow

### Step 1: Explore the codebase

Before deploying, understand what you're deploying. Check the app directory for:

- **Dockerfile**. If present, Railway will use it. No further config needed.
- **package.json** / **requirements.txt** / **go.mod** / etc. Identifies the stack.
- **Main entrypoint**. What file starts the app? (e.g. `server.js`, `app.py`, `main.go`)
- **Port**. Look for a port definition in the code (e.g. `PORT=3000`, `listen(8080)`). If none is explicitly set, use `8080` as the default, since Railway sets `PORT=8080` by convention.
- **Environment variables**. Does the app need any secrets or config values of its own? If it does, ask the user for them. Do not invent values, and never pass the deploy tokens through as app config.

### Step 2: Pick a name

Ask the user for a short name: one word, or two words hyphenated. This name is used for both the Railway project and the domain `<name>.demo.nxtphase.ai`. Never use any other base domain; only `demo.nxtphase.ai` is under our control in Cloudflare.

Examples: `shopify`, `cool-app`.

### Step 3: Create the project

```bash
curl -s https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{
    "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { id name environments { edges { node { id name } } } } }",
    "variables": {
      "input": {
        "name": "<name>",
        "workspaceId": "5ebe06e4-9353-4997-b43c-5f11d4795d2c"
      }
    }
  }'
```

Save the returned project `id` and the production environment `id` (from `environments.edges[0].node.id`).

### Step 4: Create a service and generate a deploy token

Create a service inside the project:

```bash
curl -s https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{
    "query": "mutation($input: ServiceCreateInput!) { serviceCreate(input: $input) { id name } }",
    "variables": {
      "input": {
        "projectId": "<project-id>",
        "name": "<name>"
      }
    }
  }'
```

Save the returned service `id`.

Then generate a project token for the CLI to use:

```bash
curl -s https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{
    "query": "mutation($input: ProjectTokenCreateInput!) { projectTokenCreate(input: $input) }",
    "variables": {
      "input": {
        "projectId": "<project-id>",
        "environmentId": "<environment-id>",
        "name": "deploy-token"
      }
    }
  }'
```

The response returns the token string directly. Save it as the `projectToken` in the state
file. Do not print it back to the user.

### Step 5: Set up the custom domain

Set up DNS **before** deploying code, so DNS propagates while the build runs.

See [references/domains.md](references/domains.md) for the full Railway plus Cloudflare flow. Use the project ID, environment ID, and service ID from the previous steps.

### Step 6: Deploy

`cd` into the app's root directory, then deploy with the CLI using the project token:

```bash
cd /path/to/app
export RAILWAY_TOKEN="$(jq -r .projectToken .railway-deploy.json)"
railway up --service <name> --detach -m "<summary of what this app does>"
```

**Important**: `railway up` must be run from inside the app directory. Do not pass the path as an argument.

Railway has built-in buildpacks that auto-detect the stack from the source code. Do not create a Dockerfile, nginx config, or any other deployment scaffolding unless one already exists in the codebase. Just point `railway up` at the app directory and let Railway figure it out.

How Railway decides what to build:

| Found in the source | Build |
|---|---|
| Dockerfile | used as-is |
| package.json | Node.js buildpack (`npm install` then `npm start`) |
| requirements.txt / pyproject.toml | Python buildpack |
| go.mod | Go buildpack |
| index.html, no package.json | static site, served automatically |

If the auto-detected build doesn't work, check the build logs first (`railway logs --service <name> --build --lines 200`). Only then consider adding build config, not before.

### Step 7: Save state

**First-time deploy only.** After a successful deploy, write `.railway-deploy.json` in the app's root directory:

```json
{
  "projectId": "<project-id>",
  "environmentId": "<environment-id>",
  "serviceId": "<service-id>",
  "serviceName": "<name>",
  "projectToken": "<generated project token>",
  "domain": "<name>.demo.nxtphase.ai"
}
```

This file is what makes future re-deploys instant: the agent reads it and skips straight to Step 6. Confirm it is covered by `.gitignore` (Preflight step 2) before you finish.

### Step 8: Verify

```bash
# 1. Check DNS propagation against a public resolver (not local cache)
dig @9.9.9.9 <name>.demo.nxtphase.ai CNAME +short

# 2. Check build and runtime logs
export RAILWAY_TOKEN="$(jq -r .projectToken .railway-deploy.json)"
railway logs --service <name> --build --lines 100
railway logs --service <name> --lines 100 --json

# 3. Test the URL (only after dig confirms the CNAME is live)
curl -sI https://<name>.demo.nxtphase.ai
```

If `curl` fails but `dig` shows the correct CNAME, the local DNS cache may hold a stale NXDOMAIN. Wait a few minutes or flush with `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder` on macOS.

## Variables

Set variables via the GraphQL API (account token):

```bash
curl -s https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{
    "query": "mutation($input: VariableCollectionUpsertInput!) { variableCollectionUpsert(input: $input) }",
    "variables": {
      "input": {
        "projectId": "<project-id>",
        "environmentId": "<environment-id>",
        "serviceId": "<service-id>",
        "variables": { "KEY": "value" }
      }
    }
  }'
```

`RAILWAY_API_TOKEN` and `CLOUDFLARE_TOKEN` are deploy credentials for this skill, not app
config. Never set them as service variables on Railway.

List variables via the CLI (project token):

```bash
export RAILWAY_TOKEN="$(jq -r .projectToken .railway-deploy.json)"
railway variable list --service <name> --json
```

## Status and logs

These use the CLI with the project's token from `.railway-deploy.json`:

```bash
export RAILWAY_TOKEN="$(jq -r .projectToken .railway-deploy.json)"
railway status --json
railway logs --service <name> --lines 200 --json
railway logs --service <name> --build --lines 200 --json
```

## Manage releases

```bash
export RAILWAY_TOKEN="$(jq -r .projectToken .railway-deploy.json)"
railway redeploy --service <name> --yes       # rebuild from same source
railway restart --service <name> --yes         # restart without rebuilding
railway down --service <name> --yes            # remove latest deployment
```

## Reference

| Topic | File |
|---|---|
| The two tokens: what they are, which permissions they need, how to get them | [references/tokens.md](references/tokens.md) |
| Domains and DNS (Railway plus Cloudflare) | [references/domains.md](references/domains.md) |
