from flask import Flask, request, jsonify
from storage import Storage

app = Flask(__name__)
storage = Storage()

@app.route("/api/v1/calendar/add", methods=["POST"])
def add_event():
    data = request.form
    event_date = data.get("date")
    title = data.get("title")
    text = data.get("text")
    
    try:
        event = storage.add_event(event_date, title, text)
        return jsonify({"status": "ok", "event": event})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/v1/calendar/list", methods=["GET"])
def list_events():
    events = storage.list_events()
    return jsonify(events)

@app.route("/api/v1/calendar/read", methods=["GET"])
def read_event():
    event_date = request.args.get("date")
    
    try:
        event = storage.read_event(event_date)
        return jsonify(event)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404

@app.route("/api/v1/calendar/update", methods=["PUT"])
def update_event():
    data = request.form
    event_date = data.get("date")
    new_title = data.get("new_title")
    new_text = data.get("new_text")
    
    try:
        event = storage.update_event(event_date, new_title, new_text)
        return jsonify({"status": "ok", "updated_event": event})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/v1/calendar/delete", methods=["DELETE"])
def delete_event():
    event_date = request.args.get("date")
    
    try:
        storage.delete_event(event_date)
        return jsonify({"status": "ok", "message": f"Событие на дату {event_date} удалено"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404