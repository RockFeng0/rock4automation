# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.idleshell.SimpleAutoComplete

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.idleshell.SimpleAutoComplete,v 2.0 2017年2月7日
    FROM:   2016年8月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import __main__,os
from idlelib import AutoComplete,AutoCompleteWindow


class SimpleAutoComplete(AutoComplete.AutoComplete):
    
    def __init__(self, master = None, rpcclt = None, debug = False):
        ''' rpcclt is a instance of diyrpc.MyRpcClient '''
        AutoComplete.AutoComplete.__init__(self, editwin = None)
        self.text = master
        self.rpcclt = rpcclt
        self.autocompletewindow = None
        self.id_chars = AutoComplete.ID_CHARS
        self.debug = debug
        
    def get_curline_need_completion_string(self):
        ''' master must not be None and must be Tkinter's Text 
            Sample usage:
                from Tkinter import Tk,Text,Button
                root = Tk()
                text = Text(root)
                btn = Button(root)
                text.pack()
                btn.pack()    
                
                sac = SimpleAutoComplete(master = text,debug = True)
                btn.config(text = "curline", command = sac.get_curline_need_completion_string) 
                 
                root.mainloop()
        '''
        if not self.text:
            return [], []
        
        # get and analyse the need completion string in Text. 
        curline = self.text.get("insert linestart", "insert")
        i = j = len(curline)
        
        while i and curline[i-1] in self.id_chars:
            i -= 1
        comp_start = curline[i:j]
        
        if i and curline[i-1] == '.':
            comp_what = curline[0:i-1]
            if not comp_what or comp_what.find('(') != -1:
                return
        else:
            comp_what = ""
        
        if self.debug:
            print "what:",comp_what
            print "start:",comp_start
        return comp_what,comp_start
    
    def fetch_completions(self, what, mode=1):
        """ Override AutoComplete.fetch_completions
            
            what: a string which you want to complete.
            mode: default is 1, for complete the attributes.
            return comp_lists
            
            Sample usage:
                a = SimpleAutoComplete()
                print a.fetch_completions("")
                print a.fetch_completions("os")
                print a.fetch_completions("asdf")
        """
        
        if self.rpcclt:
            # complete the string with rpc server namespace            
            return self.rpcclt.remotecall("exec", "get_the_completion_list",
                                     (what, mode), {})
        else:
            # complete the string with local namespace
            if mode == AutoComplete.COMPLETE_ATTRIBUTES:
                if what == "":
                    namespace = __main__.__dict__.copy()
                    namespace.update(__main__.__builtins__.__dict__)
                    bigl = eval("dir()", namespace)
                    bigl.sort()
                    
                    if "__all__" in bigl:
                        smalll = eval("__all__", namespace)
                        smalll.sort()
                    else:
                        smalll = [s for s in bigl if s[:1] != '_']
                    
                    if self.debug:
                        print "smalll is: %r" %smalll
                else:
                    try:                        
                        entity = self.get_entity(what)
                        bigl = dir(entity)
                        bigl.sort()
                    
                        if "__all__" in bigl:
                            smalll = entity.__all__
                            smalll.sort()
                        else:
                            smalll = [s for s in bigl if s[:1] != '_']
                            
                        if self.debug:
                            print "what-smalll is: %r" %smalll
                    except:
                        return [], []

            elif mode == AutoComplete.COMPLETE_FILES:                
                if what == "":
                    what = "."
                try:
                    expandedpath = os.path.expanduser(what)
                    bigl = os.listdir(expandedpath)
                    bigl.sort()
                    smalll = [s for s in bigl if s[:1] != '.']
                except OSError:
                    return [], []

            if not smalll:
                smalll = bigl
            
            return smalll, bigl
    
    def autocomplete_event(self, event):
        """ Override AutoComplete.autocomplete_event 
            Sample usage:
                from Tkinter import Tk,Text
                root = Tk()
                text = Text(root)
                text.pack()
                 
                sac = SimpleAutoComplete(master = text)
                text.bind('<Alt-Key-/>', sac.autocomplete_event)    
                 
                root.mainloop()
        """
        if hasattr(event, "mc_state") and event.mc_state:
            # A modifier was pressed along with the tab, continue as usual.
            return
        if self.autocompletewindow and self.autocompletewindow.is_active():
            self.autocompletewindow.complete()
            return "break"
        else:
            opened = self.__show_completions()
            if opened:
                return "break"
    
    def __show_completions(self):
        ''' master must not be None and must be Tkinter's Text '''
        if not self.text:
            return
        
        self.__remove_autocomplete_window()        
        
        comp_what,comp_start = self.get_curline_need_completion_string()        
        comp_lists = self.fetch_completions(comp_what)
        
        if not comp_lists[0]:
            return
        
        complete=True; mode = 1; userWantsWin = True
        self.autocompletewindow = self.__make_autocomplete_window()        
        self.autocompletewindow.show_window(comp_lists,"insert-%dc" % len(comp_start),complete,mode,userWantsWin)
        return True
    
    def __make_autocomplete_window(self):
        ''' master must not be None and must be Tkinter's Text
            create an instance of AutoCompleteWindow.AutoCompleteWindow 
        '''        
        return AutoCompleteWindow.AutoCompleteWindow(self.text)
        
    def __remove_autocomplete_window(self):
        ''' hide and remove the self.autocompletewindow '''
        self._remove_autocomplete_window()
    
if __name__ == "__main__":
    from Tkinter import Tk,Text
    root = Tk()
    text = Text(root)
    text.pack()
     
    sac = SimpleAutoComplete(master = text)
    text.bind('<Alt-Key-/>', sac.autocomplete_event)    
     
    root.mainloop()
    
    