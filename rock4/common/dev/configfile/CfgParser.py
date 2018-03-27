# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.configfile.CfgParser

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.common.dev.configfile.CfgParser,v 2.0 2017年2月7日
    FROM:   2016年10月21日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import ConfigParser,os


class CfgParser():
    
    def __init__(self, cfgfile, **kwargs):
        ''' if kwargs is given, default items represent key = value will be setted. '''
        
        if not os.path.isfile(cfgfile):        
            raise Exception("\n\tCfgParser exception 1.1: file not exists '%s'." %(cfgfile))
        
        if kwargs:
            self.config = ConfigParser.SafeConfigParser(kwargs)
        else:
            self.config = ConfigParser.RawConfigParser()
        self.__cfgfile = cfgfile
        
    def get_config(self,section = None):
        cfg = {}
        self.config.read(self.__cfgfile)
        
        sections = self.config.sections()                    
        for sec in sections:
            cfg[sec] = {}
            options = self.config.options(sec)
            for option in options: 
                cfg[sec][option]=self.config.get(sec,option)
        
        if section:
            return cfg.get(section)
        
        return cfg
        
    def set_config(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.__cfgfile, 'wb') as f:
            self.config.write(f)
    
if __name__ == "__main__":
    p = CfgParser(r'd:\auto\buffer\install2.cfg')
    print p.get_config()
    p.set_config("Section-test", "option1-test", "value1-test")
    print p.get_config()
    
        