from flask import Flask, jsonify, request, render_template
from engine import MongoUploader  # Your MongoUploader class

app = Flask(__name__)

DATABASE_NAME = "bankdata"
COLLECTION_NAME = "bankinfo"
CSV_FILE_PATH = "bankdata.csv"

engine = MongoUploader(DATABASE_NAME, COLLECTION_NAME)


@app.route('/')
def home():
    # Serve the HTML frontend page instead of plain text
    return render_template('index.html')


@app.route('/test-connection')
def test_connection():
    try:
        engine.conntest()
        return jsonify({"status": "success", "message": "Connected to MongoDB successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/read-db')
def read_db():
    docs = engine.read_db(limit=5)
    if docs:
        return jsonify(docs)
    else:
        return jsonify({"status": "error", "message": "No documents found"}), 404

@app.route('/read_csv')
def read_csv():
    docs = engine.read_csv(CSV_FILE_PATH)
    return jsonify(docs)


@app.route('/delete-all', methods=['DELETE'])
def delete_all():
    engine.delete_all_documents()
    return jsonify({"status": "success", "message": "All documents deleted."})


@app.route('/upload', methods=['POST'])
def upload():
    engine.read_csv_mongo(CSV_FILE_PATH)
    engine.upload_to_mongo()
    return jsonify({"status": "success", "message": "Data uploaded from CSV"})


if __name__ == "__main__":
    app.run(debug=True)
