# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.datafile.htmlparser

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.datafile.htmlparser,v 1.0 2016年12月23日
    FROM:   2016年12月23日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''


import os
from bs4 import BeautifulSoup

class Html():
    def __init__(self,htmlfile):
        ''' initial xml data object with the your project        --data driver with xml'''
        if os.path.isfile(htmlfile):  
            self.root = self.get_document_element(htmlfile)            
        else:
            raise Exception("\n\tHtml exception 1.0: invalid xml file '%s'." %(htmlfile))
    
                    
    def get_document_element(self,file_path):          
        with open(file_path,'r') as f:
            #a bs4 obj's root element. named: self.xml
            result = BeautifulSoup(f,'html')
        return result
        
        
    def find_element(self,tag_list):
        ''' Sample usage:
         the index = 0, so name the function find, not find_all
            find("Login","TextUserName");#just like the xpath to use
        '''
        root = self.root
                         
        for tag in tag_list:
            root = root.findChild(tag)
            if not root:
                return        
        return root    
        
    def find_elements(self,tag_name):
        ''' find all elements by its tag name
            return objects list
        '''
        elms = self.root.find_all(tag_name)
        return elms
        
    def get_children_texts(self,node):
        result = {}    
        for i in node.children:
            tag_name = self.get_node_tagname(i)
            result[tag_name] = self.get_node_text(i)            
        return result
                
           
    def get_attr_value(self,node,attr):
        ''' Sample usage:
            print get_attr_value("des")
        '''
        return node.get(attr)
            
    def get_node_parent(self,node):
        if not node:
            return     
        return node.parent        
        
    def get_node_tagname(self,node):
        return node.name
        
    def get_node_text(self,node):
        ''' Sample usage:
            print get_node_text()
        '''
        return node.string        
                
if __name__ == "__main__":
    html = Html(r'D:\auto\python\loperf\buffer\analyzeResult.html')
    div = html.find_element(["body",'div'])
    print div,len(div)
    print "========="
    
    div_class = html.get_attr_value(div, "class")
    print div_class
    print "========="
        
    div_text = html.get_node_text(div)
    print div_text
    print "========="
    
    body = html.find_elements("body")
    print body[0]
    print "========="
    
    div_texts = html.get_children_texts(body[0])
    print div_texts
    print "========="
    print str(html.root.body.div)
    print str(html.root.body.script)
    
    
    
    