---
weight: 15
date: "2025-09-14T00:00:00+01:00"
draft: false
author: "VON"
title: "WebSocket Subscription Endpoints"
toc: true
description: "Overview of available WebSocket endpoints for real-time and delayed data subscriptions"
publishdate: "2025-09-14T00:00:00+01:00"
tags: ["API", "WebSocket", "Endpoints", "Real-time", "Delayed"]
---

## Overview

AiTrados provides multiple WebSocket endpoints to accommodate different data access needs. These endpoints allow you to subscribe to various types of financial data, including OHLC price data, news, and economic events. This document outlines the available endpoints and their specific characteristics.

## Available Subscription Endpoints

The AiTrados WebSocket API offers two primary endpoints for data subscription(OHLC, News, Economic Events):

- **Real-time data**: `wss://realtime.dataset-sub.aitrados.com/ws`
- **Delayed data**: `wss://delayed.dataset-sub.aitrados.com/ws`

