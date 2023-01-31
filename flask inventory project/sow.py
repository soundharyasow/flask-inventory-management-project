import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'sow.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class products(db.Model):
       id=db.Column('product_id',db.Integer,primary_key=True)
       product=db.Column(db.String(30),unique = True, nullable = False)
       qty=db.Column('unallocated_qty',db.Integer)
       def __init__(self,id,product,qty):
           self.id=id
           self.product=product
           self.qty=qty
       
       def __repr__(self,):
           with app.app_context():
             db.create_all()

class locations(db.Model):
       loc_id = db.Column(db.Integer, primary_key= True)
       loc_name = db.Column(db.String(20))
       def __init__(self,loc_id,loc_name):
          self.loc_id=loc_id
          self.loc_name=loc_name

       def __repr__(self,):
          with app.app_context():
           db.create_all()

class movements(db.Model):
    m_id = db.Column(db.Integer, primary_key= True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    frm = db.Column(db.String(20), nullable = False)
    to = db.Column(db.String(20), nullable = False)
    p_name = db.Column(db.String(20), nullable = False)
    p_qty = db.Column(db.Integer, nullable = False)
    def __init__(self,m_id,time,frm,to,p_name,p_qty):
         self.m_id=m_id
         self.time=time
         self.frm=frm
         self.to=to
         self.p_name=p_name
         self.p_qty=p_qty

    def __repr__(self):
         with app.app_context():
          db.create_all()

@app.route('/')
def index():
       return render_template('index.html')

@app.route('/list') 
def list():
       return render_template("list.html",products=products.query.all())
        
@app.route('/prod',methods=['GET','POST']) 
def addproduct():
   if request.method=='POST':
      product=products(request.form['id'],request.form['product'],request.form['qty'])

      db.session.add(product)  
      db.session.commit() 
      return redirect(url_for('list'))
   return render_template('prod.html')

@app.route('/edit', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        product = products.query.get(request.form.get('id'))
        product.name = request.form['id']
        product.email = request.form['product']
        product.phone = request.form['qty']
        db.session.commit()
        return redirect(url_for('list'))
@app.route('/delete/<id>',methods = ['GET','POST'])
def delete(id):
    product= products.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("list"))

@app.route('/addlocation')
def addlocation():
       return render_template('addlocation.html',locations=locations.query.all())

@app.route('/location_details',methods=['GET','POST']) 
def loc():
   if request.method=='POST':
      location=locations(request.form['loc_id'],request.form['loc_name'])

      db.session.add(location)  
      db.session.commit() 
      return redirect(url_for('addlocation'))
   return render_template('location_details.html')
 
@app.route('/transfer')
def transfer():
       return render_template('transfer.html',movements=movements.query.all())

@app.route('/movement',methods=['GET','POST']) 
def move():
   if request.method=='POST':
      movement=movements(request.form['m_id'],request.form['time'],request.form['frm'],request.form['to'],request.form['p_name'],request.form['p_qty'])

      db.session.add(movement)  
      db.session.commit()
      return redirect(url_for('transfer'))
   return render_template('movement.html')    



if __name__=="__main__":
       app.run(debug=True)


























       