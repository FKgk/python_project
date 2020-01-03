## 미로 탐색 프로그램입니다.
실행 동영상 : https://youtu.be/RFMZ6xYdpGI
<br><br>
사용자는 미로를 직접 만들거나 불러올 수 있고, 경로 탐색을 통해 출구가 있는 지와 최단 거리를 알 수 있습니다.
경로 탐색한 뒤 자신이 지정한 예상 경로와 비교해 볼 수도 있습니다. 미로를 무작위로 생성하거나 저장할 수도 있습니다.

![시연 이미지](img1.PNG)
하늘색이 사용자가 표시한 경로이고, 파란색이 컴퓨터가 탐색한 경로 입니다.
컴퓨터는 A* 알고리즘으로 경로를 탐색합니다.

main 프로그램을 실행시키면 실행메뉴창과 pygame window 창이 나타납니다.
pygame window 창에서
사용자는 마우스 좌클릭으로 시작ㆍ종료 위치를 바꿀 수 있고, 벽을 만들거나 지울 수 있습니다.
사용자는 마우스 우클릭으로 자신이 생각한 예상 경로를 표시 할 수 있습니다.
실행메뉴에서
경로 탐색, 경로 표시 삭제, 벽 삭제, 예상 경로 삭제, 랜덤으로 미로 생성, 파일 저장 및 불러오기의 기능을 사용 할 수 있습니다.
경로탐색을 실행 시킬 경우 탐색 시간과 이동한 거리가 표시됩니다.

사용한 모듈과 패키지:
pygame, pygame.locals, sys, threading, tkinter, random, time


개발 기간 : 2018-05-01 ~ 2018-06-11 (1개월 11일)
개발 인원 : 1명
