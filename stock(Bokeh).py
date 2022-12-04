import twstock
import pandas
from bokeh.plotting import figure,output_file,show
from bokeh.models.widgets import Panel,Tabs
from os import path
import csv

def _figurEShoW(dF):
    global bH1,bH2,bH3,bH4
    
    htmLN=filE+'.html'
    output_file(htmLN)
    
    bH1=figure(title="Open",x_axis_label="Days",y_axis_label="Open", plot_width=1300, plot_height=700)
    bH1.title.text_color="blue"
    bH1.title.text_font_style="bold"
    bH1.xaxis.axis_label_text_font_size = "20pt"
    bH1.yaxis.axis_label_text_font_size = "20pt" 
    
    bH2=figure(title="High",x_axis_label="Days",y_axis_label="High", plot_width=1300, plot_height=700)
    bH2.title.text_color="orange"
    bH2.title.text_font_style="bold"
    bH2.xaxis.axis_label_text_font_size = "20pt"
    bH2.yaxis.axis_label_text_font_size = "20pt" 
    
    bH3=figure(title="Low",x_axis_label="Days",y_axis_label="Low", plot_width=1300, plot_height=700)
    bH3.title.text_color="green"
    bH3.title.text_font_style="bold"
    bH3.xaxis.axis_label_text_font_size = "20pt"
    bH3.yaxis.axis_label_text_font_size = "20pt" 
    
    bH4=figure(title="Close",x_axis_label="Days",y_axis_label="Cose", plot_width=1300, plot_height=700)
    bH4.title.text_color="pink"
    bH4.title.text_font_style="bold"
    bH4.xaxis.axis_label_text_font_size = "20pt"
    bH4.yaxis.axis_label_text_font_size = "20pt" 
    bH1.line(dF["Date"],dF["Open"],line_width=5,color="blue",alpha=0.3,legend_label="Open")
    bH1.diamond(dF["Date"],dF["Open"],size=10,color="blue",legend_label="Open")
    #bH1.vbar(x=dF["Date"],top=dF["Open"],width=0.5,color="blue",legend_label="Open")
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

#nO=input("請輸入股票代號: ")
nO='2330'
stocK=twstock.Stock(nO)
#yeaR=input("請輸入哪一年: ")
yeaR='2022'
#montH=input("請輸入哪一月份: ")
montH='11'
filE=nO+'_'+yeaR+'-'+montH
filEN=filE+'.csv'
if not path.isfile(filEN):
    
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
    dF=pandas.DataFrame(lisT,columns =['Date', 'Open', 'High','Low','Close'])
    csvFileW=open(filEN,"w",newline="",encoding="utf-8-sig")
    writeR=csv.writer(csvFileW)
    writeR.writerow(['Date','Open','High','Low','Close'])
    for rowD in lisT:
        writeR.writerow([rowD[0],rowD[1],rowD[2],rowD[3],rowD[4]])
        print([rowD[0],rowD[1],rowD[2],rowD[3],rowD[4]])
    csvFileW.close()
    for dateNo in range(len(dF['Date'])):
         dF['Date'][dateNo]=dF['Date'][dateNo].split('-')[2]
    
    _figurEShoW(dF)

else:
    csvFileR=open(filEN,"r",encoding="utf-8-sig")
    lisT=csv.reader(csvFileR)
    dF=pandas.DataFrame(lisT,columns =['Date', 'Open', 'High','Low','Close'])
    
    for dateNo in range(1,len(dF['Date'])):
        dF['Date'][dateNo]=dF['Date'][dateNo].split('-')[2]
    _figurEShoW(dF)
    csvFileR.close()

    
    
    