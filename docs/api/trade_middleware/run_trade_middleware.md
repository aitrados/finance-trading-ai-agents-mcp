---
title: "Run Trading Middleware"
weight: 20
description: "Run and operate the AiTrados trading communication middleware. Quick start, sample output, instance reuse guidance, and best practices for multi-process deployments."
icon: "play"
date: "2025-09-22T21:12:07+01:00"
lastmod: "2025-09-22T21:12:07+01:00"
draft: false
author: "VON"
tags: ["Trading Middleware", "Runbook", "Deployment", "Best Practices"]
categories: ["Middleware", "Operational"]
keywords: ["run", "middleware", "GIL", "multi-process", "ZeroMQ"]
---

# Running the AiTrados Trading Middleware

This document shows a minimal, production-minded way to start the AiTrados trading communication middleware, demonstrates expected output, and describes instance reuse and multi-process best practices.

## Overview

The middleware integrates API calls, WebSocket subscription management (subscribe/unsubscribe), chart streaming (scrolling OHLC data), and multi-symbol multi-timeframe alignment. It exposes a single entrypoint to start all routers and managers, while keeping class instances reusable across modules, processes and languages via ZeroMQ.

## Quick start

Use the provided helper to start the entire middleware stack. The example below demonstrates a safe pattern that keeps the process alive until a KeyboardInterrupt is received.

```python
import time
from aitrados_api.universal_interface.trade_middleware_instance import AitradosTradeMiddlewareInstance

if __name__ == "__main__":
    # Start all middleware components (RPC router, Pub/Sub router, managers, clients, etc.)
    AitradosTradeMiddlewareInstance.run_all()

    try:
        # Keep the main thread alive while background routers run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("closing...")
```

Notes:
- run_all() initializes RPC & Pub/Sub routers, API and WS clients, chart managers, and multi-timeframe aligners.
- Keep the process alive so background threads/processes can continue to operate.

## Expected output (example logs)

```shell
2025-10-22 21:12:07.686 | INFO     | 📡 Pubsub Router Started
2025-10-22 21:12:07.686 | DEBUG    |                          Sub addr:['tcp://127.0.0.1:51593', 'ipc:///tmp/aitrados_sub_your_pc_name.sock', 'inproc://aitrados_sub']
2025-10-22 21:12:07.686 | DEBUG    |                          Pub addr:['tcp://127.0.0.1:51594', 'ipc:///tmp/aitrados_pub_sub_your_pc_name.sock', 'inproc://aitrados_pub']
2025-10-22 21:12:07.686 | INFO     | 🌐 RPC Router Started
2025-10-22 21:12:07.686 | DEBUG    |                          RPC frontend addr:['tcp://127.0.0.1:51591', 'ipc:///tmp/aitrados_frontend_sub_your_pc_name.sock', 'inproc://aitrados_frontend']
2025-10-22 21:12:07.686 | DEBUG    |                          RPC backend addr:['tcp://127.0.0.1:51592', 'ipc:///tmp/aitrados_backend_sub_your_pc_name.sock', 'inproc://aitrados_backend']
2025-10-22 21:12:07.888 | DEBUG    | RPC backend 'aitrados_api' is submitting to Register RPC Service
```

## Instance reuse (class reuse)

- api_client, ws_client, chart streaming managers, and multi-timeframe aligners are intended to be initialized once per middleware instance.
- Other modules (in the same process or connected via ZeroMQ) should reuse these instances through the exposed RPC/IPC interfaces.
- Even across processes and languages the same logical instances are accessible via the middleware’s messaging layer.

## GIL, heavy strategies and multi-process guidance

- Python's GIL can limit CPU-bound strategy performance if everything runs in a single process.
- Recommendations:
  1. Decompose heavy strategies into separate processes or services (or run them in Rust/C++ if low-latency is required).
  2. Run long-running or CPU-intensive tasks (e.g., advanced price-action analysis, local LLM inference) outside the main middleware process.
  3. Use ZeroMQ-backed RPC/pub-sub to exchange data and commands between the middleware and worker processes.

## Common strategy bundles

Typical components combined in AiTrados deployments:
- OHLC Data Processing
- Macroeconomic Analysis
- Fundamental Analysis
- Traditional Technical Indicators
- Advanced Price Action Strategies
- News & Event Processing
- Breaking News Analysis
- Financial Calendar Events
- Risk Management
- Financial MCP Tools
- LLM-Powered Strategies

Design each component as a separate, replaceable module and use the middleware to orchestrate data flows and decisions.

## Troubleshooting & operational notes

- IPC sockets under /tmp may require correct permission and cleanup between runs.
- Ensure configured TCP ports are open and not blocked by local firewall rules.
- For debugging, enable DEBUG logging to inspect router addresses and registration flow.
- When upgrading or restarting, gracefully stop components to avoid stale IPC files.

## Closing

This page provides the minimal runbook to start the middleware and practical advice to keep complex strategies scalable and maintainable. For architecture diagrams and deeper operational tips, see the main Overview page.

