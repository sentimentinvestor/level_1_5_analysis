#main.py
import time
from firebase_admin import firestore
from analysis_tools import calculate_average
from firebase_db import db
from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({
    "service": "level-1-5-analysis",
  })


@app.route('/level_1_5_analysis')
def raw_data():
  start_time = time.time()

  tickers = db().collection("tickers").get()
  tickers = [t.to_dict() for t in tickers]

  targets = db().collection("targets").document("level_1_5_analysis").get()
  target_metrics = targets.to_dict()["metrics"]

  updated_fields = {}

  for metric in target_metrics:
    average = calculate_average(tickers, metric)
    updated_fields["average_" + metric] = average
    db().collection("aggregate_analysis").document("level_1_5_analysis").collection("history").document(metric).set({
      "history": firestore.ArrayUnion([{
        "timestamp": time.time(),
        "data": average
      }])
    })

  db().collection("aggregate_analysis").document("level_1_5_analysis").set(updated_fields, merge=True)

  return jsonify({
    "time_taken": time.time() - start_time,
    "results": updated_fields
  })


if __name__ == '__main__':
  app.run()