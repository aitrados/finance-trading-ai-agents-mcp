---
title: "Overview"
weight: 10
description: "An overview of how the AiTrados API simplifies the complex process of managing real-time, rolling OHLC chart data for quantitative trading."
icon: "bar_chart"
date: "2025-09-15T10:00:00+01:00"
lastmod: "2025-09-15T10:00:00+01:00"
draft: false
tags: ["OHLC", "Real-time", "Charting", "WebSocket", "API", "Quantitative Trading"]
---

# Overview: Simplifying the Latest OHLC Chart Flow

## The Challenge: Managing a Real-Time Rolling Chart

A fundamental challenge for quantitative trading developers is maintaining a clean, up-to-date series of OHLC (Open, High, Low, Close) data, often referred to as a "rolling chart." The goal is to always have the most recent `N` candles available for analysis, allowing trading algorithms to react to the latest market movements.

Let's consider a common scenario:
- **Requirement**: You need to maintain the latest 150 candles of a 5-minute chart.
- **Current Time**: 10:07.
- **Problem**: The most recent candle in your dataset is the one for the 10:05 - 10:10 interval. This candle is still "live" or "unclosed." Its high, low, and close prices are constantly changing with every new trade. At 10:10, this candle will close, and a new one for the 10:10 - 10:15 interval will begin.

A naive implementation quickly becomes complex and error-prone. Developers often find themselves wrestling with:

1.  **Initial Data Fetching**: How to get the first `N-1` historical candles to start the process.
2.  **Real-Time Updates**: Constantly polling a REST API is inefficient, leads to rate-limiting, and introduces latency.
3.  **State Management**: Manually managing a list or DataFrame of 150 candles.
4.  **Candle Synchronization**: Writing complex logic to handle the "roll-over." This involves:
    -   Updating the `high`, `low`, and `close` of the last, unclosed candle.
    -   Precisely identifying when the current interval has ended.
    -   Appending the newly formed, closed candle to the historical series.
    -   Removing the oldest candle from the series to maintain the fixed size of 150.
    -   Handling network delays, missing data, and timestamp alignment issues.

This "data plumbing" distracts developers from their primary goal: building and testing profitable trading strategies.

## The AiTrados Solution: A Unique API Architecture

The AiTrados API provides a unique architecture that abstracts away this complexity. By combining a powerful REST API for historical data with a high-performance WebSocket stream for real-time updates, we make managing a live, rolling chart incredibly simple.

Our framework is designed to handle the entire lifecycle of the chart data for you.

### The Flow Explained

Here is how the AiTrados API elegantly solves the problem:

1.  **Initial State Hydration**: When you request a latest OHLC stream, the system first makes a **single, initial API call** to fetch the most recent `N-1` (e.g., 149) *completed* historical candles. This provides the immediate historical context needed for your indicators (like moving averages, RSI, etc.).

2.  **Real-Time WebSocket Subscription**: Simultaneously, the system automatically subscribes to a dedicated WebSocket channel for the instrument and interval you've specified.

3.  **Live Candle Management (The Magic)**: The framework now takes over completely:
    -   **Updating the Current Candle**: The system uses the real-time WebSocket feed to continuously update the `high`, `low`, and `close` values of the current, unclosed candle (the 150th candle).
    -   **Automatic Rollover**: At the exact moment the interval ends (e.g., at 10:10:00), the framework automatically:
        a. Finalizes the 150th candle, marking it as "closed."
        b. Removes the oldest candle (the 1st candle) from the dataset.
        c. Appends a new, empty candle for the next interval (e.g., 10:10 - 10:15), which now becomes the new 150th candle.
    -   **Data Push**: The newly updated dataset of 150 candles is then pushed to your client code.

### The Result: Simplicity and Focus

With this architecture, developers are freed from the complexities of state and time management. Instead of building and debugging data synchronization logic, you simply provide a callback function that receives a clean, perfectly synchronized list of the latest 150 candles on every update.

This allows you to focus 100% of your effort on what truly matters: **analyzing the data and developing your trading logic.**