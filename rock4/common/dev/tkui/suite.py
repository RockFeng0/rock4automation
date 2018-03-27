# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.tkui.suite

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.tkui.suite,v 2.0 2017年2月7日
    FROM:   2016年7月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import basic
from ui import Widget,Window,Tkconstants,Tkinter
from basic import TkFont 


class Components:
    
    @classmethod
    def GenerateMenu(cls,menubar_obj,title_tree,var,leaf=0):
        '''Sample usage:
            from com.ui import ROOT
            menubar = Widget.Menu(ROOT)
            
            Window.widg = ROOT
            Window.Config(menu = menubar)
            ROOT.option_add("*Menu.tearOff", 0)  
            result = {}
            menus = [
                 {u"执行":[u"运行当前",u"速度"]}, 
                 {u"导航":{u"呃呃":[u"得分",u"很好"]}},         
                 ]
            
            Components.GenerateMenu(menubar, menus, result)
            
            
            def test(*args):
                print args[0]
            node = result.get(u"执行")
            Components.RegisterMenu(node, u"运行当前", test, "webservice")
            node = result.get(u"呃呃")
            Components.RegisterMenu(node, u"得分", test, "current")
            ROOT.mainloop()
        '''
        if isinstance(title_tree,list):
            for i in title_tree:
                cls.GenerateMenu(menubar_obj,i,var,leaf=1);#列表格式，里边放是叶子节点,设置leaf=1
                
        elif isinstance(title_tree,dict):
            # 字典格式，里边的子节点，不是叶子节点，设置leaf=0
            for k,v in title_tree.items():             
                var[k] = Tkinter.Menu();# 记录每一个Menu子节点的实例对象
                menubar_obj.add("cascade",label=k, menu = var[k]);# cascade允许 menu参数，建立 Menu item                    
                cls.GenerateMenu(var[k],v,var,leaf=0)
        else:
            # 叶子节点
            if leaf == 0:
                var[title_tree] = Tkinter.Menu()
                menubar_obj.add("cascade",label=title_tree, menu = var[title_tree])
            else:
                # command没有menu参数,建立叶子节点
                # accelerator 选项设置 快捷键, 如  accelerator = "Ctrl + A"
                menubar_obj.add("command",label=title_tree, accelerator = None)
                
    @classmethod
    def RegisterMenu(cls,menu_node,menu_leaf_name,function,*func_args):
        command = basic.register_command(menu_node, function, *func_args)
        leaf_index = menu_node.index(menu_leaf_name)
        menu_node.delete(leaf_index)
        menu_node.insert_command(leaf_index,label=menu_leaf_name,command=command)
        
    @classmethod
    def ListWithScrollbar(cls,master):
        '''Sample usage:
            from com.ui import ROOT    
            frame1 = Widget.Labelframe(ROOT,text = "sssss")
            frame1.rowconfigure(0,weight =1, minsize = 0)
            frame1.columnconfigure(0,weight =1, minsize = 0)
            Window.widg = frame1
            Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
                
            (l,x,y) = Components.ListWithScrollbar(frame1)
            elems = ["Don't speculate, measure", "Waste not, want not", "Early to bed and early to rise makes a man healthy, wealthy, and wise", "Ask not what your country can do for you, ask what you can do for your country", "I shall return", "NOT", "A picture is worth a thousand words", "User interfaces are hard to build", "Thou shalt not steal", "A penny for your thoughts", "Fool me once, shame on you;  fool me twice, shame on me", "Every cloud has a silver lining", "Where there's smoke there's fire", "It takes one to know one", "Curiosity killed the cat", "Take this job and shove it", "Up a creek without a paddle", "I'm mad as hell and I'm not going to take it any more", "An apple a day keeps the doctor away", "Don't look a gift horse in the mouth", "Measure twice, cut once"]
            l.insert(0,*elems)
            ROOT.mainloop()
        '''
        f = TkFont()        
        lb = Widget.Listbox(master, width = 60, height = 24, font = f.font, setgrid = 1)
        s_x = Widget.Scrollbar(master,orient = Tkconstants.HORIZONTAL, command = lb.xview)
        s_y = Widget.Scrollbar(master,orient = Tkconstants.VERTICAL, command = lb.yview)
          
        Window.widg = s_y
        Window.Pack(side = "right", fill = "y")
          
        Window.widg = s_x
        Window.Pack(side = "bottom", fill = "x")
          
        Window.widg = lb
        Window.Config(xscrollcommand = s_x.set, yscrollcommand = s_y.set)
        Window.Pack(side = "top",fill = "both", expand = "yes") 
        
#         lb = Widget.Listbox(master, width = 20, height = 10, setgrid = 1)
#         s_x = Widget.Scrollbar(master,orient = Tkconstants.HORIZONTAL, command = lb.xview)
#         s_y = Widget.Scrollbar(master,orient = Tkconstants.VERTICAL, command = lb.yview)
#           
#         Window.widg = lb
#         Window.Config(xscrollcommand = s_x.set, yscrollcommand = s_y.set)
#         Window.Grid(row =0, column = 0, rowspan = 1, columnspan = 1, sticky = Tkconstants.NSEW)
#         
#         Window.widg = s_y
#         Window.Grid(row =0, column = 1, rowspan = 1, columnspan = 1, sticky = Tkconstants.NSEW)
#         
#         Window.widg = s_x
#         Window.Grid(row =1, column = 0, rowspan = 1, columnspan = 1, sticky = Tkconstants.NSEW)       
        
        return (lb,s_x,s_y)

    @classmethod
    def TextWithScrollbar(cls, master):
        '''Sample usage:
            from com.ui import ROOT    
            frame1 = Widget.Labelframe(ROOT,text = "XXXX")
            Window.widg = frame1        
            Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
            
            (t,x,y) = Components.TextWithScrollbar(frame1)    
            t.insert("end","0.ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n")
            t.insert("end","1.sdf\n")    
            ROOT.mainloop()
        '''
        f = TkFont()
        # wrap -->设置当一行文本的长度超过width选项设置的宽度时，是否换行; "none"不自动换行, "char"按字符自动换行, "word"按单词自动换行
        # undo -->设置文本 是否可以 撤销 和 恢复; 默认值是  0 或者 False,表示没有开启
        tx = Widget.Text(master, width = 60, height = 24, font = f.font, wrap = "word", setgrid = 1, undo = True, background = "white")
        s_x = Widget.Scrollbar(master,orient = Tkconstants.HORIZONTAL, command = tx.xview)
        s_y = Widget.Scrollbar(master,orient = Tkconstants.VERTICAL, command = tx.yview)
        
        Window.widg = s_y
        Window.Pack(side = "right", fill = "y")
        
        Window.widg = s_x
        Window.Pack(side = "bottom", fill = "x")
        
        Window.widg = tx
        Window.Config(xscrollcommand = s_x.set, yscrollcommand = s_y.set)
        Window.Pack(side = "top",fill = "both", expand = "yes")       
        
        return (tx,s_x,s_y)
    
    @classmethod
    def LabelWithEntryAndButton(cls, master, grid_tree):
        '''Sample usage
            from com.ui import ROOT    
            frame1 = Widget.Labelframe(ROOT,text = "YYYY")
            Window.widg = frame1        
            Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
            
            grid_tree = [
                        [(u"用户名:", u"登录")],
                        [(u"密码:", ""),(u"验证码:", "")], 
                    ]
            widgets = Components.LabelWithEntryAndButton(frame1, grid_tree)
            widgets[0][1].insert("end","hi handsome boy.")    
            ROOT.mainloop()
        '''
        result = []
        rows = len(grid_tree)
        for row in range(rows):
            result.append([])
            column = -1
            
            groups = grid_tree[row]
            for lable_name,button_name in groups:
                column = column + 1
                label           = Widget.Label(master, text = lable_name)
                result[row].append(label)
                Window.widg     = label
                Window.Grid(row, column, "w")
                
                column = column + 1
                entry           = Widget.Entry(master)
                result[row].append(entry)
                Window.widg     = entry
                Window.Grid(row, column, "ew")
                
                if button_name:
                    column = column + 1
                    button      = Widget.Button(master, text = button_name)
                    result[row].append(button)
                    Window.widg = button
                    Window.Grid(row, column, "e")
        return result 
    
    @classmethod
    def PaneWithLabelframe(cls, master,f_name,s_name, orient = Tkconstants.HORIZONTAL):
        '''Sample usage:
            from com.ui import ROOT    
            (frame1, frame2) = Components.PaneWithLabelframe(ROOT, "frame1", "frame2")[1:]
            Window.widg = Widget.Button(frame1,text = "button1")
            Window.Pack()
            
            Window.widg = Widget.Button(frame2,text = "button2")
            Window.Pack()
            ROOT.mainloop()
        '''
        p = Widget.Panedwindow(master, orient = orient)
        l1 = Widget.Labelframe(master, text = f_name)
        l2 = Widget.Labelframe(master, text = s_name)
        p.add(l1)
        p.add(l2)        
        Window.widg = p
        Window.Pack(side = "top", fill = Tkconstants.BOTH, expand = Tkconstants.YES, pady = 2, padx = 2)
        
        return (p,l1,l2)
    
    @classmethod
    def TreeviewWithScrollbar(cls, master, head_names):
        '''Sample usage:
            from com.ui import ROOT    
            heads = [u"第一列", u"第二列"]
            datas = [("Argentina","Buenos Aires"),("Australia","Canberra"),("Brazil","Brazilia"),("Canada","Ottawa"),("China","Beijing"),("France","Paris")]    
            tree = Components.TreeviewWithScrollbar(ROOT,heads)[0]
            # Add
            items_list = []
            for data in datas:
                items_list.append(tree.insert("", "end", values = data))
            print "all items: ", items_list
                    
            # Select
            print tree.column('col0')
            
            tree.selection_set("I001")
            print "current selection: ", tree.selection()
            print "current index: ", tree.index("I001")
            
            tree.tag_configure("t_tag", font = u"宋体   12 normal italic", foreground="red")
            tree.item('I001',tags = "t_tag")
            
            item_info = tree.item('I001')
            print "item info: ", item_info
            
            # Update
            c_value = ("Oh", "Handsome boy.")
            tree.item('I001',values = c_value)
            print "%s changing to %s" %(datas[tree.index("I001")], c_value)       
            
            print "item value dict: %s" %tree.set("I002")
            print "column value: %s" %tree.set("I002","col0")
            print "set column value to 'HaLo'"
            tree.set("I002","col0","Halo")
            
            # Delete
            tree.delete("I006")
            print "deleted France item."
            
            ROOT.mainloop()   
        '''  
        
        columns = []
        for i in range(len(head_names)):
            columns.append("col%d" %i)
        columns_and_headnames = zip(columns,head_names)
            
        t = Widget.Treeview(master, columns = columns, show = "headings")
        for (col,text) in columns_and_headnames:
            t.column(col, width = 100, anchor = "center")
            t.heading(col,text = text)    
        
        s_x = Widget.Scrollbar(master,orient = Tkconstants.HORIZONTAL, command = t.xview)
        s_y = Widget.Scrollbar(master,orient = Tkconstants.VERTICAL, command = t.yview)
                
        Window.widg = s_y
        Window.Pack(side = "right", fill = "y")
        
        Window.widg = s_x
        Window.Pack(side = "bottom", fill = "x")
        
        Window.widg = t
        Window.Config(xscrollcommand = s_x.set, yscrollcommand = s_y.set)
        Window.Pack(side = "top",fill = "both", expand = "yes", pady = 2, padx = 2)
        
        return (t, s_x, s_y)
    
    @classmethod
    def RadioWithLabelframe(cls, master, texts=[],values=[], command=None):
        '''Sample usage:
            from ui import ROOT    
            frame1 = Widget.Labelframe(ROOT,text = "XXXX")
            Window.widg = frame1        
            Window.Pack(side = "left", fill="both", expand="no", padx = "0.2c")
                    
            frame2 = None
            def test(a):
                print a
                if frame2:
                    frame2.config(text = var.get())
                    t.delete("1.0","end")
                    t.insert("end",var.get())
                
            var,rds = Components.RadioWithLabelframe(frame1, texts = [1,2,3,4,5], values = [1,2,3,4,5], command = lambda: test("if command has parameter; please use lambda.like this"))
            
            frame2 = Widget.Labelframe(ROOT,text = "YYYY")        
            Window.widg = frame2
            Window.Pack(side = "left", fill="both", expand="yes", padx = "0.2c")
            (t,x,y) = Components.TextWithScrollbar(frame2)
                    
            ROOT.mainloop()
        '''
        radios = []
        var = Tkinter.StringVar()
        radio_items = dict(zip(texts,values))
        for text,value in radio_items.items():
            Window.widg = Widget.Radiobutton(master, variable = var)
            Window.Config(text = text, value = value)
            if command:
                Window.Config(command = command)
            Window.Pack(side = "top", fill="x", expand = "yes", pady = 2, anchor = "w")
            radios.append(Window.widg)
        
        if radios:
            return var,radios            
        
    
if __name__ == "__main__":
    from ui import ROOT    
    frame1 = Widget.Labelframe(ROOT,text = "XXXX")
    Window.widg = frame1        
    Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
    
    (t,x,y) = Components.TextWithScrollbar(frame1)    
    t.insert("end","0.ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n")
    t.insert("end","1.sdf\n")
    t.insert("end",1)
    ROOT.mainloop()
    
    
    
