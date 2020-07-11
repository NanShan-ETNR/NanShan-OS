import os, sys
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk
import tkinter.ttk
import time
import random
import pickle
import win32api
import win32ui
import win32con
import pyautogui

global SCREEN_X
global SCREEN_Y
SCREEN_X, SCREEN_Y = pyautogui.size()
pyautogui.FAILSAFE = False

root = tkinter.Tk()
root.state("zoomed")
root.geometry('%sx%s' % (SCREEN_X,SCREEN_Y))
root.minsize(SCREEN_X,SCREEN_Y)
root.overrideredirect(True)
root.configure(background='black')
root.update()
global tmp
tmp = {}

tkinter.ttk.Style().configure('Root.EveryButtons',font=('等线',8))

time.sleep(3)
root.configure(background='blue')
lts = tkinter.Label(root,text='NanShan OS Installer安装程序\n=================================',bg='blue',fg='white',compound='left',font=('宋体',18))
lts.place(x=5,y=50)

def run():
     def clo():pass

     myroot = tkinter.Tk()
     myroot.title('NanShan OS安装程序')
     myroot.iconbitmap('install.ico')
     myroot.geometry('800x500+%s+%s' % (SCREEN_X//2-400,SCREEN_Y//2-250))
     myroot.maxsize(800,500)
     myroot.minsize(800,500)
     myroot.protocol("WM_DELETE_WINDOW",clo)

     weyno1 = tkinter.Label(myroot,text="我们将在你的电脑上安装NanShan OS",font=('等线',15))
     weyno1.place(x=10,y=20)
     weyno2 = tkinter.Label(myroot,text="由于我们检测到你的电脑上有其他文件，我们将要格式化你的磁盘，然后重新创建分区。",font=('等线',8))
     weyno2.place(x=10,y=60)
     weyno3 = tkinter.Label(myroot,text="首先，请你设置分区：",font=('等线',8))
     weyno3.place(x=10,y=130)

     columns = ("分区", "大小")
     f = tkinter.Frame(myroot,width=450,height=280)
     s1 = tkinter.Scrollbar(f,orient=tkinter.VERTICAL)
     tt4 = tkinter.Text(f,height=3,width=150)
     global weytr1
     weytr1 = ttk.Treeview(f, height=4, yscrollcommand=s1.set, show="headings", columns=columns)
     s1.pack(side=tkinter.RIGHT,fill=tkinter.Y)
     s1.config(command=weytr1.yview)
     weytr1.pack(fill=tkinter.BOTH)
     f.place(x=10,y=150)
     weytr1.column("分区", width=300, anchor='center')
     weytr1.column("大小", width=450, anchor='center')
     weytr1.heading("分区", text="分区")
     weytr1.heading("大小", text="大小(GB)")
     global name
     name = ['C:\\']
     global big
     ipcode = ['32']
     weytr1.insert('', 0, values=('C:\\','32'))

     def treeview_sort_column(tv, col, reverse):
          l = [(tv.set(k, col), k) for k in tv.get_children('')]
          l.sort(reverse=reverse)
          for index, (val, k) in enumerate(l):
               tv.move(k, '', index)
          tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

     def set_cell_value(event):
          treeview = weytr1
          for item in treeview.selection():
               item_text = treeview.item(item, "values")
          column = '#1' if event.x > 0 and event.x <= 300 else '#2'
          entryedit = Text(myroot,width=15,height = 1)
          entryedit.place(x=10,y=270)
          def saveedit():
               treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
               ur = int(item[1:]) - 1
               if column == '#1':
                    name[ur] = entryedit.get(0.0, "end")[:-1]
               if column == '#2':
                    ipcode[ur] = entryedit.get(0.0, "end")[:-1]
               entryedit.destroy()
               okb.destroy()
          okb = ttk.Button(myroot, text='OK', width=4, command=saveedit)
          okb.place(x=10+15*8,y=270)

     def newrow():
          treeview = weytr1
          name.append(chr(ord(name[len(name)-1][0])+1)+name[len(name)-1][1:])
          ipcode.append('32')
          treeview.insert('',len(name)-1, values=(name[len(name)-1], ipcode[len(name)-1]))
          treeview.update()

     weytr1.bind('<Double-1>', set_cell_value)

     newb = ttk.Button(myroot, text='新建分区', command=newrow)
     newb.place(x=700,y=110)

     weyno4 = tkinter.Label(myroot,text="接下来，请你设置格式化设置：",font=('等线',8))
     weyno4.place(x=10,y=300)

     weynt1 = tkinter.Label(myroot,text='文件系统：',font=('等线',8))
     weynt1.place(x=10,y=330)
     comvaluea=tkinter.StringVar()
     comboxlista=ttk.Combobox(myroot,textvariable=comvaluea,state='readonly') 
     comboxlista["values"]=("NanShan File System","NTFS","FAT32")  
     comboxlista.current(0)
     comboxlista.place(x=80,y=330)

     weynt2 = tkinter.Label(myroot,text='分配单元大小(KB)：',font=('等线',8))
     weynt2.place(x=300,y=330)
     comvalueb=tkinter.IntVar()
     comboxlistb=ttk.Combobox(myroot,textvariable=comvalueb,state='readonly') 
     comboxlistb["values"]=(4,8,16,32,64,128,256,512,1024,2048)  
     comboxlistb.current(0)
     comboxlistb.place(x=410,y=330)

     weyno5 = tkinter.Label(myroot,text="最后，请你开始格式化：",font=('等线',8))
     weyno5.place(x=10,y=370)

     def nextnote():
          tmp['partition'] = {}
          for i in range(len(name)):
               tmp['partition'][name[i]] = ipcode[i]
          weyno2.configure(text='我们正在格式化你的电脑……这可能需要几分钟')
          weyno3.place_forget()
          weyno4.place_forget()
          weyno5.place_forget()
          weynt1.place_forget()
          weynt2.place_forget()
          f.place_forget()
          newb.place_forget()
          comboxlista.place_forget()
          comboxlistb.place_forget()
          weygo.place_forget()
          
          canvas = tkinter.Canvas(myroot, width=780, height=22, bg="blue")
          canvas.place(x=10, y=150)
          fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
          x = random.randint(500,1500)
          n = 780 / x
          trali1 = tkinter.Label(myroot,text='当前状态：正在格式化磁盘',font=('等线',8))
          trali1.place(x=10,y=176)
          for i in range(x):
               n = n + 780 / x
               canvas.coords(fill_line, (0, 0, n, 60))
               myroot.update()
               time.sleep(random.uniform(0.01,0.05))
               urt = float(i) / float(x)
               if urt >= 0.5 and urt < 0.8:
                    trali1.configure(text='当前状态：正在创建分区')
               if urt >= 0.8 and urt < 0.95:
                    trali1.configure(text='当前状态：正在格式化分区')
               if urt >= 0.95:
                    trali1.configure(text='当前状态：正在检查是否出现错误')
          fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
          x = 190
          n = 780 / x
          for t in range(x):
               n = n + 780 / x
               canvas.coords(fill_line, (0, 0, n, 60))
               myroot.update()
               time.sleep(0)
          trali1.configure(text='当前状态：完成格式化')

          def nextnextnote():
               weyno2.configure(text='请你完善账号信息以便于电脑使用')
               canvas.place_forget()
               trali1.place_forget()
               trali2.place_forget()

               usat1 = tkinter.Label(myroot,text="*你的姓名",font=('等线',8),fg='red')
               usat1.place(x=10,y=110)
               ustt1 = ttk.Entry(myroot)
               ustt1.place(x=100,y=105)

               usat2 = tkinter.Label(myroot,text="你的电子邮箱地址",font=('等线',8))
               usat2.place(x=10,y=150)
               ustt2 = ttk.Entry(myroot)
               ustt2.place(x=150,y=145)

               usat3 = tkinter.Label(myroot,text="*管理员账户",font=('等线',8),fg='red')
               usat3.place(x=10,y=190)
               ustt3 = ttk.Entry(myroot)
               ustt3.place(x=120,y=185)

               usat4 = tkinter.Label(myroot,text="*管理员密码",font=('等线',8),fg='red')
               usat4.place(x=10,y=230)
               ustt4 = ttk.Entry(myroot,show='*')
               ustt4.place(x=120,y=225)

               columns = ("访客账户", "访客密码")
               f = tkinter.Frame(myroot,width=450,height=225-110)
               s1 = tkinter.Scrollbar(f,orient=tkinter.VERTICAL)
               tt4 = tkinter.Text(f,height=3,width=150)
               global weytr7
               weytr7 = ttk.Treeview(f, height=4, yscrollcommand=s1.set, show="headings", columns=columns)
               s1.pack(side=tkinter.RIGHT,fill=tkinter.Y)
               s1.config(command=weytr7.yview)
               weytr7.pack(fill=tkinter.BOTH)
               f.place(x=320,y=110)
               weytr7.column("访客账户", width=200, anchor='center')
               weytr7.column("访客密码", width=250, anchor='center')
               weytr7.heading("访客账户", text="访客账户")
               weytr7.heading("访客密码", text="访客密码")
               global fk
               fk = ['visitor']
               global ma
               ma = ['']
               weytr7.insert('', 0, values=('visitor',''))

               def treeview_sort_column(tv, col, reverse):
                    l = [(tv.set(k, col), k) for k in tv.get_children('')]
                    l.sort(reverse=reverse)
                    for index, (val, k) in enumerate(l):
                         tv.move(k, '', index)
                    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

               def set_cell_value(event):
                    treeview = weytr7
                    for item in treeview.selection():
                         item_text = treeview.item(item, "values")
                    column = '#1' if event.x > 0 and event.x <= 300 else '#2'
                    entryedit = Entry(myroot,width=15)
                    if column == '#2':
                         entryedit.configure(show='*')
                    entryedit.place(x=320,y=225)
                    def saveedit():
                         treeview.set(item, column=column, value=entryedit.get())
                         ur = int(item[1:]) - 1
                         if column == '#1':
                              fk[ur] = entryedit.get()[:-1]
                         if column == '#2':
                              ma[ur] = entryedit.get()[:-1]
                         entryedit.destroy()
                         okb.destroy()
                    okb = ttk.Button(myroot, text='OK', width=4, command=saveedit)
                    okb.place(x=320+15*8,y=225)

               def newrow():
                    treeview = weytr7
                    fk.append('visitor')
                    ma.append('')
                    treeview.insert('',len(fk)-1, values=('visitor',''))
                    treeview.update()

               weytr7.bind('<Double-1>', set_cell_value)

               newc = ttk.Button(myroot, text='新建访客账户', command=newrow)
               newc.place(x=650,y=225)

               def nextnextnextnote():
                    tmp['visitors'] = {}
                    for i in range(len(fk)):
                         tmp['visitors'][fk[i]] = ma[i]
                    tmp['name'] = ustt1.get()
                    tmp['email'] = ustt2.get()
                    tmp['user'] = ustt3.get()
                    tmp['pass'] = ustt4.get()
                    if ustt1.get() == '' or ustt3.get() == '' or ustt4.get() == '':
                         showinfo('NanShan OS Installer','请您将关键信息填写完整！',parent=myroot)
                         return
                    weyno1.configure(text="我们已经随时准备开始安装")
                    weyno2.configure(text="点击“安装”以进行NanShan OS的正式安装")
                    usat1.place_forget()
                    usat2.place_forget()
                    usat3.place_forget()
                    usat4.place_forget()
                    ustt1.place_forget()
                    ustt2.place_forget()
                    ustt3.place_forget()
                    ustt4.place_forget()
                    f.place_forget()
                    newc.place_forget()
                    heigo.place_forget()
                    
                    def install():
                         leigo.place_forget()
                         weyno1.configure(text="正在安装NanShan OS")
                         weyno2.place_forget()
                    
                         canvas = tkinter.Canvas(myroot, width=780, height=22, bg="blue")
                         canvas.place(x=10, y=150)
                         fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                         x = random.randint(1500,5000)
                         n = 780 / x
                         trali1 = tkinter.Label(myroot,text='当前状态：正在复制文件',font=('等线',8))
                         trali1.place(x=10,y=176)
                         for i in range(x):
                              n = n + 780 / x
                              canvas.coords(fill_line, (0, 0, n, 60))
                              myroot.update()
                              time.sleep(random.uniform(0.01,0.05))
                              urt = float(i) / float(x)
                              if urt >= 0.15 and urt < 0.25:
                                   trali1.configure(text='当前状态：正在准备需要安装的文件')
                              if urt >= 0.25 and urt < 0.4:
                                   trali1.configure(text='当前状态：正在安装内核')
                              if urt >= 0.4 and urt < 0.7:
                                   trali1.configure(text='当前状态：正在安装功能')
                              if urt >= 0.7 and urt < 0.9:
                                   trali1.configure(text='当前状态：正在安装更新')
                              if urt >= 0.9:
                                   trali1.configure(text='当前状态：正在完成')
                         fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
                         x = 190
                         n = 780 / x
                         for t in range(x):
                              n = n + 780 / x
                              canvas.coords(fill_line, (0, 0, n, 60))
                              myroot.update()
                              time.sleep(0)
                         trali1.configure(text='当前状态：已完成安装')

                         def done():
                              zeigo.place_forget()
                              trali1.place_forget()
                              canvas.place_forget()
                              weyno1.place_forget()
                              myroot.destroy()
                              f = open('temp.tmp','wb')
                              pickle.dump(tmp,f)
                              f.close()
                              lts.place_forget()
                              root.configure(background="black")
                              root.update()
                              global imag
                              imag = ImageTk.PhotoImage(file='NanShanLOGO.png')
                              urst = tkinter.Label(root,image=imag,bg='black')
                              urst.place(x=SCREEN_X//2-256//2,y=200)
                              
                              time.sleep(random.randint(2,3))

                              atr1 = tkinter.Label(root,text='正在重启...',bg='black',fg='white')
                              atr1.place(x=10,y=510)
                              ctr1 = tkinter.Canvas(root, width=SCREEN_X, height=5, bg='black')
                              ctr1.place(x=0, y=500)
                              fill_line = ctr1.create_rectangle(1.5, 1.5, 0, 23, width=0, fill='blue')
                              x = 100
                              n = SCREEN_X / x
                              for i in range(x):
                                   n = n + SCREEN_X / x
                                   ctr1.coords(fill_line, (0, 0, n, 60))
                                   root.update()
                                   time.sleep(random.uniform(0.01,0.05))
                              fill_line = ctr1.create_rectangle(1.5, 1.5, 0, 23, width=0, fill='blue')
                              x = 5
                              n = SCREEN_X / x
                              for t in range(x):
                                   n = n + SCREEN_X / x
                                   ctr1.coords(fill_line, (0, 0, n, 60))
                                   root.update()
                                   time.sleep(0)

                              time.sleep(1)
                              urst.place_forget()
                              ctr1.place_forget()
                              atr1.place_forget()
                              root.update()

                              time.sleep(3)
                              root.configure(background='cyan')
                              for i in range(9):
                                   tkinter.Label(root,bg='cyan').pack()
                              auss = tkinter.Label(root,text='我们正在为你的电脑进行相关配置。',bg='cyan',font=('等线',40))
                              auss.pack()
                              uuss = tkinter.Label(root,text='这可能需要几分钟时间...',bg='cyan',font=('等线',20))
                              uuss.pack()
                              root.update()

                              time.sleep(random.randint(20,60))

                              root.destroy()

                              f = open('temp.tmp','rb')
                              data = pickle.load(f)
                              urn = 0
                              for i in data['partition']:
                                   t = 'Files\\%s' % (i if not ':\\' in i else i[:-2])
                                   os.mkdir(t)
                                   if urn == 0:
                                        uznt = t
                                        os.mkdir(t+'\\Users')
                                   os.mkdir(t+'\\Program')
                                   urn += 1
                              for i in data['visitors']:
                                   os.mkdir(uznt+'\\Users\\'+i)
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Photo')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Document')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Desktop')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Download')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Music')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Movie')
                                   os.mkdir(uznt+'\\Users\\'+i+'\\Apps')
                              os.mkdir(uznt+'\\Users\\Administration')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user'])
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Photo')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Document')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Desktop')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Download')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Music')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Movie')
                              os.mkdir(uznt+'\\Users\\Administration\\'+data['user']+'\\Apps')

                              import NanShanrun
                         
                         zeigo = ttk.Button(myroot,text='完成并重启',command=done)
                         zeigo.place(x=10,y=400)
                    
                    leigo = ttk.Button(myroot,text='安装',command=install)
                    leigo.place(x=10,y=400)
                    
               heigo = ttk.Button(myroot,text="继续",command=nextnextnextnote)
               heigo.place(x=10,y=400)
          
          trali2 = ttk.Button(myroot,text='继续',command=nextnextnote)
          trali2.place(x=10,y=400)

     weygo = ttk.Button(myroot,text="开始格式化",command=nextnote)
     weygo.place(x=10,y=400)

     myroot.mainloop()


def goclo():
     root.destroy()
     exit()

nowroot = tkinter.Toplevel(root)
nowroot.title('NanShan OS安装程序')
nowroot.iconbitmap('install.ico')
nowroot.geometry('800x500+%s+%s' % (SCREEN_X//2-400,SCREEN_Y//2-250))
nowroot.maxsize(800,500)
nowroot.minsize(800,500)
nowroot.configure(background='blue')
nowroot.protocol("WM_DELETE_WINDOW",goclo)

global img
img = ImageTk.PhotoImage(file='NanShan.png')
tkinter.Label(nowroot,bg='blue',image=img).pack()

for i in range(5):
     tkinter.Label(nowroot,bg='blue',fg='white').pack()

style = ttk.Style()
style.configure("BW.TLabel", foreground="white", background="blue")

canvas = tkinter.Canvas(nowroot,bg='blue',width=126,height=23)
canvas.create_rectangle(0,0,126,23,width=1)
canvas.place(x=335,y=249)

def go():
     nowroot.destroy()
     run()

ttk.Button(nowroot,text='开始安装NanShan OS',style="BW.TLabel",command=go).pack()

nowroot.mainloop()
