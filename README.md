# Trade It OpenClaw Skill

Use Trade It in OpenClaw to connect brokerages, inspect accounts and holdings, and place trades on [supported brokerage accounts](https://docs.tradeit.app/brokerages): Robinhood, ETrade, Charles Schwab, Webull, Public, Tastytrade, Coinbase, and Kraken.

This repo contains a publishable OpenClaw skill that teaches agents how to use the Trade It API safely and consistently.

## What this is and what users can do with it

This project packages Trade It as an OpenClaw skill. With the right Trade It credentials, agents can help users:
- link brokerage accounts through secure OAuth flows
- inspect linked brokerage accounts, holdings, and trade history
- create stock and options trades
- execute trades on supported brokerages after explicit confirmation when appropriate
- generate hosted Trade It connect or trade URLs for browser handoff

The skill includes:
- a `SKILL.md` file that tells OpenClaw when and how to use Trade It
- a bundled Python helper for calling the API
- reference docs for endpoints, enums, examples, integration patterns, and security posture

## Why this exists

Trade It is a great fit for OpenClaw and other AI agents because it gives chat-driven products a clean path to real brokerage actions without forcing every integrator to build custom brokerage support from scratch.

## Trust, security, and user control

Trading access is sensitive. This skill is designed to be clear about that.

Key points:
- Trade It encrypts data at rest and in transit.
- Trade It stores revocable access tokens rather than usernames and passwords.
- Trade It users can revoke access directly from their brokerage or on https://tradeit.app.
- Trade It can place trades on a user's behalf, but cannot withdraw, transfer, or custody assets.
- This skill is written to prefer explicit confirmation before execution.
- The skill also acknowledges `yolo_mode`, where Trade It may place a trade immediately on create for users who have intentionally enabled that behavior. This is disabled by default.

Read more:
- Trade It site: <https://tradeit.app>
- Security: <https://tradeit.app/security>
- Privacy Policy: <https://tradeit.app/privacy-policy>
- Terms of Service: <https://tradeit.app/terms-of-service>
- Contact: <https://tradeit.app/contact>

## Important disclaimers

- All investing involves risk, including the possible loss of principal.
- This skill is an integration layer, not investment advice.
- Users remain responsible for reviewing brokerage connections, orders, account choices, and trade details.
- AI outputs can be wrong. Orders and trade flows should be reviewed carefully.
- Third-party brokerages have their own terms, availability, fees, and execution behavior.

## How authentication works

Trade It supports:
- API keys for direct API access

For this skill:
- `TRADEIT_ACCESS_TOKEN` is required
- `TRADEIT_API_URL` is optional and defaults to `https://api.tradeit.app`

API keys can be created here after creating a Trade It account:
- <https://tradeit.app/account/api-keys>

## How the skill behaves

The skill is written around two main patterns:

### 1. API-native trading flow
Gather info and place trade orders entirely in-chat.

### 2. Hosted browser handoff
A more visual experience. Trade It generates session URLs so you can connect brokerages or review, edit, and place trades in the browser.

## Drafts, execution, and `yolo_mode`

The default and recommended trading flow is:
1. create a trade
2. inspect returned status
3. if still draft, ask for confirmation
4. execute if confirmed

But if users wish to give the bot complete control to execute trades on their behalf without requesting confirmation, they may enable `yolo_mode` in the settings on https://tradeit.app.

When enabled, a `create_trade` or `create_options_trade` call may place the trade immediately, skipping the separate execution step.

That means this skill does **not** blindly assume every create call is draft-only. It checks status first.

## Repo contents

```txt
tradeit-api/
├── SKILL.md
├── scripts/
│   └── tradeit_api.py
└── references/
    ├── api-reference.md
    ├── enums.md
    ├── examples.md
    ├── integration-patterns.md
    └── security.md
```

## References included in the skill

- `api-reference.md` — JSON-first API request/response shapes
- `enums.md` — brokerage ids, order types, time-in-force values, statuses, and other constants
- `examples.md` — concrete integration and conversation examples
- `integration-patterns.md` — recommended architecture and workflow guidance
- `security.md` — public Trade It security posture summary with disclaimer language

## Installing / using

If you want to publish or distribute the packaged skill, use:
- `tradeit-api.skill`

If you want to edit the source, use the folder:
- `tradeit-api/`

Typical OpenClaw usage expects the skill to be installed into a skills directory and supplied with the needed environment variables for the agent run.

## Who should use this

This is for:
- OpenClaw users who want brokerage-backed trading flows
- developers building AI trading assistants or chatbot workflows
- products that want a unified brokerage layer instead of brokerage-by-brokerage integrations

## Questions, support, and contact

If you have questions about Trade It, supported brokerages, security, or integration details:
- Contact page: <https://tradeit.app/contact>
- Main site: <https://tradeit.app>
- Docs: <https://docs.tradeit.app>
- FAQ: <https://tradeit.app/faq>

## Legal and policy links

- Website: <https://tradeit.app>
- Docs: <https://docs.tradeit.app>
- Security: <https://tradeit.app/security>
- Privacy Policy: <https://tradeit.app/privacy-policy>
- Terms of Service: <https://tradeit.app/terms-of-service>
- Contact: <https://tradeit.app/contact>

## License

See `LICENSE` in this repository.
