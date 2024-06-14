from flask import Flask, jsonify, render_template, request , render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TipeBarang(db.Model):
    __tablename__ = 'tipebarang'
    id = db.Column(db.Integer, primary_key=True)
    nama_tipe = db.Column(db.String, nullable=False)

    def json(self):
        return {'id': self.id, 'nama_tipe': self.nama_tipe}


class Barang(db.Model):
    __tablename__ = 'barang'
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.String, nullable=False)
    nama_barang = db.Column(db.String, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tipe_id = db.Column(db.Integer, db.ForeignKey('tipebarang.id'), nullable=False)

    tipe = db.relationship("TipeBarang")

    def json(self):
        return {
            'id': self.id,
            'id_barang': self.id_barang,
            'nama_barang': self.nama_barang,
            'jumlah': self.jumlah,
            'tipe': self.tipe.json()
        }

#home
@app.route('/', methods=['GET'])
def home():
    return render_template('/home/index.html')

#barang
@app.route('/barang', methods=['GET'])
def get_all_barang():
    barang_list = Barang.query.all()
    return render_template('/barang/index.html', barang_list=barang_list)


@app.route('/barangs/update/<int:id>', methods=['GET'])
def get_barang(id):
    barang = Barang.query.get_or_404(id)
    return render_template('/barang/update.html', barang=barang)

@app.route('/barang/create', methods=['GET'])
def create_view_barang():
    return render_template('/barang/create.html')

@app.route('/barang/create', methods=['POST'])
def add_barang():
    data = request.form
    tipe = TipeBarang.query.get(data['tipe_id'])
    new_barang = Barang(
        id_barang=data['id_barang'],
        nama_barang=data['nama_barang'],
        jumlah=data['jumlah'],
        tipe_id=data['tipe_id']
    )
    db.session.add(new_barang)
    db.session.commit()
    return redirect(url_for('get_all_barang'))
    

@app.route('/barang/<int:id>', methods=['POST'])
def update_barang(id):
    data = request.form
    barang = Barang.query.get_or_404(id)
    barang.id_barang = data.get('id_barang', barang.id_barang)
    barang.nama_barang = data.get('nama_barang', barang.nama_barang)
    barang.jumlah = data.get('jumlah', barang.jumlah)
    barang.tipe_id = data.get('tipe_id', barang.tipe_id)
    db.session.commit()
    return redirect(url_for('get_all_barang'))

@app.route('/barang/delete/<int:id>')
def delete_barang(id):
    barang = Barang.query.get_or_404(id)
    db.session.delete(barang)
    db.session.commit()
    return redirect(url_for('get_all_barang'))

#tipe barang
@app.route('/tipebarang', methods=['GET'])
def get_all_tipe():
    tipe_list = TipeBarang.query.all()
    return render_template('/tipebarang/index.html', tipe_list=tipe_list)

@app.route('/tipe/update/<int:id>', methods=['GET'])
def get_tipe(id):
    tipe = TipeBarang.query.get_or_404(id)
    return render_template('/tipebarang/update.html', tipe=tipe)

@app.route('/tipe/create', methods=['GET'])
def create_view_tipe():
    return render_template('/tipebarang/create.html')

@app.route('/tipebarang/create', methods=['POST'])
def add_tipebarang():
    data = request.form
    new_tipebarang = TipeBarang(
        nama_tipe=data['nama_tipe']
    )
    db.session.add(new_tipebarang)
    db.session.commit()
    return redirect(url_for('get_all_tipe'))


@app.route('/tipebarang/update/<int:id>', methods=['POST'])
def update_tipebarang(id):
    data = request.form
    tipebarang = TipeBarang.query.get_or_404(id)
    tipebarang.nama_tipe = data.get('nama_tipe', tipebarang.nama_tipe)
    db.session.commit()
    return redirect(url_for('get_all_tipe'))

@app.route('/tipebarang/delete/<int:id>')
def delete_tipebarang(id):
    tipebarang = TipeBarang.query.get_or_404(id)
    db.session.delete(tipebarang)
    db.session.commit()
    return redirect(url_for('get_all_tipe'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
