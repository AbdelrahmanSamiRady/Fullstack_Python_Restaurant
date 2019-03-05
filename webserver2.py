#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
from database_setup import Base,Restaurant,MenuItem
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///C:/Users/Boudi/PycharmProjects/fullstack/restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(bytes(output, 'utf-8'))
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # Objective 3 Step 1 - Create a Link to create a new menu item
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(bytes(output,'utf-8'))
                return



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s"%port)
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()


# from http.server import BaseHTTPRequestHandler,HTTPServer

# class webserverHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         try:
#             if self.path.endswith("/helllo"):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#
#                 output = ""
#                 output += "<html><body>Hello!</body></html>"
#                 #self.wfile.write(output)
#                 print(output)
#                 return"hello"
#
#         except:
#             self.send_error(404,"File Not Found%s"%self.path)
#
#
# def main():
#     try:
#         port = 8080
#         server = HTTPServer(('',port), webserverHandler)
#         print("Web server running on port %s"%port)
#         server.serve_forever()
#
#     except KeyboardInterrupt:
#         print("^C entered , stopping web server...")
#         server.socket.close()
#
#
#
#
# if __name__=='__main__':
#     main()