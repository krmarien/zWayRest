from zwayrest import app
import os

import zwayrest.restapi.account
import zwayrest.restapi.zwave

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join(path).replace('\\','/'))
