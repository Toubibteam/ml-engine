import os
import sys
import logging
import json
import falcon
from falcon_cors import CORS

from serve import get_code, get_similarcode

model_code_api = get_code() # load the model
model_similarcode_api = get_similarcode()

public_cors = CORS(
                allow_all_origins=True,
                allow_all_headers=True,
                allow_all_methods=True)

api = falcon.API(middleware=[public_cors.middleware])

class ModelRoute:

    def on_post(self, req, resp):
        """API function
        All model-specific logic to be defined in the get_model_api() function
        """
        if req.content_length:
            input_data = json.loads(req.stream.read().decode('utf-8'))
        else:
            print 'missing parameters'
            return

        diagnostic = input_data["diagnostic"]
        print "diagnostic: " + diagnostic.encode('utf-8')
        resp.media = model_code_api(diagnostic)

api.add_route('/api', ModelRoute())
