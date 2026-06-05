# Notification System Design

A backend system design project that covers database design,
API development, performance optimization, and real-time
notification delivery.

---

## Project Structure

- notification_system_design.md — System design documentation
- priority_inbox.py — Priority inbox implementation
- register.py — Registration script
- get_token.py — Authentication script

---

## Stages Covered

### Stage 1 — System Design
Designed the overall notification system architecture
including database choice, API structure, and real-time
delivery mechanism using WebSockets.

### Stage 2 — Database Design
Chose MongoDB for its flexible schema and scalability.
Designed the notification collection schema and wrote
basic CRUD queries.

### Stage 3 — SQL Query Analysis
Analyzed a slow performing SQL query on a large dataset.
Identified full table scan as the root cause and fixed it
using composite indexing. Also wrote an optimized query
to find students with placement notifications in last 7 days.

### Stage 4 — Performance Optimization
Identified the problem of DB getting overwhelmed due to
notifications being fetched on every page load.
Suggested caching with Redis, pagination, WebSockets,
and background jobs as solutions with tradeoffs.

### Stage 5 — Reliable Notification Delivery
Analyzed shortcomings of a sequential notify_all function.
Redesigned it using a message queue approach to handle
50,000 students reliably with retry logic for failures.

### Stage 6 — Priority Inbox
Built a working Python solution that fetches notifications
from a live API and ranks them by priority score.
Priority is calculated based on notification type weight
and recency. Top 10 notifications are displayed.

Priority weights used:
- Placement = highest priority
- Result = medium priority
- Event = lowest priority

---

## How to Run Stage 6

Install dependencies:
pip install requests

Run the priority inbox:
python priority_inbox.py

---

## Tech Stack

- Python
- REST APIs
- MongoDB (design)
- Redis (design)
- WebSockets / Socket.IO (design)
- Git and GitHub