from flask import Flask, jsonify, abort, request, url_for


app = Flask(__name__)

siamese = {"breed": "Siamese", "style": "Feisty"}

persian = {"breed": "Persian", "style": "Ambivalent"}

catbreed_list = [siamese, persian]


@app.route("/api/catbreeds/<int:id>", methods=["GET"])
def catbreed(id):
    if id < 0 or id >= len(catbreed_list):
        abort(404)
    return jsonify(catbreed_list[id])


@app.route("/api/catbreeds", methods=["GET"])
def catbreeds():
    return jsonify({"catbreeds": catbreed_list})


@app.route("/api/catbreeds", methods=["POST"])
def new_catbreed():
    if not request.json:
        abort(400)
    new_breed = request.get_json()
    if "breed" not in new_breed or "style" not in new_breed:
        abort(400)
    new_breed["id"] = 999
    new_breed["location"] = url_for("catbreed", id=999)
    return jsonify(new_breed)
