from bottle import route, run, static_file


STATIC_DIR = "html_resourse"

def wrapup_templates(html_):
    temp = open(f"{STATIC_DIR}/{html_}.html").read()
    template = "<body>" \
              "<h1>Blog 🐒</h1>" \
              "<a href='/' style='float:right'>🏠</a>" \
              "<div style=\"margin:5px;" \
              "padding:5px;" \
              "background-color: white;" \
              "overflow: auto;" \
              f"text-align:justify;\">{temp}</div></body>"
    return template

@route('/')
def hello():
    return static_file(f"index.html", root=STATIC_DIR)

@route("/<loc>")
def render_template(loc):
    return wrapup_templates(loc)


run(host='localhost', port=8080, debug=True)