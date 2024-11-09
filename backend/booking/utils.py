import logging

logger = logging.getLogger(__name__)


def gen_uuid_alphanum(lenght=16):
    import random
    import string
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))
    return x

def gen_uuid():
    import uuid
    return str(uuid.uuid4())
