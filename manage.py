from flask.ext.script import Manager

from locator.locator import app, db, Point, Geolimit

manager = Manager(app)


@manager.command
def create_db():
    db.create_all()


@manager.command
def fastcgi():
    from flup.server.fcgi import WSGIServer
    WSGIServer(app).run()


@manager.command
def geolocate():
    from geopy import geocoders
    from datetime import date
    today_geolimit = Geolimit.query.filter_by(date=date.today()).first()
    if today_geolimit and today_geolimit.quota >= 2500:
        raise Exception("Dail quota exceeded")
    if not today_geolimit:
        today_geolimit = Geolimit()
        db.session.add(today_geolimit)
        db.session.flush()
    gc = geocoders.GoogleV3()
    points = Point.query.filter(db.or_(Point.status == 'new', Point.status == 'changed', Point.status == None)).all()
    ungeocoded_points = db.session.query(db.func.count(Point.id)).filter(db.or_(Point.status == 'new', Point.status == 'changed', Point.status == None)).scalar()
    if ungeocoded_points > 2500 - today_geolimit.quota:
        number_of_queries = 2500 - today_geolimit.quota
    else:
        number_of_queries = ungeocoded_points
    for i in xrange(int(number_of_queries)):
        place, (lat, lng) = gc.geocode(u"{0} {1} {2}".format(points[i].street, points[i].city, points[i].province))
        points[i].status = 'ready'
        points[i].position = "POINT({0} {1})".format(lat, lng)
        db.session.add(points[i])
        today_geolimit.quota += 1
    db.session.add(today_geolimit)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
