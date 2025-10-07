import functools, http.server, os, pathlib, socket, tempfile, threading, shutil, logging

def run(temp_dir):
    # replace logger
    http.server.SimpleHTTPRequestHandler.log_message = lambda self, format, *args: logging.info(
        "%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args
        )
    )

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=temp_dir)
    httpd = http.server.HTTPServer(("127.0.0.3", 0), handler)

    host, port = httpd.server_address

    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    return f"http://{host}:{port}/index.html"

def copy_path(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def start(include):
    temp_dir = pathlib.Path(tempfile.mkdtemp())
    for path in include:
        copy_path(path, temp_dir)
    
    addr = run(temp_dir)

    return temp_dir, addr