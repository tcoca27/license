import json

def test_frames_success(app, client):
    res = client.get('/api/frames?name=test&time=1')
    assert 'OK' == json.loads(res.get_data(as_text=True))

def test_frames_missing_arguments(app, client):
    res = client.get('/api/frames?name=tes')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/frames?time=1')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/frames')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)

def test_side_success(app, client):
    res = client.get('/api/side?name=test')
    assert res.get_data(as_text=True).find('right') > -1

def test_side_missing_arguments(app, client):
    res = client.get('/api/side')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)

def test_side_video_not_found(app, client):
    res = client.get('/api/side?name=notFound')
    assert res.get_data(as_text=True).find('right') == -1 and res.get_data(as_text=True).find('left') == -1

def test_paint_success(app, client):
    res = client.get('/api/paint?name=test&side=right')
    assert res.get_data(as_text=True).find('test') > -1 and res.get_data(as_text=True).find('paint') > -1

def test_paint_missing_arguments(app, client):
    res = client.get('/api/paint')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/paint?name=test')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/paint?side=left')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)

def test_paint_video_not_found(app, client):
    res = client.get('/api/paint?name=notFound')
    assert res.get_data(as_text=True).find('right') == -1 and res.get_data(as_text=True).find('left') == -1

def test_team_detection_success(app, client):
    res = client.get('/api/person-teams-detection?name=test&attColor=dark_blue&defColor=red')
    assert res.get_data(as_text=True).find('test') > -1 and res.get_data(as_text=True).find('teams') > -1

def test_team_missing_arguments(app, client):
    res = client.get('/api/person-teams-detection')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/person-teams-detection?name=test')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/person-teams-detection?attColor=blue')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/person-teams-detection?attColor=blue&defColor=red')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)

def test_team_video_not_found(app, client):
    res = client.get('/api/person-teams-detection?name=notFound')
    assert res.get_data(as_text=True).find('right') == -1 and res.get_data(as_text=True).find('left') == -1

def test_analysis_missing_arguments(app, client):
    res = client.get('/api/analysis')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/analysis?name=test')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/analysis?attColor=blue')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)
    res = client.get('/api/analysis?attColor=blue&defColor=red')
    assert 'Error: Not all arguments provided.' == res.get_data(as_text=True)