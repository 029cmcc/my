import json
import urllib.request


CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"



def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(file,data):

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def download(url):

    print("================")
    print("下载接口:")
    print(url)


    req = urllib.request.Request(

        url,

        headers={
            "User-Agent":
            "Mozilla/5.0"
        }

    )


    with urllib.request.urlopen(
        req,
        timeout=30
    ) as r:


        return json.loads(
            r.read()
            .decode("utf-8")
        )




def main():


    cfg = load_json(
        CONFIG_FILE
    )


    data = download(
        cfg["source"]
    )


    if "sites" not in data:

        raise Exception(
            "接口异常，没有sites字段"
        )


    sites = data["sites"]


    print(
        "原始站点:",
        len(sites)
    )


    keep_keys = cfg["keep_keys"]


    result = []



    for site in sites:


        key = site.get(
            "key",
            ""
        )


        name = site.get(
            "name",
            ""
        )


        text = key + name



        # ========
        # 优先保留
        # ========

        if key in keep_keys:

            result.append(site)

            continue



        # ========
        # 删除关键词
        # ========


        remove = False


        for word in cfg["remove_keywords"]:


            if word in text:

                remove = True

                break



        if remove:

            continue



    # ==========
    # 改名
    # ==========


    rename = cfg["rename"]


    for site in result:


        key = site.get(
            "key"
        )


        if key in rename:


            site["name"] = rename[key]




    # ==========
    # 排序
    # ==========


    order = cfg["order"]


    new_sites = []



    for key in order:


        for site in result:


            if site.get("key") == key:

                new_sites.append(site)

                break



    data["sites"] = new_sites



    print("================")

    print(
        "过滤后站点:",
        len(new_sites)
    )

    print("================")



    for s in new_sites:


        print(

            s.get("key"),

            "|",

            s.get("name")

        )



    print("================")



    save_json(

        OUTPUT_FILE,

        data

    )



    print(
        "生成完成:",
        OUTPUT_FILE
    )




if __name__ == "__main__":

    main()
