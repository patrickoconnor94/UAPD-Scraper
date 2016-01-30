import requests
from bs4 import BeautifulSoup
import csv
from time import gmtime, strftime

for counts in range(, ):
    tableurl = "http://uapd.arizona.edu/daily-activity-crime-log/2014?page=" + str(counts)
    #example using 2014 data, change the range to equal the number of pages needing to be scraped with 0 being the first page 
    if counts == 0:
        url = "http://uapd.arizona.edu/daily-activity-crime-log/2014"
        print("I am just starting on the first page")
    else:
        print("I finished page " + str(counts) + " at " + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    tablepage = requests.get(tableurl, allow_redirects = False)
    tablec = tablepage.content
    # tablec now has all of the HTML from the table page, this from the requests module

    tablesoup = BeautifulSoup(tablec)
    # we now have a soup of the entire table through the beautifulsoup module,
    # this means we can access the html more easily and scrape better

    localcaselist = []
    # contains the case numbers that requests will grab info from

    for string in tablesoup.body.tbody.find_all('a'):
        lemon = repr(string)
        if len(lemon) == 57:
            localcaselist.append(lemon[45:53])
        elif len(lemon) == 63:
            localcaselist.append(lemon[48:59])
        elif len(lemon) == 61:
            localcaselist.append(lemon[47:57])
        else:
            print("Something dun goofed on this page")
            localcaselist.append(lemon)
    # generates a list of cases from the table page and adds the number to localcaselist, checks case length to catch exceptions

    for cases in range(0, len(localcaselist)):
        caseurl = "http://uapd.arizona.edu/daily-activity-crime-log/" + str(localcaselist[cases])
        casepage = requests.get(caseurl, allow_redirects = False)
        casec = casepage.content
        casesoup = BeautifulSoup(casec)
        # turns the page into a searchable soup, and prevents endless redirects

        NewLine = []
        # Each new row of the CSV will be writen here, when called again it is erased

        if counts == 0 and cases == 0:
            headers = ["Case Code", "Report Time and Date", "Offense Time and Date", "Crime Code", "Crime Code Definition", "Street Address", "Premise Code Definition", "Date Cleared", "Clearance Code Definition"]
            CSVfile = open('newfile.txt','w')
            headerwriter = csv.writer(CSVfile, dialect='excel')
            headerwriter.writerow(headers)
            CSVfile.close()
            #generates
        NewLine.append(str(localcaselist[cases]))
        # adds case from url to the case code list

        try:
            RDT = casesoup.body.find("div",
                                     class_="""field field-name-field-report-date-and-time field-type-datetime field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            RDT = RDT.strip("\n")
            RDT = RDT.strip(" ")
            NewLine.append(RDT)
        # gets RDT, strips out formatting, and stores it in list

        try:
            ODT = casesoup.body.find("div",
                                     class_="""field field-name-field-offense-date-and-time field-type-datetime field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            ODT = ODT.strip("\n")
            ODT = ODT.strip(" ")
            NewLine.append(ODT)
        # gets ODT, strips out formatting, and stores it in list

        try:
            CC = casesoup.body.find("div",
                                    class_="""field field-name-field-crime-code field-type-text field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            CC = CC.strip("\n")
            CC = CC.strip(" ")
            NewLine.append(CC)
        # gets CC, strips out formatting, and stores it in list
        
         try:
            CCD = casesoup.body.find("div",
                                    class_="""field field-name-field-crime-code-definition field-type-text field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            CCD = CCD.strip("\n")
            CCD = CCD.strip(" ")
            NewLine.append(CCD)
        # gets CCD, strips out formatting, and stores it in list
        
        try:
            SA = casesoup.body.find("div",
                                    class_="""field field-name-field-street-address field-type-text field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            SA = SA.strip("\n")
            SA = SA.strip(" ")
            NewLine.append(SA)
        # gets SA, strips out formatting, and stores it in list

        try:
            PCD = casesoup.body.find("div",
                                     class_="""field field-name-field-premise-code-definition field-type-text field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            PCD = PCD.strip("\n")
            PCD = PCD.strip(" ")
            NewLine.append(PCD)
        # gets PCD, strips out formatting, and stores it in list

        try:
            DC = casesoup.body.find("div",
                                    class_="""field field-name-field-date-cleared field-type-datetime field-label-above""").get_text()
        except AttributeError:
             NewLine.append("NA")
        else:
            DC = DC.strip("\n")
            DC = DC.strip(" ")
            NewLine.append(DC)
        # gets DC, strips out formatting, and stores it in list

        try:
            CCD = casesoup.body.find("div",
                                     class_="""field field-name-field-clearance-code-definition field-type-text field-label-above""").get_text()
        except AttributeError:
            NewLine.append("NA")
        else:
            CCD = CCD.strip("\n")
            CCD = CCD.strip(" ")
            NewLine.append(CCD)
            # gets CCD, strips out formatting, and stores it in list
        with open('newfile.txt','a') as CSVfile:
            rowwriter = csv.writer(CSVfile, dialect="excel")
            rowwriter.writerow(NewLine)
        #writes NewLine list to a row of the csv and then reloops for the next case in the list
print("2014 scraping done ")
