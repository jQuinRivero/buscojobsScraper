if __name__ == "__main__":
    from requestData import extractData, saveData
    from auxFunctions import csvData
    llamados = extractData("programador", "montevideo")
    saveData(llamados, "csv")
