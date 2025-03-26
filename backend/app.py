from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)

db.create_all()

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        data = request.json
        new_item = MenuItem(name=data['name'], img=data['img'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "菜品添加成功"}), 201
    
    items = MenuItem.query.all()
    return jsonify([{ "id": i.id, "name": i.name, "img": i.img } for i in items])

@app.route('/checkout', methods=['POST'])
def checkout():
    email = request.json.get('email')
    orders = request.json.get('order', [])

    content = "您的订单：\n" + "\n".join([str(o) for o in orders])
    send_email(email, "您的订单", content)

    return jsonify({"message": "订单已发送"})

def send_email(to_email, subject, content):
    sender_email = "your-email@qq.com"
    sender_password = "your-email-password"

    msg = MIMEText(content)
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
