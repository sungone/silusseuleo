from tkinter import *
from tkinter import font
import SiluList
from tkinter import INSERT
import webbrowser
from gmplot import gmplot
from collections import defaultdict
import requests
from PIL import Image, ImageTk
import Image
import Gmail
import sortbykey

api_key = 'AIzaSyBLgIymSA0TWviqVmTyD2i4ukkXOaVSVAA'

bgColor = 'lemon chiffon'
width, height = 310, 120
MailList = []
SavedTextList = []


class silusseuleo:
    def __init__(self):
        self.window = Tk()
        self.window.title('시루쓰러')
        self.window.geometry('1200x800')
        self.window.configure(background=bgColor)

        self.font = font.Font(self.window, size=20, weight='bold', family="메이플스토리")
        self.font2 = font.Font(self.window, size=18, weight='bold', family="메이플스토리")
        self.font3 = font.Font(self.window, size=16, weight='bold', family="메이플스토리")

        self.initLogo()  ## 지역화폐 시루 로고

        self.initMail()  ## 메일창

        self.initInputLabel()  ## 검색창
        self.initSearchButton()  ## 검색버튼
        self.initListBox()  ## 가맹점 리스트 박스
        self.initSavedTextDisplay()

        self.initGraphButton()

        self.initSaveTextButton()  # 정보 저장 버튼
        self.initInformation()  ## 정보창
        self.initMap()  ## 지도버튼

        self.window.mainloop()

    def initLogo(self):
        self.logoImage = PhotoImage(file='resources/logo.png')
        logo = Label(self.window, image=self.logoImage, background=bgColor)
        logo.place(x=25, y=5)

    def initMail(self):
        self.mailImage = PhotoImage(file='resources/gmail.png')
        self.mailButton = Button(self.window, cursor='heart', image=self.mailImage, bg=bgColor, command=self.sendMail)
        self.mailButton.place(x=1000, y=500)

    def sendMail(self):
        global MailList
        MailList = SavedTextList
        Gmail.sendMail(MailList)

    def initListBox(self):
        global Search
        ListScrollbar = Scrollbar(self.window)
        ListScrollbar.place(x=100, y=300)

        Search = Listbox(self.window, font=self.font3, activestyle='dotbox', width=35, height=20, bd=2,
                         cursor='heart', relief='ridge', fg='thistle4', selectbackground='thistle4',
                         yscrollcommand=ListScrollbar.set)

        for i in range(2000):
            Search.insert(i, SiluList.SiluList[i][0])

        Search.pack()
        Search.place(x=40, y=250)
        ListScrollbar.config(command=Search.yview)

        Search.bind("<ButtonRelease-1>", self.listbox_click_handler)

    def listbox_click_handler(self, event):
        global Search
        selected_index = Search.curselection()

        InfoText.configure(state='normal')
        InfoText.delete(1.0, END)

        if selected_index:
            selected_store_name = Search.get(selected_index)
            self.InsertInformation(selected_store_name)

    def initInputLabel(self):  #검색 창
        global InputLabel
        InputLabel = Entry(self.window, font=self.font, width=14, bd=2, relief='ridge', cursor='heart', fg='thistle4')
        InputLabel.pack()
        InputLabel.place(x=45, y=200)

    def initSearchButton(self):
        SearchButton = Button(self.window, font=self.font2, bg='lavender blush', text="검색", cursor='heart',
                              command=self.SearchButtonAction)
        SearchButton.pack()
        SearchButton.place(x=287, y=190)

    def SearchButtonAction(self):
        global InfoText, InputLabel
        InfoText.configure(state='normal')
        InfoText.delete(1.0, END)
        Store = InputLabel.get()
        self.InsertInformation(Store)

    def InsertEatery(self):
        global EateryText
        List = SiluList.getList()
        count = 1
        for i in range(len(List)):
            EateryText.insert(INSERT, "[")
            EateryText.insert(INSERT, count)
            EateryText.insert(INSERT, "] ")
            EateryText.insert(INSERT, List[i][0] + "\n\n")
            count += 1

    def InsertInformation(self, StoreName):
        global InfoText, Name, Lat, Long, MailList

        List = SiluList.getList()
        MailList.clear()

        for i in range(len(List)):
            for j in range(len(List[i])):
                if List[i][j] == None:
                    List[i][j] = ""
            if StoreName == List[i][0]:
                InfoText.insert(INSERT, "사업장명 : " + List[i][0] + "\n\n")
                InfoText.insert(INSERT, "도로명주소 : " + List[i][1] + "\n\n")
                InfoText.insert(INSERT, "지번주소 : " + List[i][2] + "\n\n")

                MailList.append("사업장명 : " + List[i][0])
                MailList.append("도로명주소 : " + List[i][1])
                MailList.append("지번주소 : " + List[i][2])

                Name = List[i][0]
                Lat = float(List[i][3])
                Long = float(List[i][4])

    def initInformation(self):  ## 가게의 정보를 알려주는 text box
        global InfoText
        InfoText = Text(self.window, width=40, height=10, borderwidth=2, relief='ridge', cursor='heart')
        InfoText.pack()
        InfoText.place(x=500, y=250)
        InfoText.configure(state='disabled')

    def initGraphButton(self):
        graphButton = Button(self.window, font=self.font2, bg='lavender blush', text='그래프',
                             command=self.graphButtonAction)
        graphButton.pack()
        graphButton.place(x=500, y=190)

    def graphButtonAction(self):
        graphCanvasWidth = 1000
        graphCanvasHeight = 1000
        codeList = []
        tempList = SiluList.getList()
        for i in range(len(tempList)):
            codeList.append(tempList[i][5])
        graphWindow = Toplevel(self.window, width=graphCanvasWidth, height=graphCanvasHeight)
        graphCanvas = Canvas(graphWindow, bg='lavender blush', width=graphCanvasWidth, height=graphCanvasHeight)
        graphCanvas.pack()
        graphCanvas.place(x=0, y=0)

        frequency = defaultdict(int)
        for code in codeList:
            frequency[code] += 1

        frequency = sortbykey.sort_key(frequency)

        margin = 50
        barWidth = 40
        max_height = graphCanvasHeight - 2*margin
        max_value = max(frequency.values())

        gap = (graphCanvasWidth - 2*margin)/len(frequency) - 50

        for i, (code, count) in enumerate(frequency.items()):
            x0 = margin + i*barWidth + gap
            y0 = graphCanvasHeight - margin
            x1 = x0 + barWidth
            y1 = y0 - (count/max_value) * max_height
            graphCanvas.create_rectangle(x0, y0, x1, y1, fill="red")
            graphCanvas.create_text(x0 + barWidth / 2, y0 + 10, text=code)
            graphCanvas.create_text(x0 + barWidth / 2, y1 - 10, text=str(count))

    def initMap(self):  # map 출력
        self.mapImage = PhotoImage(file='resources/map.png')
        self.mapButton = Button(self.window, cursor='heart', image=self.mapImage, bg=bgColor, command=self.openMap)
        self.mapButton.place(x=1000, y=630)

    def openMap(self):
        global Lat, Long
        mapWindow = Toplevel()
        mapWindow.title("google map")
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={Lat},{Long}&zoom=16&size=600x400&maptype=roadmap&markers=color:red|{Lat},{Long}&key={api_key}"

        im = requests.get(url)
        f = open("Map_Image.png", "wb")
        f.write(im.content)
        Image.mapImage('Map_Image.png', mapWindow)

        self.button_zoomin = Button(mapWindow, font=self.font2, text='로드뷰', command=self.openStreetview)
        self.button_zoomin.pack()
        self.button_zoomin.place(x=500, y=350)

    def openStreetview(self):
        global Lat, Long
        url = f"https://maps.googleapis.com/maps/api/streetview?location={Lat},{Long}&size={'800x600'}&key={api_key}"
        lView = requests.get(url)
        f = open("Load_View.png", "wb")
        f.write(lView.content)
        webbrowser.open_new("Load_View.png")

    def initSaveTextButton(self):  # 정보 저장 버튼
        SaveTextButton = Button(self.window, font=self.font2, bg='lavender blush', text="정보 저장", cursor='heart',
                                command=self.save_text)
        SaveTextButton.pack()
        SaveTextButton.place(x=365, y=190)

    def initSavedTextDisplay(self):
        global SavedTextDisplay
        SavedTextDisplay = Text(self.window, width=40, height=30, borderwidth=2, relief='ridge', cursor='heart')
        SavedTextDisplay.pack()
        SavedTextDisplay.place(x=500, y=400)
        SavedTextDisplay.configure(state='disabled')

    def save_text(self):
        global InfoText, SavedTextList, SavedTextDisplay
        new_text = InfoText.get(1.0, END).split("\n")
        grouped_text = []
        group = []
        for line in new_text:
            if line.startswith("사업장명") or line.startswith("도로명주소") or line.startswith("지번주소"):
                group.append(line)

        if group:  # 마지막 그룹 추가
            grouped_text.append(group)
        SavedTextList.extend(grouped_text)
        print("Text saved:", SavedTextList)

        # SavedTextDisplay에 정보 표시
        SavedTextDisplay.configure(state='normal')
        SavedTextDisplay.delete(1.0, END)
        for group in SavedTextList:
            for line in group:
                SavedTextDisplay.insert(END, line + "\n")
            SavedTextDisplay.insert(END, "\n")
        SavedTextDisplay.configure(state='disabled')


silusseuleo()
