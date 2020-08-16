#!/usr/bin/python
import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import messagebox
import os
import copy
import threading, time

class cell():
    road = 0
    start = False
    end = False
    canMove = False
    moveNoMove = False
    rotate = False
    move2_canMove = False
    #rotateNoMove = False
    
    def __init__(self, road, start, end, canMove, moveNoMove, rotate, move2_canMove):
        self.road = 0
        self.start = start
        self.end = end
        self.canMove = canMove
        self.moveNoMove = moveNoMove
        self.rotate = rotate
        self.move2_canMove = move2_canMove
    
class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        # 設定色彩固定常數
        self.CAN_MOVE_COLOR = '#99CC00'
        self.MOVE_NOMOVE_COLOR = '#00FF00'
        self.ROTATE_COLOR = '#0000FF'
        self.MOVE2_CANMOVE_COLOR = '#FFFF00'
        self.ROTATE_NOMOVE_COLOR = '#660000'
        #
        self.HAVE_ROAD_COLOR = 'red'
        self.START_COLOR = 'blue'
        self.END_COLOR = 'green'
        self.isSuccess = False
        self.lstMoveSteps = []
        self.lstMoveStepsString = []
        self.timeStart = -1
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
        self.remainSteps = 5
        # 關卡預設行列數
        self.rows = 4
        self.cols = 4
        # 關卡中的起始位置(男生所在位置), 此變數是方便在判斷是否連接道路成功時(check函數)所需
        # 此變數將會在getCells函數裡被重新正確記錄
        self.start = [-1, -1]
        #
        # 建立"設定"窗格
        self.pwSetting = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.label = tk.Label(self.pwSetting, text='最大限定完成移動次數:')
        self.pwSetting.add(self.label)
        self.svMaxSteps = tk.StringVar()
        self.svMaxSteps.set(self.maxSteps) #default value
        self.svMaxSteps.trace("w", lambda name, index, mode, sv=self.svMaxSteps: self.maxSteps_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.svMaxSteps, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.label = tk.Label(self.pwSetting, text='格子列數:')
        self.pwSetting.add(self.label)
        self.svRows = tk.StringVar()
        self.svRows.set(self.rows) #default value
        self.svRows.trace("w", lambda name, index, mode, sv=self.svRows: self.rows_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.svRows, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.label = tk.Label(self.pwSetting, text='格子行數:')
        self.pwSetting.add(self.label)
        self.svCols = tk.StringVar()
        self.svCols.set(self.cols) #default value
        self.svCols.trace("w", lambda name, index, mode, sv=self.svCols: self.cols_changed(sv))
        self.entry = tk.Entry(self.pwSetting, textvariable=self.svCols, width=2, justify=tk.CENTER)
        self.pwSetting.add(self.entry)
        #
        self.button = tk.Button(self.pwSetting, text='生成格子', command=self.cells_setting)
        self.pwSetting.add(self.button)
        #
        self.label = tk.Label(self.pwSetting, text='      ')
        self.pwSetting.add(self.label)
        #
        self.button = tk.Button(self.pwSetting, text='讀取', command=self.readCellsFromFile)
        self.pwSetting.add(self.button)
        #
        self.button = tk.Button(self.pwSetting, text='存檔', command=self.saveCellsToFile)
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
    
    def saveCellsToFile(self):
        self.getCells()
        s = str(self.maxSteps) + ';\n' + str(self.rows) + ';\n' + str(self.cols) + ';\n'
        for i in range(self.rows):
            for j in range(self.cols):
                s += str(self.cells[i][j].road) + ',' \
                    + str(self.cells[i][j].start) + ',' \
                    + str(self.cells[i][j].end) + ',' \
                    + str(self.cells[i][j].canMove) + ',' \
                    + str(self.cells[i][j].moveNoMove) + ',' \
                    + str(self.cells[i][j].rotate) + ',' \
                    + str(self.cells[i][j].move2_canMove)
                s += '\n'
            s += '\n'
        currentPath = os.getcwd()
        csvPath = currentPath+'\\data\\'
        csvFile = 'test'
        ftypes = [('CSV files', '.csv'),
                      ('All files', '*')]
        if not os.path.exists(csvPath):
            os.mkdir(csvPath)
        csvFile = asksaveasfilename(initialdir=csvPath, filetypes=ftypes, defaultextension=".csv")
        #print(csvFile)
        with open(csvFile, 'w') as fileObj:
            fileObj.write(s)
    
    def readCellsFromFile(self):
        currentPath = os.getcwd()
        csvPath = currentPath+'\\data\\'
        ftypes = [('CSV files', '.csv'),
                      ('All files', '*')]
        csvFile = askopenfilename(initialdir=csvPath, filetypes=ftypes)
        with open(csvFile, 'r') as fileObj:
            s = fileObj.read()
        mainItems = s.split(';\n')
        self.maxSteps = int(mainItems[0])
        self.svMaxSteps.set(self.maxSteps) #default value
        self.maxSteps_changed(self.svMaxSteps)
        self.rows = int(mainItems[1])
        self.svRows.set(self.rows)
        self.rows_changed(self.svRows)
        self.cols = int(mainItems[2])
        self.svCols.set(self.cols)
        self.cols_changed(self.svCols)
        self.cells_setting()
        tmpRows = mainItems[3].split('\n\n')[:-1]
        #print(len(tmpRows))
        #print(tmpRows)
        #print()
        cells = []
        for row in tmpRows:
            cols = row.split('\n')
            cells.append(cols)
        for i in range(self.rows):
            for j in range(self.cols):
                items = cells[i][j].split(',')
                try:
                    if items[0] == 'True':
                        self.btnUp[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnUp[i][j].config(bg = 'SystemButtonFace')
                    if items[1] == 'True':
                        self.btnRight[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnRight[i][j].config(bg = 'SystemButtonFace')
                    if items[2] == 'True':
                        self.btnDown[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnDown[i][j].config(bg = 'SystemButtonFace')
                    if items[3] == 'True':
                        self.btnLeft[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnLeft[i][j].config(bg = 'SystemButtonFace')
                    if items[4] == 'True':
                        self.btnCenter[i][j].config(bg = self.START_COLOR)
                    elif items[5] == 'True':
                        self.btnCenter[i][j].config(bg = self.END_COLOR)
                    else:
                        self.btnCenter[i][j].config(bg = 'SystemButtonFace')
                    if items[7] == 'True':
                        self.frmCell[i][j].config(bg = self.MOVE_NOMOVE_COLOR)
                    elif items[8] == 'True':
                        self.frmCell[i][j].config(bg = self.ROTATE_COLOR)
                    elif items[9] == 'True':
                        self.frmCell[i][j].config(bg = self.MOVE2_CANMOVE_COLOR)
                    elif items[6] == 'True':
                        self.frmCell[i][j].config(bg = self.CAN_MOVE_COLOR)
                    else:
                        self.frmCell[i][j].config(bg = 'SystemButtonFace')
                except:
                    if int(items[0]) & 1 == 1:
                        self.btnUp[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnUp[i][j].config(bg = 'SystemButtonFace')
                    if int(items[0]) & 2 == 2:
                        self.btnRight[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnRight[i][j].config(bg = 'SystemButtonFace')
                    if int(items[0]) & 4 == 4:
                        self.btnDown[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnDown[i][j].config(bg = 'SystemButtonFace')
                    if int(items[0]) & 8 == 8:
                        self.btnLeft[i][j].config(bg = self.HAVE_ROAD_COLOR)
                    else:
                        self.btnLeft[i][j].config(bg = 'SystemButtonFace')
                    if items[1] == 'True':
                        self.btnCenter[i][j].config(bg = self.START_COLOR)
                    elif items[2] == 'True':
                        self.btnCenter[i][j].config(bg = self.END_COLOR)
                    else:
                        self.btnCenter[i][j].config(bg = 'SystemButtonFace')
                    if items[4] == 'True':
                        self.frmCell[i][j].config(bg = self.MOVE_NOMOVE_COLOR)
                    elif items[5] == 'True':
                        self.frmCell[i][j].config(bg = self.ROTATE_COLOR)
                    elif items[6] == 'True':
                        self.frmCell[i][j].config(bg = self.MOVE2_CANMOVE_COLOR)
                    elif items[3] == 'True':
                        self.frmCell[i][j].config(bg = self.CAN_MOVE_COLOR)
                    else:
                        self.frmCell[i][j].config(bg = 'SystemButtonFace')
        self.isSuccess = False
        self.lstMoveSteps = []
        self.lstMoveStepsString = []
 
    def maxSteps_changed(self, sv):
        #global maxSteps
        try:
            self.maxSteps = int(sv.get())
        except:
            self.maxSteps = sv.get()
        try:
            self.remainSteps = int(sv.get())
        except:
            self.remainSteps = sv.get()
    
    def remainSteps_changed(self, sv):
        try:
            self.remainSteps = int(sv.get())
        except:
            self.remainSteps = sv.get()

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
            p.widget.config(bg = self.MOVE2_CANMOVE_COLOR)
        elif p.widget.config('bg')[-1] == self.MOVE2_CANMOVE_COLOR:
            p.widget.config(bg = self.ROTATE_NOMOVE_COLOR)
        elif p.widget.config('bg')[-1] == self.ROTATE_NOMOVE_COLOR:
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
        self.cells = [[cell for y in range(self.cols)] for x in range(self.rows)]
        self.lstMoveGroup = []
        #
        self.btnMoveUp = [0 for y in range(self.cols)]
        self.frmCell = [[0 for y in range(self.cols)] for x in range(self.rows)]
        self.btnUp=  [[0 for y in range(self.cols)] for x in range(self.rows)] 
        self.btnLeft= [[0 for y in range(self.cols)] for x in range(self.rows)]
        self.btnRight = [[0 for y in range(self.cols)] for x in range(self.rows)]
        self.btnDown = [[0 for y in range(self.cols)] for x in range(self.rows)]
        self.btnCenter = [[0 for y in range(self.cols)] for x in range(self.rows)]
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150*self.rows, height=25)
        for j in range(self.cols):
            self.btnMoveUp[j] = tk.Button(self.pwInner, text='上', bg='pink', command=lambda text='上', n=j: self.btnMove(text,n))
            self.btnMoveUp[j].place(width=80, height=25, x=j*140+60, y=0)
        self.pwCells.add(self.pwInner)
        for i in range(self.rows):
            self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150, height=150)
            self.btn = tk.Button(self.pwInner, text='左', bg='pink', width=2, command=lambda text='左', n=i: self.btnMove(text,n))
            self.pwInner.add(self.btn)
            #pwInner = Frame(pwCells, width=300, height=150)
            for j in range(self.cols):
                self.frmCell[i][j] = tk.LabelFrame(self.pwInner, text=str(i) + "," + str(j), width=138, height=138)
                self.frmCell[i][j].bind('<Button-1>',self.frame_bgColor_change)
                #self.frmCell[i][j].grid(row=i, column=j)
                self.pwInner.add(self.frmCell[i][j])
                self.btnUp[i][j] = tk.Button(self.frmCell[i][j], text="", width=3, height=2) #, command= lambda x1=j, y1=i: up_color_change(x1,y1))
                self.btnUp[i][j].grid(row=0, column=1)
                self.btnUp[i][j].bind('<Button-1>', self.road_bgColor_change)
                self.btnLeft[i][j] = tk.Button(self.frmCell[i][j], text="", width=5, height=1)
                self.btnLeft[i][j].grid(row=1, column=0)
                self.btnLeft[i][j].bind('<Button-1>', self.road_bgColor_change)
                self.btnCenter[i][j] = tk.Button(self.frmCell[i][j], text="", width=4, height=2)
                self.btnCenter[i][j].grid(row=1, column=1)
                self.btnCenter[i][j].bind('<Button-1>', self.center_bgColor_change)
                self.btnRight[i][j] = tk.Button(self.frmCell[i][j], text="", width=5, height=1)
                self.btnRight[i][j].grid(row=1, column=2)
                self.btnRight[i][j].bind('<Button-1>', self.road_bgColor_change)
                self.btnDown[i][j] = tk.Button(self.frmCell[i][j], text="", width=3, height=2)
                self.btnDown[i][j].grid(row=2, column=1)
                self.btnDown[i][j].bind('<Button-1>', self.road_bgColor_change)
            self.btn = tk.Button(self.pwInner, text='右', width=2, bg='pink', command=lambda text='右', n=i: self.btnMove(text,n))
            self.pwInner.add(self.btn)
            self.pwCells.add(self.pwInner)
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL, width=150*self.cols, height=25)
        for j in range(self.cols):
            self.btn = tk.Button(self.pwInner, text='下', bg='pink', command=lambda text='下', n=j: self.btnMove(text,n))
            self.btn.place(width=80, height=25, x=j*140+60, y=0)
        self.pwCells.add(self.pwInner)
        #
        self.pwInner = tk.PanedWindow(orient=tk.HORIZONTAL)
        self.label = tk.Label(self.pwInner, text='餘次:')
        self.pwInner.add(self.label)
        self.svRemainSteps = tk.StringVar()
        self.svRemainSteps.set(self.remainSteps) #default value
        self.svRemainSteps.trace("w", lambda name, index, mode, sv=self.svRemainSteps: self.remainSteps_changed(sv))
        self.entry = tk.Entry(self.pwInner, textvariable=self.svRemainSteps, width=2, justify=tk.CENTER)
        self.pwInner.add(self.entry)
        self.btnSolve = tk.Button(self.pwInner, text='Solve', bg='yellow', command=self.solve)
        self.pwInner.add(self.btnSolve)
        self.pwCells.add(self.pwInner)

    def btnMove(self, text, n):
        self.getCells()
        lstGroup = self.getMovableGroup(self.cells)
        if text == '上':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == False:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if y == n:
                            #print('up', n, lstGroup[i][2])
                            (x1, y1) = lstGroup[i][2][0]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1] 
                            tmpFrmCell = self.frmCell[x1][y1].config('bg')[-1]
                            for k in range(len(lstGroup[i][2])-1):
                                (x1, y1) = lstGroup[i][2][k]
                                (x2, y2) = lstGroup[i][2][k+1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                                self.frmCell[x1][y1].config(bg = self.frmCell[x2][y2].config('bg')[-1])
                                if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                    self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                                elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                    tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                    self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                    self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                    self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                    self.btnLeft[x1][y1].config(bg = tmpBg)
                            (x1, y1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            self.frmCell[x1][y1].config(bg = tmpFrmCell)
                            if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                            elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = tmpBg)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)
            #for i in range(self.rows):
            #    for j in range(self.cols):
            #        print(self.cells[i][j].up, self.cells[i][j].right, self.cells[i][j].down, self.cells[i][j].left, 
            #              self.cells[i][j].start, self.cells[i][j].end, self.cells[i][j].canMove,
            #             self.cells[i][j].moveNoMove, self.cells[i][j].rotate, self.cells[i][j].move2_canMove)
        elif text == '左':
            isFound = False
            for i in range(len(lstGroup)):
                if lstGroup[i][0] == True:
                    for j in range(len(lstGroup[i][2])):
                        (x, y) = lstGroup[i][2][j]
                        if x == n:
                            #print('up', n, lstGroup[i][2])
                            (x1, y1) = lstGroup[i][2][0]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            tmpFrmCell = self.frmCell[x1][y1].config('bg')[-1]
                            for k in range(len(lstGroup[i][2])-1):
                                (x1, y1) = lstGroup[i][2][k]
                                (x2, y2) = lstGroup[i][2][k+1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                                self.frmCell[x1][y1].config(bg = self.frmCell[x2][y2].config('bg')[-1])
                                if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                    self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                                elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                    tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                    self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                    self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                    self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                    self.btnLeft[x1][y1].config(bg = tmpBg)
                            (x1, y1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            self.frmCell[x1][y1].config(bg = tmpFrmCell)
                            if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                            elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = tmpBg)
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
                            (x1, y1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            tmpFrmCell = self.frmCell[x1][y1].config('bg')[-1]
                            for k in range(len(lstGroup[i][2])-1, -1, -1):
                                (x1, y1) = lstGroup[i][2][k]
                                (x2, y2) = lstGroup[i][2][k-1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                                self.frmCell[x1][y1].config(bg = self.frmCell[x2][y2].config('bg')[-1])
                                if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                    self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                                elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                    tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                    self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                    self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                    self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                    self.btnLeft[x1][y1].config(bg = tmpBg)
                            (x1, y1) = lstGroup[i][2][0]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            self.frmCell[x1][y1].config(bg = tmpFrmCell)
                            if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                            elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = tmpBg)
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
                        if x == n:
                            #print('up', n, lstGroup[i][2])
                            (x1, y1) = lstGroup[i][2][len(lstGroup[i][2])-1]
                            tmpUp = self.btnUp[x1][y1].config('bg')[-1]
                            tmpRight = self.btnRight[x1][y1].config('bg')[-1]
                            tmpDown = self.btnDown[x1][y1].config('bg')[-1]
                            tmpLeft = self.btnLeft[x1][y1].config('bg')[-1]
                            tmpCenter = self.btnCenter[x1][y1].config('bg')[-1]                            
                            tmpFrmCell = self.frmCell[x1][y1].config('bg')[-1]
                            for k in range(len(lstGroup[i][2])-1, -1, -1):
                                (x1, y1) = lstGroup[i][2][k]
                                (x2, y2) = lstGroup[i][2][k-1]
                                (self.cells[x1][y1], self.cells[x2][y2]) = (self.cells[x2][y2], self.cells[x1][y1])
                                #(self.btnUp[x1][y1], self.btnUp[x2][y2]) = (self.btnUp[x2][y2], self.btnUp[x1][y1])
                                self.btnUp[x1][y1].config(bg = self.btnUp[x2][y2].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnRight[x2][y2].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnDown[x2][y2].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = self.btnLeft[x2][y2].config('bg')[-1])
                                self.btnCenter[x1][y1].config(bg = self.btnCenter[x2][y2].config('bg')[-1])
                                self.frmCell[x1][y1].config(bg = self.frmCell[x2][y2].config('bg')[-1])
                                if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                    self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                                elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                    tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                    self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                    self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                    self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                    self.btnLeft[x1][y1].config(bg = tmpBg)
                            (x1, y1) = lstGroup[i][2][0]
                            self.btnUp[x1][y1].config(bg = tmpUp)
                            self.btnRight[x1][y1].config(bg = tmpRight)
                            self.btnDown[x1][y1].config(bg = tmpDown)
                            self.btnLeft[x1][y1].config(bg = tmpLeft)
                            self.btnCenter[x1][y1].config(bg = tmpCenter)
                            self.frmCell[x1][y1].config(bg = tmpFrmCell)
                            if self.frmCell[x1][y1].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                                self.frmCell[x1][y1].config(bg = 'SystemButtonFace')
                            elif self.frmCell[x1][y1].config('bg')[-1] == self.ROTATE_COLOR:
                                tmpBg = self.btnUp[x1][y1].config('bg')[-1]
                                self.btnUp[x1][y1].config(bg = self.btnRight[x1][y1].config('bg')[-1])
                                self.btnRight[x1][y1].config(bg = self.btnDown[x1][y1].config('bg')[-1])
                                self.btnDown[x1][y1].config(bg = self.btnLeft[x1][y1].config('bg')[-1])
                                self.btnLeft[x1][y1].config(bg = tmpBg)
                            isFound = True
                            break
                if isFound:
                    break
            #print(text, n)
        self.remainSteps -= 1
        self.svRemainSteps.set(self.remainSteps)
        self.remainSteps_changed(self.svRemainSteps)
        #
        self.getCells()
        isSuccess = self.check(self.cells)
        if isSuccess:
            (i, j) = self.start
            #print('start', i, j)
            if self.cells[i][j].road == 1:
                preRoad = 1
                i -= 1
            elif self.cells[i][j].road == 2:
                preRoad = 2
                j += 1
            elif self.cells[i][j].road == 4:
                preRoad = 4
                i += 1
            elif self.cells[i][j].road == 8:
                preRoad = 8
                j -= 1
            while(True):
                if self.cells[i][j].end == True:
                    break
                self.btnCenter[i][j].config(bg = 'red')
                if self.cells[i][j].road == (preRoad * 4 % 15 + preRoad) % 15:
                    preRoad = self.cells[i][j].road - preRoad * 4 % 15
                elif self.cells[i][j].road == (preRoad * 4 % 15 + preRoad * 2 % 15) % 15:
                    preRoad = self.cells[i][j].road - preRoad * 4 % 15
                elif self.cells[i][j].road == (preRoad * 4 % 15 + preRoad * 8 % 15) % 15:
                    preRoad = self.cells[i][j].road - preRoad * 4 % 15
                else:
                    break
                if preRoad == 1:
                    i -= 1
                elif preRoad == 2:
                    j += 1
                elif preRoad == 4:
                    i += 1
                elif preRoad == 8:
                    j -= 1
            messagebox.showinfo('完成', '恭禧！你成功了！')
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.btnCenter[i][j].config('bg')[-1] == 'red':
                        self.btnCenter[i][j].config(bg = 'SystemButtonFace')
        if self.maxSteps-self.remainSteps >= 2:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.frmCell[i][j].config('bg')[-1] == self.MOVE2_CANMOVE_COLOR:
                        self.frmCell[i][j].config(bg = self.CAN＿MOVE_COLOR)
        #print()
        #for i in range(self.rows):
        #    for j in range(self.cols):
        #        print(self.cells[i][j].up, self.cells[i][j].right, self.cells[i][j].down, self.cells[i][j].left, 
        #              self.cells[i][j].start, self.cells[i][j].end, self.cells[i][j].canMove,
        #             self.cells[i][j].moveNoMove, self.cells[i][j].rotate, self.cells[i][j].move2_canMove)

    def getCells(self):
        self.cells = []
        for i in range(self.rows):
            self.cells.append([])
            for j in range(self.cols):
                self.cells[i].append(cell(0, False, False, False, False, False, False))
                #
                self.cells[i][j].road = int(self.btnLeft[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)*8 \
                                    + int(self.btnDown[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)*4 \
                                    + int(self.btnRight[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)*2 \
                                    + int(self.btnUp[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)
                #self.cells[i][j].up = (self.btnUp[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)
                #self.cells[i][j].right = (self.btnRight[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)
                #self.cells[i][j].down = (self.btnDown[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)
                #self.cells[i][j].left = (self.btnLeft[i][j].config('bg')[-1] == self.HAVE_ROAD_COLOR)
                #
                if self.btnCenter[i][j].config('bg')[-1] == self.START_COLOR:
                    self.cells[i][j].start = True
                    self.cells[i][j].end = False
                    self.start = [i, j]
                elif self.btnCenter[i][j].config('bg')[-1] == self.END_COLOR:
                    self.cells[i][j].start = False
                    self.cells[i][j].end = True
                else:
                    self.cells[i][j].start = False
                    self.cells[i][j].end = False
                #
                #(self.cells[i][j].start, self.cells[i][j].end) = \
                #    (self.btnCenter[i][j].config('bg')[-1] == self.START_COLOR, \
                #     self.btnCenter[i][j].config('bg')[-1] == self.END_COLOR)
                #
                if self.frmCell[i][j].config('bg')[-1] == self.CAN_MOVE_COLOR:
                    self.cells[i][j].canMove = True
                    self.cells[i][j].moveNoMove = False
                    self.cells[i][j].rotate = False
                    self.cells[i][j].move2_canMove = False
                elif self.frmCell[i][j].config('bg')[-1] == self.MOVE_NOMOVE_COLOR:
                    self.cells[i][j].canMove = True
                    self.cells[i][j].moveNoMove = True
                    self.cells[i][j].rotate = False
                    self.cells[i][j].move2_canMove = False
                elif self.frmCell[i][j].config('bg')[-1] == self.ROTATE_COLOR:
                    self.cells[i][j].canMove = True
                    self.cells[i][j].moveNoMove = False
                    self.cells[i][j].rotate = True
                    self.cells[i][j].move2_canMove = False
                elif self.frmCell[i][j].config('bg')[-1] == self.MOVE2_CANMOVE_COLOR:
                    self.cells[i][j].canMove = False
                    self.cells[i][j].moveNoMove = False
                    self.cells[i][j].rotate = False
                    self.cells[i][j].move2_canMove = True
                else:
                    self.cells[i][j].canMove = False
                    self.cells[i][j].moveNoMove = False
                    self.cells[i][j].rotate = False
                    self.cells[i][j].move2_canMove = False
        #for i in range(self.rows):
        #    for j in range(self.cols):
        #        print(self.cells[i][j].up, self.cells[i][j].right, self.cells[i][j].down, self.cells[i][j].left, 
        #              self.cells[i][j].start, self.cells[i][j].end, self.cells[i][j].canMove,
        #             self.cells[i][j].moveNoMove, self.cells[i][j].rotate, self.cells[i][j].move2_canMove)
        
    def getMovableGroup(self, cells):
        #print('----getMovableGroup start----')
        #for i in range(self.rows):
        #    for j in range(self.cols):
        #        print(cells[i][j].up, cells[i][j].right, cells[i][j].down, cells[i][j].left, 
        #              cells[i][j].start, cells[i][j].end, cells[i][j].canMove,
        #             cells[i][j].moveNoMove, cells[i][j].rotate, cells[i][j].move2_canMove)
        tmpGroupList = []
        # 先查橫向可移動群組, 找到的群組第一個欄位為橫縱向, 橫向為True; 第二個欄位為向左向右, 向右為True, 向左為False
        for i in range(self.rows):
            tmpList = []
            for j in range(self.cols):
                #print(cells[i][j])
                #if len(cells[i][j]) == 0:
                #    continue
                if cells[i][j].canMove: # CanMove
                    tmpList.append(j)
                else:
                    thisCells = []
                    for k in range(len(tmpList)):
                        thisCells.append((i, tmpList[k]))
                    if len(thisCells) == 2:
                        tmpGroupList.append([True, True, thisCells])
                    elif len(thisCells) > 2:
                        tmpGroupList.append([True, True, thisCells])
                        tmpGroupList.append([True, False, thisCells])
                    tmpList = []
            if len(tmpList) > 0:
                thisCells = []
                for k in range(len(tmpList)):
                    thisCells.append((i, tmpList[k]))
                if len(thisCells) == 2:
                    tmpGroupList.append([True, True, thisCells])
                elif len(thisCells) > 2:
                    tmpGroupList.append([True, True, thisCells])
                    tmpGroupList.append([True, False, thisCells])
                tmpList = []
        # 先查縱向可移動群組, 找到的群組第一個欄位為橫縱向, 縱向為False; 第二個欄位為向上向下, 向下為True, 向上為False
        for j in range(self.cols):
            tmpList = []
            for i in range(self.rows):
                #print(cells[i][j])
                #if len(cells[i][j]) == 0:
                #    continue
                if cells[i][j].canMove: # CanMove
                    tmpList.append(i)
                else:
                    thisCells = []
                    for k in range(len(tmpList)):
                        thisCells.append((tmpList[k], j))
                    if len(thisCells) == 2:
                        tmpGroupList.append([False, True, thisCells])
                    elif len(thisCells) > 2:
                        tmpGroupList.append([False, True, thisCells])
                        tmpGroupList.append([False, False, thisCells])
                    tmpList = []
            if len(tmpList) > 0:
                thisCells = []
                for k in range(len(tmpList)):
                    thisCells.append((tmpList[k], j))
                if len(thisCells) == 2:
                    tmpGroupList.append([False, True, thisCells])
                elif len(thisCells) > 2:
                    tmpGroupList.append([False, True, thisCells])
                    tmpGroupList.append([False, False, thisCells])
                tmpList = []
        #return
        #print(tmpGroupList)
        #print('----end----')
        return tmpGroupList
    
    def solve(self):
        self.timeStart = time.time()
        #import pandas as pd
        #df = pd.DataFrame(self.cells)
        #df.columns = [['up', 'right', 'down', 'left', 'start', 'end', 'canMove', 'move_noMove', 'rotate', 'move2_canMove']]
        # 以上為遊戲題目出題之視覺界面設定完成, 轉化出之df為出題結果之三維陣列
        # 接下去才開始進入解題, 解題程式尚未寫作
        #print(self.rows)
        #print(self.cols)
        self.getCells()
        self.lstGroup = self.getMovableGroup(self.cells)
        #print(len(self.lstGroup))
        self.times = 0
        self.move(0, self.cells, self.lstGroup)
        #print(self.lstGroup)
        #print(df)
    
    def move(self, steps, cells, lstGroup):
        for i in range(len(lstGroup)):
            if steps >= self.maxSteps:
                return
            if self.isSuccess:
                #print('1------')
                #for x in range(self.rows):
                #    for y in range(self.cols):
                #        print(cells[x][y].up, cells[x][y].right, cells[x][y].down, cells[x][y].left, 
                #              cells[x][y].start, cells[x][y].end, cells[x][y].canMove,
                #             cells[x][y].moveNoMove, cells[x][y].rotate, cells[x][y].move2_canMove)
                return
            if len(self.lstMoveSteps) > 0:
                if (lstGroup[i] == self.lstMoveSteps[-1]) and (len(lstGroup[i][2]) < 3):
                    continue
                elif (lstGroup[i][2] == self.lstMoveSteps[-1][2]) \
                    and (lstGroup[i][0] == self.lstMoveSteps[-1][0]) \
                    and (lstGroup[i][1] != self.lstMoveSteps[-1][1]):
                    continue
            preCells = copy.deepcopy(cells)
            preLstGroup = copy.deepcopy(lstGroup)
            #print(self.times, i)
            #for x in range(self.rows):
            #    for y in range(self.cols):
            #        print(cells[x][y].up, cells[x][y].right, cells[x][y].down, cells[x][y].left, 
            #              cells[x][y].start, cells[x][y].end, cells[x][y].canMove,
            #             cells[x][y].moveNoMove, cells[x][y].rotate, cells[x][y].move2_canMove)
            #print(lstGroup)
            (cells, needRefreshOfLstGroup) = self.thisMove(lstGroup[i], cells, steps)
            #time.sleep(10)
            preLenGroup = len(lstGroup)
            if needRefreshOfLstGroup:
                lstGroup = self.getMovableGroup(cells)                    
            #print(needRefreshOfLstGroup, lstGroup)
            #print('----end----')
            #print(self.times, i)
            #for x in range(self.rows):
            #    for y in range(self.cols):
            #        print(cells[x][y].up, cells[x][y].right, cells[x][y].down, cells[x][y].left, 
            #              cells[x][y].start, cells[x][y].end, cells[x][y].canMove,
            #             cells[x][y].moveNoMove, cells[x][y].rotate, cells[x][y].move2_canMove)
            if steps > self.maxSteps - 3:
                self.isSuccess = self.check(cells)
                if self.isSuccess:
                    #print('2-----')
                    #for x in range(self.rows):
                    #    for y in range(self.cols):
                    #        print(cells[x][y].up, cells[x][y].right, cells[x][y].down, cells[x][y].left, 
                    #              cells[x][y].start, cells[x][y].end, cells[x][y].canMove,
                    #             cells[x][y].moveNoMove, cells[x][y].rotate, cells[x][y].move2_canMove)
                    s = ''
                    timeEnd = time.time()
                    timeSpend = timeEnd - self.timeStart
                    if timeSpend < 60:
                        s += '執行時間：' + str(timeSpend) + '秒\n'
                    else:
                        s += '執行時間：' + str(timeSpend // 60) + '分 ' + str(timeSpend % 60) + '秒\n'
                    for i in range(len(self.lstMoveStepsString)):
                        s += self.lstMoveStepsString[i] + '\n'
                    s = s.rstrip('->\n')
                    print(s)
                    messagebox.showinfo('移動步驟', s)
                    break            
            self.move(steps+1, cells, lstGroup)
            #threadObj = threading.Thread(target=self.move, args=[steps+1, cells, lstGroup])
            #threadObj.start()
            #time.sleep(1)
            cells = copy.deepcopy(preCells)
            lstGroup = copy.deepcopy(preLstGroup)
            self.lstMoveStepsString.pop()
            self.lstMoveSteps.pop()
            if len(lstGroup) != preLenGroup:
                i = -1
    
    def thisMove(self, lstGroup, cells, steps):
        self.times+=1
        needRefreshOfLstGroup = False
        #print(self.times, lstGroup)
        if len(lstGroup[2]) == 2:
            (x1, y1) = lstGroup[2][0]
            (x2, y2) = lstGroup[2][1]
            (cells[x1][y1], cells[x2][y2]) = (cells[x2][y2], cells[x1][y1])
            if cells[x1][y1].moveNoMove:
                cells[x1][y1].canMove = False
                cells[x1][y1].moveNoMove = False
                needRefreshOfLstGroup = True
            elif cells[x1][y1].rotate:
                cells[x1][y1].road = cells[x1][y1].road * 2 % 15
                #(cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down, cells[x1][y1].left) \
                #= (cells[x1][y1].left, cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down)
            if cells[x2][y2].moveNoMove:
                cells[x2][y2].canMove = False
                cells[x1][y1].moveNoMove = False
                needRefreshOfLstGroup = True
            elif cells[x2][y2].rotate:
                cells[x2][y2].road = cells[x2][y2].road * 2 % 15
                #(cells[x2][y2].up, cells[x2][y2].right, cells[x2][y2].down, cells[x2][y2].left) \
                #= (cells[x2][y2].left, cells[x2][y2].up, cells[x2][y2].right, cells[x2][y2].down)
            if lstGroup[0] == True:
                self.lstMoveStepsString.append('row '+str(x1)+' right -->')
            else:
                self.lstMoveStepsString.append('col '+str(y1)+' down -->')
        else:
            if lstGroup[1] == True:
                for i in range(len(lstGroup[2])-1, 0, -1):
                    (x1, y1) = lstGroup[2][i]
                    (x2, y2) = lstGroup[2][i-1]
                    (cells[x1][y1], cells[x2][y2]) = (cells[x2][y2], cells[x1][y1])
                    if cells[x1][y1].moveNoMove:
                        cells[x1][y1].canMove = False
                        cells[x1][y1].moveNoMove = False
                        needRefreshOfLstGroup = True
                    elif cells[x1][y1].rotate:
                        cells[x1][y1].road = cells[x1][y1].road * 2 % 15
                        #(cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down, cells[x1][y1].left) \
                        #= (cells[x1][y1].left, cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down)
                (x1, y1) = lstGroup[2][0]
                if cells[x1][y1].moveNoMove:
                    cells[x1][y1].canMove = False
                    cells[x1][y1].moveNoMove = False
                    needRefreshOfLstGroup = True
                elif cells[x1][y1].rotate:
                    cells[x1][y1].road = cells[x1][y1].road * 2 % 15
                    #(cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down, cells[x1][y1].left) \
                    #= (cells[x1][y1].left, cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down)
                if lstGroup[0] == True:
                    self.lstMoveStepsString.append('row '+str(x1)+' right -->')
                else:
                    self.lstMoveStepsString.append('col '+str(y1)+' down -->')
            else:
                for i in range(len(lstGroup[2])-1):
                    (x1, y1) = lstGroup[2][i]
                    (x2, y2) = lstGroup[2][i+1]
                    (cells[x1][y1], cells[x2][y2]) = (cells[x2][y2], cells[x1][y1])
                    if cells[x1][y1].moveNoMove:
                        cells[x1][y1].canMove = False
                        cells[x1][y1].moveNoMove = False
                        needRefreshOfLstGroup = True
                    elif cells[x1][y1].rotate:
                        cells[x1][y1].road = cells[x1][y1].road * 2 % 15
                        #(cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down, cells[x1][y1].left) \
                        #= (cells[x1][y1].left, cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down)
                try:
                    (x1, y1) = lstGroup[2][len(lstGroup[2])-1]
                except:
                    print('*****Error*****', lstGroup[2])
                if cells[x1][y1].moveNoMove:
                    cells[x1][y1].canMove = False
                    cells[x1][y1].moveNoMove = False
                    needRefreshOfLstGroup = True
                elif cells[x1][y1].rotate:
                    cells[x1][y1].road = cells[x1][y1].road * 2 % 15
                    #(cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down, cells[x1][y1].left) \
                    #= (cells[x1][y1].left, cells[x1][y1].up, cells[x1][y1].right, cells[x1][y1].down)
                if lstGroup[0] == True:
                    self.lstMoveStepsString.append('row '+str(x1)+' left -->')
                else:
                    self.lstMoveStepsString.append('col '+str(y1)+' up -->')
        if steps==1:
            for i in range(self.rows):
                for j in range(self.cols):
                    if cells[i][j].move2_canMove:
                        cells[i][j].canMove = True
                        cells[x1][y1].move2_canMove = False
                        needRefreshOfLstGroup = True
        self.lstMoveSteps.append(lstGroup)
        #print(self.times, steps, self.lstMoveStepsString)
        #print()
        return (cells, needRefreshOfLstGroup)
    
    def check(self, cells):
        isFinished = False
        #for x in range(self.rows):
        #    for y in range(self.cols):
        #        print(cells[x][y].road, \
        #            cells[x][y].start, cells[x][y].end, cells[x][y].canMove, \
        #            cells[x][y].moveNoMove, cells[x][y].rotate, cells[x][y].move2_canMove)
        (i, j) = self.start
        #print('start', i, j)
        if cells[i][j].road == 1:
            preRoad = 1
            i -= 1
        elif cells[i][j].road == 2:
            preRoad = 2
            j += 1
        elif cells[i][j].road == 4:
            preRoad = 4
            i += 1
        elif cells[i][j].road == 8:
            preRoad = 8
            j -= 1
        while(True):
            if cells[i][j].end == True:
                if cells[i][j].road == preRoad * 4 % 15:
                    isFinished = True
                    print('Successed')
                    break
            if cells[i][j].road == (preRoad * 4 % 15 + preRoad) % 15:
                preRoad = cells[i][j].road - preRoad * 4 % 15
            elif cells[i][j].road == (preRoad * 4 % 15 + preRoad * 2 % 15) % 15:
                preRoad = cells[i][j].road - preRoad * 4 % 15
            elif cells[i][j].road == (preRoad * 4 % 15 + preRoad * 8 % 15) % 15:
                preRoad = cells[i][j].road - preRoad * 4 % 15
            else:
                break
            if preRoad == 1:
                i -= 1
                if i < 0:
                    break
            elif preRoad == 2:
                j += 1
                if j > self.cols-1:
                    break
            elif preRoad == 4:
                i += 1
                if i > self.rows-1:
                    break
            elif preRoad == 8:
                j -= 1
                if j < 0:
                    break
        return isFinished
    
    def move2(self, steps, cells, lstGroup):
        Ture = True
        

if __name__ == "__main__":
    root = tk.Tk()
    App(root).pack(side="top", fill="both", expand=True)
    root.mainloop()