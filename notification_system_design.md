# Stage 1

## Notification System REST API Design

This notification system is used to send real-time updates for:

- Placements
- Events
- Results

---

# Core Actions

1. Create Notification
2. Get Notifications
3. Mark Notification as Read
4. Delete Notification
5. Real-Time Notification Delivery

---

# 1. Create Notification

## Endpoint

POST /api/notifications

## Headers

```http
Authorization: Bearer token
Content-Type: application/json
```

## Request Body

```json
{
  "type": "Placement",
  "message": "CSX Corporation hiring"
}
```

## Response

```json
{
  "success": true,
  "notificationId": "b283218f"
}
```

---

# 2. Get Notifications

## Endpoint

GET /api/notifications

## Response

```json
[
  {
    "id": "b283218f",
    "type": "Placement",
    "message": "CSX Corporation hiring",
    "timestamp": "2026-04-22 17:51:18",
    "isRead": false
  }
]
```

---

# 3. Mark Notification as Read

## Endpoint

PATCH /api/notifications/:id/read

## Response

```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

# 4. Delete Notification

## Endpoint

DELETE /api/notifications/:id

## Response

```json
{
  "success": true,
  "message": "Notification deleted"
}
```

---

# Real-Time Notification Mechanism

Real-time notifications can be implemented using:

- WebSockets
- Socket.IO

Whenever a new notification is created, the server instantly pushes the notification to connected users without refreshing the page.
# Stage 2

## Database Choice

I suggest using MongoDB because:

- Flexible schema
- Easy to scale
- Suitable for real-time notification systems
- Fast data retrieval

---

# Notification Collection Schema

```json
{
  "_id": "ObjectId",
  "type": "Placement",
  "message": "CSX Corporation hiring",
  "timestamp": "2026-04-22 17:51:18",
  "isRead": false
}
```

---

# Problems as Data Volume Increases

1. Slow query performance
2. Increased storage usage
3. High server load
4. Delayed notification delivery

---

# Solutions

1. Database indexing
2. Pagination
3. Caching using Redis
4. Database sharding
5. Load balancing

---

# MongoDB Queries

## Insert Notification

```js
db.notifications.insertOne({
  type: "Placement",
  message: "CSX Corporation hiring",
  timestamp: "2026-04-22 17:51:18",
  isRead: false
})
```

---

## Get Notifications

```js
db.notifications.find()
```

---

## Mark Notification as Read

```js
db.notifications.updateOne(
  { _id: ObjectId("b283218f") },
  { $set: { isRead: true } }
)
```

---

## Delete Notification

```js
db.notifications.deleteOne(
  { _id: ObjectId("b283218f") }
)
```
# Stage 3

## Query Analysis and Optimization

### The Query Given:

SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;

---

### Is this query accurate?

Yes, this query is correct in terms of what it is trying to do.
It fetches unread notifications for a particular student (ID 1042)
and shows the latest ones first. The logic and syntax are fine.

---

### Then why is it slow?

The problem is not the query itself — it is the data size.
We have 50,000 students and 5 million notifications.
When there is no index on the table, the database has no choice
but to go through every single row in the notifications table
to find the ones that match. This is called a full table scan
and it becomes very slow as data grows.

---

### What I would change:

First, I would add a composite index on the columns
we are filtering and sorting by:

CREATE INDEX idx_notify_student
ON notifications(studentID, isRead, createdAt DESC);

This way the database directly jumps to the relevant rows
instead of scanning everything.

Second, I would stop using SELECT * because it fetches
all columns even if we don't need them. Instead:

SELECT id, message, notificationType, createdAt
FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt DESC;

### Computation cost difference:

Without index — database reads all 5 million rows every time.
With index — database reads only the rows for that student.
The time goes from O(n) to O(log n) which is a huge difference
especially when the data keeps growing.

---

### About indexing every column:

I don't think that is a good idea.
Yes, indexes make reads faster but they slow down writes.
Every time we insert or update a row, the database has to
update all the indexes too. If every column is indexed,
that becomes a lot of extra work for every single write.
It also uses a lot more storage.
The right approach is to only index columns that are
frequently used in WHERE, ORDER BY or JOIN conditions.

---

### Query to find students who got a Placement notification in the last 7 days:

SELECT DISTINCT studentID
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL 7 DAY
ORDER BY studentID;

Here I used DISTINCT because one student might have received
multiple placement notifications. The INTERVAL 7 DAY part
makes sure we only look at the last 7 days from today.
The notificationType column uses enum values and
'Placement' is one of them along with 'Event' and 'Result'.
# Stage 4

## The Problem

Every time a student opens the app, the server goes to the
database and fetches notifications. This happens for every
student on every page load. When 50,000 students are using
the app at the same time, the database gets hit thousands
of times per second. That is why it is getting overwhelmed
and the experience becomes slow.

---

## What I would do to fix this

### 1. Add Caching with Redis

My first thought was to use caching. Instead of going to
the database every single time, we save the notifications
in Redis for a short time. Redis is like a temporary memory
that is much faster than a database.

So when a student opens the app, we check Redis first.
If the data is there, we return it directly without touching
the database at all. Only when the cache expires or is empty
do we go to the database.

The tradeoff here is that sometimes the student might see
slightly old notifications for a minute or two until the
cache refreshes. But that is acceptable for most cases.

---

### 2. Pagination

Right now it seems like all notifications are being loaded
at once. That is unnecessary. I would load only 10 or 20
at a time and let the student scroll to load more.

This makes each request much smaller and faster.
The downside is the student needs to scroll to see older ones
but that is a normal pattern in most apps anyway.

---

### 3. Push notifications using WebSockets

Instead of fetching every time the page loads, we can push
new notifications to the student the moment they arrive.
This way the page does not need to keep asking the server
again and again.

The tradeoff is that keeping WebSocket connections open
for all 50,000 students at once requires more server memory.
But it completely removes the repeated DB hits problem.

---

### 4. Background jobs

We can prepare and compute the notifications in the
background before the student even opens the page.
When they open it, we just return the already ready result.

The only downside is a small delay - the notification appears
after the background job runs, not instantly. But for most
use cases this delay is only a few seconds.

---

## What I would actually go with

I would combine caching and pagination together.
Cache the recent unread notifications per student in Redis.
Load them in pages of 20 at a time.
This reduces DB load significantly and keeps the app fast
without much complexity added.