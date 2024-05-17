from tkinter import *
from tkinter import font
import SiluList
from tkinter import INSERT
import folium
import webbrowser
from googlemaps import Client

bgColor = 'lemon chiffon'
width, height = 310, 120
MailList = []

class silusseuleo :
    def __init__(self) :
        self.window = Tk()
        self.window.title('시루쓰러')
        self.window.geometry('1200x800')
        self.window.configure(background=bgColor)   

        self.font = font.Font(self.window, size=20, weight='bold', family="메이플스토리")
        self.font2 = font.Font(self.window, size=18, weight='bold', family="메이플스토리")
        self.font3 = font.Font(self.window, size=16, weight='bold', family="메이플스토리")

        self.initLogo() ## 지역화폐 시루 로고
        self.initMail() ## 메일창 

        self.initInputLabel() ## 검색창
        self.initSearchButton() ## 검색버튼
        self.initListBox() ## 가맹점 리스트 박스

        self.initInformation() ## 정보창
        self.initMap() ## 지도버튼

        self.window.mainloop()

    def initLogo(self):     
        self.logoImage = PhotoImage(file='resources/logo.png')
        logo = Label(self.window, image=self.logoImage, background=bgColor)
        logo.place(x=25, y=5)

    def initMail(self):
        self.mailImage = PhotoImage(file='resources/gmail.png')
        self.mailButton = Button(self.window, cursor='heart', image=self.mailImage, bg=bgColor) # command=self.sendMail
        self.mailButton.place(x=1000, y=500)

    def initListBox(self) :
        global Search
        ListScrollbar = Scrollbar(self.window)
        ListScrollbar.place(x=100 , y=300)

        Search = Listbox(self.window, font=self.font3, activestyle='dotbox', width=35, height=20, bd=2,
                             cursor='heart', relief='ridge', fg='thistle4', selectbackground='thistle4',
                         yscrollcommand=ListScrollbar.set)
        
        for i in range(2000) :
            Search.insert(i , SiluList.SiluList[i][0])

        Search.pack()
        Search.place(x=40 , y=250)
        ListScrollbar.config(command=Search.yview) 

    def initInputLabel(self):   #검색 창
        global InputLabel
        InputLabel = Entry(self.window, font=self.font, width=14, bd=2, relief='ridge', cursor='heart', fg='thistle4')
        InputLabel.pack()
        InputLabel.place(x=45, y=200)

    def initSearchButton(self):
        SearchButton = Button(self.window, font=self.font2, bg='lavender blush', text="검색", cursor='heart' , command=self.SearchButtonAction) 
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

    def InsertInformation(self , StoreName):
        global InfoText , Name , Lat , Long , MailList

        List = SiluList.getList()
        MailList.clear()

        for i in range(len(List)):
            for j in range(len(List[i])):
                if List[i][j] == None:
                    List[i][j] = ""
            if StoreName == List[i][0] :
                InfoText.insert(INSERT, "사업장명 : " + List[i][0] + "\n\n")
                InfoText.insert(INSERT, "도로명주소 : " + List[i][1] + "\n\n")
                InfoText.insert(INSERT, "지번주소 : " + List[i][2] + "\n\n")

                MailList.append("사업장명 : " + List[i][0])
                MailList.append("도로명주소 : " + List[i][1])
                MailList.append("지번주소 : " + List[i][2])

                Name = List[i][0]
                Lat = List[i][3]
                Long = List[i][4]

    def initInformation(self): ## 가게의 정보를 알려주는 text box
        global InfoText
        InfoText = Text(self.window, width=55, height=40, borderwidth=2, relief='ridge', cursor='heart')
        InfoText.pack()
        InfoText.place(x=500, y=250)
        InfoText.configure(state='disabled')

    def initMap(self): ## map 출력
        self.mapImage = PhotoImage(file='resources/map.png')
        self.mapButton = Button(self.window, cursor='heart', image=self.mapImage, bg=bgColor , command=self.openMap)
        self.mapButton.place(x=1000, y=630)

    def openMap(self):
        global Name, Lat, Long
        map = folium.Map(location=[Lat, Long], zoom_start=15)           # 위도, 경도 지정
        icon = folium.Icon(icon='glyphicon glyphicon-cutlery', color='pink')
        folium.Marker([Lat, Long], popup=Name, icon=icon).add_to(map)   # 마커 지정
        map.save('silusseuleo_MAP.html')                                  # html 파일로 저장
        webbrowser.open_new('silusseuleo_MAP.html')

silusseuleo()