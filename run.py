from functools import partial

import requests, datetime
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate, pyqtSignal, pyqtSlot
from bs4 import BeautifulSoup

# class Communicator():
#     signal = pyqtSignal(str, int)
#     def __init__(self):
#         super(Communicator, self).__init__()
#         self.do_something()
#
#     def do_something(self):
#        print("emit")
#############################################################################################################
class TimelineScraper(object):
    url = ""
    def __init__(self, url):
        self.url = url      # sportspress' timeline url
        self.timeline = []

    def scrapeTimeline(self):
        # get timeline html code
        source = requests.get(self.url).text
        soup = BeautifulSoup(source, features="html.parser")
        table = soup.find("div", class_="sportspress")
        if table is None:
            print("table is None")
        else:
            date = table.find_all("td", {"class":"data-date"})
            for i in date:
                strDate = (i.text)[0:10]
                date1 = datetime.strptime(strDate, "%Y-%m-%d").strftime("%Y-%m-%d")
                self.timeline.append(date1)

            teams = table.find_all("td", {"class":"data-event"})
            for i in teams:
                self.timeline.append(i.text)

            matchResult = table.find_all("td", {"class":"data-time"})
            for mr in matchResult:
                self.timeline.append(mr.text)

            league = table.find_all("td", {"class": "data-league"})
            for i in league:
                self.timeline.append(i.text)

            field = table.find_all("td", {"class": "data-venue"})
            for i in field:
                self.timeline.append(i.text)

            round = table.find_all("td", {"class": "data-day"})
            for i in round:
                self.timeline.append(i.text)
            # self.timeline.append(table.find_all("td", {"class":"data-day"}))
            return self.timeline

from datetime import datetime, date

#############################################################################################################
class HTMLbuilder():
    startDate = date
    endDate = date

    # @pyqtSlot(str, int)
    def setStartDate(self, strDate):
        qdate = datetime.strptime(strDate, "%Y-%m-%d")
        self.startDate = qdate.date()

    def setEndDate(self, strDate):
        qdate = datetime.strptime(strDate, "%Y-%m-%d")
        self.endDate = qdate.date()

    def buildHTMLcode(self, timeline):
        startHTMLcode = '<html lang="pl"><head><link rel="stylesheet" href="css\global.css">'\
                        '<link rel="stylesheet" href="css\\timeline.css"></head>'\
                        '<body><div id="container"><div id="top_bar"><img src="img/belka_gora.png" id="img_top">'\
                        '<div id="league">NOWOHUCKA AMATORSKA LIGA FUTSALU</div><div id="division">_DIVISION_</div>'\
                        '</div><div id="timeline"><table class="timeline_table">'
        endHTMLcode = '</table></div><div id="bottom_bar"><img src="img/druzyny-logo-belka.png" id="img_bottom">'\
                        '</div></div></body></html>'
        contentHTMLcode = ''
        replacedStartHTMLcode = ''
        isodd = True
        nrOfItems = int(len(timeline)/6)
        for i in range(0,nrOfItems):
            date = timeline[i]
            date_object = datetime.strptime(date, '%Y-%m-%d').date()
            print(date_object)
            print(self.startDate)
            if date_object >= self.startDate and date_object <= self.endDate:
                teams = timeline[i + 1*nrOfItems]
                splittedTeams = teams.split(" — ")
                homeTeam = splittedTeams[0]
                homeTeam = homeTeam[2:]
                awayTeam = splittedTeams[1]
                matchResult = timeline[i + 2*nrOfItems]
                if len(matchResult)>8:
                    matchResult = matchResult[1:6]
                league = timeline[i + 3*nrOfItems]
                field = timeline[i + 4*nrOfItems]
                round = timeline[i + 5*nrOfItems]
                if isodd == True:
                    oddOrEven = "odd"
                else:
                    oddOrEven = "even"
                contentHTMLcode += '<tr class="' + oddOrEven + '"><td class="date">' + str(date_object) + '</td><td class="homeTeam">'\
                                   + homeTeam + '</td><td class="matchResult">' + matchResult + \
                                   '</td><td class="awayTeam">' + awayTeam + '</td>' + \
                                   '<td class ="league" > ' + league + '</td>' + \
                                   '<td class="round">' + round + '</td></tr>'
                if isodd == True:
                    isodd = False
                else:
                    isodd = True
                replacedStartHTMLcode = startHTMLcode.replace("_DIVISION_", league)
        timelineHTMLcode = replacedStartHTMLcode + contentHTMLcode + endHTMLcode
        return timelineHTMLcode

#############################################################################################################
class HTMLwriter():
    def __init__(self):
        self.pth = "Sceny\\generatedScenes\\"

    def htmlWriter(self, path, fileName, htmlCode):
        try:
            x = self.pth+path+"\\"+fileName
            with open(x,"w+") as f:
                f.write(htmlCode)
                f.close()

        except TypeError as valerr:
            print(valerr)

from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel, QGroupBox, QDialog, QPushButton
from PyQt5.QtGui import QPalette, QColor
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
#############################################################################################################
class TimelineWidget(QWidget):

    changedValue = pyqtSignal(str)


    def __init__(self):
        super().__init__()
        self.labelLastMatches = QLabel("Ostatnie wyniki", self)
        self.labelLastMatches.move(5, 0)
        self.btnSetLastMatchesStartDate = QPushButton("DATA OD", self)
        self.btnSetLastMatchesStartDate.setGeometry(5, 15, 80, 21)
        self.btnSetLastMatchesEndDate = QPushButton("DATA DO", self)
        self.btnSetLastMatchesEndDate.setGeometry(5, 37, 80, 21)
        lastWednesday = str(MainWindow.lastWednesday)
        lastTuesday = str(MainWindow.lastTuesday)
        nextTuesday = str(MainWindow.nextTuesday)
        nextWednesday = str(MainWindow.nextWednesday)
        self.labelLastMatchesStartDate = QLabel(lastTuesday, self)
        self.labelLastMatchesEndDate = QLabel(lastWednesday, self)
        self.labelLastMatchesStartDate.setGeometry(90,15,100,21)
        self.labelLastMatchesEndDate.setGeometry(90,37,100,21)

        self.labelNextMatches = QLabel("Najbliższe mecze", self)
        self.labelNextMatches.move(5, 65)
        self.btnSetNextMatchesStartDate = QPushButton("DATA OD", self)
        self.btnSetNextMatchesStartDate.setGeometry(5, 79, 80, 21)
        self.btnSetNextMatchesEndDate = QPushButton("DATA DO", self)
        self.btnSetNextMatchesEndDate.setGeometry(5, 101, 80, 21)
        self.labelNextMatchesStartDate = QLabel(nextTuesday, self)
        self.labelNextMatchesEndDate = QLabel(nextWednesday, self)
        self.labelNextMatchesStartDate.setGeometry(90,79,100,21)
        self.labelNextMatchesEndDate.setGeometry(90,101,100,21)

        self.btnDoIt = QPushButton("DO IT", self)
        self.btnDoIt.setGeometry(5, 123, 80, 21)

        self.btnDoIt.clicked.connect(self.doIt)


        # self.btnSetPTimelineStartDate = QPushButton("'P' od", self)
        # self.btnSetPTimelineStartDate.setGeometry(5, 93, 80, 21)
        # self.btnSetPTimelineEndDate = QPushButton("'P' do", self)
        # self.btnSetPTimelineEndDate.setGeometry(5, 115, 80, 21)
        # self.labelPTimelineStartDate = QLabel("DATA od", self)
        # self.labelPTimelineEndDate = QLabel("DATA do", self)
        # self.labelPTimelineStartDate.setGeometry(90,93,100,21)
        # self.labelPTimelineEndDate.setGeometry(90,115,100,21)

        calendar = CalendarWindow()
        self.lastMatchesStartDate = CalendarWindow()
        self.lastMatchesEndDate = CalendarWindow()
        self.nextMatchesStartDate = CalendarWindow()
        self.nextMatchesEndDate = CalendarWindow()
        self.btnSetLastMatchesStartDate.clicked.connect(partial(self.lastMatchesStartDate.createCalendar, self.lastMatchesStartDate, 0))
        self.btnSetLastMatchesEndDate.clicked.connect(partial(self.lastMatchesEndDate.createCalendar, self.lastMatchesEndDate, 1))
        self.btnSetNextMatchesStartDate.clicked.connect(partial(self.nextMatchesStartDate.createCalendar, self.nextMatchesStartDate, 2))
        self.btnSetNextMatchesEndDate.clicked.connect(partial(self.nextMatchesEndDate.createCalendar, self.nextMatchesEndDate, 3))
        # self.btnSetLastMatchesStartDate.clicked.connect(partial(lastMatchesStartDate.createCalendar, 0))
        # self.btnSetLastMatchesEndDate.clicked.connect(partial(lastMatchesEndDate.createCalendar, 1))
        # self.btnSetNextMatchesStartDate.clicked.connect(partial(nextMatchesStartDate.createCalendar, 2))
        # self.btnSetNextMatchesEndDate.clicked.connect(partial(nextMatchesEndDate.createCalendar, 3))

        self.lastMatchesStartDate.signal.connect(self.setLabelText)
        # lastMatchesStartDate.signal.connect(partial(self.setLabelText, self.labelLastMatchesStartDate))
        self.lastMatchesEndDate.signal.connect(self.setLabelText)
        self.nextMatchesStartDate.signal.connect(self.setLabelText)
        self.nextMatchesEndDate.signal.connect(self.setLabelText)

    def doIt(self):
        scrapeLeagueA = MainWindow.leagueAscraper.scrapeTimeline()
        codeLastLeagueA = MainWindow.lastMatchesHtmlBuilder.buildHTMLcode(scrapeLeagueA)
        codeNextLeagueA = MainWindow.nextMatchesHtmlBuilder.buildHTMLcode(scrapeLeagueA)
        scrapeLeagueB = MainWindow.leagueBscraper.scrapeTimeline()
        codeLastLeagueB = MainWindow.lastMatchesHtmlBuilder.buildHTMLcode(scrapeLeagueB)
        codeNextLeagueB = MainWindow.nextMatchesHtmlBuilder.buildHTMLcode(scrapeLeagueB)
        scrapeCup = MainWindow.cupScraper.scrapeTimeline()
        codeLastCup = MainWindow.lastMatchesHtmlBuilder.buildHTMLcode(scrapeCup)
        codeNextCup = MainWindow.nextMatchesHtmlBuilder.buildHTMLcode(scrapeCup)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("A", "wyniki.html", codeLastLeagueA)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("A", "terminarz.html", codeNextLeagueA)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("B", "wyniki.html", codeLastLeagueB)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("B", "terminarz.html", codeNextLeagueB)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("P", "wyniki.html", codeLastCup)
        MainWindow.lastMatchesHtmlWriter.htmlWriter("P", "terminarz.html", codeNextCup)
        MainWindow.tableScraper.scrape_table("http://nalffutsal.pl/?page_id=16", "A")
        MainWindow.tableScraper.scrape_table("http://nalffutsal.pl/?page_id=36", "B")
        MainWindow.tableScraper.scrape_strikers("strzelcy", "http://nalffutsal.pl/?page_id=50", "A")
        MainWindow.tableScraper.scrape_strikers("asystenci", "http://nalffutsal.pl/?page_id=3191", "A")
        MainWindow.tableScraper.scrape_strikers("kanadyjska", "http://nalffutsal.pl/?page_id=42", "A")
        MainWindow.tableScraper.scrape_strikers("strzelcy", "http://nalffutsal.pl/?page_id=18", "B")
        MainWindow.tableScraper.scrape_strikers("asystenci", "http://nalffutsal.pl/?page_id=3274", "B")
        MainWindow.tableScraper.scrape_strikers("kanadyjska", "http://nalffutsal.pl/?page_id=44", "B")
        MainWindow.tableScraper.scrape_strikers("strzelcy", "http://nalffutsal.pl/?page_id=38", "P")
        MainWindow.tableScraper.scrape_strikers("asystenci", "http://nalffutsal.pl/?page_id=3317", "P")
        MainWindow.tableScraper.scrape_strikers("kanadyjska", "http://nalffutsal.pl/?page_id=54", "P")


    @pyqtSlot(str, int)
    def setLabelText(self, value, number):
        assert isinstance(value, str)
        assert isinstance(number, int)
        if number == 0:
            self.labelLastMatchesStartDate.setText(value)
            MainWindow.lastMatchesHtmlBuilder.setStartDate(value)
        if number == 1:
            self.labelLastMatchesEndDate.setText(value)
            MainWindow.lastMatchesHtmlBuilder.setEndDate(value)
        if number == 2:
            self.labelNextMatchesStartDate.setText(value)
            MainWindow.nextMatchesHtmlBuilder.setStartDate(value)
        if number == 3:
            self.labelNextMatchesEndDate.setText(value)
            MainWindow.nextMatchesHtmlBuilder.setEndDate(value)

    #     self.setStartDate(value, number)
    #
    # def setStartDate(self, strDate, number):
    #     assert isinstance(strDate, str)
    #     print("setStartDate")

#############################################################################################################
class CalendarWindow(QWidget):
    signal = pyqtSignal(str, int)

    # comm1 = Communicator()
    # comm2 = Communicator()
    # comm3 = Communicator()
    # comm4 = Communicator()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pyside2 Calendar")
        self.setGeometry(300, 200, 250, 200)

    def createCalendar(self, cal, var):
        self.vbox = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

        self.vbox.addWidget(self.calendar)
        self.setLayout(self.vbox)
        self.calendar.clicked.connect(partial(self.setDate, var))
        self.show()
        # self.calendar.clicked[QDate].connect(partial(self.setDate, var))

    def printit(self):
        print("connect")

    def setDate(self, var, qDate):
        # strDate = date.toString()
        # date1 = datetime.strptime(strDate, "%Y-%m-%d").strftime("%Y-%m-%d")

        strDate = qDate.toString("yyyy-MM-dd")
        self.signal.emit(strDate, var)
        # self.buttonSelector(var, qDate)
        self.close()

    def buttonSelector(self, var, qDate):
        strDate = qDate.toString("yyyy-MM-dd")
        self.signal.emit(strDate, var)
        # if var == 0:
        #     self.signal.emit(strDate, var)
        # if var == 1:
        #     self.signal.emit(strDate, var)
        # if var == 2:
        #     self.signal.emit(strDate, var)
        # if var == 3:
        #     self.signal.emit(strDate, var)




#############################################################################################################
class Scrape():

    adress_a = 'http://nalffutsal.pl/?page_id=16'
    adress_b = 'http://nalffutsal.pl/?page_id=36'
    pathA = 'A\\'
    pathB = 'B\\'

    def scrape_strikers(self, type, adress, division):
        source = requests.get(adress).text
        soup = BeautifulSoup(source, features="html.parser")
        sportspress_div = soup.find('div', class_='sportspress')
        header = sportspress_div.find('h4').text
        table = sportspress_div.find('table')
        table_header = table.find('thead')
        table_rows = table.find_all('tr')
        self.make_html(type, header, table_header, table_rows, division)


    def make_html(self, type, header, thead, table_rows, division):
        my_filename = "Sceny\\generatedScenes\\" + division + "\\" + type + ".html"
        start_html = '<html lang="pl"><head><link rel="stylesheet" href="css\global.css">'\
                     '<link rel="stylesheet" href="css\strzelcy.css"></head><body><div id="container"><div id="top_bar"><img src="img/belka_gora.png" id="img_top"><div id="league">NOWOHUCKA AMATORSKA LIGA FUTSALU</div>'
        table_html = '<div id="division">' + str(header) + '</div></div><div class="table"><div id="table_b"><table id="tab_a">' + str(thead) + '<tbody>'
        insert_html = ''
        end_html = '</table></div></div><div id="bottom_bar"><img src="img/druzyny-logo-belka.png" id="img_bottom"></div></body></html>'

        for i in range(len(table_rows)):
            if i > 0 and i < 11:
                insert_html += str(table_rows[i])

        raw_html = start_html + table_html + insert_html + end_html
        html = self.prepare_html(raw_html)
        with open(my_filename, "w+") as f:
            f.write(html)
            f.close()
            # table.clear()

    def prepare_html(self, raw_html):
        bs = BeautifulSoup(raw_html, features="html.parser")

        for a in bs.findAll('a'):
            del a['href']
        str_bs = str(bs)
        new_str_bs = str_bs.replace('<tr>', '<tr class="invisible_text">')
        return new_str_bs

    def scrape_table(self, adress, division):
        source = requests.get(adress).text
        soup = BeautifulSoup(source, features="html.parser")
        table_a_div = soup.find('div', class_='sportspress')

        team_position = table_a_div.find_all("td", {"class":"data-rank"})
        team_name = table_a_div.find_all("td", {"class":"data-name"})
        team_matches = table_a_div.find_all("td", {"class":"data-m"})
        team_wins = table_a_div.find_all("td", {"class":"data-z"})
        team_ties = table_a_div.find_all("td", {"class":"data-r"})
        team_loses = table_a_div.find_all("td", {"class":"data-p"})
        team_goals_scored = table_a_div.find_all("td", {"class":"data-gz"})
        team_goals_lost = table_a_div.find_all("td", {"class":"data-gs"})
        team_points = table_a_div.find_all("td", {"class":"data-pkt"})
        team_a = []

        table = []

        ile = len(team_position)
        for i in range(ile):
            row = [team_position[i].text, team_name[i].text, team_matches[i].text, team_wins[i].text, team_ties[i].text,\
                           team_loses[i].text, team_goals_scored[i].text, team_goals_lost[i].text, team_points[i].text]
            table.append(row)


       # # def save_table2(adress):
        my_filename = "Sceny\\generatedScenes\\" + division + "\\tabela.html"
        start_html = '<html lang="pl"><head><link rel="stylesheet" href="css\global.css">'\
                     '<link rel="stylesheet" href="css\\tabela.css"></head><body><div id="container"><div id="top_bar"><img src="img/belka_gora.png" id="img_top"><div id="league">NOWOHUCKA AMATORSKA LIGA FUTSALU</div>'
        if adress == self.adress_a:
            table_html = '<div id="division">Dywizja A</div></div><div class="table"><div id="table_b"><table id="tab_a"><thead><tr class="class_header"><th class="data-rank"></th><th class="data-name"></th><th class="data-m">M</th><th class="data-z">Z</th><th class="data-r">R</th><th class="data-p">P</th><th class="data-gz">GZ</th><th class="data-gs">GS</th><th class="data-pkt">Pkt</th></tr></thead><tbody>'
        elif adress == self.adress_b:
            table_html = '<div id="division">Dywizja B</div></div><div class="table"><div id="table_b"><table id="tab_b"><thead><tr class="class_header"><th class="data-rank"></th><th class="data-name"></th><th class="data-m">M</th><th class="data-z">Z</th><th class="data-r">R</th><th class="data-p">P</th><th class="data-gz">GZ</th><th class="data-gs">GS</th><th class="data-pkt">Pkt</th></tr></thead><tbody>'
        insert_html = ''
        end_html = '</table></div></div><div id="bottom_bar"><img src="img/druzyny-logo-belka.png" id="img_bottom"></div></div></body></html>'
        which = bool
        tr_class = ''
        for i in range(ile):
            if which != True:
                tr_class = "odd"
            else: tr_class = "even"
            insert_html += '<tr class="'+ tr_class +'"><td class="team_pos">' + table[i][0] + \
                           '</td><td class="team_name">' + table[i][1] + '</td><td>' + table[i][2] + \
                           '</td><td>' + table[i][3] + '</td><td>' + table[i][4] + \
                          '</td><td>' + table[i][5] + '</td><td>' + table[i][6] + \
                          '</td><td>' + table[i][7] + '</td><td class="points">' + table[i][8] + \
                           '</td></tr>'
            if which == True:
                which = False
            else: which = True

        final_html = start_html + table_html + insert_html + end_html

        with open(my_filename, "w+") as f:
            f.write(final_html)
            f.close()
            table.clear()
#############################################################################################################
from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy
import codecs
class MatchSelectorWidget(QWidget):
    matchNr = 0
    matches = []
    address = []
    def __init__(self):
        super().__init__()
        self.fileReader()
        self.drawGUI()



    def drawGUI(self):

        self.btnPreviousMatch = QPushButton("◄", self)
        self.btnPreviousMatch.setGeometry(25,25,60,60)
        self.btnPreviousMatch.clicked.connect(self.btnPreviousMatchOnClick)

        self.labelMatchNr = QLabel(str(self.matchNr + 1), self)
        self.labelMatchNr.setGeometry(88,26,58,58)
        self.labelMatchNr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelMatchNr.setAlignment(Qt.AlignCenter)
        self.labelMatchNr.setStyleSheet("QLabel {background-color: gray; font-size: 30px;}")

        self.labelTeams = QLabel(self.matches[self.matchNr], self)
        self.labelTeams.setGeometry(0,0,230,23)
        self.labelTeams.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelTeams.setAlignment(Qt.AlignCenter)
        self.labelTeams.setStyleSheet("QLabel {border: 1px solid gray; font-size: 13px;}")

        self.btnNextMatch = QPushButton("►", self)
        self.btnNextMatch.setGeometry(150,25,60,60)
        self.btnNextMatch.clicked.connect(self.btnNextMatchOnClick)

        self.labelAddress = QLabel(self.address[self.matchNr], self)
        self.labelAddress.setVisible(False)
        self.labelAddress.setGeometry(0,90,230,23)
        self.labelAddress.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelAddress.setAlignment(Qt.AlignCenter)
        self.labelAddress.setStyleSheet("QLabel {border: 1px solid gray; font-size: 13px;}")
        startLabel = self.scrapeTitle(self.address[self.matchNr])
        self.labelAddress.setText("startLabel")
        # self.labelAddress.setText(startLabel)

        self.doRedirectPage(self.address[self.matchNr])
        self.saveFile(self.matches[self.matchNr])

        self.bestFiveBtn = QPushButton("Piątka kolejki", self)
        self.bestFiveBtn.setGeometry(60,100,115,25)
        self.bestFiveBtn.clicked.connect(self.bestFiveBtnOnClick)


    def btnPreviousMatchOnClick(self):
        if self.matchNr > 0:
            self.matchNr -= 1
            self.labelMatchNr.setText(str(self.matchNr + 1))
            self.labelTeams.setText(self.matches[self.matchNr])
            self.scrapeTitle(self.address[self.matchNr])
            title = self.scrapeTitle(self.address[self.matchNr])
            self.labelAddress.setText(title)
            self.doRedirectPage(self.address[self.matchNr])
            self.saveFile(self.matches[self.matchNr])

    def btnNextMatchOnClick(self):
        if self.matchNr < len(self.matches) - 1:
            self.matchNr += 1
            self.labelMatchNr.setText(str(self.matchNr + 1))
            self.labelTeams.setText(self.matches[self.matchNr])
            title = self.scrapeTitle(self.address[self.matchNr])
            self.labelAddress.setText(title)
            self.doRedirectPage(self.address[self.matchNr])
            self.saveFile(self.matches[self.matchNr])

    def bestFiveBtnOnClick(self):
        self.bestFiveWindow = BestFiveWindow(self)
        self.bestFiveWindow.show()


    def saveFile(self, text):
        path = "Sceny\\inUseScenes\\txt\\"
        x = path + "mecz.txt"
        with codecs.open(x, "w", encoding='utf8') as f:
            f.write(text)

    def doRedirectPage(self, address):
        if address == "!adres!":
            allHtml = "<html><head/><body/></html>"
        else:
            address = address[32:]
            startHtml = '<html><head><title>HTML Redirect</title><meta http-equiv="refresh" content="0; url=https://www.youtube.com/embed/'
            endHtml = '?autoplay=1&showinfo=0&controls=0&rel=0&showinfo=0"/></head><body></body></html>'
            allHtml = startHtml + address + endHtml
        path = "Sceny\\inUseScenes\\"
        x = path + "skrot.html"
        with open(x, "w") as f:
            f.write(allHtml)


    def fileReader(self):
        pathToFile = "Sceny\\inUseScenes\\txt\\"
        fileToRead = pathToFile + "mecze.txt"
        with open(fileToRead) as file_in:
            for line in file_in:
                if line[-1:] == "\n":
                    line = line[0:-1]
                dividedString = line.split(",")
                self.matches.append(dividedString[0])
                self.address.append(dividedString[1])

    def scrapeTitle(self, address):

        if address == "!adres!":
            return ""
        else:
            source = requests.get(address).text
            soup = BeautifulSoup(source, features="html.parser")
            htmlHeadCode = soup.find('head')

            title = htmlHeadCode.find("title")
            return title
            # return title.string

# Widget - edit episode number and description
from PyQt5.QtWidgets import QTextEdit
import os, codecs
class EpisodeDescriptionWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.drawGUI()

    def drawGUI(self):
        self.path = "Sceny\\inUseScenes\\txt\\"

        try:
            pathToFile = self.path + "odcinekNumer.txt"
            with codecs.open(pathToFile, "r", "utf-8") as f:
                episodeNr = f.read()
                self.episodeNumber = episodeNr[1:]
        except TypeError as valerr:
            print(valerr)

        try:
            pathToFile = self.path + "odcinekOpis1.txt"
            with codecs.open(pathToFile, "r", "utf-8") as f:
                self.episodeDescryption1 = f.read()
        except TypeError as valerr:
            print(valerr)

        try:
            pathToFile = self.path + "odcinekOpis2.txt"
            with codecs.open(pathToFile, "r", "utf-8") as f:
                self.episodeDescryption2 = f.read()
        except TypeError as valerr:
            print(valerr)


        self.labelEpisodeNumber = QLabel("Odcinek #", self)
        self.labelEpisodeNumber.setGeometry(5, 25, 50, 25)

        self.textEditEpisodeNr = QTextEdit(self.episodeNumber, self)
        self.textEditEpisodeNr.setGeometry(60,25,35,25)

        self.textEditEpisodeDescryption1 = QTextEdit(self.episodeDescryption1, self)
        self.textEditEpisodeDescryption1.setGeometry(5, 53, 223, 25)

        self.textEditEpisodeDescryption2 = QTextEdit(self.episodeDescryption2, self)
        self.textEditEpisodeDescryption2.setGeometry(5, 81, 223, 25)

        self.btnSave = QPushButton("Zapisz", self)
        self.btnSave.setGeometry(40, 108, 150, 21)
        self.btnSave.clicked.connect(self.btnSaveClick)

    def btnSaveClick(self):
        try:
            self.filePath = "Sceny\\inUseScenes\\txt\\odcinekNumer.txt"
            x = self.filePath
            nr = str(self.textEditEpisodeNr.toPlainText())
            with codecs.open(x,"w+", "utf-8") as f:
                f.write("#"+nr)
                f.close()

        except TypeError as valerr:
            print(valerr)

        try:
            self.filePath = "Sceny\\inUseScenes\\txt\\odcinekOpis1.txt"
            x = self.filePath
            txt = self.textEditEpisodeDescryption1.toPlainText()
            with codecs.open(x, "w+", "utf-8") as f:
                f.write(txt)
                f.close()

        except TypeError as valerr:
            print(1, valerr)

        try:
            self.filePath = "Sceny\\inUseScenes\\txt\\odcinekOpis2.txt"
            x = self.filePath
            txt = self.textEditEpisodeDescryption2.toPlainText()
            with codecs.open(x,"w+", "utf-8") as f:
                f.write(txt)
                f.close()

        except TypeError as valerr:
            print(valerr)

#############################################################################################################
# Window "Best Five"

from PyQt5.QtWidgets import QRadioButton, QComboBox, QErrorMessage
import json

class BestFiveWindow(QWidget):

    teamsDict = {"": "",
                 "AZS":"AZS Collegium Medicum UJ",
                "BOA": "Boanerges",
                "DRI": "Drink Team",
                "DRU": "DRUG-ony",
                "ENH": "eNHa",
                "GEC": "Geco Team",
                "HAT": "Hattrick",
                "IGL": "IGLOMEN&RodzinneRestauracje",
                "JRU": "JRU Futsal",
                "KRA": "Krakowiak",
                "MKT": "MK Team",
                "NPŚ": "Nie Przez Środek",
                "OCE": "Ocean’s Eleven",
                "RAC": "Racing Kart – tor gokartowy",
                "ROC": "Rocket Fuel",
                "SPA": "Sparta Kraków",
                "TEA": "Team One",
                "WAT": "Wataha",
                "ZŁO": "Złote Chłopaki",
                "ŻAR": "Żarłacze"}


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.drawGui()
        self.readDataFromJson()

    def drawGui(self):
        self.setGeometry(550, 200, 250, 205)
        self.setWindowTitle("Piątka Kolejki")

        self.divisionGroupBox = QGroupBox(self)
        self.divisionGroupBox.setGeometry(5, 5, 240, 30)
        self.divisionSelectLabel1 = QLabel(self.divisionGroupBox)
        self.divisionSelectLabel1.setGeometry(5,2,30,25)
        self.divisionSelectLabel1.setText("Piątka")
        self.roundNrTextBox = QTextEdit(self.divisionGroupBox)
        self.roundNrTextBox.setGeometry(35,4,23,23)
        self.divisionSelectLabel2 = QLabel(self.divisionGroupBox)
        self.divisionSelectLabel2.setGeometry(60,2,70,25)
        self.divisionSelectLabel2.setText("kolejki Dywizji")
        self.divisionSelectRadioButtonA = QRadioButton(self.divisionGroupBox)
        self.divisionSelectRadioButtonA.move(130,8)
        self.divisionSelectRadioButtonA.setText("A")
        self.divisionSelectRadioButtonA.setChecked(True)
        self.divisionSelectRadioButtonB = QRadioButton(self.divisionGroupBox)
        self.divisionSelectRadioButtonB.move(170,8)
        self.divisionSelectRadioButtonB.setText("B")
        self.divisionSelectRadioButtonC = QRadioButton(self.divisionGroupBox)
        self.divisionSelectRadioButtonC.move(210,8)
        self.divisionSelectRadioButtonC.setText("C")
        self.divisionSelectRadioButtonC.setEnabled(False)

        self.divisionSelectRadioButtonA.clicked.connect(self.readDataFromJson)
        self.divisionSelectRadioButtonB.clicked.connect(self.readDataFromJson)
        self.divisionSelectRadioButtonC.clicked.connect(self.readDataFromJson)

        self.bestFiveListGroupBox = QGroupBox(self)
        self.bestFiveListGroupBox.setGeometry(5, 40, 240, 160)
        best5left = 20
        best5width = 150
        best5height = 23
        top = [5,30,55,80,105]
        self.bestFive1TextBox = QTextEdit(self.bestFiveListGroupBox)
        self.bestFive1TextBox.setGeometry(best5left, top[0], best5width, best5height)
        self.bestFive2TextBox = QTextEdit(self.bestFiveListGroupBox)
        self.bestFive2TextBox.setGeometry(best5left, top[1], best5width, best5height)
        self.bestFive3TextBox = QTextEdit(self.bestFiveListGroupBox)
        self.bestFive3TextBox.setGeometry(best5left, top[2], best5width, best5height)
        self.bestFive4TextBox = QTextEdit(self.bestFiveListGroupBox)
        self.bestFive4TextBox.setGeometry(best5left, top[3], best5width, best5height)
        self.bestFive5TextBox = QTextEdit(self.bestFiveListGroupBox)
        self.bestFive5TextBox.setGeometry(best5left, top[4], best5width, best5height)

        bestPlayerLeft = 5
        self.bestPlayerRadioBtn1 = QRadioButton(self.bestFiveListGroupBox)
        self.bestPlayerRadioBtn2 = QRadioButton(self.bestFiveListGroupBox)
        self.bestPlayerRadioBtn3 = QRadioButton(self.bestFiveListGroupBox)
        self.bestPlayerRadioBtn4 = QRadioButton(self.bestFiveListGroupBox)
        self.bestPlayerRadioBtn5 = QRadioButton(self.bestFiveListGroupBox)
        self.bestPlayerRadioBtn1.move(bestPlayerLeft, 10)
        self.bestPlayerRadioBtn2.move(bestPlayerLeft, 35)
        self.bestPlayerRadioBtn3.move(bestPlayerLeft, 60)
        self.bestPlayerRadioBtn4.move(bestPlayerLeft, 85)
        self.bestPlayerRadioBtn5.move(bestPlayerLeft, 110)

        buttonsTop = 170
        buttonsHeight = 25
        buttonsWidth = 60
        self.saveBtn = QPushButton(self)
        self.clearBtn = QPushButton(self)
        self.clear2Btn = QPushButton(self)
        self.saveBtn.setText("Zapisz")
        self.saveBtn.setGeometry(40, buttonsTop, buttonsWidth, buttonsHeight)
        self.clearBtn.setGeometry(115, buttonsTop, buttonsWidth, buttonsHeight)
        self.clear2Btn.setGeometry(115, buttonsTop, buttonsWidth, buttonsHeight)
        self.clearBtn.setText("Wyczyść")
        self.clear2Btn.setText("Potwierdź")
        self.saveBtn.clicked.connect(self.saveBtnOnClick)
        self.clearBtn.clicked.connect(self.clearBtnUnlock)
        self.clear2Btn.clicked.connect(self.clear2BtnOnClick)
        self.clear2Btn.setVisible(False)

        teamShortNameComboBoxLeft = 180
        teamShortNameComboBoxWidth = 60
        teamShortNameComboBoxHeight = 23
        self.team1SelectComboBox = QComboBox(self.bestFiveListGroupBox)
        self.team2SelectComboBox = QComboBox(self.bestFiveListGroupBox)
        self.team3SelectComboBox = QComboBox(self.bestFiveListGroupBox)
        self.team4SelectComboBox = QComboBox(self.bestFiveListGroupBox)
        self.team5SelectComboBox = QComboBox(self.bestFiveListGroupBox)
        self.team1SelectComboBox.setGeometry(teamShortNameComboBoxLeft, top[0], teamShortNameComboBoxWidth, teamShortNameComboBoxHeight)
        self.team2SelectComboBox.setGeometry(teamShortNameComboBoxLeft, top[1], teamShortNameComboBoxWidth, teamShortNameComboBoxHeight)
        self.team3SelectComboBox.setGeometry(teamShortNameComboBoxLeft, top[2], teamShortNameComboBoxWidth, teamShortNameComboBoxHeight)
        self.team4SelectComboBox.setGeometry(teamShortNameComboBoxLeft, top[3], teamShortNameComboBoxWidth, teamShortNameComboBoxHeight)
        self.team5SelectComboBox.setGeometry(teamShortNameComboBoxLeft, top[4], teamShortNameComboBoxWidth, teamShortNameComboBoxHeight)
        self.addTeamsToCombobox(self.team1SelectComboBox)
        self.addTeamsToCombobox(self.team2SelectComboBox)
        self.addTeamsToCombobox(self.team3SelectComboBox)
        self.addTeamsToCombobox(self.team4SelectComboBox)
        self.addTeamsToCombobox(self.team5SelectComboBox)

###########  METHODS FOR READ DATA FROM JSON AND PUT IT IN GUI ####################
    def readDataFromJson(self):
        letter = self.getDivisionLetter()
        file = "Sceny\\generatedScenes\\" + letter + "\\5kolejki.json"
        jsonObject = self.readJson(file)
        self.json2gui(jsonObject)

    def json2gui(self, jsonObject):
        self.roundNrTextBox.setText(jsonObject["round"])
        self.bestFive1TextBox.setText(jsonObject["player1"]["fullName"])
        self.bestFive2TextBox.setText(jsonObject["player2"]["fullName"])
        self.bestFive3TextBox.setText(jsonObject["player3"]["fullName"])
        self.bestFive4TextBox.setText(jsonObject["player4"]["fullName"])
        self.bestFive5TextBox.setText(jsonObject["player5"]["fullName"])

        self.json2guiRadioBtnSet(jsonObject["player1"]["isBestPlayer"], self.bestPlayerRadioBtn1)
        self.json2guiRadioBtnSet(jsonObject["player2"]["isBestPlayer"], self.bestPlayerRadioBtn2)
        self.json2guiRadioBtnSet(jsonObject["player3"]["isBestPlayer"], self.bestPlayerRadioBtn3)
        self.json2guiRadioBtnSet(jsonObject["player4"]["isBestPlayer"], self.bestPlayerRadioBtn4)
        self.json2guiRadioBtnSet(jsonObject["player5"]["isBestPlayer"], self.bestPlayerRadioBtn5)

        self.json2guiComboBoxSelect(self.team1SelectComboBox, jsonObject["player1"]["team"])
        self.json2guiComboBoxSelect(self.team2SelectComboBox, jsonObject["player2"]["team"])
        self.json2guiComboBoxSelect(self.team3SelectComboBox, jsonObject["player3"]["team"])
        self.json2guiComboBoxSelect(self.team4SelectComboBox, jsonObject["player4"]["team"])
        self.json2guiComboBoxSelect(self.team5SelectComboBox, jsonObject["player5"]["team"])

    def json2guiRadioBtnSet(self, jsonObj, radiobutton):
        if jsonObj is True:
            radiobutton.setChecked(True)
        else:
            radiobutton.setChecked(False)

    def json2guiComboBoxSelect(self, combobox, text):
        index = combobox.findText(text)
        combobox.setCurrentIndex(index)


    def readJson(self, file):
        with codecs.open(file, "r", "utf-8") as f:
            jsonString = f.read()
            jsonValues = json.loads(jsonString)
            return jsonValues

############# METHODS TO SAVE GUI VALUES TO JSON FILE #################

    def collectData(self):
        values = {
            "round": self.roundNrTextBox.toPlainText(),
            "division": self.getDivisionLetter(),
            "player1": {
                "isBestPlayer": self.isBestPlayer(self.bestPlayerRadioBtn1),
                "fullName": self.bestFive1TextBox.toPlainText(),
                "team": self.team1SelectComboBox.currentText()
            },
            "player2": {
                "isBestPlayer": self.isBestPlayer(self.bestPlayerRadioBtn2),
                "fullName": self.bestFive2TextBox.toPlainText(),
                "team": self.team2SelectComboBox.currentText()
            },
            "player3": {
                "isBestPlayer": self.isBestPlayer(self.bestPlayerRadioBtn3),
                "fullName": self.bestFive3TextBox.toPlainText(),
                "team": self.team3SelectComboBox.currentText()
            },
            "player4": {
                "isBestPlayer": self.isBestPlayer(self.bestPlayerRadioBtn4),
                "fullName": self.bestFive4TextBox.toPlainText(),
                "team": self.team4SelectComboBox.currentText()
            },
            "player5": {
                "isBestPlayer": self.isBestPlayer(self.bestPlayerRadioBtn5),
                "fullName": self.bestFive5TextBox.toPlainText(),
                "team": self.team5SelectComboBox.currentText()
            }
        }
        return values

    def saveValuesToJson(self):
        values = self.collectData()
        letter = self.getDivisionLetter()
        file = "Sceny\\generatedScenes\\" + letter + "\\5kolejki.json"
        with codecs.open(file, 'w') as outfile:
            json.dump(values, outfile)

    #############################################################

    def addTeamsToCombobox(self, combobox):
        for i in self.teamsDict:
            combobox.addItem(i)

    def saveBtnOnClick(self):
        self.generateHtmlFile()
        self.saveGeneratedFile(self.generateHtmlFile(), self.divisionLetter)
        self.saveValuesToJson()

    def generateHtmlFile(self):
        roundNr = self.roundNrTextBox.toPlainText()
        self.divisionLetter = self.getDivisionLetter()
        head = '<html><head><meta charset="utf-8"><link rel="stylesheet" href="css/global.css"><link rel="stylesheet" href="css/5kolejki.css"></head>'
        bodyToTbody = '<body><div id="container"><div id="top_bar"><img id="img_top" src="img/belka_gora.png" /><div id="league">NOWOHUCKA AMATORSKA LIGA FUTSALU</div>'\
                      '<div id="division">Piątka ' + roundNr + ' kolejki Dywizji ' + self.divisionLetter + '</div></div><div class="table"><div id="table_b"><table id="tab_a"><tbody>'
        bodyToEnd = '</tbody></table></div></div><div id="bottom_bar"><img id="img_bottom" src="img/druzyny-logo-belka.png" /></div></div></body></html>'
        tableBody = ""
        tableBody += self.addTableRow(self.bestFive1TextBox.toPlainText(), self.changeKeyToValue(self.team1SelectComboBox), self.isBestPlayer(self.bestPlayerRadioBtn1), True)
        tableBody += self.addTableRow(self.bestFive2TextBox.toPlainText(), self.changeKeyToValue(self.team2SelectComboBox), self.isBestPlayer(self.bestPlayerRadioBtn2))
        tableBody += self.addTableRow(self.bestFive3TextBox.toPlainText(), self.changeKeyToValue(self.team3SelectComboBox), self.isBestPlayer(self.bestPlayerRadioBtn3), True)
        tableBody += self.addTableRow(self.bestFive4TextBox.toPlainText(), self.changeKeyToValue(self.team4SelectComboBox), self.isBestPlayer(self.bestPlayerRadioBtn4))
        tableBody += self.addTableRow(self.bestFive5TextBox.toPlainText(), self.changeKeyToValue(self.team5SelectComboBox), self.isBestPlayer(self.bestPlayerRadioBtn5), True)

        allHtml = head + bodyToTbody + tableBody + bodyToEnd
        return allHtml

    def changeKeyToValue(self, combobox):
        for i in self.teamsDict:
            if i == combobox.currentText():
                teamName = self.teamsDict[i]
        return teamName

    def addTableRow(self, textbox, combobox, radiobutton, isodd=False):

        if isodd is True:
            tr = '<tr class="odd">'
        else:
            tr = '<tr class="even">'
        tds = '<td class="best_player"><a>' + radiobutton + '</a></td>' \
        '<td class="data-name"><a>' + textbox + '</a></td>' \
        '<td class="data-team"><a>' + combobox + '</a></td></tr>'
        trAndTds = tr + tds
        return trAndTds

    def isBestPlayer(self, radioButton):
        if radioButton.isChecked():
            return "&#9733"
        else:
            return ""

    def getDivisionLetter(self):
        if self.divisionSelectRadioButtonA.isChecked():
            letter = "A"
        elif self.divisionSelectRadioButtonB.isChecked():
            letter = "B"
        elif self.divisionSelectRadioButtonC.isChecked():
            letter = "C"
        return letter

    def saveGeneratedFile(self, generatedFile, division):
        try:
            my_filename = "Sceny\\generatedScenes\\" + division + "\\5kolejki.html"
            with codecs.open(my_filename, "w+", "utf-8") as f:
                f.write(generatedFile)
                f.close()
        except:
            print("Error saveGeneratedFile")

    def clearBtnUnlock(self):
        self.clear2Btn.setVisible(True)

    def clear2BtnOnClick(self):
        self.bestFive1TextBox.setText("")
        self.bestFive2TextBox.setText("")
        self.bestFive3TextBox.setText("")
        self.bestFive4TextBox.setText("")
        self.bestFive5TextBox.setText("")
        self.roundNrTextBox.setText("")
        self.team1SelectComboBox.setCurrentIndex(0)
        self.team2SelectComboBox.setCurrentIndex(0)
        self.team3SelectComboBox.setCurrentIndex(0)
        self.team4SelectComboBox.setCurrentIndex(0)
        self.team5SelectComboBox.setCurrentIndex(0)
        # self.divisionSelectRadioButtonA.setChecked(False)
        #         # self.divisionSelectRadioButtonB.setChecked(False)
        #         # self.divisionSelectRadioButtonC.setChecked(False)
        #         # self.bestPlayerRadioBtn1.setChecked(False)
        #         # self.bestPlayerRadioBtn2.setChecked(False)
        #         # self.bestPlayerRadioBtn3.setChecked(False)
        #         # self.bestPlayerRadioBtn4.setChecked(False)
        #         # self.bestPlayerRadioBtn5.setChecked(False)
        self.clear2Btn.setVisible(False)
#############################################################################################################
class MainWindow(QMainWindow):
    from datetime import date
    from datetime import timedelta
    today = date.today()
    lto = (today.weekday() - 1) % 7
    lwo = (today.weekday() - 2) % 7
    nto = (today.weekday() + 2) % 7
    nwo = (today.weekday() + 3) % 7
    lastTuesday = today - timedelta(days=lto)
    lastWednesday = today - timedelta(days=lwo)
    nextTuesday = today + timedelta(days=nto)
    nextWednesday = today + timedelta(days=nwo)


    lastMatchesHtmlBuilder = HTMLbuilder()
    lastMatchesHtmlBuilder.setStartDate(str(lastTuesday))
    lastMatchesHtmlBuilder.setEndDate(str(lastWednesday))
    nextMatchesHtmlBuilder = HTMLbuilder()
    nextMatchesHtmlBuilder.setStartDate(str(nextTuesday))
    nextMatchesHtmlBuilder.setEndDate(str(nextWednesday))
    # nextMatchesHtmlBuilder.setStartDate(str(nextTuesday))
    # nextMatchesHtmlBuilder.setEndDate(str(nextWednesday))

    lastMatchesHtmlWriter = HTMLwriter()
    nextMatchesHtmlWriter = HTMLwriter()

    leagueAscraper = TimelineScraper("http://nalffutsal.pl/?page_id=34")
    leagueBscraper = TimelineScraper("http://nalffutsal.pl/?page_id=52")
    cupScraper = TimelineScraper("http://nalffutsal.pl/?page_id=32")

    tableScraper = Scrape()




    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.drawGUI()




    def drawGUI(self):
        self.setGeometry(300, 200, 250, 450)
        self.setWindowTitle("Magazyn Ligowy")

        layout = QVBoxLayout()
        self.timelineWidget = TimelineWidget()
        layout.addWidget(self.timelineWidget)
        self.matchSelector = MatchSelectorWidget()
        layout.addWidget(self.matchSelector)
        self.episodeDescription = EpisodeDescriptionWidget()
        layout.addWidget(self.episodeDescription)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


from bs4 import BeautifulSoup
import requests





############################
# TO JEST KLASA POMOCNICZA #
class Color(QWidget):

    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

# KONIEC KLASY POMOCNICZEJ #
############################
class Run(object):
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())



