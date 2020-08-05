CAN_MOVE = '#99CC00'
MOVE_NOMOVE = '#00FF00'
ROTATE = '#FFFF00'
MOVE2_CANMOVE = '#660000'
ROTATE_NOMOVE = '#0000FF'

HAVE_ROAD = 'red'
START_COLOR = 'blue'
END_COLOR = 'green'

def up_color_change(x,y):
    if btnUp[x][y].config('bg')[-1] == HAVE_ROAD:
        btnUp[x][y].config(bg = 'SystemButtonFace')
    else:
        btnUp[x][y].config(bg = HAVE_ROAD)
        
def road_bgColor_change(p):
    if p.widget.config('bg')[-1] == HAVE_ROAD:
        p.widget.config(bg = 'SystemButtonFace')
    else:
        p.widget.config(bg = HAVE_ROAD)
        
def center_bgColor_change(p):
    if p.widget.config('bg')[-1] == START_COLOR:
        p.widget.config(bg = END_COLOR)
    elif p.widget.config('bg')[-1] == END_COLOR:
        p.widget.config(bg = 'SystemButtonFace')        
    else:
        p.widget.config(bg = START_COLOR)        

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
            if btnUp[i][j].config('bg')[-1] == HAVE_ROAD:
                cells[i][j].append(True)
            else:
                cells[i][j].append(False)
            #
            if btnRight[i][j].config('bg')[-1] == HAVE_ROAD:
                cells[i][j].append(True)
            else:
                cells[i][j].append(False)
            #
            if btnDown[i][j].config('bg')[-1] == HAVE_ROAD:
                cells[i][j].append(True)
            else:
                cells[i][j].append(False)
            #
            if btnLeft[i][j].config('bg')[-1] == HAVE_ROAD:
                cells[i][j].append(True)
            else:
                cells[i][j].append(False)
            #
            if btnCenter[i][j].config('bg')[-1] == START_COLOR:
                cells[i][j].append(True)
                cells[i][j].append(False)
            elif btnCenter[i][j].config('bg')[-1] == END_COLOR:
                cells[i][j].append(False)
                cells[i][j].append(True)
            else:
                cells[i][j].append(False)
                cells[i][j].append(False)
            #
            if frmCell[i][j].config('bg')[-1] == CAN_MOVE:
                cells[i][j].append(True) # initially movable
                cells[i][j].append(False)
                cells[i][j].append(False)
                cells[i][j].append(False)                
            elif frmCell[i][j].config('bg')[-1] == MOVE_NOMOVE:
                cells[i][j].append(True) # initially movable
                cells[i][j].append(True) # cannot move after move
                cells[i][j].append(False)
                cells[i][j].append(False)                
            elif frmCell[i][j].config('bg')[-1] == ROTATE:
                cells[i][j].append(True) # initially movable
                cells[i][j].append(False)
                cells[i][j].append(True) # will rotate when each move
                cells[i][j].append(False)                
            elif frmCell[i][j].config('bg')[-1] == MOVE2_CANMOVE:
                cells[i][j].append(False)
                cells[i][j].append(False)                
                cells[i][j].append(False)                
                cells[i][j].append(True) # initially cannot move until totally 2 steps of move               
            else:
                cells[i][j].append(False)
                cells[i][j].append(False)
                cells[i][j].append(False)
                cells[i][j].append(False)                
    import pandas as pd
    df = pd.DataFrame(cells)
    #df.columns = [['up', 'right', 'down', 'left', 'start', 'end', 'canMove', 'move_noMove', 'rotate', 'move2_canMove']]
    # 以上為遊戲題目出題之視覺界面設定完成, 轉化出之df為出題結果之三維陣列
    # 接下去才開始進入解題, 解題程式尚未寫作
    print(rows)
    print(cols)
    print(df)
    getMovableGroup()
    move(0, cells)

def getMovableGroup():
    return

def move(steps, cells):
    if steps == maxSteps:
        print(cells)
        return
    thisMove()
    check()
    steps += 1
    move(steps, cells)

def thisMove():
    return

def check():
    return

def maxSteps_changed(sv):
    global maxSteps
    maxSteps = int(sv.get())

def rows_changed(sv):
    global rows
    try:
        rows = int(sv.get())
    except:
        rows = sv.get()

def cols_changed(sv):
    global cols
    try:
        cols = int(sv.get())
    except:
        cols = sv.get()
    
def cells_setting():
    global rows, cols, cells, frmCell, btnUp, btnLeft, btnRight, btnDown, btnCenter
    if len(pwCells.panes()) > 0:
        #print('before')
        #print(pwCells.winfo_children())
        for widget in pwCells.winfo_children():
            widget.destroy()
        for pane in pwCells.panes():
            #print(pane.winfo_children())
            pwCells.remove(pane)
        #print('after')
        #print(pwCells.winfo_children())

    if rows > 0 and cols > 0:
        w = max(143*cols+60, 500)
    else:
        w = 500
    h = 150*rows+150
    x = (screenWidth - w) / 2
    y = (screenHeight - h) / 2
    root.geometry('%dx%d+%d+%d' % (w,h,x,y))

    cells = [[[] for x in range(rows)] for y in range(cols)]

    frmCell = [[0 for x in range(rows)] for y in range(cols)]
    btnUp=  [[0 for x in range(rows)] for y in range(cols)] 
    btnLeft= [[0 for x in range(rows)] for y in range(cols)]
    btnRight = [[0 for x in range(rows)] for y in range(cols)]
    btnDown = [[0 for x in range(rows)] for y in range(cols)]
    btnCenter = [[0 for x in range(rows)] for y in range(cols)]
    pwInner = PanedWindow(orient=HORIZONTAL, width=150*cols)
    for j in range(cols):
        btn = Button(pwInner, text='上', width=21, height=1, padx=2)
        pwInner.add(btn)
    pwCells.add(pwInner)
    for i in range(rows):
        pwInner = PanedWindow(orient=HORIZONTAL, width=150, height=150)
        btn = Button(pwInner, text='左', width=2)
        pwInner.add(btn)
        #pwInner = Frame(pwCells, width=300, height=150)
        for j in range(cols):
            frmCell[j][i] = LabelFrame(pwInner, text=str(i) + "," + str(j), width=138, height=138)
            frmCell[j][i].bind('<Button-1>',frame_bgColor_change)
            #frmCell[j][i].grid(row=i, column=j)
            pwInner.add(frmCell[j][i])
            btnUp[j][i] = Button(frmCell[j][i], text="", width=3, height=2) #, command= lambda x1=j, y1=i: up_color_change(x1,y1))
            btnUp[j][i].grid(row=0, column=1)
            btnUp[j][i].bind('<Button-1>', road_bgColor_change)
            btnLeft[j][i] = Button(frmCell[j][i], text="", width=5, height=1)
            btnLeft[j][i].grid(row=1, column=0)
            btnLeft[j][i].bind('<Button-1>', road_bgColor_change)
            btnCenter[j][i] = Button(frmCell[j][i], text="", width=4, height=2)
            btnCenter[j][i].grid(row=1, column=1)
            btnCenter[j][i].bind('<Button-1>', center_bgColor_change)
            btnRight[j][i] = Button(frmCell[j][i], text="", width=5, height=1)
            btnRight[j][i].grid(row=1, column=2)
            btnRight[j][i].bind('<Button-1>', road_bgColor_change)
            btnDown[j][i] = Button(frmCell[j][i], text="", width=3, height=2)
            btnDown[j][i].grid(row=2, column=1)
            btnDown[j][i].bind('<Button-1>', road_bgColor_change)
        btn = Button(pwInner, text='右', width=2)
        pwInner.add(btn)
        pwCells.add(pwInner)
    pwInner = PanedWindow(orient=HORIZONTAL, width=150*cols)
    for j in range(cols):
        btn = Button(pwInner, text='下', width=21, height=1, padx=2)
        pwInner.add(btn)
    pwCells.add(pwInner)

    pwInner = PanedWindow(orient=HORIZONTAL)
    btnSolve = Button(pwInner, text='Solve', bg='yellow', command=solve)
    pwInner.add(btnSolve)
    pwCells.add(pwInner)

from tkinter import *

root = Tk()
root.title("test")

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

maxSteps = 5
rows = 3
cols = 3

pwSetting = PanedWindow(orient=HORIZONTAL)
label = Label(pwSetting, text='最大限定完成移動次數:')
pwSetting.add(label)
sv = StringVar()
sv.set(maxSteps) #default value
sv.trace("w", lambda name, index, mode, sv=sv: maxSteps_changed(sv))
entry = Entry(pwSetting, textvariable=sv, width=5)
pwSetting.add(entry)
#
label = Label(pwSetting, text='格子列數:')
pwSetting.add(label)
sv = StringVar()
sv.set(rows) #default value
sv.trace("w", lambda name, index, mode, sv=sv: rows_changed(sv))
entry = Entry(pwSetting, textvariable=sv, width=5)
pwSetting.add(entry)
#
label = Label(pwSetting, text='格子行數:')
pwSetting.add(label)
sv = StringVar()
sv.set(cols) #default value
sv.trace("w", lambda name, index, mode, sv=sv: cols_changed(sv))
entry = Entry(pwSetting, textvariable=sv, width=5)
pwSetting.add(entry)
#
button = Button(pwSetting, text='生成格子', command=cells_setting)
pwSetting.add(button)
#
pwSetting.pack()

cells = []
frmCell = []
btnUp=  []
btnLeft= []
btnRight = []
btnDown = []
btnCenter = []

pwCells = PanedWindow(orient=VERTICAL)

cells_setting()

pwCells.pack(fill=BOTH, expand=True, padx=10, pady=10)

root.mainloop()
