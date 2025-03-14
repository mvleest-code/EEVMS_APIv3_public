# README

## Overview

This repository contains two main Python scripts: `app.poll.events.py` and `app.sse.subscription.py`. Both scripts are designed to handle event-driven data but use different methods to achieve this. Both scripts save the output into `events.log`.

## Scripts

### app.poll.events.py

- **Description**: This script uses a polling mechanism to check for new events at regular intervals.
- **Usage**: Suitable for environments where Server-Sent Events (SSE) are not supported or when a simpler implementation is preferred.
- **Pros**:
    - Simpler to implement.
    - Works in environments without SSE support.
- **Cons**:
    - Higher latency due to polling intervals.
    - Increased load on the server due to frequent requests.

### app.sse.subscription.py

- **Description**: This script uses Server-Sent Events (SSE) to receive real-time updates from the server.
- **Usage**: Ideal for applications requiring real-time data updates with minimal latency.
- **Pros**:
    - Lower latency as events are pushed from the server.
    - Reduced server load compared to polling.
- **Cons**:
    - Requires SSE support on both client and server.
    - More complex to implement.

## Differences

- **Mechanism**:
    - `app.poll.events.py` uses polling.
    - `app.sse.subscription.py` uses Server-Sent Events (SSE).
- **Latency**:
    - `app.poll.events.py` has higher latency.
    - `app.sse.subscription.py` has lower latency.
- **Server Load**:
    - `app.poll.events.py` increases server load.
    - `app.sse.subscription.py` reduces server load.
- **Complexity**:
    - `app.poll.events.py` is simpler to implement.
    - `app.sse.subscription.py` is more complex.

## Authentication

Both scripts require a `clientId` and `secret` for authentication, as well as a non-rotating token. Without a non-rotating token, you need to generate a new refresh token every time you want to run the code.

### Instructions

1. **Obtain `clientId` and `secret`**:
    - Register your application with the service provider to get the `clientId` and `secret`.
    - Ensure you have the necessary permissions for accessing the event data.

2. **Non-Rotating Token**:
    - Generate a non-rotating token from the service provider's dashboard.
    - This token will be used for authenticating API requests.

3. **Configuration**:
    - Update the configuration file or environment variables with the `clientId`, `secret`, and non-rotating token.
    - Ensure the scripts can access these credentials securely.

## Conclusion

Choose `app.poll.events.py` for simpler implementations or environments without SSE support. Opt for `app.sse.subscription.py` for real-time updates with lower latency and reduced server load. Both scripts save the output into `events.log`.

