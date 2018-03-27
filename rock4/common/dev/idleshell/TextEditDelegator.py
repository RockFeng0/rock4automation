# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.idleshell.TextEditDelegator

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.idleshell.TextEditDelegator,v 2.0 2017年2月7日
    FROM:   2016年8月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


from idlelib.ColorDelegator import ColorDelegator
from idlelib.Percolator import Percolator
from SimpleAutoComplete import SimpleAutoComplete
   
class TextEditDelegator():
    '''
        from pyrunner.tkui.suite import Components
        from pyrunner.tkui.ui import ROOT,Widget,Window
           
        frame1 = Widget.Labelframe(ROOT,text = "XXXX")
        Window.widg = frame1        
        Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
         
        (t,x,y) = Components.TextWithScrollbar(frame1)
         
        a = TextEditDelegator(t)    
        a.effect_on_text("STRING", {'font': u"Calibri 10 normal roman",'foreground': 'red','background': '#ffffff'})
         
        t.insert("end","0.ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n")
        t.insert("end","1.sdf\n")  
        ROOT.mainloop()
    '''
    def __init__(self, master, rpcclt = None):
        self.text = master
        self.color_delegator = ColorDelegator()      
        self.auto_complete = SimpleAutoComplete(master = master, rpcclt = rpcclt)
            
    def effect_on_text(self, tag_name = None, value = None):
        p = Percolator(self.text)
        if tag_name and value:
            self.__set_idlelib_tag_defs(tag_name, value)            
        p.insertfilter(self.color_delegator)
        
        self.__add_common_event()
    
    def __set_idlelib_tag_defs(self, tag_name, value):
        ''' parameter:
            tag_name --> should be in ColorDelegator().tagdefs.keys(); they are ("COMMENT", "DEFINITION", "BUILTIN", "hit", "STRING", "KEYWORD", "ERROR", "TODO", "SYNC", "BREAK")
            value --> Tkinte.Text's STANDARD OPTIONS
            
            # idlelib  --> default tagdefs
            self.tagdefs = {
                'COMMENT': {'foreground': '#dd0000','background': '#ffffff'},
                'DEFINITION': {'foreground': '#0000ff','background': '#ffffff'},
                'BUILTIN': {'foreground': '#900090','background': '#ffffff'},
                'hit': {'foreground': '#ffffff','background': '#000000'},
                'STRING': {'foreground': '#00aa00','background': '#ffffff'},
                'KEYWORD': {'foreground': '#ff7700','background': '#ffffff'},
                'ERROR': {'foreground': '#000000','background': '#ff7777'},
                'TODO': {'foreground': None,'background': None},
                'SYNC': {'foreground': None,'background': None},
                'BREAK': {'foreground': 'black','background': '#ffff55'}
            }
        '''
        if tag_name not in self.color_delegator.tagdefs.keys():
            return
        
        if not isinstance(value, dict):
            return
        
        tagdefs = {
                'COMMENT': {'foreground': None,'background': None},
                'DEFINITION': {'foreground': None,'background': None},
                'BUILTIN': {'foreground': None,'background': None},
                'hit': {'foreground': None,'background': None},
                'STRING': {'foreground': None,'background': None},
                'KEYWORD': {'foreground': None,'background': None},
                'ERROR': {'foreground': None,'background': None},
                'TODO': {'foreground': None,'background': None},
                'SYNC': {'foreground': None,'background': None},
                'BREAK': {'foreground': None,'background': None}
            }
        tagdefs.update({tag_name:value})    
        self.color_delegator.tagdefs.update(tagdefs)
    
    def __show_idlelib_comp_lists_backup(self,event):
        if not self.comp_lists:
            return
        comp_lists = (self.comp_lists,[])
        comp_start=""
        complete=True
        mode = 1
        userWantsWin = True
        self.auto_complete_win.show_window(comp_lists,"insert-%dc" % len(comp_start),complete,mode,userWantsWin)
                
    def __event_add(self, viture_event, keylist):
        # Tkinter源码中event_add, 用于新增一个虚拟事件,并将该虚拟事件绑定到 事件序列; 
        # 事件序列，有其相应的格式,Tkinter.py-》Misc.bind的__doc__中有详细说明;  虚拟事件，格式<<AsString>>也在 这里有说明，其中AsString是任意的
        # event_add("<<copy>>", ['<Control-Key-c>', '<Control-Key-C>'])
        for k in keylist:
            self.text.event_add(viture_event,k)
            
    def __cut(self, event):
        # Tkinter源码中event_add的__doc__介绍:  Generate an event SEQUENCE.
        # 个人理解为，产生或者激发一次虚拟事件，如果绑定了 Func，那么就调用Func.
        self.text.event_generate("<<Cut>>")
        return "break"
    
    def __copy(self, event):
        if not self.text.tag_ranges("sel"):
            # There is no selection, so do nothing and maybe interrupt.
            return
        self.text.event_generate("<<Copy>>")
        return "break"
    
    def __paste(self, event):
        self.text.event_generate("<<Paste>>")
        self.text.see("insert")
        return "break"
    
    def __select_all(self, event=None):
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "1.0")
        self.text.see("insert")
        return "break"
    
    def __redo(self, event):
        self.text.event_generate('<<Redo>>')
        return "break"
    
    def __undo(self, event):
        self.text.event_generate('<<Undo>>')
        return "break"
    
    def __add_common_event(self):
        vevent = {
                  "<<autocomplete>>": (['<Alt-Key-/>'], self.auto_complete.autocomplete_event),
                  "<<copy>>": (['<Control-Key-c>', '<Control-Key-C>'], self.__copy),
                  "<<cut>>": (['<Control-Key-x>', '<Control-Key-X>'], self.__cut),
                  "<<paste>>": (['<Control-Key-v>', '<Control-Key-V>'], self.__paste),
                  "<<select-all>>": (['<Control-Key-a>', '<Control-Key-A>'], self.__select_all),
                  "<<redo>>": (['<Control-Key-y>', '<Control-Key-Y>'], self.__redo),
                  "<<undo>>": (['<Control-Key-z>', '<Control-Key-Z>'], self.__undo),
                  }
        for seq, seq_key in vevent.items():            
            self.__event_add(seq, seq_key[0])
            self.text.bind(seq, seq_key[1])


if __name__ == "__main__":
    from rock4.common.dev.tkui.suite import Components
    from rock4.common.dev.tkui.ui import ROOT,Widget,Window
       
    frame1 = Widget.Labelframe(ROOT,text = "XXXX")
    Window.widg = frame1        
    Window.Pack(side = "top", fill="both", expand="yes", padx = "0.2c")
     
    (t,x,y) = Components.TextWithScrollbar(frame1)
        
    a = TextEditDelegator(t)    
    a.effect_on_text("STRING", {'font': u"Calibri 10 normal roman",'foreground': 'red','background': '#ffffff'})
     
    t.insert("end","0.ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss\n")
    t.insert("end","1.sdf\n")  
    ROOT.mainloop()
    
    