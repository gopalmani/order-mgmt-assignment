# order-mgmt-assignment
Built a backend system to manage and process orders in an e-commerce platform. 

# E-commerce Order Management System 🛒

A scalable backend system for managing and processing e-commerce orders with RESTful APIs, asynchronous processing, and real-time metrics.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Build](https://img.shields.io/badge/Build-Passing-success)

---

## Table of Contents
- [Features](#features-)
- [Technologies](#technologies-)
- [Quick Start](#quick-start-)
- [API Documentation](#api-documentation-)
- [Design Decisions](#design-decisions-)
- [Database Schema](#database-schema-)
- [Load Testing](#load-testing-)
- [License](#license-)

---

## Features ✨
- **Order Submission**: REST API to create orders
- **Async Processing**: In-memory queue with worker threads
- **Order Tracking**: Check status (`pending`/`processing`/`completed`)
- **Metrics**: Real-time stats (total orders, avg processing time, status counts)
- **Scalable**: Handles 1,000+ concurrent orders

---

## Technologies 🛠️
- **Backend**: Python/Flask
- **Database**: SQLite (lightweight, serverless)
- **Queue**: `queue.Queue` with threading
- **Testing**: Built-in unittest module

---

## Quick Start 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ecommerce-order-system.git
cd ecommerce-order-system
2. Create Virtual Environment
bash
Copy
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
3. Install Dependencies
bash
Copy
pip install -r requirements.txt
4. Initialize Database
bash
Copy
python app.py  # Creates orders.db automatically
5. Start the Server
bash
Copy
python app.py
Server runs at http://localhost:5000

API Documentation 📚
1. Create an Order
bash
Copy
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "order_id": "order_456",
    "item_ids": ["item_1", "item_2"],
    "total_amount": 150.99
  }'
Response:

json
Copy
{
  "order_id": "order_456",
  "status": "pending"
}
2. Check Order Status
bash
Copy
curl http://localhost:5000/orders/order_456/status
Response:

json
Copy
{
  "order_id": "order_456",
  "status": "completed"
}
3. Get Metrics
bash
Copy
curl http://localhost:5000/metrics
Response:

json
Copy
{
  "total_orders": 42,
  "average_processing_time": 0.5,
  "status_counts": {
    "pending": 2,
    "processing": 5,
    "completed": 35
  }
}
Design Decisions 💡
Database Choice (SQLite)
Why SQLite?

Serverless & lightweight for rapid development

ACID-compliant with transaction support

Single-file storage simplifies deployment

Trade-off: Not ideal for distributed systems (use PostgreSQL in production)

Queue Implementation
In-Memory Queue:

Uses Python's queue.Queue for simplicity

4 worker threads for parallel processing

Limitation: Not persistent (use Redis/RabbitMQ in production)

Thread Safety
SQLite write-ahead log (WAL) mode ensures thread-safe DB operations

Scalability
Worker Threads: Configurable via num_workers in QueueManager

Concurrency: Flask runs in threaded mode (threaded=True)

Database Schema 🔍
sql
Copy
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  item_ids TEXT NOT NULL,  -- Stored as JSON array
  total_amount REAL NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP
);
Timestamps:

created_at: Order submission time

started_at: Processing start time

completed_at: Order completion time

Load Testing ⚡
Simulate 1,000 concurrent orders:

bash
Copy
./load_test.sh
Sample Script (load_test.sh):

bash
Copy
#!/bin/bash
for i in {1..1000}; do
  curl -X POST http://localhost:5000/orders \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": \"user_$i\",
      \"order_id\": \"order_$i\",
      \"item_ids\": [\"item_$i\"],
      \"total_amount\": $i
    }" &
done
wait
License 📄
MIT License - See LICENSE

Contribution: Feel free to open issues or PRs!
Author: Your Name
Contact: your.email@example.com

Copy

---

**How to Use This README**:
1. Replace `yourusername`, `your.email@example.com`, etc.
2. Add actual `requirements.txt` and `LICENSE` files
3. Include `load_test.sh` in your repo

This provides everything a user needs to understand, run, and extend your system! 🎉
