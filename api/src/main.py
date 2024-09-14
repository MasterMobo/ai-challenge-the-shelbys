from videoSearcher import VideoSearcher
from flask import Flask, request, jsonify
from flask_cors import CORS

videoSearcher = VideoSearcher()

# Flask app
app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET'])
def search():

    # data = request.json
    # query = data.get('query')
    # output_file_name = data.get('out')

    query = request.args.get('query')
    output_file_name = request.args.get('out')

    if query is None: #out param is optional
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    result_df = videoSearcher.search(query)
    videoSearcher.writeResult.write_to_csv(result_df, output_file_name)
    result_json = result_df.to_dict(orient='records')

    return jsonify(result_json)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
