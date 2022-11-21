from redis import Redis
from flask import current_app as app


authorization_header = {
    "Authorization": {
        "description":
        "Authorization HTTP header with JWT access token, like: Authorization: Bearer asdf.qwer.zxcv",
        "in":
        "header",
        "type":
        "string",
        "required":
        True
    }
}

FACEYELP_API_CACHE = Redis.from_url(app.config["FACEYELP_API_REDIS_CACHE"], decode_responses=True)
