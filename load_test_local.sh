#!/bin/bash
for i in {1..1000}; do
  curl -X POST \
    http://127.0.0.1:5000/orders \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": \"user_$i\",
      \"order_id\": \"order_$i\",
      \"item_ids\": [\"item_$i\"],
      \"total_amount\": $i
    }" &
done
wait