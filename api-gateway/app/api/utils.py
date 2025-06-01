from uuid import UUID


def user_headers(user):
    return {"X-User-Id": user["user_id"]}


def convert_uuids_to_str(obj):
    if isinstance(obj, dict):
        return {k: convert_uuids_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_uuids_to_str(i) for i in obj]
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        return obj