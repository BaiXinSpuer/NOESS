#转载清标明出处
#by BaiXinSuper
import tkinter as tk
import random as r
import threading,time,os,base64,json,hashlib,easygui
class Main():
    def __init__(self):
        self.root=tk.Tk()
        self.root.resizable(0,0)
        self.root.geometry('600x250')
        self.root.title('算术题游戏(小学带计时版)')
        self.stateLock='LOCKED'
        with open('ICON','rb') as f:
            icon=f.read()
            f.close()
        with open('tmp.ico','wb+') as a:
            a.write(base64.b64decode(icon))
            a.close()
            self.root.iconbitmap('tmp.ico')
            os.remove('tmp.ico')
        self.btn1=tk.Button(self.root,width=10,height=3,text='10以内加减法',command=lambda:self.choose(0))
        self.btn2=tk.Button(self.root,width=10,height=3,text='50以内加减法',command=lambda:self.choose(1))
        self.btn3=tk.Button(self.root,width=10,height=3,text='100以内加减法',command=lambda:self.choose(2))
        self.btn4=tk.Button(self.root,width=12,height=3,text='1000以内加减法',command=lambda:self.choose(3))
        self.btn5=tk.Button(self.root,width=15,height=3,text='10000以内加减法',command=lambda:self.choose(4))
        self.btn6=tk.Button(self.root,width=10,height=3,text='10以内乘除法',command=lambda:self.choose(5))
        self.btn_info=tk.Button(self.root,width=10,height=3,text='99乘法表',command=lambda:self.choose('99'))
        self.btn_settings=tk.Button(self.root,width=5,height=1,text='设置',command=self.SettingWindow)
        self.btn_wrongBook=tk.Button(self.root,width=10,height=2,text='错题集',command=self.wrongBook)
        self.btn1.place(x=0,y=0)
        self.btn2.place(x=100,y=0)
        self.btn3.place(x=200,y=0)
        self.btn4.place(x=300,y=0)
        self.btn5.place(x=400,y=0)
        self.btn6.place(x=0,y=100)
        self.btn_info.place(x=0,y=170)
        self.btn_settings.place(x=550,y=215)
        self.btn_wrongBook.place(x=200,y=75)
        thread1=threading.Thread(target=self.normalBtns)
        thread1.daemon=True
        thread1.start()
        self.updateoptions()
        self.root.mainloop()
    def choose(self,num):
        if type(num)==int:
            self.chuti(num)
        elif type(num)==str:
            a=''
            for i in range(1,10):
                for b in range(1,i+1):
                    a=a+'%dx%d=%d  '%(i,b,i*b)
                a=a+'\n'
            easygui.msgbox(title='99',msg=a)
    def updateoptions(self):
        with open('config.ini','r') as f:
            option=[]
            options=f.readlines()
            for i in options:
                option.append(i.replace('\n',''))
            options=[]
            for i in option:
                options.append('"'+i.replace('=','":"')+'"')
            option=''
            for i in options:
                option=option+','+i
            option='{..s'+option+'}'
            option=option.replace('..s,','')
            options=json.dumps(option)
            option=json.loads(json.loads(options))
            self.options=option
    def changePwd(self):
        self.updateoptions()
        if self.options['password']=='0':
            self.window=tk.Toplevel()
            self.wlab=tk.Label(self.window,text='设置密码')
            self.wlab.pack()
            self.wentry=tk.Entry(self.window,width=30)
            self.wentry.pack()
            self.wbtn1=tk.Button(self.window,text='确认',command=self.change)
            self.wbtn1.pack()
            self.window.mainloop()
        else:
            self.window=tk.Tk()
            self.wlab1=tk.Label(self.window,text='原密码：')
            self.wlab1.pack()
            self.wentry1=tk.Entry(self.window,width=30)
            self.wentry1.pack()
            self.wlab2=tk.Label(self.window,text='新密码：')
            self.wlab2.pack()
            self.wentry2=tk.Entry(self.window,width=30)
            self.wentry2.pack()
            self.wbtn1=tk.Button(self.window,text='确认',command=self.change)
            self.wbtn1.pack()
            self.window.mainloop()
        
    def change(self):
        if self.options['password']=='0':
            pwd=self.wentry.get()
            pwd=hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            with open('config.ini','r') as f:
                file=f.read()
                f.close()
                file=file.replace('password=0','password=%s'%pwd)
                with open('config.ini','w') as f:
                    f.write(file)
                    f.close()
                easygui.msgbox(title='success',msg='修改成功')
                self.setWindow.destroy()
        else:
            if hashlib.sha256(self.wentry1.get().encode('utf-8')).hexdigest()==self.options['password']:
                pwd=self.wentry2.get()
                pwd=hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                with open('config.ini','r') as f:
                    file=f.read()
                    f.close()
                    file=file.replace('password=%s'%self.options['password'],'password=%s'%pwd)
                    with open('config.ini','w') as f:
                        f.write(file)
                        f.close()
                    easygui.msgbox(title='success',msg='修改成功')
                    self.setWindow.destroy()
            else:
                easygui.msgbox(title='fail',msg='修改失败\n原密码错误')
        self.window.destroy()
    def SettingWindow(self):
        self.btn_settings['state']='disable'
        self.updateoptions()
        self.setWindow=tk.Toplevel()
        self.setWindow.resizable(0,0)
        if self.stateLock=='LOCKED':
            if self.options['password']=='0':
                easygui.msgbox('第一次进入清先设置密码')
                self.changePwd()
                self.setWindow.destroy()
            else:
                a=tk.Label(self.setWindow,text='解锁密码')
                a.pack()
                self.lockentry=tk.Entry(self.setWindow,width=30)
                self.lockentry.pack()
                self.lockbtn=tk.Button(self.setWindow,text='解锁',command=self.Unlock)
                self.lockbtn.pack()
                self.setWindow.mainloop()
        else:
            self.setWindow.geometry('600x300')
            self.timulens=tk.Label(self.setWindow,text='题目数量：%s'%self.options['num'])
            self.timubtn=tk.Button(self.setWindow,text='编辑',command=lambda:self.changeOptions(0))
            self.timertxt=tk.Label(self.setWindow,text='')
            self.timebtn=tk.Button(self.setWindow,text='',command=lambda:self.changeOptions(1))
            self.jjcfb=tk.Label(self.setWindow,text='')
            self.jjcfbBTN=tk.Button(self.setWindow,text='',command=lambda:self.changeOptions(2))
            self.changebtn=tk.Button(self.setWindow,text='修改密码',command=self.changePwd)
            self.changebtn.place(x=0,y=260)
            self.timertxt.place(x=0,y=60)
            self.timebtn.place(x=0,y=90)
            self.jjcfb.place(x=0,y=120)
            self.jjcfbBTN.place(x=0,y=150)
            self.timubtn.place(x=0,y=30)
            self.timulens.place(x=0,y=0)
            if self.options['Timer']=='False':
                self.timertxt['text']='计时器已禁用'
                self.timebtn['text']='启用计时器'
            else:
                self.timertxt['text']='计时器已启用'
                self.timebtn['text']='禁用计时器'
            if self.options['AllowUse99InGaming']=='True':
                self.jjcfb['text']='在计算中允许使用99乘法表'
                self.jjcfbBTN['text']='禁用'
            else:
                self.jjcfb['text']='在计算中禁止使用99乘法表'
                self.jjcfbBTN['text']='启用'
            self.setWindow.mainloop()
    def changeOptions(self,num):
        if num==0:
            a=int(easygui.enterbox(title='题目数量',msg='题目数量：'))
            if a>=1:
                with open('config.ini','r') as f:
                    old=f.read()
                    f.close()
                    new=old.replace('num=%s'%self.options['num'],'num=%d'%a)
                    with open('config.ini','w') as f:
                        f.write(new)
                        f.close()
        elif num==1:
            if self.options['Timer']=='False':
                self.timertxt['text']='计时器已启用'
                self.timebtn['text']='禁用计时器'
                with open('config.ini','r') as f:
                    old=f.read()
                    f.close()
                    new=old.replace('Timer=False','Timer=True')
                    with open('config.ini','w') as f:
                        f.write(new)
                        f.close()
            else:
                self.timertxt['text']='计时器已禁用'
                self.timebtn['text']='启用计时器'
                with open('config.ini','r') as f:
                    old=f.read()
                    f.close()
                    new=old.replace('Timer=True','Timer=False')
                    with open('config.ini','w') as f:
                        f.write(new)
                        f.close()
        elif num==2:
            if self.options['AllowUse99InGaming']=='True':
                with open('config.ini','r') as f:
                    old=f.read()
                    new=old.replace('AllowUse99InGaming=True','AllowUse99InGaming=False')
                    f.close()
                    with open('config.ini','w') as f:
                        f.write(new)
                        f.close()
            else:
                with open('config.ini','r') as f:
                    old=f.read()
                    new=old.replace('AllowUse99InGaming=False','AllowUse99InGaming=True')
                    f.close()
                    self.jjcfb['text']='在计算中允许使用99乘法表'
                    self.jjcfbBTN['text']='禁用'
                    with open('config.ini','w') as f:
                        f.write(new)
                        f.close()
                        self.jjcfb['text']='在计算中禁止使用99乘法表'
                        self.jjcfbBTN['text']='启用'
        self.updateoptions()
        self.setWindow.destroy()
        self.SettingWindow()
    def Unlock(self):
        if hashlib.sha256(self.lockentry.get().encode('utf-8')).hexdigest()==self.options['password']:
            self.stateLock='UNLOCKED'
            self.setWindow.destroy()
            self.SettingWindow()
        else:
            easygui.msgbox(title='fail',msg='密码错误')
    def wrongBook(self):
        self.book=tk.Toplevel()
        self.book.geometry('300x200')
        self.book.resizable(0,0)
        with open('wrongBook.ini','r') as f:
            wrongs=f.readlines()
            #print(wrongs)
            self.wrong=[]
            for i in wrongs:
                self.wrong.append(i.replace('\n',''))
        if wrongs==[]:
            self.wrong.append('你暂时没有错题哦')
        self.now=0
        txt=tk.Label(self.book,text='错题集：')
        txt.pack()
        self.CTJtimu=tk.Label(self.book,text=self.wrong[self.now])
        self.CTJtimu.pack()
        self.errorentry=tk.Entry(self.book,width=30)
        self.errorentry.pack()
        checkBtn=tk.Button(self.book,text='检查',command=self.Bookcheck,state='normal')
        checkBtn.pack()
        self.leftbtn=tk.Button(self.book,text='上一题',command=lambda:self.changectj(0))
        self.leftbtn.place(x=0,y=170)
        self.rightbtn=tk.Button(self.book,text='下一题',command=lambda:self.changectj(1))
        self.rightbtn.place(x=255,y=170)
        if wrongs==[]:
            checkBtn['state']='disable'
    def changectj(self,num):
        if num==0:
            if self.now>0:
                self.now-=1
                self.CTJtimu['text']=self.wrong[self.now]
        else:
            if self.now<len(self.wrong):
                self.now+=1
                self.CTJtimu['text']=self.wrong[self.now]
    def normalBtns(self):
        while 1:
            try:
                if self.book.state()=='normal':
                    self.btn_wrongBook['state']='disable'
            except:
                self.btn_wrongBook['state']='normal'
            try:
                if self.setWindow.state()=='normal':
                    self.btn_settings['state']='disable'
            except:
                self.btn_settings['state']='normal'
            try:
                if self.now==0:
                     self.leftbtn['state']='disable'
                else:
                    self.leftbtn['state']='normal'
                if self.now==len(self.wrong)-1:
                    self.rightbtn['state']='disable'
                else:
                    self.rightbtn['state']='normal'
            except:
                pass
            try:
                if self.ss.state()=='normal' and self.options['AllowUse99InGaming']=='False':
                    self.btn1['state']='disable'
                    self.btn2['state']='disable'
                    self.btn3['state']='disable'
                    self.btn4['state']='disable'
                    self.btn5['state']='disable'
                    self.btn6['state']='disable'
                    self.btn_wrongBook['state']='disable'
                    self.btn_settings['state']='disable'
                    self.btn_info['state']='disable'
                elif self.ss.state()=='normal':
                        self.btn1['state']='disable'
                        self.btn2['state']='disable'
                        self.btn3['state']='disable'
                        self.btn4['state']='disable'
                        self.btn5['state']='disable'
                        self.btn6['state']='disable'
                        self.btn_wrongBook['state']='disable'
                        self.btn_settings['state']='disable'
                else:
                    self.btn1['state']='normal'
                    self.btn2['state']='normal'
                    self.btn3['state']='normal'
                    self.btn4['state']='normal'
                    self.btn5['state']='normal'
                    self.btn6['state']='normal'
                    self.btn_wrongBook['state']='normal'
                    self.btn_settings['state']='normal'
            except:
                self.btn1['state']='normal'
                self.btn2['state']='normal'
                self.btn3['state']='normal'
                self.btn4['state']='normal'
                self.btn5['state']='normal'
                self.btn6['state']='normal'
                self.btn_info['state']='normal'
            time.sleep(0.5)
    def Bookcheck(self):#自写算法
        timu=str(self.wrong[self.now])
        yuanti=timu
        szlist=[]
        realsz=[]
        sflist=[]
        while 1:
            try:
                if timu[0]=='+' or timu[0]=='-':
                    if timu[0]=='+':
                        sflist.append('+')
                        timu=timu.replace('+','',1)
                    else:
                        sflist.append('-')
                        timu=timu.replace('-','',1)
                    int(timu)
                    szlist.append(timu)
                    break
                else:
                    int(timu)
                    szlist.append(timu)
                    break
            except:
                sz,sf=self.Bookcheck2(timu)
                szlist.append(sz)
                szlist.append(sf)
                #print(sz,sf)
                a=sz+sf
                timu=timu.replace(a,'',1)
        for i in range(0,len(szlist),2):
            realsz.append(int(szlist[i]))
        for i in range(1,len(szlist),2):
            sflist.append(szlist[i])
        #print(szlist)
        for i in range(0,len(sflist)):
            if sflist[i]=='x' or sflist[i]=='/':
                if sflist[i]=='x':
                    realsz.insert(i,realsz[i]*realsz[i+1])
                    realsz.remove(realsz[i+1])
                    realsz.remove(realsz[i+1])
                elif sflist[i]=='/':
                    realsz.insert(i,realsz[i]/realsz[i+1])
                    realsz.remove(realsz[i+1])
                    realsz.remove(realsz[i+1])
        try:
            sflist.remove('x')
            sflist.remove('/')
        except:
            print(sflist)
        while 1:
            for i in range(0,len(sflist)):
                if sflist[i]=='+':
                    #print(i,realsz)
                    realsz.insert(i,realsz[i]+realsz[i+1])
                    realsz.remove(realsz[i+1])
                    realsz.remove(realsz[i+1])
                    sflist.pop(i)
                    break
                elif sflist[i]=='-':
                    realsz.insert(i,realsz[i]-realsz[i+1])
                    realsz.remove(realsz[i+1])
                    realsz.remove(realsz[i+1])
                    sflist.pop(i)
                    break
            else:
                break
        realsz=realsz[0]
        if type(realsz)==float:
            realsz=round(realsz,2)
        if self.errorentry.get()==str(realsz):
            easygui.msgbox(title='你答对啦！',msg='你答对啦！')
            with open('wrongBook.ini','r') as f:
                txt=f.read()
                f.close()
                txt=txt.replace('\n'+yuanti,'',1)
                with open('wrongBook.ini','w') as f:
                    f.write(txt)
                    f.close()
        else:
            easygui.msgbox(title='很遗憾!',msg='你答错了！\n你需要加强训练了哦！')
        # print(realsz)
    def Bookcheck2(self,timu):
        a=''
        for i in timu:
            try:
                a=a+str(int(i))
            except:
                return a,i
    def chuti(self,num):
        self.mode=num
        self.ss=tk.Toplevel()
        self.ss.title('答题中')
        self.ss.geometry('300x200')
        self.wrongtimu=0
        self.lenstimu=0
        self.lasttime=0
        self.ss.resizable(0,0)
        self.timutext1=tk.Label(self.ss,text='按下回车开始')
        self.timutext1.pack()
        self.timuEntry=tk.Entry(self.ss,width=30)
        self.timuEntry.pack()
        self.stateTime=time.time()
        self.ss.bind('<Return>',self.Next)
        self.ss.mainloop()
    def Next(self,a):
        modes=[10,50,100,1000,10000,10]
        maxnum=modes[self.mode]
        if time.time()-self.lasttime>0.3:
            if self.timutext1['text']!='按下回车开始':
                if not str(self.timudaan)==self.timuEntry.get():
                    #print(self.timudaan,self.timuEntry.get())
                    with open('wrongBook.ini','r') as f:
                        old=f.read()
                        f.close()
                        with open('wrongBook.ini','w') as f:
                            f.write(old+'\n'+self.timutext1['text'])
                            self.wrongtimu+=1
            self.timuEntry.delete(0, 999999)
            if self.lenstimu<int(self.options['num']):
                self.lenstimu+=1
                if 4>=self.mode>=0:
                    sf=['+','-']
                    sf=sf[r.randint(0,1)]
                    if sf=='+':
                        num1=str(r.randint(0,maxnum))
                        num2=str(r.randint(0,maxnum))
                        self.timutext1['text']=num1+'+'+num2
                        self.timudaan=int(num1)+int(num2)
                    elif sf=='-':
                        num1=str(r.randint(0,maxnum))
                        num=str(r.randint(int(num1),maxnum))
                        self.timutext1['text']=num+'-'+num1
                        self.timudaan=int(num)-int(num1)
                elif self.mode==5:
                    sf=['*','/']
                    sf=sf[r.randint(0,1)]
                    if sf=='*':
                        num1=str(r.randint(0,maxnum))
                        num2=str(r.randint(0,maxnum))
                        self.timutext1['text']=num1+'x'+num2
                        self.timudaan=int(num1)*int(num2)
                    elif sf=='/':
                        num1=str(r.randint(0,maxnum))
                        num2=str(r.randint(1,maxnum))
                        self.timutext1['text']=str(int(num1)*int(num2))+'/'+num2
                        self.timudaan=int(num1)
            else:
                self.getResult()
        self.lasttime=time.time()
    def getResult(self):
        if self.options['Timer']=='True':
            self.endtime=time.time()
            easygui.msgbox(title='结束啦！',msg='本次答题%s道，共计错误%d道\n共计用时：%f秒'%(self.options['num'],self.wrongtimu,self.endtime-self.stateTime))
        else:
            easygui.msgbox(title='结束啦！',msg='本次答题%s道，共计错误%d道'%(self.options['num'],self.wrongtimu))
        self.ss.destroy()
        
Main()