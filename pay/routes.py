from flask import Blueprint, request, jsonify
import stripe, os

pay_bp = Blueprint('pay', __name__)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@pay_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': data.get('service', 'Reserva')},
                'unit_amount': int(data.get('amount', 1000)),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success',
        cancel_url='http://localhost:5000/cancel',
    )
    return jsonify({'id': session.id})

@pay_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        return str(e), 400
    if event["type"] == "checkout.session.completed":
        print("💳 Pago confirmado", event["data"]["object"])
    return "", 200
