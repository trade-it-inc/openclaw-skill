# Trade It Enums and Constants

Use these values exactly. Do not invent alternates.

## Brokerage ids

```json
{
  "BrokerageID": {
    "Robinhood": 1,
    "ETrade": 2,
    "Coinbase": 3,
    "Kraken": 5,
    "CharlesSchwab": 7,
    "Webull": 8,
    "Public": 11,
    "Tastytrade": 12
  }
}
```

## Brokerage token status

```json
{
  "BrokerageTokenStatus": {
    "Pending": 0,
    "Verified": 1,
    "Error": 10
  }
}
```

## Trade action

```json
{
  "TradeAction": {
    "Buy": "buy",
    "Sell": "sell"
  }
}
```

## Position effect

```json
{
  "PositionEffect": {
    "Open": "open",
    "Close": "close"
  }
}
```

## Order type

```json
{
  "OrderType": {
    "Market": "market",
    "Limit": "limit",
    "Stop": "stop",
    "StopLimit": "stop_limit"
  }
}
```

## Order direction

```json
{
  "OrderDirection": {
    "Debit": "debit",
    "Credit": "credit"
  }
}
```

## Time in force

```json
{
  "TimeInForce": {
    "Day": "day",
    "GoodTillCanceled": "gtc",
    "ImmediateOrCancel": "ioc",
    "FillOrKill": "fok"
  }
}
```

## Trade unit

```json
{
  "TradeUnit": {
    "Dollars": "dollars",
    "Shares": "shares"
  }
}
```

## Trade status

```json
{
  "TradeStatus": {
    "Draft": "draft",
    "Pending": "pending",
    "Placed": "placed",
    "PartiallyFilled": "partially_filled",
    "Complete": "complete",
    "Canceled": "canceled",
    "Failed": "failed",
    "Disconnected": "disconnected"
  }
}
```

## Guidance

When the user names a brokerage in natural language, map it to the correct numeric `brokerageId` from this file instead of guessing.

When building orders, prefer enum values from this file over prose labels.