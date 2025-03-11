from flask import Flask, request, jsonify
from models import init_db, insert_order, get_order_status, get_metrics
from queue_manager import QueueManager

app = Flask(__name__)
queue_manager = QueueManager(num_workers=4)
queue_manager.start()

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order_id = data.get('order_id')
    user_id = data.get('user_id')
    item_ids = data.get('item_ids')
    total_amount = data.get('total_amount')

    if not all([order_id, user_id, item_ids, total_amount is not None]):
        return jsonify({'error': 'Missing required fields'}), 400

    success = insert_order(order_id, user_id, item_ids, total_amount)
    if not success:
        return jsonify({'error': 'Order ID already exists'}), 400

    queue_manager.add_order(order_id)
    return jsonify({'order_id': order_id, 'status': 'pending'}), 201

@app.route('/orders/<order_id>/status', methods=['GET'])
def order_status(order_id):
    status = get_order_status(order_id)
    if status is None:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({'order_id': order_id, 'status': status})

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(get_metrics())

if __name__ == '__main__':
    init_db()
    app.run(threaded=True)