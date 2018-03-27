# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.common.ModelEntrance

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.common.ModelEntrance,v 1.0 2017年2月18日
    FROM:   2017年2月18日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os
from ModelEntryway import ModelEntryway
from rock4.common.p_executer import TestEntrance

class ModelEntrance(TestEntrance):           
            
    def test_cases(self):
        # model: excel,yaml
        # model_type: web,pad,pcmfc,pcwpf,api
        
        (devdriver, model_file, model_type, debug) = self._get_args()
        model = os.path.splitext(model_file)[1]        
        if model == ".yaml":
            model = "yaml"            
        elif model == ".xlsx" or model == ".xls":
            model = "excel"
        else:
            self.fail("Parameter 'modelfile' should be in (.yaml, .xlsx, .xls).")       
        
        try:                  
            model_obj,errmsg = ModelEntryway.Select(model = model, model_type =model_type)
            if model_obj:
                model_obj(model_file, ModelEntryway.parent_model_class).apply_actions(devdriver, debug = debug)
            else:
                self.fail(errmsg)
        except Exception,e:
            self.fail(e)
    
    def _get_args(self):
        model_file = self.params.get("modelfile")
        if not model_file:
            self.fail("Parameter 'modelfile' not exists.")
        
        devdriver = self.params.get("devdriver")        
        model_type = self.params.get("modeltype")
                
        debug = self.params.get("debug")        
        if not debug:
            debug = False
        return (devdriver, model_file, model_type, debug)
            
def test_start(**kwargs):
    suite = TestEntrance.parametrize(ModelEntrance, **kwargs)
    TestEntrance.go(suite)
    
    


