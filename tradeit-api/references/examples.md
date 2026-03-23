# Example Prompts and Implementation Patterns

## Trigger examples

These are the kinds of requests that should trigger this skill:
- "Add Trade It REST API support to our OpenClaw skill"
- "Implement endpoints for get accounts, create trade, and execute trade"
- "When the user isn't connected, generate a Trade It connect URL"
- "Build a chatbot flow that drafts trades first, then executes on confirmation"
- "Fetch holdings and trades from Trade It and summarize the account"

## Example server adapter

```ts
async function tradeItFetch<T>(path: string, init: RequestInit, accessToken: string): Promise<T> {
  const res = await fetch(`${process.env.TRADEIT_API_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
      ...(init.headers ?? {}),
    },
  });

  if (!res.ok) {
    throw new Error(`Trade It request failed: ${res.status} ${await res.text()}`);
  }

  return res.json() as Promise<T>;
}
```

## Example account lookup

```ts
export function getTradeItAccounts(accessToken: string) {
  return tradeItFetch('/api/tool/execute', {
    method: 'POST',
    body: JSON.stringify({
      toolName: 'get_accounts',
      params: {},
    }),
  }, accessToken);
}
```

## Example draft trade creation

```ts
export function createTradeItDraftTrade(accessToken: string, accountId: number) {
  return tradeItFetch('/api/tool/execute', {
    method: 'POST',
    body: JSON.stringify({
      toolName: 'create_trade',
      params: {
        symbol: 'TSLA',
        amount: 1000,
        unit: 'dollars',
        buy_or_sell: 'buy',
        order_type: 'limit',
        limit_price: 250,
        time_in_force: 'day',
        account_id: accountId,
      },
    }),
  }, accessToken);
}
```

## Example draft options trade creation

```ts
export function createTradeItDraftOptionsTrade(accessToken: string, accountId: number) {
  return tradeItFetch('/api/tool/execute', {
    method: 'POST',
    body: JSON.stringify({
      toolName: 'create_options_trade',
      params: {
        symbol: 'SPY',
        legs: [
          {
            type: 'option',
            action: 'buy',
            position_effect: 'open',
            occ: '260620P00580000',
            quantity: 1,
          },
          {
            type: 'option',
            action: 'sell',
            position_effect: 'open',
            occ: '260620P00570000',
            quantity: 1,
          },
        ],
        direction: 'debit',
        order_type: 'limit',
        limit_price: 2.35,
        time_in_force: 'day',
        account_id: accountId,
      },
    }),
  }, accessToken);
}
```

## Example execute step

```ts
export function executeTradeItTrade(accessToken: string, tradeId: number) {
  return tradeItFetch('/api/tool/execute', {
    method: 'POST',
    body: JSON.stringify({
      toolName: 'execute_trade',
      params: { trade_id: tradeId },
    }),
  }, accessToken);
}
```

## Example session URL generation

```ts
export function createTradeItSessionUrl(
  accessToken: string,
  body: { target: 'connect' | 'trade'; brokerageId?: number }
) {
  return tradeItFetch('/api/session/url', {
    method: 'POST',
    body: JSON.stringify(body),
  }, accessToken);
}
```

## Example reads

```ts
export function getTradeItUser(accessToken: string) {
  return tradeItFetch('/api/auth/login', { method: 'GET' }, accessToken);
}

export function getTradeItConnection(accessToken: string, id: number) {
  return tradeItFetch(`/api/brokerageConnection/${id}`, { method: 'GET' }, accessToken);
}

export function getTradeItHoldings(accessToken: string, id: number) {
  return tradeItFetch(`/api/account/${id}/holdings`, { method: 'GET' }, accessToken);
}

export function getTradeItTrades(accessToken: string, query = 'orderBy=id DESC') {
  return tradeItFetch(`/api/trade?${query}`, { method: 'GET' }, accessToken);
}
```

## Example chatbot flow

### Not connected yet

User:
"Buy $1000 of TSLA on my Robinhood account"

Assistant:
"First I need you to connect Robinhood in Trade It. Open this link, finish the connection, then come back and I'll draft the order."

Backend action:
- `POST /api/session/url` with `{ "target": "connect", "brokerageId": 1 }`

### Connected, draft first

User:
"Buy $1000 of TSLA at $250 limit on Robinhood"

Assistant:
"I created the trade request and it is still in draft status: buy about $1000 of TSLA as a day limit order at $250 in account Robinhood x1234. Want me to place it?"

Backend actions:
- `get_accounts`
- `create_trade`
- inspect returned `status`

### Connected, yolo mode enabled

User:
"Buy $1000 of TSLA at $250 limit on Robinhood"

Assistant:
"The trade was placed immediately because yolo mode is enabled on your account."

Backend actions:
- `getTradeItUser` or equivalent user-context lookup when available
- `create_trade`
- inspect returned `status`

### Explicit execution

User:
"Yes, place it"

Assistant:
"Done. The order has been sent to the brokerage."

Backend action:
- `execute_trade`
