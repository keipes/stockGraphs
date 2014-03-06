from bottle import route, run, request, template, get, static_file, redirect
import query


@route('/stock/<stock>')
def index(stock):
    return query.stock_last_month(stock)


@route('/')
def index():
    if not request.query.ticker:
        redirect('/?ticker=GOOG')
    return template('tpl/index.html')


@get('/pub/<filename>')
def pub_data(filename):
    return static_file(filename, root='pub')

run(host='localhost', port=9097, reloader=True)