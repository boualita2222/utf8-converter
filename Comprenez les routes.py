# Une route = une URL

@app.route("/")              # http://localhost:5000/
def accueil():
    return "Bonjour !"

@app.route("/encoder")      # http://localhost:5000/encoder
def encoder():
    return "Encodeur UTF-8"

@app.route("/api/encoder",  # http://localhost:5000/api/encoder
           methods=["POST"])
def api_encoder():
    data = request.get_json()
    texte = data["texte"]
    # encoder le texte...
    return jsonify({"hex": "C3 A9"})