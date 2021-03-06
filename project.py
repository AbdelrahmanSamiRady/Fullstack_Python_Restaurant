from flask import Flask, render_template, request, redirect,url_for
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///C:/Users/Boudi/PycharmProjects/fullstack/restaurantmenu.db')
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()

@app.route('/')
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    # output = ''
    # for i in items:
    #     output += i.name
    #     output += '</br>'
    #     output += i.price
    #     output += '</br>'
    #     output += i.description
    #     output += '</br>'
    #     output += '</br>'
    return render_template('menu.html', restaurant=restaurant, items = items)
# Task 1: Create route for newMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
        editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
                if request.form['name']:
                    editedItem.name = request.form['name']
                session.add(editedItem)
                session.commit()
                return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

        else:
            return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,i=editedItem)


# Task 3: Create a route for deleteMenuItem function here


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)