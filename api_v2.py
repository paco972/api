import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

mydb = mysql.connector.connect(
    #host = "127.0.0.1",
    #user = "root",
    #password = "",
    host = "192.168.1.xxx",
    user = "extern_user",
    password = "bt5@c13l972",
    database = "ciel_2025"
    )

cursor = mydb.cursor()

@app.route('/v2/etudiants/', methods=['GET'])
def getEtudiants():
    etudiants = []
    req = "SELECT * FROM etudiant"
    cursor.execute(req)
    result = cursor.fetchall()
    for row in result:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
            }
        etudiants.append(etudiant)
    return jsonify(etudiants), 200

@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print (req)
    try :
        cursor.execute(req)
        row = cursor.fetchone()
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    except TypeError :
        return jsonify({'erreur':'id invalide'}), 404


@app.route('/v2/etudiants/', methods=['POST'])
def addEtudiant():
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"INSERT INTO etudiant (nom, prenom, email, telephone) \
        VALUES ('{nom}','{prenom}','{email}','{telephone}')"
    cursor.execute(req)
    mydb.commit()
    #return req
    return jsonify({'message':'Ajout OK'}), 201

@app.route('/v2/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    nom = request.json['nom']
    prenom = request.json['prenom']
    email = request.json['email']
    telephone = request.json['telephone']
    req = f"UPDATE etudiant \
        SET nom='{nom}', prenom='{prenom}', email='{email}', telephone='{telephone}' \
        WHERE idEtudiant={id}"
    cursor.execute(req)
    mydb.commit()
    #return req
    return jsonify({'message':'Modification OK'}), 200

@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    req = f"DELETE FROM etudiant WHERE idEtudiant={id}"
    cursor.execute(req)
    mydb.commit()
    #return req
    return jsonify({'message':'Suppression OK'}), 200

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
 