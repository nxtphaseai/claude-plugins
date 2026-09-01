# Domains and DNS

Every deployed app gets a custom URL on `demo.nxtphase.ai`. This is the only base domain we control in Cloudflare, so never use anything else.

Both API calls below read their token from `.env`. Load the file once with
`set -a; . ./.env; set +a` and reference `$RAILWAY_API_TOKEN` and `$CLOUDFLARE_TOKEN`, so
no literal token value ends up in shell history or in the transcript. See
[tokens.md](tokens.md).

## URL format

Always `<name>.demo.nxtphase.ai` where `<name>` is one or two lowercase words joined by a hyphen. Ask the user to pick this name before deploying. Examples: `shopify.demo.nxtphase.ai`, `cool-app.demo.nxtphase.ai`.

## Full domain setup flow

**Important**: Steps 1 and 2 must be done back-to-back with nothing in between. If there is a gap between creating the Railway domain and creating the Cloudflare DNS records, DNS resolvers will cache an NXDOMAIN (domain not found) response for the subdomain, which can take up to 30 minutes to clear.

After the service is created on Railway:

### Step 1: Add the custom domain on Railway

Use the Railway GraphQL API with the account token. Use the project ID, environment ID, and service ID from the deploy flow:

```bash
curl -s https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -d '{
    "query": "mutation($input: CustomDomainCreateInput!) { customDomainCreate(input: $input) { id domain status { dnsRecords { hostlabel requiredValue } verificationDnsHost verificationToken verified } } }",
    "variables": {
      "input": {
        "projectId": "<project-id>",
        "environmentId": "<environment-id>",
        "serviceId": "<service-id>",
        "domain": "<name>.demo.nxtphase.ai"
      }
    }
  }'
```

The response contains **two** pieces of DNS info in different locations. You need both:

1. **CNAME target**, from `status.dnsRecords[0].requiredValue` (e.g. `6eaarp78.up.railway.app`)
2. **TXT verification hostname**, from `status.verificationDnsHost` (e.g. `_railway-verify.<name>.demo`)
3. **TXT verification value**, from `status.verificationToken` (e.g. `railway-verify=064f987...`)

The TXT fields are NOT inside `dnsRecords`. They are separate fields on `status`.

### Step 2: Create DNS records in Cloudflare

Use the Cloudflare API with `CLOUDFLARE_TOKEN`. The zone ID for `nxtphase.ai` is `e40778c5acc095d398219f0cb955b9b3`.

**CNAME record**, points the subdomain to Railway. Must use `proxied: false`, because Railway handles TLS itself and Cloudflare proxying breaks the SSL handshake (Cloudflare's free cert covers `*.nxtphase.ai` but not `*.demo.nxtphase.ai`):

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/e40778c5acc095d398219f0cb955b9b3/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "<name>.demo.nxtphase.ai",
    "content": "<hash>.up.railway.app",
    "ttl": 1,
    "proxied": false
  }'
```

**TXT record**, proves domain ownership to Railway. Use the `verificationDnsHost` and `verificationToken` from the domain creation response:

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/e40778c5acc095d398219f0cb955b9b3/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "TXT",
    "name": "<verificationDnsHost>.nxtphase.ai",
    "content": "<verificationToken>",
    "ttl": 3600,
    "proxied": false
  }'
```

### Step 3: Verify DNS propagation

Check against a public resolver first. Do not rely on `curl` from the local machine, since the local DNS cache may hold a stale NXDOMAIN:

```bash
# macOS/Linux:
dig @9.9.9.9 <name>.demo.nxtphase.ai CNAME +short    # should return <hash>.up.railway.app
dig @9.9.9.9 _railway-verify.<name>.demo.nxtphase.ai TXT +short

# Windows:
# nslookup -type=CNAME <name>.demo.nxtphase.ai 9.9.9.9
# nslookup -type=TXT _railway-verify.<name>.demo.nxtphase.ai 9.9.9.9
```

Once DNS confirms both records, test the URL:

```bash
curl -sI https://<name>.demo.nxtphase.ai               # should return 200
```

If `curl` fails but DNS looks correct, the local DNS cache is stale. Flush it or wait a few minutes:
- **macOS**: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- **Windows**: `ipconfig /flushdns`

## Remove a domain

To remove a custom domain, delete both DNS records from Cloudflare and remove the domain from Railway:

```bash
# Delete Cloudflare records by ID
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/e40778c5acc095d398219f0cb955b9b3/dns_records/<record-id>" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN"
```

Look up record IDs by querying existing records:

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/e40778c5acc095d398219f0cb955b9b3/dns_records?search=<name>.demo.nxtphase.ai" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN"
```
