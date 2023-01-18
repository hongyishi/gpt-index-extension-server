import json
from pathlib import Path
from gpt_index import GPTSimpleVectorIndex, SimpleWebPageReader
import hashlib
import base64
from functools import lru_cache


def check_url_index(url, api_key, json_file):
    # Check if the url is in the index
    Path(json_file).touch(exist_ok=True)
    import os

    if os.stat(json_file).st_size == 0:
        return False

    with open(json_file) as f:
        data = json.load(f)
        if url in data:
            url_index_file = data[url] + ".json"
            try:
                import os

                os.environ["OPENAI_API_KEY"] = api_key
                GPTSimpleVectorIndex.load_from_disk(url_index_file)
                return True
            except Exception as e:
                return False
        else:
            return False


def get_or_create_url_index(url, json_file):
    # If the url is not indexed, add it to the json file as key, value pair
    # where key is url and value is hashed url which will be
    # the webpage index file.
    # Else, return the index of the url.

    Path(json_file).touch(exist_ok=True)

    with open(json_file) as f:
        try:
            data = json.load(f)
        except ValueError:
            data = {}

        if url in data:
            return data[url]
        else:
            data[url] = str(
                base64.urlsafe_b64encode(
                    hashlib.md5(url.encode(encoding="UTF-8", errors="strict")).digest()
                )
            )
            print(data[url])
            with open(json_file, "w") as f:
                json.dump(data, f)
            return data[url]


def index_url(url, url_index_file, api_key):

    try:
        print("Url index file: " + url_index_file)
        import os

        os.environ["OPENAI_API_KEY"] = api_key
        index = GPTSimpleVectorIndex.load_from_disk(url_index_file)
        print("Index file already exists")
        return True

    except Exception as e:
        print(e)

        Path(url_index_file).touch(exist_ok=True)
        if os.path.exists(url_index_file + ".lock"):
            return False

        try:
            Path(url_index_file + ".lock").touch(exist_ok=True)
            import os

            os.environ["OPENAI_API_KEY"] = api_key
            documents = SimpleWebPageReader(html_to_text=True).load_data([url])
            index = GPTSimpleVectorIndex(documents)
            index.save_to_disk(url_index_file)
            os.remove(url_index_file + ".lock")
            return True

        except Exception as e:
            print(e)
            raise e
            return False


@lru_cache
def query_url(url, query, api_key, index_file):

    import os

    os.environ["OPENAI_API_KEY"] = api_key

    url_index = get_or_create_url_index(url, index_file) + ".json"
    print(url_index)
    # try:
    index = GPTSimpleVectorIndex.load_from_disk(url_index)
    query_response = index.query(query)
    text_refs = [
        {"node_info": node.node_info, "source_text": node.source_text}
        for node in query_response.source_nodes
    ]
    return {"response_str": query_response.response, "text_refs": text_refs}
    # except Exception as e:
    #     return str(e)
