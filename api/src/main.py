from videoSearcher import VideoSearcher
from flask import Flask, request, jsonify

videoSearcher = VideoSearcher()

# Flask app
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')

    result_df = videoSearcher.search(query)
    videoSearcher.writeResult.write_to_csv(result_df)
    result_json = result_df.to_dict(orient='records')

    return jsonify(result_json)
