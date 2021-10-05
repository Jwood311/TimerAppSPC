from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Models import Time
from json import JSONEncoder
import pymysql

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default

JSONEncoder.default = _default

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/TimerApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
engine = create_engine('mysql+pymysql://root:root@localhost:8889/TimerApp', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)



@app.route('/getTimes')
def getTimes():

    try:
        session = Session()
        times = session.query(Time).all()
        return jsonify(times)
    # db.session.query(text('1')).from_statement(text('SELECT 1')).all()
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text



@app.route('/clearTimes')
def clearTimes():

    try:
        session = Session()
        db.session.query(Time).delete()
        db.session.commit()
        return jsonify('Times Cleared')
    # db.session.query(text('1')).from_statement(text('SELECT 1')).all()
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text



@app.route('/AddTime', methods=['POST'])
def addTimePost():
    input_json = request.get_json(force=True)
    dictToReturn = {'time':input_json["time"]}
    session = Session()
    app.logger.info('try')

    try:
        newTime = Time()
        newTime.time = dictToReturn["time"]
        session.add(newTime)
        session.commit()
    except Exception as e:
        app.logger.info('try')

        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    finally:
        session.flush()
        session.close()
        return jsonify(dictToReturn)

if __name__ == '__main__':
    app.run(debug=True)