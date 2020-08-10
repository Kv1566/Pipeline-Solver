#!/usr/bin/python
import tkinter as tk

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # 設定色彩固定常數
        self.CAN_MOVE_COLOR = '#99CC00'
        self.MOVE_NOMOVE_COLOR = '#00FF00'
        self.ROTATE_COLOR = '#FFFF00'
        self.MOVE2_CANMOVE_COLOR = '#660000'
        self.ROTATE_NOMOVE_COLOR = '#0000FF'
        #
        self.HAVE_ROAD_COLOR = 'red'
        self.START_COLOR = 'blue'
        self.END_COLOR = 'green'
        #
        # 初始化視窗
        self.parent.title("Pipeline Solver")
        #self.pack(fill="both", expand=True, side="top")
        self.parent.state('zoomed')
        self.parent.update()
        self.screenWidth  = self.parent.winfo_width()
        self.screenHeight = self.parent.winfo_height()
        #screenWidth = self.winfo_screenwidth()
        #screenHeight = self.winfo_screenheight()-60
        self.parent.state('normal')
        #
        # 關卡預設三顆星最大移動次數
        self.maxSteps = 5
        # 關卡預設行列數
        self.rows = 3
        self.cols = 3
        #
        # 建立"設定"窗格
        self.pwSetting = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.label = tk.Label(self.pwSetting, text='最大限定完成移動次數:')
        self.pwSetting.add(self.label)
        self.sv = tk.StringVar()
        self.sv.set(self.maxSteps) #default value
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.maxSteps_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.sv, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.label = tk.Label(self.pwSetting, text='格子列數:')
        self.pwSetting.add(self.label)
        self.sv = tk.StringVar()
        self.sv.set(self.rows) #default value
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.rows_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.sv, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.label = tk.Label(self.pwSetting, text='格子行數:')
        self.pwSetting.add(self.label)
        self.sv = tk.StringVar()
        self.sv.set(self.cols) #default value
        self.sv.trace("w", lambda name, index, mode, sv=self.sv: self.cols_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.sv, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.button = tk.Button(self.pwSetting, text='生成格子', command=self.cells_setting)
        self.pwSetting.add(self.button)
        #
        self.label = tk.Label(self.pwSetting, text='      ')
        self.pwSetting.add(self.label)
        #
        self.button = tk.Button(self.pwSetting, text='讀取')
        self.pwSetting.add(self.button)
        #
        self.button = tk.Button(self.pwSetting, text='存檔')
        self.pwSetting.add(self.button)
        #
        self.pwSetting.pack()
        #
        # 初始化變數
        self.cells = []
        self.frmCell = []
        self.btnUp=  []
        self.btnLeft= []
        self.btnRight = []
        self.btnDown = []
        self.btnCenter = []
        #
        # 建立棋盤窗格
        self.pwCells = tk.PanedWindow(orient=tk.VERTICAL)
        # 設定棋盤內各別子格
        self.cells_setting()
        #
        self.pwCells.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def maxSteps_changed(self, sv):
        #global maxSteps
        self.maxSteps = int(sv.get())

    def rows_changed(self, sv):
        #global rows
        try:
            self.rows = int(sv.get())
        except:
            self.rows = sv.get()

    def cols_changed(self, sv):
        #global cols
        try:
            self.cols = int(sv.get())
        except:
            self.cols = sv.get()

    def road_bgColor_change(self, p):
        if p.widget.config('bg')[-1] == self.HAVE_ROAD_COLOR:
            p.widget.config(bg = 'SystemButtonFace')
        else:
            p.widget.config(bg = self.HAVE_ROAD_COLOR)
            
    def center_bgColor_change(self, p):
        if p.widget.config('bg')[-1] == self.START_COLOR:
            p.widget.config(bg = self.END_COLOR)
        elif p.widget.config('bg')[-1] == self.END_COLOR:
            p.widget.config(bg = 'SystemButtonFace')        
        else:
            p.widget.config(bg = self.START_COLOR)        
    
    def frame_bgColor_change(self, p):
        if p.widget.config('bg')[-1] == self.CAN_MOVE_COLOR:
            p.widget.config(bg = self.MOVE_NOMOVE_COLOR)
        elif p.widget.config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
            p.widget.config(bg = self.ROTATE_COLOR)
        elif p.widget.config('bg')[-1] == self.ROTATE_COLOR:
            p.widget.config(bg = self.ROTATE_NOMOVE_COLOR)
        elif p.widget.config('bg')[-1] == self.ROTATE_NOMOVE_COLOR:
            p.widget.config(bg = self.MOVE2_CANMOVE_COLOR)
        elif p.widget.config('bg')[-1] == self.MOVE2_CANMOVE_COLOR:
            p.widget.config(bg = 'SystemButtonFace')
        else:
            p.widget.config(bg = self.CAN_MOVE_COLOR)
    
    def cells_setting(self):
        # 清除cells窗格中所有內容
        if len(self.pwCells.panes()) > 0:
            for widget in self.pwCells.winfo_children():
                widget.destroy()
            for pane in self.pwCells.panes():
                self.pwCells.remove(pane)
        
        if self.rows > 0 and self.cols > 0:
            w = max(145*self.cols+60, 500)
        else:
            w = 500
        h = 150*self.rows+150
        x = (self.screenWidth - w) / 2
        y = (self.screenHeight - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w,h,x,y))
        #root.overrideredirect(False)
        #
        self.cells = [[[] for x in range(self.rows)] for y in range(self.cols)]
        self.lstMoveGroup = []
        #
        self.btnMoveUp = [0 for x in range(self.cols)]
        self.frmCell = [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.btnUp=  [[0 for x in range(self.rows)] for y in range(self.cols)] 
        self.btnLeft= [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.btnRight = [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.btnDown = [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.btnCenter = [[0 for x in range(self.rows)] for y in range(self.cols)]
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150*self.cols, height=25)
        for j in range(self.cols):
            self.btnMoveUp[j] = tk.Button(self.pwInner, text='上', bg='pink', command=lambda text='上', n=j: self.btnMove(text,n))
            self.btnMoveUp[j].place(width=100, height=25, x=j*140+45, y=0)
        self.pwCells.add(self.pwInner)
        for i in range(self.rows):
            self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150, height=150)
            self.btn = tk.Button(self.pwInner, text='左', bg='pink', width=2, command=lambda text='左', n=i: self.btnMove(text,n))
            self.pwInner.add(self.btn)
            #pwInner = Frame(pwCells, width=300, height=150)
            for j in range(self.cols):
                self.frmCell[j][i] = tk.LabelFrame(self.pwInner, text=str(i) + "," + str(j), width=138, height=138)
                self.frmCell[j][i].bind('<Button-1>',self.frame_bgColor_change)
                #self.frmCell[j][i].grid(row=i, column=j)
                self.pwInner.add(self.frmCell[j][i])
                self.btnUp[j][i] = tk.Button(self.frmCell[j][i], text="", width=3, height=2) #, command= lambda x1=j, y1=i: up_color_change(x1,y1))
                self.btnUp[j][i].grid(row=0, column=1)
                self.btnUp[j][i].bind('<Button-1>', self.road_bgColor_change)
                self.btnLeft[j][i] = tk.Button(self.frmCell[j][i], text="", width=5, height=1)
                self.btnLeft[j][i].grid(row=1, column=0)
                self.btnLeft[j][i].bind('<Button-1>', self.road_bgColor_change)
                self.btnCenter[j][i] = tk.Button(self.frmCell[j][i], text="", width=4, height=2)
                self.btnCenter[j][i].grid(row=1, column=1)
                self.btnCenter[j][i].bind('<Button-1>', self.center_bgColor_change)
                self.btnRight[j][i] = tk.Button(self.frmCell[j][i], text="", width=5, height=1)
                self.btnRight[j][i].grid(row=1, column=2)
                self.btnRight[j][i].bind('<Button-1>', self.road_bgColor_change)
                self.btnDown[j][i] = tk.Button(self.frmCell[j][i], text="", width=3, height=2)
                self.btnDown[j][i].grid(row=2, column=1)
                self.btnDown[j][i].bind('<Button-1>', self.road_bgColor_change)
            self.btn = tk.Button(self.pwInner, text='右', width=2, bg='pink', command=lambda text='右', n=i: self.btnMove(text,n))
            self.pwInner.add(self.btn)
            self.pwCells.add(self.pwInner)
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150*self.cols, height=25)
        for j in range(self.cols):
            self.btn = tk.Button(self.pwInner, text='下', bg='pink', command=lambda text='下', n=j: self.btnMove(text,n))
            self.btn.place(width=100, height=25, x=j*140+45, y=0)
        self.pwCells.add(self.pwInner)
        #
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.btnSolve = tk.Button(self.pwInner, text='Solve', bg='yellow', command=self.solve)
        self.pwInner.add(self.btnSolve)
        self.pwCells.add(self.pwInner)

    def btnMove(self, text, n):
        self.getCells()
        lstGroup = self.getMovableGroup()
        if text == '上':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == False:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if y == n:
                            #print('up', n, lstGroup[i][2])
                            (y1, x1) = lstGroup[i][2][0]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            for k in range(len(lstGroup[i][2])-1):
                                (y1, x1) = lstGroup[i][2][k]
                                (y2, x2) = lstGroup[i][2][k+1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                            (y1, x1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)
            #for i in range(self.rows):
            #    for j in range(self.cols):
            #        print(self.cells[j][i])
        elif text == '左':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == True:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if y == n:
                            #print('up', n, lstGroup[i][2])
                            (y1, x1) = lstGroup[i][2][0]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            for k in range(len(lstGroup[i][2])-1):
                                (y1, x1) = lstGroup[i][2][k]
                                (y2, x2) = lstGroup[i][2][k+1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                            (y1, x1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)
        elif text == '下':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == False:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if y == n:
                            #print('up', n, lstGroup[i][2])
                            (y1, x1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            for k in range(len(lstGroup[i][2])-1, -1, -1):
                                (y1, x1) = lstGroup[i][2][k]
                                (y2, x2) = lstGroup[i][2][k-1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                            (y1, x1) = lstGroup[i][2][0]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)
        elif text == '右':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == True:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if y == n:
                            #print('up', n, lstGroup[i][2])
                            (y1, x1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            for k in range(len(lstGroup[i][2])-1, -1, -1):
                                (y1, x1) = lstGroup[i][2][k]
                                (y2, x2) = lstGroup[i][2][k-1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                            (y1, x1) = lstGroup[i][2][0]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)

    def solve(self):
        import pandas as pd
        df = pd.DataFrame(self.cells)
        #df.columns = [['up', 'right', 'down', 'left', 'start', 'end', 'canMove', 'move_noMove', 'rotate', 'move2_canMove']]
        # 以上為遊戲題目出題之視覺界面設定完成, 轉化出之df為出題結果之三維陣列
        # 接下去才開始進入解題, 解題程式尚未寫作
        #print(self.rows)
        #print(self.cols)
        self.lstGroup = self.getMovableGroup()
        self.move(0, self.cells)
        print(self.lstGroup)
        #print(df)
    
    def getCells(self):
        self.cells = [[[] for x in range(self.rows)] for y in range(self.cols)]
        for j in range(self.rows):
            for i in range(self.cols):
                if self.btnUp[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR:
                    self.cells[i][j].append(True)
                else:
                    self.cells[i][j].append(False)
                #
                if self.btnRight[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR:
                    self.cells[i][j].append(True)
                else:
                    self.cells[i][j].append(False)
                #
                if self.btnDown[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR:
                    self.cells[i][j].append(True)
                else:
                    self.cells[i][j].append(False)
                #
                if self.btnLeft[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR:
                    self.cells[i][j].append(True)
                else:
                    self.cells[i][j].append(False)
                #
                if self.btnCenter[i][j].config('bg')[-1] == self.START_COLOR:
                    self.cells[i][j].append(True)
                    self.cells[i][j].append(False)
                elif self.btnCenter[i][j].config('bg')[-1] == self.END_COLOR:
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(True)
                else:
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)
                #
                if self.frmCell[i][j].config('bg')[-1] == self.CAN_MOVE_COLOR:
                    self.cells[i][j].append(True) # initially movable
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)                
                elif self.frmCell[i][j].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                    self.cells[i][j].append(True) # initially movable
                    self.cells[i][j].append(True) # cannot move after move
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)                
                elif self.frmCell[i][j].config('bg')[-1] == self.ROTATE_COLOR:
                    self.cells[i][j].append(True) # initially movable
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(True) # will rotate when each move
                    self.cells[i][j].append(False)                
                elif self.frmCell[i][j].config('bg')[-1] == self.MOVE2_CANMOVE_COLOR:
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)                
                    self.cells[i][j].append(False)                
                    self.cells[i][j].append(True) # initially cannot move until totally 2 steps of move               
                else:
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)
                    self.cells[i][j].append(False)                
        
    def getMovableGroup(self):
        #for i in range(self.rows):
        #    for j in range(self.cols):
        #        print(self.cells[j][i])
        tmpGroupList = []
        # 先查橫向可移動群組, 找到的群組第一個欄位為橫縱向, 橫向為True; 第二個欄位為向左向右, 向右為True, 向左為False
        for i in range(self.rows):
            tmpList = []
            for j in range(self.cols):
                #print(self.cells[i][j])
                if self.cells[j][i][6] == True: # CanMove
                    tmpList.append(j)
                else:
                    cells = []
                    for k in range(len(tmpList)):
                        cells.append((i, tmpList[k]))
                    if len(cells) == 2:
                        tmpGroupList.append([True, True, cells])
                    elif len(cells) > 2:
                        tmpGroupList.append([True, True, cells])
                        tmpGroupList.append([True, False, cells])
                    tmpList = []
            if len(tmpList) > 0:
                cells = []
                for k in range(len(tmpList)):
                    cells.append((i, tmpList[k]))
                if len(cells) == 2:
                    tmpGroupList.append([True, True, cells])
                elif len(cells) > 2:
                    tmpGroupList.append([True, True, cells])
                    tmpGroupList.append([True, False, cells])
        # 先查縱向可移動群組, 找到的群組第一個欄位為橫縱向, 縱向為False; 第二個欄位為向上向下, 向下為True, 向上為False
        for j in range(self.cols):
            tmpList = []
            for i in range(self.rows):
                #print(self.cells[i][j])
                if self.cells[j][i][6] == True: # CanMove
                    tmpList.append(i)
                else:
                    cells = []
                    for k in range(len(tmpList)):
                        cells.append((tmpList[k], j))
                    if len(cells) == 2:
                        tmpGroupList.append([False, True, cells])
                    elif len(cells) > 2:
                        tmpGroupList.append([False, True, cells])
                        tmpGroupList.append([False, False, cells])
                    tmpList = []
            if len(tmpList) > 0:
                cells = []
                for k in range(len(tmpList)):
                    cells.append((tmpList[k], j))
                if len(cells) == 2:
                    tmpGroupList.append([False, True, cells])
                elif len(cells) > 2:
                    tmpGroupList.append([False, True, cells])
                    tmpGroupList.append([False, False, cells])
        #return
        return tmpGroupList
    
    def move(self, steps, cells):
        if steps == self.maxSteps:
            #print(self.cells)
            return
        self.thisMove()
        self.check()
        steps += 1
        self.move(steps, self.cells)
    
    def thisMove(self):
        return
    
    def check(self):
        return

if __name__ == "__main__":
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()