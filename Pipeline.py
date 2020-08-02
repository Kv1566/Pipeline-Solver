CAN_MOVE = '#99CC00'
MOVE_NOMOVE = '#00FF00'
ROTATE = '#FFFF00'
ROTATE_NOMOVE = '#0000FF'
MOVE2_CANMOVE = '#660000'

HAVE_ROAD = 'red'
START_COLOR = 'blue'
END_COLOR = 'green'

from tkinter import *

root = Tk()
root.title("test")

pw = PanedWindow(orient=VERTICAL)

def up_color_change(x,y):
    if btnUp[x][y].config('bg')[-1] == HAVE_ROAD:
        btnUp[x][y].config(bg = 'SystemButtonFace')
    else:
        btnUp[x][y].config(bg = HAVE_ROAD)
        
def bg_center_color_change(p):
    if p.widget.config('bg')[-1] == START_COLOR:
        p.widget.config(bg = END_COLOR)
    elif p.widget.config('bg')[-1] == END_COLOR:
        p.widget.config(bg = 'SystemButtonFace')        
    else:
        p.widget.config(bg = START_COLOR)        

def bg_color_change(p):
    if p.widget.config('bg')[-1] == HAVE_ROAD:
        p.widget.config(bg = 'SystemButtonFace')
    else:
        p.widget.config(bg = HAVE_ROAD)
        
def frame_bgColor_change(p):
    if p.widget.config('bg')[-1] == CAN_MOVE:
        p.widget.config(bg = MOVE_NOMOVE)
    elif p.widget.config('bg')[-1] == MOVE_NOMOVE:
        p.widget.config(bg = ROTATE)
    elif p.widget.config('bg')[-1] == ROTATE:
        p.widget.config(bg = ROTATE_NOMOVE)
    elif p.widget.config('bg')[-1] == ROTATE_NOMOVE:
        p.widget.config(bg = MOVE2_CANMOVE)
    elif p.widget.config('bg')[-1] == MOVE2_CANMOVE:
        p.widget.config(bg = 'SystemButtonFace')
    else:
        p.widget.config(bg = CAN_MOVE)

def solve():
    for j in range(ROW):
        for i in range(COL):
            thisCells = []
            #print(btnUp[j][i].config('bg')[-1])
            if btnUp[i][j].config('bg')[-1] == HAVE_ROAD:
                thisCells.append(True)
            else:
                thisCells.append(False)
            #
            if btnRight[i][j].config('bg')[-1] == HAVE_ROAD:
                thisCells.append(True)
            else:
                thisCells.append(False)
            #
            if btnDown[i][j].config('bg')[-1] == HAVE_ROAD:
                thisCells.append(True)
            else:
                thisCells.append(False)
            #
            if btnLeft[i][j].config('bg')[-1] == HAVE_ROAD:
                thisCells.append(True)
            else:
                thisCells.append(False)
            #
            if btnCenter[i][j].config('bg')[-1] == START_COLOR:
                thisCells.append(True)
                thisCells.append(False)
            elif btnCenter[i][j].config('bg')[-1] == END_COLOR:
                thisCells.append(False)
                thisCells.append(True)
            else:
                thisCells.append(False)
                thisCells.append(False)
            #
            if frmCell[i][j].config('bg')[-1] == CAN_MOVE:
                thisCells.append(True) # initially movable
                thisCells.append(False)
                thisCells.append(False)
                thisCells.append(False)                
            elif frmCell[i][j].config('bg')[-1] == MOVE_NOMOVE:
                thisCells.append(True) # initially movable
                thisCells.append(True) # cannot move after move
                thisCells.append(False)
                thisCells.append(False)                
            elif frmCell[i][j].config('bg')[-1] == ROTATE:
                thisCells.append(True) # initially movable
                thisCells.append(False)
                thisCells.append(True) # will rotate when each move
                thisCells.append(False)                
            elif frmCell[i][j].config('bg')[-1] == MOVE2_CANMOVE:
                thisCells.append(False)
                thisCells.append(False)                
                thisCells.append(False)                
                thisCells.append(True) # initially cannot move until totally 2 steps of move               
            else:
                thisCells.append(False)
                thisCells.append(False)
                thisCells.append(False)
                thisCells.append(False)                
            #
            cells[i][j] = thisCells
    import pandas as pd
    df = pd.DataFrame(cells)
    #df.columns = [['up', 'right', 'down', 'left', 'start', 'end', 'canMove', 'move_noMove', 'rotate', 'move2_canMove']]
    # 以上為遊戲題目出題之視覺界面設定完成, 轉化出之df為出題結果之三維陣列
    # 接下去才開始進入解題, 解題程式尚未寫作
    getMovableGroup()
    move(0, cells)

def getMovableGroup():
    return

def move(steps, cells):
    if steps == MAXSTEPS:
        print(cells)
        return
    thisMove()
    check()
    steps += 1
    #print(df)
    move(steps, cells)

def thisMove():
    return

def check():
    return

MAXSTEPS = 1

ROW = 3
COL = 3
cells = [[[] for x in range(ROW)] for y in range(COL)]

frmCell = [[0 for x in range(ROW)] for y in range(COL)]
btnUp=  [[0 for x in range(ROW)] for y in range(COL)] 
btnLeft= [[0 for x in range(ROW)] for y in range(COL)]
btnRight = [[0 for x in range(ROW)] for y in range(COL)]
btnDown = [[0 for x in range(ROW)] for y in range(COL)]
btnCenter = [[0 for x in range(ROW)] for y in range(COL)]
for i in range(ROW):
    pwInner = PanedWindow(orient=HORIZONTAL)
    for j in range(COL):
        frmCell[j][i] = LabelFrame(pwInner, text=str(i) + "," + str(j), width=80, height=40)
        frmCell[j][i].bind('<Button-1>',frame_bgColor_change)
        pwInner.add(frmCell[j][i])
        btnUp[j][i] = Button(frmCell[j][i], text="", width=3, height=2) #, command= lambda x1=j, y1=i: up_color_change(x1,y1))
        btnUp[j][i].grid(row=0, column=1)
        btnUp[j][i].bind('<Button-1>', bg_color_change)
        btnLeft[j][i] = Button(frmCell[j][i], text="", width=5, height=1)
        btnLeft[j][i].grid(row=1, column=0)
        btnLeft[j][i].bind('<Button-1>',bg_color_change)
        btnCenter[j][i] = Button(frmCell[j][i], text="", width=5, height=2)
        btnCenter[j][i].grid(row=1, column=1)
        btnCenter[j][i].bind('<Button-1>',bg_center_color_change)
        btnRight[j][i] = Button(frmCell[j][i], text="", width=5, height=1)
        btnRight[j][i].grid(row=1, column=2)
        btnRight[j][i].bind('<Button-1>',bg_color_change)
        btnDown[j][i] = Button(frmCell[j][i], text="", width=3, height=2)
        btnDown[j][i].grid(row=2, column=1)
        btnDown[j][i].bind('<Button-1>',bg_color_change)
    pw.add(pwInner)

btnSolve = Button(pw, text='Solve', bg='yellow', command=solve)
pw.add(btnSolve)

pw.pack(fill=BOTH, expand=True, padx=10, pady=10)

root.mainloop()