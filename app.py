"""
Backend API Assessment
"""
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request
from flask_caching import Cache
import requests

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

URL = 'https://api.hatchways.io/assessment/blog/posts'

@app.route("/api/ping", methods=['GET'])
def ping_api():
    """
    API ping test
    """
    return jsonify(success = True), 200

@app.route("/api/posts", methods=['GET'])
@cache.cached(timeout=60, query_string=True, key_prefix='posts')
def get_posts():
    """
    Get blog posts using give url params from hatchways api
    """
    # Separate all the args to be used
    tags = request.args.get("tags", type=str)
    sort_by = request.args.get("sortBy", default="id", type=str)
    direction = request.args.get("direction", default="asc", type=str)

    # Handle no tag parameter or empty tag
    if tags is None or tags == "":
        return jsonify({'error': "Tags parameter is required"}), 400

    # Handle invalid direction parameter
    if direction not in ['asc', 'desc']:
        return jsonify({'error': "direction parameter is invalid"}), 400

    # Handle invalid sortBy parameter
    if sort_by not in ['id', 'reads', 'likes', 'popularity']:
        return jsonify({'error': 'sortBy parameter is invalid'}), 400

    # Initialize data dict
    data = {'posts': []}

    # Make a request for each given tag and add the posts to the data dict
    # I'll be honest I don't know if this is running concurrently
    with ThreadPoolExecutor(max_workers=len(tags.split())) as pool:
        for tag in tags.split(','):
            posts = requests.get(f'{URL}?tag={tag}').json()['posts']
            data['posts'] += posts

    # remove duplicates from the posts
    final_data = []
    for post in data['posts']:
        if post not in final_data:
            final_data.append(post)

    data['posts'] = final_data

    # Sort based on sortBy and direction
    if direction == 'desc':
        data['posts'].sort(key=lambda x: x[sort_by], reverse=True)
    else:
        data['posts'].sort(key=lambda x: x[sort_by])

    return data, 200


if __name__ == '__main__':
    app.run()
