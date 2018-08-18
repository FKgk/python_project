import pygame
import sys
from pygame.locals import *
import random as random
pygame.init()

class node():
        def __init__(self,value,point):
            self.point = point # 좌표
            self.value = value # 값 - 지날 수 있는 지 여부
            self.g = 0
            self.h = 0
            self.f = 0
            self.parent = None
        def get_g(self, g):
            self.g = g + 1
            self.f = self.g + self.h
        def get_h(self,end_node):
            self.h = abs(self.point[0] - end_node.point[0]) + abs(self.point[1] - end_node.point[1])

def save_map(f): # 맵 저장
        global file_number,map_point, start_node, end_node
        for i in range(30):
                for j in range(40):
                        f.write(str(map_point[i][j].value))
                f.write('\n')
        s = "%d %d"%(start_node.point[0],start_node.point[1])
        f.write(s)
        f.write('\n')
        s = "%d %d"%(end_node.point[0],end_node.point[1])
        f.write(s)
        
def open_map(file): # 맵 불러오기
        WALLDELL()
        PATHDELL()
        UPATHDELL()
        global map_point, start_node, end_node, WHITE, GRAY
        file_list = file.split()
        for i in range(30):
                list_number = file_list[i]
                for j in range(40):
                        if list_number[j] == '1':
                                map_point[i][j].value =1
                                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(map_point[i][j].point[1]*25 + 1), int(map_point[i][j].point[0]*25 + 1), 23, 23))
                        
                        if list_number[j] == '0':
                                list_GRAY.add(map_point[i][j])
                                map_point[i][j].value =0
                                pygame.draw.rect(ourScreen, GRAY, pygame.Rect(int(map_point[i][j].point[1]*25 + 1), int(map_point[i][j].point[0]*25 + 1), 23, 23))
        s = list()
        for i in range(30, 34):
                s.append(int(file_list[i]))
                
        start_node = map_point[s[0]][s[1]]
        if start_node in list_GRAY:
                list_GRAY.remove(start_node)
                start_mode.value = 1
        pygame.draw.rect(ourScreen, GREEN, pygame.Rect(int(start_node.point[1]*25 + 1), int(start_node.point[0]*25 + 1), 23, 23))

        end_node = map_point[s[2]][s[3]]
        if end_node in list_GRAY:
                list_GRAY.remove(end_node)
                end_mode.value = 1
        pygame.draw.rect(ourScreen, RED, pygame.Rect(int(end_node.point[1]*25 + 1), int(end_node.point[0]*25 + 1), 23, 23))
        pygame.display.flip()

def WALLDELL(): # 벽 없애기
        global list_GRAY,WHITE
        while list_GRAY:
                node = list_GRAY.pop()
                node.value = 1
                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(node.point[1]*25 + 1), int(node.point[0]*25 + 1), 23, 23))
        pygame.display.flip()
        
def PATHDELL(): # 경로 없애기
        global list_BLUE,WHITE
        while list_BLUE:
                node = list_BLUE.pop()
                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(node.point[1]*25 + 1), int(node.point[0]*25 + 1), 23, 23))
        pygame.display.flip()
        
def UPATHDELL(): #사용자 지정 경로 없애기
        global list_SKYBLUE, WHITE
        while list_SKYBLUE:
                node = list_SKYBLUE.pop()
                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(node.point[1]*25 + 1), int(node.point[0]*25 + 1), 23, 23))
        pygame.display.flip()
        
def node4(node, map_point): # 현재 노드로부터 주변 노드 반환
        global point_yp, point_xp
        point_y, point_x = node.point
        li = set()
        for i in range(4):
                current_y = point_y + point_yp[i]
                current_x = point_x + point_xp[i]
                if 0 <= current_y and current_y < 30 and 0 <= current_x and current_x < 40:
                        if map_point[current_y][current_x].value:
                                li.add(map_point[current_y][current_x])
        return li

def draw_blue(node): # 경로 그리기
        global list_BLUE, list_SKYBLUE
        if node in list_SKYBLUE:
                list_SKYBLUE.remove(node)
        list_BLUE.add(node)
        pygame.draw.rect(ourScreen, BLUE, pygame.Rect(int(node.point[1]*25 + 1), int(node.point[0]*25 + 1), 23, 23))

def search(map_point): # 맵 탐색
    global start_node,end_node
    open_list = set() # 지나야 할 노드
    close_list = set() # 지나온 노드
    
    current_node = start_node
    
    current_node.get_h(end_node)
    current_node.get_g(-1)
    open_list.add(current_node) # 현재노드를 열린 목록에 넣기

    while open_list:
        # open_list에 있는 노드 중 f값이 가장 작은 노드를 current_node에 대입
        current_node = min(open_list, key = lambda x: x.f)
        
        if current_node == end_node: # 목적 노드에 도달했을 때
            current_node = current_node.parent
            while  not current_node == start_node:
                draw_blue(current_node)
                current_node = current_node.parent
            pygame.display.flip()
            return 
        
        open_list.remove(current_node)
        close_list.add(current_node)
        
        for node in node4(current_node, map_point):
            if node in close_list: # 닫힌 목록에 있을 때
                    continue
            if node in open_list : # 열린 목록에 있을 때
                    if node.g > current_node.g + 1:
                        node.get_g(current_node.g)
                        node.parent = current_node
            else: #닫힌, 열린 목록에 없을 때
                node.get_h(end_node)
                node.get_g(current_node.g)
                node.parent = current_node
                open_list.add(node)
    else: print("경로를 찾지 못했습니다.")
        
def draw_ret(map_node): # 좌 클릭 할 때
    global cnt, list_GRAY, list_BLUE, list_SKYBLUE, start_node, end_node, drag
    
    if cnt == 0: 
        if map_node == start_node and drag < 2: # 시작 위치 일 때 
            cnt = 1
            
        elif map_node == end_node and drag < 2: # 종료 위치 일 때
            cnt = 2
            
        elif map_node.value == 1: # 길 일 때
            if drag == 1: drag = 2
            if map_node == start_node or map_node == end_node: return ;
            if drag == 2:
                if map_node in list_BLUE: # 이 길이 경로 일 때
                        list_BLUE.remove(map_node)
                if map_node in list_SKYBLUE:
                        list_SKYBLUE.remove(map_node)
                map_node.value = 0
                list_GRAY.add(map_node)
                pygame.draw.rect(ourScreen, GRAY, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))
                   
        elif map_node.value == 0: # 벽 일 때
            if drag == 1: drag = 3
            if map_node == start_node or map_node == end_node: return ;
            if drag == 3:
                map_node.value = 1
                list_GRAY.remove(map_node)
                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))

                    
    elif cnt == 1: # 시작 위치에서 드래그 할 때
        if map_node == end_node or map_node in list_GRAY: return ;
        if map_node in list_BLUE:
                list_BLUE.remove(map_node)
        if map_node in list_SKYBLUE:
                        list_SKYBLUE.remove(map_node)
        pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(start_node.point[1]*25 + 1), int(start_node.point[0]*25 + 1), 23, 23))
        start_node = map_node
        pygame.draw.rect(ourScreen, GREEN, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))

    elif cnt == 2: # 종료 위치에서 드래그 할 때
        if map_node == start_node or map_node in list_GRAY : return ;
        if map_node in list_BLUE:
                list_BLUE.remove(map_node)
        if map_node in list_SKYBLUE:
                        list_SKYBLUE.remove(map_node)
        pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(end_node.point[1]*25 + 1), int(end_node.point[0]*25 + 1), 23, 23))
        end_node = map_node
        pygame.draw.rect(ourScreen, RED, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))
    pygame.display.flip()
    
def draw_Uret(map_node):
        global list_GRAY, start_node, end_node, list_BLUE, list_SKYBLUE, SKYBLUE, WHITE
        if map_node in list_GRAY: return
        if map_node == start_node or map_node == end_node: return
        
        if cnt == -1:
                if map_node in list_BLUE: return
                if not map_node in list_SKYBLUE: return
                list_SKYBLUE.remove(map_node)
                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))

        elif cnt == -2:
                if map_node in list_BLUE: list_BLUE.remove(map_node)
                list_SKYBLUE.add(map_node)
                pygame.draw.rect(ourScreen, SKYBLUE, pygame.Rect(int(map_node.point[1]*25 + 1), int(map_node.point[0]*25 + 1), 23, 23))
        pygame.display.flip()
        
def random_create_map(): # 랜덤으로 맵 생성
        global list_GRAY, start_node, end_node, WHITE, GRAY
        WALLDELL()
        PATHDELL()
        UPATHDELL()
        for i in range(30):
                for j in range(40):
                        if map_point[i][j] == end_node or map_point[i][j] == start_node: continue

                        if random.randrange(0,4):
                                
                                map_point[i][j].value =1
                                pygame.draw.rect(ourScreen, WHITE, pygame.Rect(int(map_point[i][j].point[1]*25 + 1), int(map_point[i][j].point[0]*25 + 1), 23, 23))
                        else :
                                list_GRAY.add(map_point[i][j])
                                map_point[i][j].value =0
                                pygame.draw.rect(ourScreen, GRAY, pygame.Rect(int(map_point[i][j].point[1]*25 + 1), int(map_point[i][j].point[0]*25 + 1), 23, 23))
        pygame.display.flip()

# 함수에 쓰일 변수
list_GRAY = set() # 벽 위치 값
list_BLUE = set() # 경로 위치 값
list_SKYBLUE = set()
point_xp = (1,-1,0,0) # 현재 노드의 주변 노드 가져오기 위해
point_yp = (0,0,1,-1) # 현재 노드의 주변 노드 가져오기 위해
display_width = 1000 # 맵의 가로길이 : 40
display_height = 750 # 맵의 세로길이 : 30
WHITE = (255, 255, 255) # 길
BLACK = (0, 0, 0) # 줄
GRAY = (192, 192, 192) # 벽
GREEN = (0, 255, 0) # 시작 위치
RED = (255, 0, 0) # 종료 위치
BLUE = (0, 0, 255) # 이동 경로
SKYBLUE = (135, 206, 235) # 사용자가 표시한 경로
# 맵 생성
map_point = [[1]*int(display_width / 25) for i in range(int(display_height / 25))]
# 맵의 노드화
for i in range(int(display_height / 25)):
        for j in range(int(display_width / 25)):
            map_point[i][j] = node(map_point[i][j],[i,j])
ourScreen = pygame.display.set_mode((display_width, display_height))

# 맵 그리기
pygame.draw.rect(ourScreen, WHITE, pygame.Rect(0, 0, display_width, display_height))
for i in range(0, display_height + 1, 25):
    pygame.draw.line(ourScreen, BLACK, (0,i), (display_width, i), 1)
for j in range(0, display_width + 1, 25):
    pygame.draw.line(ourScreen, BLACK, (j,0), (j, display_height), 1)


# 시작위치, 종료 위치 표현
start_node = map_point[12][10] # 시작 노드
end_node = map_point[12][30] # 종료 노드
pygame.draw.rect(ourScreen, GREEN, pygame.Rect(10 * 25 + 1, 12 * 25 + 1, 23, 23))
pygame.draw.rect(ourScreen, RED, pygame.Rect(30 * 25 + 1, 12 * 25 + 1, 23, 23))
pygame.display.flip()

cnt = 0 # 0이면 길, 1 다음 시작위치, 2 다음 종료 위치
drag = 0 # drag 0이면 드래그 종료 1이면 드래그 중

def map_start(map_point):
    global drag, cnt
    LEFT = 1  # 왼쪽 버튼에 대한 버튼 인덱스
    RIGHT = 3  # 오른쪽 버튼에 대한 버튼 인덱스

    x, y = 0, 0
    while True:
        for event in pygame.event.get():
            pixelArray = pygame.PixelArray(ourScreen)
            if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
               # 마우스 왼쪽 버튼으로 드래그나 클릭을 시작
               drag = 1
               x, y= pygame.mouse.get_pos()
               x = int ((x - x % 25)/25)
               y = int ((y - y % 25)/25)
               draw_ret(map_point[y][x])
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                    # 마우스 오른쪽 버튼으로 드래그나 클릭을 시작
                    x, y= pygame.mouse.get_pos()
                    x = int ((x - x % 25)/25)
                    y = int ((y - y % 25)/25)
                    if map_point[y][x] in list_SKYBLUE: cnt = -1
                    else : cnt = -2
                    draw_Uret(map_point[y][x])
                    drag = -1
            elif event.type == MOUSEBUTTONUP:
                    # 마우스 버튼으로 드래그나 클릭을 종료
                    drag = 0
                    cnt = 0
            elif event.type == pygame.MOUSEMOTION:
                # 드래그 중
                if drag > 0:
                      sx, sy = pygame.mouse.get_pos()
                      sx = int ((sx - sx % 25)/25)
                      sy = int ((sy - sy % 25)/25)
                      if abs(x - sx) + abs(y - sy):
                          y,x = [sy,sx]
                          draw_ret(map_point[y][x])
                elif drag == -1:
                        sx, sy = pygame.mouse.get_pos()
                        sx = int ((sx - sx % 25)/25)
                        sy = int ((sy - sy % 25)/25)
                        if abs(x - sx) + abs(y - sy):
                          y,x = [sy,sx]
                          draw_Uret(map_point[y][x])
                          
            elif event.type == QUIT: # pygame 창 닫기
                pygame.quit()
                sys.exit()
