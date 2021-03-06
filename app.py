from flask import Flask,request,jsonify,redirect,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noteerrr.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
ma=Marshmallow(app)

from models import DataModel,data_schema,data_all_schema


@app.route('/',methods=['POST'])
def add_data():
    name=request.form['name']
    content=request.form['content']
    new_data=DataModel(name,content)
    db.session.add(new_data)
    db.session.commit()
    return redirect('/')

@app.route('/',methods=['GET'])
def get_data():
        all_data=DataModel.query.all()
        result=data_all_schema.dump(all_data)
        return render_template('base.html',datasets=all_data)

@app.route('/datapi/<id>',methods=['PUT'])       #API
def update_data(id):
    data=DataModel.query.get(id)
    name=request.json['name']
    content=request.json['content']
    data.name=name
    data.content=content
    db.session.commit()
    return data_schema.jsonify(data)

@app.route('/delete/<int:id>')
def delete_data(id):
    data=DataModel.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)