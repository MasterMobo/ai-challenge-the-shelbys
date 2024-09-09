from videoSearcher import VideoSearcher
from flask import Flask, request, jsonify

videoSearcher = VideoSearcher()

# Flask app
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    output_file_name = request.args.get('out')

    if (query is None) or (output_file_name is None):
        return jsonify({"error": "Missing 'query' or 'out' parameter"}), 400
    
    result_df = videoSearcher.search(query)
    videoSearcher.writeResult.write_to_csv(result_df, output_file_name)
    result_json = result_df.to_dict(orient='records')

    return jsonify(result_json)
