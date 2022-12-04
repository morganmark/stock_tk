import tkinter as tk
import twstock
import pandas
from bokeh.plotting import figure,output_file,show
from bokeh.models.widgets import Panel,Tabs
import os
import csv
import tkinter.messagebox

#輸出成HTML
def _figurEShoW(dF,filE):
    global bH1,bH2,bH3,bH4
    
    htmLN=filE+'.html'
    output_file(htmLN)
    #Open
    bH1=figure(title="Open",x_axis_label="日期",y_axis_label="開盤價", plot_width=1300, plot_height=700)
    bH1.title.text_color="blue"
    bH1.title.text_font_style="bold"
    bH1.xaxis.axis_label_text_font_size = "20pt"
    bH1.yaxis.axis_label_text_font_size = "20pt" 
    #High
    bH2=figure(title="High",x_axis_label="日期",y_axis_label="最高價", plot_width=1300, plot_height=700)
    bH2.title.text_color="orange"
    bH2.title.text_font_style="bold"
    bH2.xaxis.axis_label_text_font_size = "20pt"
    bH2.yaxis.axis_label_text_font_size = "20pt" 
    #Low
    bH3=figure(title="Low",x_axis_label="日期",y_axis_label="最低價", plot_width=1300, plot_height=700)
    bH3.title.text_color="green"
    bH3.title.text_font_style="bold"
    bH3.xaxis.axis_label_text_font_size = "20pt"
    bH3.yaxis.axis_label_text_font_size = "20pt" 
    #Close
    bH4=figure(title="Close",x_axis_label="日期",y_axis_label="收盤價", plot_width=1300, plot_height=700)
    bH4.title.text_color="pink"
    bH4.title.text_font_style="bold"
    bH4.xaxis.axis_label_text_font_size = "20pt"
    bH4.yaxis.axis_label_text_font_size = "20pt" 
    
    bH1.line(dF["Date"],dF["Open"],line_width=5,color="blue",alpha=0.3,legend_label="Open")
    bH1.diamond(dF["Date"],dF["Open"],size=10,color="blue",legend_label="Open")
    bH1.legend.location = "top_left"
    bH1.legend.click_policy="hide"
    
    bH2.line(dF["Date"],dF["High"],line_width=5,color="orange",alpha=0.3,legend_label="High")
    bH2.diamond(dF["Date"],dF["High"],size=10,color="orange",legend_label="High")
    bH2.legend.location = "top_left"
    bH2.legend.click_policy="hide"
    
    bH3.line(dF["Date"],dF["Low"],line_width=5,color="green",alpha=0.3,legend_label="Low")
    bH3.diamond(dF["Date"],dF["Low"],size=10,color="green",legend_label="Low")
    bH3.legend.location = "top_left"
    bH3.legend.click_policy="hide"
    
    bH4.line(dF["Date"],dF["Close"],line_width=5,color="pink",alpha=0.3,legend_label="Close")
    bH4.diamond(dF["Date"],dF["Close"],size=10,color="pink",legend_label="Close")
    bH4.legend.location = "top_left"
    bH4.legend.click_policy="hide"
    
    t1 = Panel(child=bH1, title="Open")
    t2 = Panel(child=bH2, title="High")
    t3 = Panel(child=bH3, title="Low")
    t4 = Panel(child=bH4, title="Close")
    bH = Tabs(tabs=[t1,t2,t3,t4])
    show(bH)

def _hit1():
    #接收資料
    nO=enteName.get()
    stocK=twstock.Stock(nO)
    yeaR=enteYear.get()
    montH=enteMon.get()
    #設檔名
    filE=yeaR+'-'+montH
    #判別目錄存在
    stockDir=nO+ "/"
    if not os.path.exists(stockDir):
        os.mkdir(stockDir)
        
    filEN=stockDir+"\\"+filE+'.csv'
    #判斷檔案是否存在
    if not os.path.isfile(filEN):
        #用stock抓股票資料
        datA=stocK.fetch(int(yeaR),int(montH))
        lisT=[]
        for vI in range(len(datA)):
            lisTs=[]
            datE=str(datA[vI][0])
            datE=datE.split(" ")[0]
            opeN=str(datA[vI][3])
            higH=str(datA[vI][4])
            loW=str(datA[vI][5])
            closE=str(datA[vI][6])
            lisTs.append(datE)
            lisTs.append(opeN)
            lisTs.append(higH)
            lisTs.append(loW)
            lisTs.append(closE)
            lisT.append(lisTs)
        #轉成DF
        dF=pandas.DataFrame(lisT,columns =['Date', 'Open', 'High','Low','Close'])
        #寫成CSV
        csvFileW=open(filEN,"w",newline="",encoding="utf-8-sig")
        writeR=csv.writer(csvFileW)
        writeR.writerow(['Date','Open','High','Low','Close'])
        for rowD in lisT:
            writeR.writerow([rowD[0],rowD[1],rowD[2],rowD[3],rowD[4]])
        csvFileW.close()
        for dateNo in range(len(dF['Date'])):
             dF['Date'][dateNo]=dF['Date'][dateNo].split('-')[2]
        
        _figurEShoW(dF,filE)
    
    else:
        #讀CSV
        csvFileR=open(filEN,"r",encoding="utf-8-sig")
        lisT=csv.reader(csvFileR)
        dF=pandas.DataFrame(lisT,columns =['Date', 'Open', 'High','Low','Close'])
        
        for dateNo in range(1,len(dF['Date'])):
            dF['Date'][dateNo]=dF['Date'][dateNo].split('-')[2]
        _figurEShoW(dF,filE)
        csvFileR.close()
    
    enteName.delete(0,tk.END)
    enteYear.delete(0,tk.END)
    enteMon.delete(0,tk.END)
    
def _hit2():
    qQ=tk.messagebox.askokcancel("離開確定","確定要結束程式嗎???")
    if qQ:
        wiN.destroy()


wiN = tk.Tk()
wiN.title("Stock!!!")
wiN.geometry("400x400+1100+100")
wiN.configure(background='skyblue')
wiN.resizable(False, False)
#視窗置頂
wiN.wm_attributes('-topmost',1)

labeLN=tk.Label(wiN, text='股票代碼:', font=("Arial Black", 20), fg ="red", bg ="skyblue")
labeLN.pack()
enteName=tk.Entry(wiN,font=("Arial",18),bd=5)
enteName.pack() 

labeLY=tk.Label(wiN, text='年份:', font=("Arial Black", 20), fg ="red", bg ="skyblue")
labeLY.pack()
enteYear=tk.Entry(wiN,font=("Arial",18),bd=5)
enteYear.pack() 

labeLM=tk.Label(wiN, text='月份:', font=("Arial Black", 20), fg ="red", bg ="skyblue")
labeLM.pack()
enteMon=tk.Entry(wiN,font=("Arial",18),bd=5)
enteMon.pack() 

btN1 = tk.Button(wiN, text="查詢!!", font=("Arial Black", 20),fg ="red",bg="orange", width=8, height=1, command=_hit1)
btN1.pack() 
btN2 = tk.Button(wiN, text="離開!!", font=("Arial Black", 20),fg ="lime",bg="red", width=8, height=1, command=_hit2)
btN2.pack() 

wiN.mainloop()

