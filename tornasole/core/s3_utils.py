from tornasole.core.access_layer.s3handler import S3Handler, ListRequest
from tornasole.core.utils import get_logger


logger = get_logger()


# list_info will be a list of ListRequest objects. Returns list of lists of files for each request
def _list_s3_prefixes(list_info):
    files = S3Handler().list_prefixes(list_info)
    if len(files) == 1:
        files = files[0]
    return files


def list_s3_objects(bucket, prefix, start_after_key=None):
    last_token = None
    if start_after_key is None:
        start_after_key = prefix
    logger.debug(f'Trying to load index files after {start_after_key}')
    list_params = {'Bucket': bucket, 'Prefix': prefix, 'StartAfter': start_after_key}
    req = ListRequest(**list_params)
    objects = _list_s3_prefixes([req])
    if len(objects) > 0:
        last_token = objects[-1]
    return objects, last_token