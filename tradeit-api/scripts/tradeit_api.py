#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def fail(msg, code=1):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def env_or(name, explicit=None):
    value = explicit if explicit not in (None, "") else os.environ.get(name)
    if not value:
        fail(f"Missing required value: {name}")
    return value


def request_json(method, base_url, access_token, path, body=None, query=None):
    url = base_url.rstrip("/") + path
    if query:
        qs = urllib.parse.urlencode(query, doseq=True)
        if qs:
            url += "?" + qs
    data = None
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"error": raw}
        fail(json.dumps({"status": e.code, "response": payload}, indent=2), e.code)


def load_json_arg(raw, file_path):
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    if raw:
        return json.loads(raw)
    return {}


def main():
    p = argparse.ArgumentParser(description="Trade It REST API helper for OpenClaw skills")
    p.add_argument("--api-url", default=os.environ.get("TRADEIT_API_URL"))
    p.add_argument("--access-token", default=os.environ.get("TRADEIT_ACCESS_TOKEN"))

    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("get-user")

    c = sub.add_parser("get-connection")
    c.add_argument("--id", type=int, required=True)

    h = sub.add_parser("get-holdings")
    h.add_argument("--account-id", type=int, required=True)

    ga = sub.add_parser("get-accounts")

    gt = sub.add_parser("get-trades")
    gt.add_argument("--order-by")
    gt.add_argument("--filter")
    gt.add_argument("--cursor")
    gt.add_argument("--refresh")
    gt.add_argument("--expand")

    te = sub.add_parser("tool-execute")
    te.add_argument("--tool-name", required=True)
    te.add_argument("--params-json")
    te.add_argument("--params-file")

    ct = sub.add_parser("create-trade")
    ct.add_argument("--params-json")
    ct.add_argument("--params-file")

    cot = sub.add_parser("create-options-trade")
    cot.add_argument("--params-json")
    cot.add_argument("--params-file")

    et = sub.add_parser("execute-trade")
    et.add_argument("--trade-id", type=int, required=True)

    su = sub.add_parser("get-session-url")
    su.add_argument("--target", choices=["connect", "trade"], required=True)
    su.add_argument("--brokerage-id", type=int)

    args = p.parse_args()
    api_url = env_or("TRADEIT_API_URL", args.api_url)
    access_token = env_or("TRADEIT_ACCESS_TOKEN", args.access_token)

    if args.command == "get-user":
        out = request_json("GET", api_url, access_token, "/api/auth/login")
    elif args.command == "get-connection":
        out = request_json("GET", api_url, access_token, f"/api/brokerageConnection/{args.id}")
    elif args.command == "get-holdings":
        out = request_json("GET", api_url, access_token, f"/api/account/{args.account_id}/holdings")
    elif args.command == "get-accounts":
        out = request_json("POST", api_url, access_token, "/api/tool/execute", {
            "toolName": "get_accounts",
            "params": {},
        })
    elif args.command == "get-trades":
        query = {}
        for key in ["order_by", "filter", "cursor", "refresh", "expand"]:
            val = getattr(args, key)
            if val is not None:
                query[{"order_by": "orderBy"}.get(key, key)] = val
        out = request_json("GET", api_url, access_token, "/api/trade", query=query)
    elif args.command == "tool-execute":
        out = request_json("POST", api_url, access_token, "/api/tool/execute", {
            "toolName": args.tool_name,
            "params": load_json_arg(args.params_json, args.params_file),
        })
    elif args.command == "create-trade":
        out = request_json("POST", api_url, access_token, "/api/tool/execute", {
            "toolName": "create_trade",
            "params": load_json_arg(args.params_json, args.params_file),
        })
    elif args.command == "create-options-trade":
        out = request_json("POST", api_url, access_token, "/api/tool/execute", {
            "toolName": "create_options_trade",
            "params": load_json_arg(args.params_json, args.params_file),
        })
    elif args.command == "execute-trade":
        out = request_json("POST", api_url, access_token, "/api/tool/execute", {
            "toolName": "execute_trade",
            "params": {"trade_id": args.trade_id},
        })
    elif args.command == "get-session-url":
        body = {"target": args.target}
        if args.brokerage_id is not None:
            body["brokerageId"] = args.brokerage_id
        out = request_json("POST", api_url, access_token, "/api/session/url", body)
    else:
        fail(f"Unknown command: {args.command}")

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
