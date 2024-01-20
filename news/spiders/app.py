from flask import Flask, request, jsonify
from google.cloud import bigquery

app = Flask(__name__)

client = bigquery.Client()


@app.route('/api/search', methods=['GET'])
def search_data():
    
    keyword = request.args.get('keyword', '')

  
    query = f"""
        SELECT *
        FROM `codingchallenge-411613.theguardian.news_table`
        WHERE LOWER(Text) LIKE '%{keyword}%'
        ORDER BY Published_On DESC
    """

    query_job = client.query(query)

    results = query_job.result()
    
    data = [
        {key: str(value) for key, value in row.items()}
        for row in results
    ]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)