from Handler import *

if __name__ == '__main__':
    dataHandler = DataHandler()
    dataHandler.delete_all()

    spinLabHandler = SpinLabHandler()
    for company in spinLabHandler.companies:
        dataHandler.insert(company)

    basislagerHandler = BasislagerHandler()
    for company in basislagerHandler.companies:
        dataHandler.insert(company)

    dataHandler.close_connection()

    GelbeseitenHandler("Leipzig")


