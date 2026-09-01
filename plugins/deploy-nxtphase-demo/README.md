# deploy-nxtphase-demo

Put any app on `<name>.demo.nxtphase.ai`, as a Claude Code skill.

Point Claude Code at an app, give it a short name, and it creates a Railway project in
the shared **Nxtphase AI demos** workspace, creates the service, registers the custom
domain, writes the CNAME and TXT records in Cloudflare, uploads the source, and verifies
that the URL actually answers. Roughly five minutes, most of it waiting on the build.

## Ships without credentials

This plugin contains no tokens, passwords, or keys. The skill reads two values from a
`.env` file in the root of the app you are deploying:

```
RAILWAY_API_TOKEN=<railway account token>
CLOUDFLARE_TOKEN=<cloudflare api token>
```

**Both values are in our shared password manager**, under the "Nxtphase AI demos" Railway
workspace and the `nxtphase.ai` Cloudflare zone. Copy them from there into `.env`. No
access to that vault yet, or the entries are missing? Ask a developer on the team, and have
them shared through the password manager, not through chat, a ticket, or a Notion page.

Prefer to mint your own? `skills/deploy-nxtphase-demo/references/tokens.md` lists the exact
permissions each token needs, plus a one-line check per token to confirm it works. A
fill-in template lives at `skills/deploy-nxtphase-demo/assets/env.example`.

The skill refuses to run without both tokens. It will not guess them, reuse a token from
another project, or go hunting for them elsewhere on the machine.

The workspace ID and the Cloudflare zone ID *are* in the skill. They are account
identifiers, not credentials, and they do nothing without a token.

## What it gives an agent

**A preflight that fails loudly.** Before touching anything it checks the two tokens, adds
`.env` and `.railway-deploy.json` to the app's `.gitignore`, verifies the Railway CLI is
installed, and calls `{ me { id name } }` to confirm the account token is live. If `.env`
is already tracked by git it stops and says the token needs rotating first.

**The Railway API, not guesswork.** Projects, services, deploy tokens, variables, and
custom domains all go through the GraphQL API at `backboard.railway.com`. The CLI is used
only for `railway up` and `railway logs`, because it does not accept account tokens. Each
app gets its own generated project token for that.

**The DNS ordering that actually works.** Registering the Railway domain and writing the
Cloudflare records has to happen back-to-back. Leave a gap and resolvers cache an NXDOMAIN
for the subdomain, which takes up to 30 minutes to clear. The CNAME must be
`proxied: false`, because Railway terminates TLS itself and Cloudflare's free certificate
covers `*.nxtphase.ai` but not `*.demo.nxtphase.ai`. The TXT verification fields sit on
`status.verificationDnsHost` and `status.verificationToken`, not inside `dnsRecords`, which
is the detail that costs an hour if you have not hit it before.

**Instant re-deploys.** After the first run the skill writes `.railway-deploy.json` next to
the app with the project, environment, and service IDs plus the deploy token. Every later
run reads that file and jumps straight to `railway up`. That file holds a live credential,
so it is gitignored alongside `.env`.

**Restraint about build config.** Railway's buildpacks detect the stack from the source.
The skill is told not to write a Dockerfile, an nginx config, or any other scaffolding
unless the repo already has one. If a build fails, read the build logs first.

## Install

Through the marketplace:

```bash
claude /plugin marketplace add nxtphaseai/claude-plugins
claude /plugin install deploy-nxtphase-demo@nxtphaseai
```

Or manually:

```bash
git clone git@github.com:nxtphaseai/claude-plugins.git
bash claude-plugins/plugins/deploy-nxtphase-demo/install.sh --user
```

Restart Claude Code afterwards so the skill loads.

You also need the Railway CLI:

```bash
brew install railway          # macOS
npm i -g @railway/cli         # Windows
bash <(curl -fsSL cli.new)    # anything else
```

## Use

Open Claude Code in the app's folder, make sure `.env` is there, and invoke:

```
/deploy-nxtphase-demo
```

It will ask for a short name, one word or two hyphenated, and use it for both the Railway
project and the subdomain. Then it runs a lot of commands for a few minutes. Let it.

## Layout

```
plugins/deploy-nxtphase-demo/
├── .claude-plugin/plugin.json
├── install.sh
├── README.md
└── skills/deploy-nxtphase-demo/
    ├── SKILL.md                  # the deploy flow, preflight to verification
    ├── assets/env.example        # .env template, no values filled in
    └── references/
        ├── tokens.md             # what the two tokens are, permissions, how to get them
        └── domains.md            # Railway + Cloudflare DNS, and the ordering it depends on
```
