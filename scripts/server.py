import flask
from flask import request, jsonify
from get_frames_from_video import get_frames_from_video
from find_side import find_side
from paint_segmentation import paint_segmentation
from person_team_detection import person_detection_team_classification
from homography import homography
from multiprocessing import Process

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Working..."


@app.route('/api/frames', methods=['GET'])
def api_frames():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if 'time' in request.args:
        time = float(request.args['time'])
        error += 1
    if error != 2:
        return "Error: Not all arguments provided."

    get_frames_from_video(name, time)

    return jsonify('OK')


@app.route('/api/side', methods=['GET'])
def api_side():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if error != 1:
        return "Error: Not all arguments provided."

    return jsonify(find_side(name))


@app.route('/api/paint', methods=['GET'])
def api_paint():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if 'side' in request.args:
        side = request.args['side']
        error += 1
    if error != 2:
        return "Error: Not all arguments provided."

    paint_segmentation(name, side)

    return jsonify('OK')


@app.route('/api/person-teams-detection', methods=['GET'])
def api_persons_team():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if 'attColor' in request.args:
        attColor = request.args['attColor']
        error += 1
    if 'defColor' in request.args:
        defColor = request.args['defColor']
        error += 1
    if error != 3:
        return "Error: Not all arguments provided."

    person_detection_team_classification(name, attColor, defColor)

    return jsonify('OK')


@app.route('/api/homography', methods=['GET'])
def api_homography():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if 'side' in request.args:
        side = request.args['side']
        error += 1
    if error != 2:
        return "Error: Not all arguments provided."

    return jsonify(homography(name, side))


@app.route('/api/analysis', methods=['GET'])
def api_analysis():
    error = 0
    if 'name' in request.args:
        name = request.args['name']
        error += 1
    if 'time' in request.args:
        time = float(request.args['time'])
        error += 1
    if 'attColor' in request.args:
        attColor = request.args['attColor']
        error += 1
    if 'defColor' in request.args:
        defColor = request.args['defColor']
        error += 1
    if error != 4:
        return "Error: Not all arguments provided."

    get_frames_from_video(name, time)
    side = find_side(name)
    attColor = attColor.lower()
    defColor = defColor.lower()

    print(attColor, defColor)

    p1 = Process(target=paint_segmentation, args=(name, side))
    p1.start()
    p2 = Process(target=person_detection_team_classification, args=(name, attColor, defColor))
    p2.start()
    p1.join()
    p2.join()
    return jsonify(homography(name, side))

if __name__ == '__main__':
    app.run()
