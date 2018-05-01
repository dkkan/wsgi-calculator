"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!
"""


def home():
    """
    Main page for the wsgi-calculator
    :return:
    """

    page = """<h1>wsgi-calculator</h1>
              <h2>Help</h2>
              <p>
                  Your users should be able to send appropriate requests and get back proper responses. For example, if I open a
                  browser to your wsgi application at
                  <a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a> then the response body in my
                  browser should be 15.
              </p>
              <p><b>Consider the following URL/Response body pairs as tests:</b></p>
              <ul>
                  <li>http://localhost:8080/multiply/3/5   => 15</li>
                  <li>http://localhost:8080/add/23/42      => 65</li>
                  <li>http://localhost:8080/subtract/23/42 => -19</li>
                  <li>http://localhost:8080/divide/22/11   => 2</li>
                  <li>http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"</li>
                  <li>http://localhost:8080/               => <html>Here's how to use this page...</html></li>
              </ul>"""
    if not page or page is None:
        raise NameError("No content in page.")
    return page


def addition(*args):
    """
    Performs addition operation
    :param args: tuple object ('23', 42')
    :return: str type '65' due to headers.append(('Content-length', str(len(body)))
    """

    sum = 0
    for a in args:
        sum += int(a)
    return str(sum)


def subtraction(*args):
    """
    Performs subtraction operation
    :param args: tuple type ('23', 42')
    :return: str type '-19' due to headers.append(('Content-length', str(len(body)))
    """

    result = int(args[0])
    for a in args[1:]:
        result -= int(a)
    return str(result)


def multiplication(*args):
    """
    Performs multiplication operation
    :param args: tuple type ('3', 5')
    :return: str type '15' due to headers.append(('Content-length', str(len(body)))
    """

    result = int(args[0])
    for a in args[1:]:
        result *= int(a)
    return str(result)


def division(*args):
    """
    Performs division operation
    :param args: tuple type ('22', 11')
    :return: str type '2' due to headers.append(('Content-length', str(len(body)))
    """

    result = int(args[0])
    for a in args[1:]:
        result /= int(a)
    return str(int(result))


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    args = path.split('/')[1:]
    functions = args.pop(0)
    params = {'': home,
              'add': addition,
              'subtract': subtraction,
              'multiply': multiplication,
              'divide': division,}.get(functions)
    return params, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.

    headers = [('Content-type', 'text/html')]
    body = ''
    status = ''
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        params, args = resolve_path(path)
        body = params(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':

    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
