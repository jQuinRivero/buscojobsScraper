if __name__ == "__main__":
    print("Archivo no ejecutable")
else:
    import json

    def formatURL(position, location, pageNum):
        """Generar URL para diferentes lugares"""
        template = "https://www.buscojobs.com.uy/search/rd451/{}_{}/{}"
        url = template.format(position, location, pageNum)
        return url

    def iterateLists(originArray):
        dumparray = []
        for item in originArray:
            item_ = item.contents[0]
            dumparray.append(item_)
        return dumparray

    def jsonifyData(data):
        json_list = []
        for dato in data:
            json_list.append(json.dumps(dato, ensure_ascii=False))
        return json_list

    def csvData(data):
        keys = data[0].keys()
        return keys