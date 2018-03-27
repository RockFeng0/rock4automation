# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.idleshell.diyoid

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.idleshell.diyoid,v 2.0 2017年2月7日
    FROM:   2016年8月17日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import types

class OidMap:
    ''' Create OidMap '''
    def __init__(self):        
        self.map = {}
            
    def get_oid_map(self):
        return self.map
    
    def map_objs(self,**kwobjs):
        ''' Usually use to update the map.
        
            Sample usage:
                class A:
                    pass
                class B:
                    pass
                
                om = OidMap()
                am.map_obj(a=A(), b = B())
                print om.get_oid_map()
            
        '''
        self.map.update(kwobjs)
        
    def map_scope_objs(self, scope):
        ''' Parameter 'scope':  a dict type, always be globals() or locals().
        
            This method support the callback in modules which need to map objects. 
            Sample usage:
                class A:
                    pass
                
                class B:
                    pass
                
                class Asdf:
                    def __init__(self):
                        self.hh = "ni hao"
                        self.hh2 = ""
                         
                    def sdfs2(self,*args,**kwargs):
                        print "asdf"
                        print self.hh2
                        print self.hh
                        self.hh2 = "OK..."
                
                d = globals()
                oidmap.map_scope_objs(d)
                print oidmap.get_oid_map()
                
            Return a map of lowwer class_name -> class instance
        '''

        if not isinstance(scope, dict):
            return
        
        func_dicts = scope.items()
        raw_alias_class = dict([(s.lower(),o) for s,o in func_dicts if s[:1] != "_" and isinstance(o, (type, types.ClassType)) and s != "OidMap"])
        
        args_not_enough = []
        for alias, func in raw_alias_class.items():
            try:
                self.map[alias] = func()
            except TypeError,e:
        #         print e
                args_not_enough.append(func)
        
        if args_not_enough:
#             raise Exception("TypeError in %r" %args_not_enough)
            print "Waring[diyoid]: TypeError in %r" %args_not_enough
    
    def map_module_objs(self,mod):
        ''' Parameter 'mod': a module name which define map classes. Befor to call this method, check sys.path 
            Sample usage:
                module1.py:
                    class A:
                        pass
                    class B:
                        pass
                oidmap.map_module_objs("module1")
                print oidmap.get_oid_map()
            
            Return a map of lowwer class_name -> class instance
        '''
        m = __import__(mod)    
        raw_alias_class = dict([(a.lower(), m.__dict__.get(a)) for a in dir(m) if a[:1] != "_" and isinstance(m.__dict__.get(a), types.ClassType)])
         
        args_not_enough = []
        for alias, func in raw_alias_class.items():
            try:
                self.map[alias] = func()
            except TypeError,e:
#                 print e
                args_not_enough.append(str(func))
         
        if args_not_enough:
#             raise Exception("TypeError in %r" %args_not_enough)
            print "Waring[diyoid]: TypeError in %r" %args_not_enough
        
    
oidmap = OidMap()

if __name__ == "__main__":
    import sys
    sys.path.append(r'd:\auto\buffer')
    oidmap.map_module_objs("sdf")
    print oidmap.get_oid_map()
    

