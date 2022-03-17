import re, os
from http.server import BaseHTTPRequestHandler
from routes import routes, statics
import sqlite3
from jinja2 import Environment, FileSystemLoader


class Processors:

    def get_main(self):
        conn = sqlite3.connect('sqlite3.db')
        caps = conn.execute(
            "SELECT STATUS_ID, STATUS_NAME, DESCRIPTION from STATUSES ORDER BY STATUS_ID ASC").fetchall()
        data = []
        for status in caps:
            data.append(conn.execute(
                "select id, task, status, description from tasks where status=" + str(status[0]) + " order by id desc;").fetchall())
        file_loader = FileSystemLoader('pages')
        env = Environment(loader=file_loader)
        template = env.get_template('main.html')
        response_content = template.render(caps=caps, data=data)
        conn.close()
        return response_content, "text/html"

    def get_404(self):
        return open("pages/{}".format('404.html')).read(), 'text/html'

    def get_images(self, path):
        root = os.path.dirname(os.path.abspath(__file__))
        filename = root + path
        print("fname", filename)
        if filename[-4:] == '.png':
            content_type = 'image/png'
        else:
            return Processors.get_404(), True

        with open(filename, 'rb') as fh:
            out = fh.read()
        return out, content_type, False

    def parse_form(self, data):
        output = {}
        for pairs in data.split('&'):
            parts = pairs.split('=')
            output[parts[0]] = parts[1]
        return output

    def post_task(self, data):
        fields = Processors.parse_form(self, data)
        conn = sqlite3.connect('sqlite3.db')
        conn.cursor().execute(
            "INSERT INTO TASKS (task, status, description) values ('" + fields['ticketid'] + "', 1, '" + fields[
                'description'] + "');")
        conn.commit()
        print(fields)
        conn.close()
        return "okay"

    def post_move(self, data):
        fields = Processors.parse_form(self, data)
        conn = sqlite3.connect('sqlite3.db')
        max_stat = conn.execute("select max(STATUS_ID) from statuses;").fetchone()
        new_pos = 1
        if fields['move'] == 'R':
            new_pos = int(fields['position'])+1
        if fields['move'] == 'L':
            new_pos = int(fields['position'])-1
        if new_pos < 1:
            new_pos = 1
        if new_pos > int(max_stat[0]):
            new_pos = int(max_stat[0])
        conn.cursor().execute("update tasks set status="+str(new_pos)+" where id="+fields['taskid']+";")
        print(fields, max_stat[0], new_pos)
        conn.commit()
        conn.close()


class Server(BaseHTTPRequestHandler):

    def do_HEAD(self):
        return

    def do_POST(self):
        try:
            target = getattr(Processors, routes[self.path]['target'])
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            responce = target(Processors, post_data)
        except KeyError:
            target = getattr(Processors, 'get_404')

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        status = 200
        response_content = content_type = ""
        encoding = ''
        try:
            target = getattr(Processors, routes[self.path]['target'])
            response_content, content_type = target(Processors)
            encoding = 'UTF-8'
        except KeyError:
            target = getattr(Processors, 'get_404')
            for static in statics:
                if re.match(static, self.path) is not None:
                    print(statics[static]['target'])
                    target = getattr(Processors, statics[static]['target'])
                    response_content, content_type, is_err = target(Processors, self.path)
                    encoding = ''
                    pass

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        if encoding == '':
            self.wfile.write(bytes(response_content))
        else:
            self.wfile.write(bytes(response_content, encoding))
