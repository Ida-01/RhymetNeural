import random
import math
import sys
import json
import numpy as np

class Setter():
    def __init__(self):
        NetWorkFrame = open("NetworkInfo.json", "r")
        OpenFrame = json.load(NetWorkFrame)
        NetWorkFrame.close()
        self.Neurons = OpenFrame['Neurons']
        exec('self.Activtions = ' + OpenFrame["Activtions"])
        exec('self.CostFunction = ' + OpenFrame["CostFunction"])
        self.Pooling = OpenFrame['Pooling']
        self.Chunk = OpenFrame['Chunk']
        exec('self.LoadingBar = ' + OpenFrame["LoadingBar"])
        exec('self.Filters = ' + OpenFrame["Filters"])

#This is a NeuralFrame, It is used for Compressing Data in Parameters
class NeuralFrame:

    def __init__(self, ParNeur, ParActi):
        self.NeurList = []
        self.ActivList = ParActi
        self.ActivName = []
        self.CostFun = self.ActivList.pop(0)
        self.PoolNumb = 0
        self.ChunkNumb = 0
        for i in range(len(ParNeur)):
            if ParNeur[i] == "Pool":
                self.PoolNumb += 1
            else:
                self.NeurList.append(ParNeur[i])

        for i in range(len(ParActi)):
            self.ActivName.append(ParActi[i].__name__)
        self.ActivName = str(self.ActivName).replace("'", "")

        if self.PoolNumb > 0:
            self.ChunkNumb = int(math.sqrt(self.NeurList[-1]) + 2 * self.PoolNumb)

        self.loadbar = LoadingBarPre
        self.Filters = []

    def SetCusLoad(self, load):
        self.loadbar = load
        return self

    def SetFilters(self, NewFilter):
        self.Filters = NewFilter
        return self



def CombineGrids(GridList):
    NewGrid = np.zeros((len(GridList[0]), len(GridList[0][0]))).tolist()

    for l in range(len(GridList)): 

        for i in range(len(GridList[0])): 

            for j in range(len(GridList[0][0])): 

                NewGrid[i][j] += GridList[l][i][j]

    for i in range(len(GridList[0])): 
        for j in range(len(GridList[0][0])): 
            NewGrid[i][j] = NewGrid[i][j]/len(GridList)

    return NewGrid

def Convolution(Image, IMGfilter):
    NewIMG = []
    Image = Chunk(Image, int(math.sqrt(len(Image))))
    Image = np.pad(Image, ((1,1),(1,1)), 'constant').tolist()

    for i in range(1, len(Image) - 1):

        NewRow = []
        for j in range(1, len(Image[0]) - 1):
            Total = 0

            for r in range(-1,2):
                for c in range(-1,2):
                    Total += Image[i+r][j+c] * IMGfilter[r+1][c+1]

            NewRow.append(abs(Total))
        NewIMG.append(NewRow)
        
    return(NewIMG)

#This is a Neural Network pool
def PoolAry(Kw, Kh, Image):
    NewImage = []
    for i in range(len(Image) - (Kh - 1)):

        NewRow = []
        
        for j in range(len(Image[0]) - (Kw - 1)):



            if (i + Kh) <= len(Image) and (j + Kw) <= len(Image[0]):

                max = Image[i][j]

                for r in range(Kh):
                    for c in range(Kw):
                        if Image[i + r][j + c] > max:

                            max = Image[i + r][j + c]

                
                NewRow.append(max)

        NewImage.append(NewRow)

    return (NewImage)



def SumCheck(x):
    if type(x) != list:
        return x

    return sum(x)

#Turns a 1D list into a 2D list
def Chunk(Lis, Spli):
    newLis = []
    for i in range(0, len(Lis), Spli):
        newLis.append(Lis[i : i + Spli])

    return (newLis)


#Turns a 2D list into a 1D list
def UnChunk(Lis):
    newLis = []
    for i in range(len(Lis)):

        for j in range(len(Lis[i])):

            newLis.append(Lis[i][j])

    return (newLis)



def CalcCost(Exp, Real):
    CosList = []
    for i in range(len(Real)):
        CosList.append(2 * (Exp[i] - Real[i]))
    return CosList


#Cost Activation Function
def RealCalcCost(Exp, Real):
    CosList = []
    for i in range(len(Real)):
        CosList.append(pow(Exp[i] - Real[i], 2))
    return sum(CosList)


#Finds the Max number in a list
def FindMax(Output):
    Maxam = Output[0]
    Awn = 0
    for i in range(len(Output)):
        if Output[i] > Maxam:
            Maxam = Output[i]
            Awn = i

    return Awn



#Sigmoid Activation Function
def Sigmoid(x):
    try:
        return 1 / (1 + math.exp(-x))
    except OverflowError:
        return 0

#Sigmoid Derivative Function
def SigmoidDerv(y):
    return Sigmoid(y) * (1 - Sigmoid(y))


#Tanh Activation Function (this is here so i don't get confused)
def Tanh(x):
    return math.tanh(x)

#Tanh Derivative Function
def TanhDerv(y):
    return 1 - (pow(math.tanh(y), 2))

#Swish Activation Function
def Swish(x):
    try:
        return x * Sigmoid(x)
    except OverflowError:
        return 0

#Swish Derivative Function
def SwishDerv(y):
    try:
        return y * SigmoidDerv(y) + Sigmoid(y) #Swish(y) + Sigmoid(y) * (1-Swish(y))
    except OverflowError:
        return 0

#Relu Activation Function
def Relu(x):
	return max(0.0, x)

#Relu Derivative Function
def ReluDerv(y):
    return np.greater(y, 0.).astype(np.float32)

#LeakyRelu Activation Function
def LeakyRelu(x):
	return max(x/4, x)

#LeakyRelu Derivative Function
def LeakyReluDerv(y):
    return max(np.sign(y), 0.25)

#Linear Activation Function
def Linear(x):
    return x

#Linear Derivative Function
def LinearDerv(y):
    return 1
    
#Applies Activation Function to a list
def ActivationList(x, Acti):
    newList = []
    for i in x:
        newList.append(Acti(i))
    return newList


#Random Float between -11 and 11
def rand():
    return random.uniform(-1, 1)   #randrange(-10, 10) + (random.randrange(-100, 100) / 100)



#converts a string of float into a list of float
def ConvFloatList(listparam):
    return list(map(float, listparam.split()))


#This creates a Fresh List for Weights
def GetFresh(LayLis):
    
    WFreash = []
    for i in range(len(LayLis)):
        l1 = []
        try:
            for j in range(LayLis[i]):
                l2 = []
                for k in range(LayLis[i + 1]):
                    l2.append(0)
                l1.append(l2)
            WFreash.append(l1)
        except:
            break

    return(WFreash)


#This is used to get text from a file 
#Because 
class TxtGetW():
    def __init__(self, FileNum):
        NetWeTxt = open("WBL" + str(FileNum) + "/WeightsLay.json", "r")
        Content = json.load(NetWeTxt)
        NetWeTxt.close()
        self.Weights = Content['Weights']
        self.Bias = Content['Bias']

#This gets the Weights from text file
def GetTxT(LayLis):
    WFtxt = []
    WBtxt = []

    for i in range(len(LayLis) - 1):

        FileNum = (len(LayLis) - 2) - i
        FileRead = TxtGetW(FileNum)

        FileWeights = FileRead.Weights
        FileBias = FileRead.Bias

        WFtxt.append(FileWeights)
        WBtxt.append(FileBias)

    return((WFtxt, WBtxt))


#Creates Weights in a text file
def MakeTxT(Frame):
    LayLis = Frame.NeurList

    WFreash = []

    for i in range(len(LayLis) - 1):
            
        FileNum = (len(LayLis) - 2) - i

        if FileNum > -1:
            srtTofile = []
            for j in range(LayLis[i]):
                srtTofile.append([])
                sd = math.sqrt(2/LayLis[i + 1])
                for k in range(LayLis[i + 1]):

                    srtTofile[j].append(rand())#np.random.normal(loc=0, scale=sd))


            NewData = json.loads('{"Weights": [], "Bias":0}')
            NewData['Weights'] = srtTofile
            OpenFile = open("WBL" + str(FileNum) + "/WeightsLay.json", "w")
            json.dump(NewData, OpenFile)
            OpenFile.close()




    SavedFrame = json.loads('{"Neurons": 0, "Activtions": 0, "CostFunction":0 , "Pooling":0, "Chunk":0, "LoadingBar":0, "Filters":0 }')
    SavedFrame['Neurons'] = Frame.NeurList
    SavedFrame['Activtions'] = Frame.ActivName
    SavedFrame['CostFunction'] = Frame.CostFun.__name__
    SavedFrame['Pooling'] = Frame.PoolNumb
    SavedFrame['Chunk'] = Frame.ChunkNumb
    SavedFrame['LoadingBar'] = Frame.loadbar.__name__
    SavedFrame['Filters'] = str(Frame.Filters)
    OpenFile = open("NetworkInfo.json", "w")
    json.dump(SavedFrame, OpenFile)
    OpenFile.close()


    print("Previous data overwritten, New data inserted")
    return(WFreash)


#Adds to Weights in the text file 
def AddTxT(NewLis, OldLays, DevBy):
    WeiLis = NewLis[0]
    BiaLis = NewLis[1]
    OldWei = OldLays[0]
    OldBia = OldLays[1]

    NewWei = []
    NewBia = []
    for i in range(len(WeiLis)):

        srtTofile = []
        biaTofile = (OldBia[i] + (BiaLis[i] / DevBy))
        FileNum = (len(WeiLis) - 1) - i

        for j in range(len(WeiLis[i])):
            srtTofile.append([])
            for k in range(len(WeiLis[i][j])):
                srtTofile[j].append(OldWei[i][j][k] + (WeiLis[i][j][k] / DevBy))


        NewData = json.loads('{"Weights": [], "Bias":0}')
        NewData['Weights'] = srtTofile
        NewData['Bias'] = biaTofile
        OpenFile = open("WBL" + str(FileNum) + "/WeightsLay.json", "w")
        json.dump(NewData, OpenFile)
        OpenFile.close()


        NewWei.append(srtTofile)
        NewBia.append(biaTofile)


    return (NewWei, NewBia)

#this gets the Bias from text file
def GetBia(LayLis):
    Biatxt = []

    for i in range(len(LayLis) - 1):

        FileNum = (len(LayLis) - 2) - i
        Data = open("WBL" + str(FileNum) + "/BiasLay.txt", "r")
        Content = Data.read()
        Data.close()

        Biatxt.append(float(Content))

    return(Biatxt)


#Adds to Bias in the text file 
def AddBia(BiaLis, OGLay, DevBy):
    OGBia = GetBia(OGLay)
    for i in range(len(BiaLis)):

        srtTofile = ""
        FileNum = (len(BiaLis) - 1) - i

        srtTofile += str(OGBia[i] + (BiaLis[i] / DevBy))


        open("WBL" + str(FileNum) + "/BiasLay.txt", "w").write(srtTofile)

#This creates a Fresh List for Bias
def FreshBi(BiLa):
    fre = []
    for i in range(len(BiLa)):
        fre.append(0)
    
    return(fre)

#Calculation foe example 
def CalcExpe(x):
    NEl = []
    for i in range(10):

        if i == x:

            NEl.append(1)

        else:

            NEl.append(0)
        
    return NEl




#these are just loading functions


def LoadingBarPre(LoadingPro):
    LoadingPro += "█"
    LoadUn = "░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░⦘"
    sys.stdout.write("\033[F")
    NewLoad = "⦗" + LoadingPro + LoadUn[len(LoadingPro) : 51]
    print(NewLoad)


    return LoadingPro


def LoadingBarHig(LoadingPro):
    LoadingPro += "▩"
    LoadUn = "□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□⦘"
    sys.stdout.write("\033[F")
    NewLoad = "⦗" + LoadingPro + "█" + LoadUn[len(LoadingPro) : 51]
     
    print(NewLoad)
    if NewLoad == "⦗▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩█⦘":
        sys.stdout.write("\033[F")
        print("⦗▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩▩⦘")
        print("\n")
        return ""

    return LoadingPro



def LoadingText(LoadingPro):
    LoadingDic = {
                     "│" : "╱", 
                     "╱" : "──",
                    "──" : '╲ ',
                    '╲ ' : '│',
                      "" : '│',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro


def LoadingCir(LoadingPro):
    LoadingDic = {
                     "◜ " : " ◝", 
                     " ◝" : " ◞",
                    " ◞" : '◟ ',
                    '◟ ' : '◜ ',
                      "" : '◜ ',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro


def LoadingCirFull(LoadingPro):
    LoadingDic = {
                     "◴" : "◷", 
                     "◷" : "◶",
                     "◶" : "◵",
                     "◵" : "◴",
                      "" : '◴',
                 }
    LoadingPro = LoadingDic[LoadingPro]
    sys.stdout.write("\033[F")
    print("Loading: " + LoadingPro)
    return LoadingPro




def LoadingCard(LoadingPro):

    if LoadingPro == ""  or int(LoadingPro[0:6]) > 127150:
        LoadingPro = "127137"

    CardInt = int(LoadingPro[0:6])  

    LoadingPro += chr(CardInt)

    sys.stdout.write("\033[F")
    
    AfterNumb = LoadingPro[6 : len(LoadingPro)]

    print("Loading: " + AfterNumb + "🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘🂘"[len(LoadingPro) - 6: 14])

    LoadingPro = str(CardInt + 1) + AfterNumb 


    return LoadingPro


def LoadingDice(LoadingPro):

    if LoadingPro == ""  or int(LoadingPro[0:4]) > 9861:
        LoadingPro = "9856"

    CardInt = int(LoadingPro[0:4])  

    LoadingPro = str(CardInt + 1) + chr(CardInt)

    sys.stdout.write("\033[F")
    

    print("Loading: " + LoadingPro[4:5])



    return LoadingPro