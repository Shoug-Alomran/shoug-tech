#!/usr/bin/env bash
# What visitors ask the About page assistant, as anonymous topic counts.
# The Worker records only a topic label per question (no text, no IP) in the
# Workers Analytics Engine dataset "about_assistant_topics".
#
# Needs a Cloudflare API token with "Account Analytics: Read":
#   CF_ACCOUNT_ID=... CF_API_TOKEN=... scripts/about_assistant_topics.sh [days]
set -euo pipefail
: "${CF_ACCOUNT_ID:?set CF_ACCOUNT_ID (Cloudflare dashboard > Workers > Account ID)}"
: "${CF_API_TOKEN:?set CF_API_TOKEN (API token with Account Analytics: Read)}"
DAYS="${1:-30}"
[[ "$DAYS" =~ ^[0-9]+$ ]] || { echo "days must be a number" >&2; exit 2; }

curl -sS "https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/analytics_engine/sql" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  --data "SELECT blob1 AS topic, SUM(_sample_interval) AS questions
          FROM about_assistant_topics
          WHERE timestamp > NOW() - INTERVAL '${DAYS}' DAY
          GROUP BY topic ORDER BY questions DESC
          FORMAT TabSeparatedWithNames"
echo
