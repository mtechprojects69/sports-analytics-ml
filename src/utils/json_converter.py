import json


def json_to_ndjson(json_content: str) -> str:
    data = json.loads(json_content)

    return "\n".join(
        json.dumps(item, ensure_ascii=False)
        for item in data
    )