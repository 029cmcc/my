import json
import urllib.request
import os


CONFIG = "config.json"


def load_config():

    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)



def get_source(url):

    print("获取源接口:")

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(req, timeout=30) as r:

        data = r.read()

    return json.loads(data.decode("utf-8"))



def filter_sites(data, cfg):

    sites = data.get("sites", [])

    keep = []

    rename = cfg["rename"]

    order = cfg["order"]


    # 按key保留

    site_map = {}

    for site in sites:

        key = site.get("key")

        if key in rename:

            site["name"] = rename[key]

            site_map[key] = site



    # 按排序输出

    for key in order:

        if key in site_map:

            keep.append(site_map[key])


    data["sites"] = keep


    return data



def save_json(data, path):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def main():

    cfg = load_config()


    source = cfg["source"]

    output = cfg["output"]


    data = get_source(source)


    if "sites" not in data:

        raise Exception(
            "接口没有sites字段"
        )


    old = len(data["sites"])


    data = filter_sites(
        data,
        cfg
    )


    new = len(data["sites"])


    save_json(
        data,
        output
    )


    print(
        f"完成: {old} -> {new}"
    )



if __name__ == "__main__":

    main()
