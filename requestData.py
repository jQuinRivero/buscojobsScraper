if __name__ == "__main__":
    print("Archivo no ejecutable")
else:
    import csv
    import json
    from datetime import datetime, timedelta
    import requests
    from bs4 import BeautifulSoup
    import re
    import auxFunctions as af




    def extractData(position, location):
        pag = 0
        job_posting_list= []
        job_postings = ['dummy']
        while(len(job_postings) > 0):
            pag = pag + 1
            url = af.formatURL(position,location,pag)

            ## extraer HTML
            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")

            # row result click destacada-listado  -- div que buscamos

            job_postings = soup.find_all("div", "row result click destacada-listado")


            for job_posting in job_postings:

                """
                    INFO DE PÁGINA PRINCIPAL
                """

                # obtener nombre del titulo solicitado
                job_title = job_posting.h3.a.contents
                """
                # obtener descripción de trabajo - SE ELIMINA PORQUE ES AL PEDO
                job_description_div = job_posting.find_all(lambda tag: tag.name == "div" and
                                           tag.get("class") == ["row"])
                job_description_span = job_description_div[0].find_all("span")
                job_description = job_description_span[0].contents
                """

                # obtener nombre de empresa que contrata
                title_div = job_posting.find_all("div", "row link-header")
                company_span = title_div[0].find_all("span")
                company_a = company_span[0].find_all("a")
                if(len(company_a) != 0):
                    company_name = company_a[0].span.contents
                else:
                    company_name = "U"

                # obtener fecha de publicación
                date_unformatted = job_posting.find_all("span", "pull-right")[0].contents[0]
                split_date = date_unformatted.split(" ")
                split_date = split_date[len(split_date)-2:]

                if(split_date[0] == "un"):
                    # qué lindo eh
                    split_date[0] = "1"

                split_date[0] = int(split_date[0])
                split_date[1] = split_date[1][0].upper()

                if(split_date[1] == "M"):
                    split_date[0] = split_date[0]*30

                formatted_days_count = split_date[0]
                postingDate = (datetime.today() - timedelta(days=formatted_days_count)).date()
                postingDate = str(postingDate)


                """
                    INFORMACIÓN DEL LINK INTERNO A CADA LLAMADO
                """
                #formateo de URL
                url_post = title_div[0].find_all("h3")[0].find_all("a")[0]["href"]
                url_post = "https:"+url_post

                #parseo de sublink
                post_response = requests.get(url_post)
                subSoup = BeautifulSoup(post_response.text, "html.parser")

                #obtener conocimientos del llamado
                requirements = subSoup.find_all("a", href=re.compile("conocimiento"))
                conocimientos = af.iterateLists(requirements)

                #obtener áreas del llamado
                areas = subSoup.find_all("a", href=re.compile("search"))
                knowledge_areas = af.iterateLists(areas)[:-1] # el -1 es para eliminar el "Ver más llamados similares"


                # crear diccionario con datos del llamado
                dict_job = {
                    "job_title": job_title[0],
                    "company": company_name[0],
                    "posting_date": postingDate,
                    "requirements": conocimientos,
                     "knowledge_areas": knowledge_areas
                    }
                job_posting_list.append(dict_job)

        return job_posting_list

    def saveData(dataExtraction, format="JSON"):
        fileName = "data/JobPostings-{}.{}"
        extractionDate = str(datetime.today()).replace(" ", "-").replace(":","")[:-7]
        formattedFileName = fileName.format(extractionDate, format)


        if(format.upper()=="JSON"):
            data = af.jsonifyData(dataExtraction)
            with open(formattedFileName, "w") as f:
                json.dump(data, f)
        elif(format.upper()=="CSV"):
            keys = af.csvData(dataExtraction)

            with open(formattedFileName, "w") as f:
                dict_writer = csv.DictWriter(f, keys)
                dict_writer.writeheader()
                dict_writer.writerows(dataExtraction)
        else:
            print("Formato incorrecto")

        print("Archivo guardado correctamente")

