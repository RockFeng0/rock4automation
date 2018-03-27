# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.tkui.ui

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.tkui.ui,v 2.0 2017年2月7日
    FROM:   2016年7月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import Tkinter,Tkconstants


ROOT = Tkinter.Tk()


import basic
class Window:    
    widg = None
    
    @classmethod
    def Top(cls,title,geometry="", resizable_x = 0, resizable_y = 0):
#         geometry = 510x140+200+200
        top = basic.get_widget_toplevel(cls.widg)
        top.title(title)
        top.geometry(geometry)
        top.resizable(resizable_x,resizable_y) 
    
    @classmethod
    def Pack(cls,side = Tkconstants.TOP, fill = Tkconstants.NONE, expand = Tkconstants.NO, pady = 0, padx = 0, anchor = "center",**kw):
        # padx,pady-表示外边距; ipadx,ipady-表示内边距; 如 padx = 20, pady="2c"; 默认单位为像素，可选单位为c（厘米）、m（毫米）、i（英寸）、p（打印机的点，即1/27英寸）用法为在值后加以上一个后缀既可。
        cls.widg.pack(side = side,fill = fill, expand = expand, pady = pady, padx = padx, anchor = anchor, **kw)
    
    @classmethod
    def Grid(cls,row=0,column=0,sticky="", **kw):
        cls.widg.grid(row = row, column = column, sticky = sticky, **kw)
        
    @classmethod
    def Config(cls,**conf):
        keys = basic.get_configuration_keys(cls.widg)
        for k in conf:
            if not k in keys:
                raise Exception("invalide configuration key: %s" %k)
        basic.set_configuration(cls.widg,**conf)
    
    @classmethod
    def ConfigVar(cls,var_key="listvariable"):        
        '''Sample usage:
                var = ConfigVar("textvariable")
                var.set("set values")
                print var.get()
        '''
        confs = {}
        confs[var_key] = Tkinter.StringVar()
        basic.set_configuration(cls.widg,**confs)
        return confs.get(var_key)    
    
    @classmethod
    def TextTagConfig(cls,tag_name,font = None ,background = None, foreground = None, relief = None):
        '''
        Param:
            font -->参数 顺序：  family size weight slant  ; 如 u"宋体    12", "Courier", "Courier 14", "Courier 14 normal roman"
            background,foreground --> 颜色号, 可以用  英文/HEX/RGB
            relief --> 参数值为:  flat raised  sunken
        Sample usage:    
            tx = Widget.Text(ROOT)
            Window.widg = tx
            Window.TextTagConfig("t_tag", u"宋体   12 normal italic", foreground="red")
            Window.Pack()
            tx.insert("end", u"你好呀啊啊 \n", "t_tag")
            tx.insert("end", "osidfsdf\n", "t_tag")
            tx.insert("end", tx.tag_names(), "t_tag")
            ROOT.mainloop()
        '''        
        cls.widg.tag_configure(tag_name,font = font ,background = background, foreground = foreground, relief = relief)
#         all_tags = cls.widg.tag_names()
#         print all_tags
#         cls.widg.tag_delete(tag_name)
                        
      
    @classmethod  
    def Bind(cls, sequence=None, func=None, add=None, className=None):
        '''Sample usage:
            def printkey(event):
                print('你按下了: ' + event.char)
            entry = Widget.Entry(ROOT)
            Window.widg = entry    
            Window.Pack()
            
            entry1 = Widget.Entry(ROOT)
            Window.widg = entry1    
            Window.Pack()    
            Window.Bind("<Key>", printkey,className="all")
            
            ROOT.mainloop()            
        '''
        if className == None:
            return cls.widg.bind(sequence, func, add)
        elif className.lower() == "all":
            return cls.widg.bind_all(sequence, func, add)
        else:
            return cls.widg.bind_class(className, sequence, func, add)

    @classmethod
    def UnBind(cls, sequence, className = None):
        if className == None:
            return cls.widg.unbind(sequence)
        elif className.lower() == "all":
            return cls.widg.unbind_all(sequence)
        else:
            return cls.widg.unbind_class(className, sequence)

        
import ttk
class Widget:
    '''"
    Not packing:
        Combobox", "Frame",
       "Menubutton", "Notebook",
       "Scale","Separator", "Sizegrip", "Style",       
    '''
            
    @classmethod
    def NewTop(cls):
        return Tkinter.Toplevel()
        
    @classmethod
    def Labelframe(cls,master=None, **kw):
        return ttk.Labelframe(master,**kw)
    
    @classmethod
    def Panedwindow(cls,master=None, **kw):
        return ttk.PanedWindow(master, **kw)
    
    @classmethod
    def Progressbar(cls,master,**kw):
        return ttk.Progressbar(master,**kw)
    
    @classmethod
    def Label(cls,master,**kw):
        return ttk.Label(master,**kw)
    
    @classmethod
    def Entry(cls,master,**kw):
        return ttk.Entry(master,**kw)
    
    @classmethod
    def Radiobutton(cls,master,**kw):
        return ttk.Radiobutton(master,**kw)
    
    @classmethod
    def Checkbutton(cls,master,**kw):
        return ttk.Checkbutton(master,**kw)
    
    @classmethod
    def Scrollbar(cls,master,**kw):
        return ttk.Scrollbar(master,**kw)
#         return Tkinter.Scrollbar(master,**kw)
    
    @classmethod
    def Treeview(cls,master,**kw):
        return ttk.Treeview(master,**kw)
        
    @classmethod
    def Button(cls,master,**kw):
        return ttk.Button(master,**kw)
    
    @classmethod
    def Text(cls,master=None, cnf={}, **kw):
        return Tkinter.Text(master, cnf, **kw)
         
    @classmethod
    def Listbox(cls,master=None, cnf={}, **kw):
        return Tkinter.Listbox(master, cnf, **kw)    
    
    @classmethod
    def Menu(cls,master=None, cnf={}, **kw):
        return Tkinter.Menu(master, cnf, **kw)

