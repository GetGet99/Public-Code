# -*- coding: utf-8 -*-
"""
7 Puzzle

Created on Sat Sep 19 16:12:45 2020

@author: Get

Code นี้มี Code ขยะจำนวนมาก ต้องขออภัยมาใน ณ ที่นี้ด้วย
"""


import pandas as pd;
# from IPython.display import display;

import warnings
warnings.filterwarnings('ignore')

Table = pd.DataFrame([[1,5,2],[4,8,3],[7,6," "]])
CorrectAns = pd.DataFrame([[1,2,3],[4,5,6],[7,8," "]])
print("""8 Puzzle by Sirawich Smitsomboon
      How to Play:
          Type the number that is ajacent to blank cell to move that number to blank cell
          พิมพ์เลขที่ต้องการจะย้าย
          
          Type 'AI' to get help by AI
          พิมพ์ 'AI' เพื่อให้ได้ Step การ Solve จาก AI
          
          Type 'end' to exit
      Note:
          Please ignore 0 1 2 on the top and on the side, it is just the table format""")
def MoveTo(Table,number,x,y,MoveToX,MoveToY):
    Table2 = Table.copy(deep=True);
    Table2.iloc[MoveToY,MoveToX] = number;
    Table2.iloc[y,x] = " ";
    return Table2;
def CheckPossibleAndMove(Table):
    CanMove = [];

    MoveToX = 0;
    MoveToY = 0;

    for i in range(3):
        row = Table.iloc[i,:];
        index = row[row == " "].index
        if (len(index) != 1): continue;
        index = index[0];
        MoveToY = i;
        MoveToX = index;
        if (index == 0):
            CanMove.append((row[1],1,i));
        elif (index == 1):
            CanMove.append((row[0],0,i));
            CanMove.append((row[2],2,i));
        elif (index == 2):
            CanMove.append((row[1],1,i));
        break;

    for i in range(3):
        column = Table.iloc[:,i];
        index = column[column == " "].index
        if (len(index) != 1): continue;
        index = index[0];
        if (index == 0):
            CanMove.append((column[1],i,1));
        elif (index == 1):
            CanMove.append((column[0],i,0));
            CanMove.append((column[2],i,2));
        elif (index == 2):
            CanMove.append((column[1],i,1));
        break;
    return CanMove, MoveToX, MoveToY;

def CalculateNextStep(OldData, OldTrace):
    CanMove, MoveToX, MoveToY = CheckPossibleAndMove(OldData.copy(deep=True));
    List = []
    
    for i, x, y in CanMove:
        MovedData = MoveTo(OldData.copy(deep=True),i,x,y,MoveToX,MoveToY);
        if (MovedData == OldData).all().all(): continue;
        List.append((OldTrace+[i], MovedData));
    return List;

def CheckSearchResult(Data):
    Value = (Data == CorrectAns).all().all();
    return Value;
def BFSearch(Data,CalculateNext,CheckSearchResult):
    """
    BFSearch(object[] Data,Func CalculateNext, Func CheckSearchResult)

    Parameters
    ----------
    Data : object
        Data.
    Params : object[]
        Parameter, each item will be used to call CalculateNext.
    CalculateNext : Func
        Function that return a list of 'turple of NewDatas and Trace' from OldData and OldTrace
    CheckSearchResult : Func
        Function that return boolean that if the data is what is looking for. If True, BFSearch will be ended.
    
    Returns
    -------
    List of the Params in order from first to last to produce the Searched Data.

    """
    def OneLayer(Data,Trace):
        NewDatas = CalculateNext(Data,Trace);
        return NewDatas;
    NodeList = OneLayer(Data,[]);
    while True and len(NodeList) > 0:
        # Node = NodeList[0];
        Trace, Data = NodeList[0];
        del NodeList[0];
        # for Trace, Data in Node:
        NewNodes = OneLayer(Data,Trace);
        for NewTrace, NewData in NewNodes:
            if CheckSearchResult(NewData): return NewTrace;
        NodeList += NewNodes;
def display(Table):
    for i in range(3):
        for j in range(3):
            print(Table.iloc[i,j],end=" ")
        print()
while True and not ((Table == CorrectAns).all().all()):
    CanMove, MoveToX, MoveToY = CheckPossibleAndMove(Table);
    while True:
        display(Table)
        Move = input("Move what? > ");
        if (Move == "end"): break;
        elif (Move == "AI"):
            print("This might take few seconds/minutes - depend on how fast your computer is")
            print(f"Type according to this sequence to get to the end! -> {BFSearch(Table,CalculateNextStep,CheckSearchResult)}")
            continue;
        try:
            Move = int(Move);
            Moved = False;
            for i, x, y in CanMove:
                if i == int(Move):
                    Moved = True
                    Table = MoveTo(Table,i,x,y,MoveToX,MoveToY);
                    CanMove, MoveToX, MoveToY = CheckPossibleAndMove(Table);
                    break;
            if (Moved): break;
            else: print("Please Enter a valid number")
        except:
            print("Please Enter a valid number")
    if Move == "end": break;
print("Game Ended, this is the final table")
display(Table)