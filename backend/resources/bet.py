from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Bet, User
from datetime import datetime, timezone

bet_bp = Blueprint('bet', __name__)

@bet_bp.route('', methods=['POST'])
@jwt_required()
def create_bet():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    event = data.get('event')
    amount = data.get('amount')
    odds = data.get('odds')
    result = data.get('result', 'Pending')
    date_str = data.get('date')
    bet_type = data.get('bet_type')
    sport = data.get('sport')

    if not event or amount is None or odds is None:
        return jsonify({"error": "event, amount, and odds are required"}), 400
    
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    if odds <= 0:
        return jsonify({"error": "Odds must be positive"}), 400

    try:
        if date_str:
            date = datetime.fromisoformat(date_str)
        else:
            date = datetime.now(timezone.utc)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    
    bet = Bet(
        event=event,
        amount=amount,
        odds=odds,
        result=result,
        date=date,
        bet_type=bet_type,
        sport=sport,
        user_id=user_id
    )

    db.session.add(bet)
    db.session.commit()

    return jsonify({
        "id": bet.id,
        "event": bet.event,
        "amount": bet.amount,
        "odds": bet.odds,
        "result": bet.result,
        "date": bet.date.isoformat(),
        "bet_type": bet.bet_type,
        "sport": bet.sport,
        "payout": bet.payout
    }), 201

@bet_bp.route('', methods=['GET'])
@jwt_required()
def get_bets():
    user_id = int(get_jwt_identity())

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    paginated = Bet.query.filter_by(user_id=user_id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "bets": [
            {
                "id": bet.id,
                "event": bet.event,
                "amount": bet.amount,
                "odds": bet.odds,
                "result": bet.result,
                "date": bet.date.isoformat(),
                "bet_type": bet.bet_type,
                "sport": bet.sport,
                "payout": bet.payout
            } for bet in paginated.items
        ],
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total_bets": paginated.total,
        "total_pages": paginated.pages
    })

@bet_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_bet(id):
    user_id = int(get_jwt_identity())
    bet = Bet.query.filter_by(id=id, user_id=user_id).first()

    if not bet:
        return jsonify({"error": "Bet not found"}), 404
    
    return jsonify({
        "id": bet.id,
        "event": bet.event,
        "amount": bet.amount,
        "odds": bet.odds,
        "result": bet.result,
        "date": bet.date.isoformat(),
        "bet_type": bet.bet_type,
        "sport": bet.sport,
        "payout": bet.payout
    })

@bet_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_bet(id):
    user_id = int(get_jwt_identity())
    bet = Bet.query.filter_by(id=id, user_id=user_id).first()

    if not bet:
        return jsonify({"error": "Bet not found"}), 404
    
    data = request.get_json()

    amount = data.get('amount')
    odds = data.get('odds')

    if amount is not None and amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    if odds is not None and odds <= 0:
        return jsonify({"error": "Odds must be positive"}), 400

    bet.event = data.get('event', bet.event)
    bet.amount = amount if amount is not None else bet.amount
    bet.odds = odds if odds is not None else bet.odds
    bet.result = data.get('result', bet.result)

    date_str = data.get('date')
    if date_str:
        try:
            bet.date = datetime.fromisoformat(date_str)
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400
        
    bet.bet_type = data.get('bet_type', bet.bet_type)
    bet.sport = data.get('sport', bet.sport)

    db.session.commit()

    return jsonify({"message": "Bet updated succesfully"})

@bet_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bet(id):
    user_id = int(get_jwt_identity())
    bet = Bet.query.filter_by(id=id, user_id=user_id).first()

    if not bet:
        return jsonify({"error": "Bet not found"}), 404
    
    db.session.delete(bet)
    db.session.commit()

    return jsonify({"message": "Bet deleted successfully"})
