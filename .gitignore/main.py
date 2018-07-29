import tkinter as tk
import threading
import Astar as MAP

from tkinter import filedialog
from tkinter import messagebox


def start(): # 경로 탐색
    #a= time.time()
    print('A* 경로 탐색 시작')
    MAP.PATHDELL()
    a = 0
    for i in range(500):
        search_time = MAP.search(MAP.map_point)
        a += search_time
    a = a / 100
    print("A* 시간 : " , a)
    print("A* 메모리 : ", MAP.memory)
    #app.time.config(text = "탐색 시간 : {0:0.5f}".format((time.time() -a)*100))
    app.time.config(text = "탐색 시간 : {0:0.10f}".format(a))
    d = MAP.draw_blue()
    app.distance.config(text = "이동한 거리 : " + str(d))
    
def start_dfs():
    print('DFS 경로 탐색 시작')
    MAP.PATHDELL()
    a = 0
    for i in range(500):
        search_time = MAP.search_dfs(MAP.map_point)
        a += search_time
    a = a / 100
    print("dfs 시간 : " , a)
    print("dfs 메모리 : ", MAP.memory)
    #app.time.config(text = "탐색 시간 : {0:0.5f}".format((time.time() -a)*100))
    app.time.config(text = "탐색 시간 : {0:0.10f}".format(a))
    d = MAP.draw_blue()
    app.distance.config(text = "이동한 거리 : " + str(d))
    
    
def start_bfs():
    print('BFS 경로 탐색 시작')
    MAP.PATHDELL()
    a = 0
    for i in range(500):
        search_time = MAP.search_bfs(MAP.map_point)
        a += search_time
    a = a / 100
    print("bfs 시간 : " , a)
    print("bfs 메모리 : ", MAP.memory)
    #app.time.config(text = "탐색 시간 : {0:0.5f}".format((time.time() -a)*100))
    app.time.config(text = "탐색 시간 : {0:0.10f}".format(a))
    d = MAP.draw_blue()
    app.distance.config(text = "이동한 거리 : " + str(d))

def PathDell(): # 경로 없애기
    print('경로 없애기 실행')
    MAP.PATHDELL()
def UPathDell():
    print('사용자 지정 경로 없애기')
    MAP.UPATHDELL()
def WallDell(): # 벽 없애기
    print('벽 없애기 실행')
    MAP.WALLDELL()
    
def RANDOM_MAP_CREATE(): # 랜덤 맵 생성
    print('랜덤 맵 생성')
    MAP.random_create_map()

def FILE_OPEN(): # 맵 열기
    global app
    try :
        filename = filedialog.askopenfilename(parent=app.window, filetypes= (("txt 파일", "*.txt"), ("모든 파일", "*.*")))
        f = open(filename, 'r')
        file = f.read()
        MAP.open_map(file) #파일 이름 보내기
        f.close()
        
    except FileNotFoundError : # 취소를 눌렸을 때 발생되는 에러
        #파일을 찾을 수 없으면 askopenfilename에서 찾을 수 없다고 알려준다.
        pass
    except EOFError :
        messagebox.showinfo("Error","데이터 값이 충분하지 않는 파일을 열였습니다.")
        MAP.pygame.display.flip()
    except TypeError :
        messagebox.showinfo("Error","데이터 타입이 잘못되었습니다.")
    except IndexError :
        messagebox.showinfo("Error","데이터 값이 충분하지 않거나 저장 방식이 다릅니다.")
        MAP.pygame.display.flip()
    except :
        MAP.pygame.display.flip()
        messagebox.showinfo("Error","Error가 발생했습니다.")

def FILE_SAVE(): # 맵 저장
    try:
        filename = filedialog.asksaveasfilename(parent = app.window, filetypes =(("txt 파일", "*.txt"), ("모든 파일", ".*") ),defaultextension=".txt")
        f = open(filename,'w')
        MAP.save_map(f)
        f.close()
    except: messagebox.showinfo("Error","Error가 발생했습니다.")

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.window.quit()

    def run(self):
        self.window = tk.Tk()
        #self.window.protocol("WM_DELETE_WINDOW", self.callback)
        self.window.title("실행 메뉴")
        self.window.geometry("240x160")
        self.window.resizable(0, 0)
        self.Start = tk.Button(self.window, text = "경로 탐색 A*", command = start, width = 13)
        self.DellPath = tk.Button(self.window, text = "경로 제거", command = PathDell, width = 13)
        self.DellWall = tk.Button(self.window, text = "벽 제거", command = WallDell, width = 13)
        self.DellUPath = tk.Button(self.window, text = "예상 경로 제거", command = UPathDell, width = 13)
        self.random_map_create = tk.Button(self.window, text = '랜덤 맵 생성', command = RANDOM_MAP_CREATE, width = 13)
        self.time = tk.Label(self.window, text = "탐색 시간 : ")
        self.distance = tk.Label(self.window, text = "이동한 거리 : ")
        self.start_dfs = tk.Button(self.window, text = "경로 탐색 dfs", command = start_dfs, width = 13)
        self.start_bfs = tk.Button(self.window, text = "경로 탐색 bfs", command = start_bfs, width = 13)
        # 파일 열기, 저장 메뉴
        mainMenu = tk.Menu(self.window)
        self.window.config(menu = mainMenu)
        fileMenu = tk.Menu(mainMenu, tearoff = 0)
        mainMenu.add_cascade(label = "파일", menu = fileMenu)
        fileMenu.add_command(label = "열기", command = FILE_OPEN)
        fileMenu.add_command(label = "저장", command = FILE_SAVE)

        self.DellPath.grid(row=0,column=0)
        self.Start.grid(row=0,column=1)
        self.DellWall.grid(row=1,column=0)
        self.random_map_create.grid(row=3,column=0)
        self.DellUPath.grid(row=2,column=0)
        self.start_dfs.grid(row=1,column=1)
        self.start_bfs.grid(row =2, column =1)
        self.time.grid(row=4,column=0)
        self.distance.grid(row=5,column=0)

        self.window.mainloop()


app = App()
print('길찾기 프로그램 실행')
MAP.map_start(MAP.map_point)
