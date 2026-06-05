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