# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.tkui.basic

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.tkui.basic,v 2.0 2017年2月7日
    FROM:   2016年7月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

#### widget's Pack
def get_pack_info(obj):
    '''Usage:
        a=Tkinter.Tk()
        b=Tkinter.Button(a,text = "asdf")
        print b.pack_info
        print get_pack_info(b)
    return dict
    '''
    if get_widget_ismapped(obj):
        return obj.pack_info()
      
def del_current_pack(obj):
    obj.pack_forget()

#### widget's Grid
def get_grid_info(obj):
    if get_widget_ismapped(obj):
        return obj.grid_info()

def del_current_grid(obj):
    obj.grid_forget()


#### widget's Misc
# These used to be defined in Widget:
def get_configuration_keys(obj):
    #获取当前控件,可用于配置的所有 key
    return obj.keys()

def get_configuration_value(obj,key):
    '''Usage:
    get_configuration_value(button_obj,"command")
    '''
    return obj.cget(key)

def set_configuration(obj,**kw):
    '''Usage:
        cmd = [button_obj.register(func)] + list(args_list)
        set_configuration(button_obj, command = tuple(cmd))
    '''
    obj.config(**kw)


# Pack methods that apply to the master
def get_pack_slaves(obj):
    #获取在当前控件，已经pack的所有控件，返回列表
    obj.slaves()

# Clipboard handling:
def get_clipboard_value(obj):
    try:
        return obj.clipboard_get()
    except:
        return

# XXX grab current w/o window argument

def get_widget_toplevel(obj):
    return obj.winfo_toplevel()

def get_widget_exists(obj):
    # 判断控件 是否 destroy
    return obj.winfo_exists()

def get_widget_ismapped(obj):
    #判断控件是不是已经，map出来
    return obj.winfo_ismapped()

def get_widget_id(obj):
    return obj.winfo_id()

def get_widget_name(obj):
    return obj.winfo_name()

def get_widget_pathname(obj,widge_id):
    return obj.winfo_pathname()

def get_widget_parent(obj):
    # return the string of widget path 
    return obj.winfo_parent()

def get_widget_children(obj):
    # return a list
    return obj.winfo_children()

def get_widget_classname(obj):
    return obj.winfo_class()

def get_widget_pointxy(obj):
    return obj.winfo_pointerxy()    
    
def get_widget_geometry(obj):
    #return "widthxheight+X+Y"
    return obj.winfo_geometry()

def get_widget_width(obj):
    return obj.winfo_width()

def get_widget_height(obj):
    return obj.winfo_height()

    
# others    
def set_focus(obj):
    obj.focus()
    
def register_func(obj,func):
    '''Usage:
        def test():
            pass
        register_func(button_obj,test)
    '''
    return obj.register(func)

def register_command(obj, func, *args):
    tcl_line_cmd = [obj.register(func)] + list(args)    
    return tuple(tcl_line_cmd)
    
def mainloop(obj,loop = False):
    if loop:
        obj.mainloop()
        
def after(obj, ms, func=None, *args):
    return obj.after(ms,func,*args)

def after_idle(obj,func, *args):
    return obj.after_idle(func,*args)

def after_cancel(obj, aid):
    obj.after_cancel(aid)


import tkMessageBox
class MSG:
    
    @classmethod
    def Showinfo(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.showinfo("Spam", "Egg Information")
        '''
        tkMessageBox.showinfo(title,message,**options)
    
    @classmethod
    def Showwarning(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.showwarning("Spam", "Egg Warning")
        '''
        tkMessageBox.showwarning(title,message,**options)
    
    @classmethod
    def Showerror(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.showerror("Spam", "Egg Alert")
        '''
        tkMessageBox.showerror(title,message,**options)
    
    @classmethod
    def Askquestion(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.askquestion("Spam", "Egg Question?")
        '''
        return tkMessageBox.askquestion(title,message,**options)
    
    @classmethod    
    def Askokcancel(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.askokcancel("Spam", "Egg Proceed?")
        '''
        return tkMessageBox.askokcancel(title,message,**options)
    
    @classmethod    
    def Askyesno(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.askyesno("Spam", "Egg Got it?")
        '''
        return tkMessageBox.askyesno(title,message,**options)
    
    @classmethod
    def Askyesnocancel(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.askyesnocancel("Spam", "Want it?")
        '''
        return tkMessageBox.askyesnocancel(title,message,**options)
    
    @classmethod
    def Askretrycancel(cls,title=None, message=None, **options):
        '''Sample usage:
            tkMessageBox.askretrycancel("Spam", "Try again?")
        '''
        return tkMessageBox.askretrycancel(title,message,**options)


import tkFileDialog
class FileDilog:
    '''
        options (all have default values):
        
        - defaultextension: added to filename if not explicitly given
        
        - filetypes: sequence of (label, pattern) tuples.  the same pattern
          may occur with several patterns.  use "*" as pattern to indicate
          all files.
        
        - initialdir: initial directory.  preserved by dialog instance.
        
        - initialfile: initial file (ignored by the open dialog).  preserved
          by dialog instance.
        
        - parent: which window to place the dialog on top of
        
        - title: dialog title
        
        - multiple: if true user may select more than one file
        
        options for the directory chooser:
        
        - initialdir, parent, title: see above
        
        - mustexist: if true, user must pick an existing directory
    '''
    
    @classmethod
    def Askopenfilename(cls,**options):
        "Ask for a filename to open"
        return tkFileDialog.askopenfilename(**options)
        
    @classmethod
    def Asksaveasfilename(cls,**options):
        "Ask for a filename to save as"
        return tkFileDialog.asksaveasfilename(**options)

    @classmethod
    def Askopenfilenames(cls,**options):
        """Ask for multiple filenames and return the open file
        objects
    
        returns a list of open file objects or an empty list if
        cancel selected
        """
        return tkFileDialog.askopenfilenames(**options)
    
    @classmethod
    def Askdirectory(cls,**options):
        "Ask for a directory, and return the file name"
        return tkFileDialog.askdirectory(**options)

from tkFont import Font,NORMAL,BOLD,ROMAN,ITALIC
class TkFont():
    
    def __init__(self, family = "Calibri", weight = NORMAL, slant = ROMAN, overstrike = 0, underline = 0, size = 12):
        '''
        family: 字符集
        size: 字体大小
        weight: "bold" for boldface, "normal" for regular weight.        
        slant: "italic" for italic, "roman" for unslanted.        
        underline: 1 for underlined text, 0 for normal.
        overstrike: 1 for overstruck text, 0 for normal.
        '''
        self.font = Font(family = family, weight = weight, slant = slant, overstrike = overstrike, underline = underline, size = size)
    
    def get_actual_font_info(self):
        return self.font.actual()
    
    def config(self,**kw):
        self.font.config(**kw)
        
        
if __name__ == "__main__":
    import Tkinter
    a=Tkinter.Tk()
    b=Tkinter.Button(a,text="asdf")
    c=Tkinter.Entry(a)
    print get_pack_info(b)
    b.pack()
    print get_pack_info(b)
    print get_configuration_keys(b)
        