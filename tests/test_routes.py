"""
route tests
"""
import json

def test_ping(client):
    """
    Test the ping route
    """
    res = client.get('/api/ping')
    assert res.status == '200 OK'

    expected = {'success': True}
    assert expected == json.loads(res.get_data(as_text=True))

def test_good_tag(client):
    """
    Test for tags that exist
    """
    res = client.get('/api/posts?tags=health,tech')
    assert res.status == '200 OK'

def test_bad_tag(client):
    """
    Test for invalid tag values
    """
    bad_tag = client.get('/api/posts?tags=test')
    assert json.loads(bad_tag.data) == {'posts': []}

    no_tag = client.get('/api/posts')
    assert no_tag.status == '400 BAD REQUEST'

def test_desc_order(client):
    """
    Test for ids being in desc order
    """
    res = client.get('/api/posts?tags=science,health&direction=desc')
    posts = json.loads(res.data)['posts']

    for i in range(len(posts) - 1):
        assert posts[i]['id'] >= posts[i+1]['id']

def test_asc_order(client):
    """
    Test for popularity being in asc order
    """
    res = client.get('/api/posts?tags=science,health&sortBy=popularity')
    posts = json.loads(res.data)['posts']

    for i in range(len(posts) - 1):
        assert posts[i]['popularity'] <= posts[i+1]['popularity']

def test_sort_by(client):
    """
    Test for correct sortBy order
    """
    res = client.get('/api/posts?tags=tech&sortBy=likes')
    posts = json.loads(res.data)['posts']
    for i in range(len(posts) - 1):
        assert posts[i]['likes'] <= posts[i+1]['likes']

def test_no_duplicates(client):
    """
    Test for duplicates
    """
    res = client.get('/api/posts?tags=science,tech')
    posts = json.loads(res.data)['posts']

    for post in posts:
        assert posts.count(post) == 1
