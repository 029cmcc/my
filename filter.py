import json
import urllib.request


CONFIG_FILE = "config.json"


def load_config():

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def get_json(url):

    print("正在获取源接口...")

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    req = urllib.request.Request(
        url,
        headers=headers
    )

    with urllib.request.urlopen(
        req,
        timeout=30
    ) as response:

        data = response.read()

    return json.loads(
        data.decode("utf-8")
    )



def filter_sites(data, config):

    sites = data.get(
        "sites",
        []
    )

    rename = config["rename"]

    order = config["order"]


    site_map = {}


    # 白名单过滤

    for site in sites:

        key = site.get(
            "key"
        )

        if key in rename:

            site["name"] = rename[key]

            site_map[key] = site



    new_sites = []


    # 按指定顺序输出

    for key in order:

        if key in site_map:

            new_sites.append(
                site_map[key]
            )


    data["sites"] = new_sites


    return data



def save_json(data, filename):

    with open(
        filename,
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

    config = load_config()


    source = config["source"]

    output = config["output"]


    data = get_json(
        source
    )


    if "sites" not in data:

        raise Exception(
            "错误：接口不存在 sites"
        )


    old_count = len(
        data["sites"]
    )


    data = filter_sites(
        data,
        config
    )


    new_count = len(
        data["sites"]
    )


    save_json(
        data,
        output
    )


    print(
        "过滤完成"
    )

    print(
        f"原站点: {old_count}"
    )

    print(
        f"保留站点: {new_count}"
    )



if __name__ == "__main__":

    main()
