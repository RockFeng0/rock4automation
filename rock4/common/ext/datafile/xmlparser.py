# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.ext.datafile.xmlparser

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      pyrunner.ext.datafile.xmlparser,v 1.0 2016年5月7日
    FROM:   2016年5月7日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,sys

class Xml():
    def __init__(self,xmlfile):
        ''' initial xml data object with the your project        --data driver with xml'''
        if os.path.isfile(xmlfile):
            self.swt = "Minidom"        
            self.root = self.get_document_element(xmlfile)            
        else:
            raise Exception("\n\tXml exception 1.0: invalid xml file '%s'." %(xmlfile))
    
                    
    def get_document_element(self,file_path):
        result = None           
        try:
            from bs4 import BeautifulSoup
            self.swt = "Beautiful"            
            with open(file_path,'r') as f:
                #a bs4 obj's root element. named: self.xml
                result = BeautifulSoup(f,'xml')            
        except:            
            try:
                from xml.dom import minidom
                self.swt = "Minidom"
                result =  minidom.parse(file_path).documentElement                
            except Exception,e:
                print "warning:%s" %e    
                if sys.subversion[0].lower() == 'ironpython':
                    import clr,os
                    clr.AddReference('System.Xml')
                    from System import Xml
                    self.swt = "System"
                    dom = Xml.XmlDocument()
                    dom.Load(file_path)        
                    result = dom.DocumentElement
        finally:
            print self.swt
            return result
        
        
    def find_element(self,tag_list):
        ''' Sample usage:
         the index = 0, so name the function find, not find_all
            find("Login","TextUserName");#just like the xpath to use
        '''
        root = self.root
        if self.swt == "Minidom":
            index = 0            
            for tag in tag_list:
                root = root.getElementsByTagName(tag)
                if not root:
                    return
                root = root.item(index)
            if root == self.root:
                return
            return root
        
        if self.swt == "Beautiful":            
            for tag in tag_list:
                root = root.findChild(tag)
                if not root:
                    return        
            return root    
        
        if self.swt == "System":
            index = 0
            x_path = ['/']
            for tag in tag_list:
                if tag:
                    x_path.append(tag)
            x_path = x_path[0].join(x_path)            
            nodes = root.SelectNodes(x_path)        
            if nodes.Count:    
                return nodes.Item(index)

    def find_elements(self,tag_name):
        ''' find all elements by its tag name
            return objects list
        '''
        elms = []

        if self.swt == "Beautiful":        
            elms = self.root.find_all(tag_name)    
            
        if self.swt == "Minidom":
            if self.root:                
                obj_elm = self.root.getElementsByTagName(tag_name)                
                count = obj_elm.length
                
                fc = lambda index: obj_elm.item(index)
                for index in range(count):
                    elms.append(fc(index))
        
        if self.swt == "System":
            if self.root:
                obj_elm = self.root.GetElementsByTagName(tag_name)
                count = obj_elm.Count
                
                fc = lambda index: obj_elm.Item(index)
                for index in range(count):
                    elms.append(fc(index))
            
        return elms
        
    def get_children_texts(self,node):
        result = {}
        if self.swt == "Minidom": 
            count = node.childNodes.length
            
            for i in range(count):
                elem = node.childNodes.item(i)
                tag_name = self.get_node_tagname(elem)                
                result[tag_name] = self.get_node_text(elem)
            return result
        
        if self.swt == "Beautiful":
            for i in node.children:
                tag_name = self.get_node_tagname(i)
                result[tag_name] = self.get_node_text(i)            
            return result
        
        if self.swt == "System":
            count = node.ChildNodes.Count            
            for i in range(count):
                elem = node.ChildNodes.Item(i)
                tag_name = self.get_node_tagname(elem)    
                result[tag_name] = self.get_node_text(elem)
            return result
        
           
    def get_attr_value(self,node,attr):
        ''' Sample usage:
            print get_attr_value("des")
        '''
        if self.swt == "Minidom":
            try:
                if not self.__is_exists(node):
                    return
                if not node.hasAttributes():
                    return                        
                return node.getAttribute(attr)
            except:
                return
            
        if self.swt == "Beautiful":
            return node.get(attr)
        
        if self.swt == "System":
            try:
                if not self.__is_exists(node):
                    return
                if not node.HasAttributes:
                    return                        
                return node.GetAttribute(attr)
            except:
                return
    
    def get_node_parent(self,node):
        if not node:
            return
                
        if self.swt == "Beautiful":        
            return node.parent        
        
        if self.swt == "Minidom":
            return node.parentNode
            
        if self.swt == "System":
            return node.ParentNode
    
    def get_node_tagname(self,node):
        if self.swt == "Minidom":
            try:
                return node.tagName
            except:
                return
        
        if self.swt == "Beautiful":
            return node.name
        
        if self.swt == "System":
            return node.Name
                
    def get_node_text(self,node):
        ''' Sample usage:
            print get_node_text()
        '''
        if self.swt == "Minidom":
            try:
                if not self.__is_exists(node):
                    return
                if not node.hasChildNodes():
                    return
                return node.firstChild.nodeValue
            except:
                return
        
        if self.swt == "Beautiful":
            return node.string
        
        if self.swt == "System":
            try:                
                if not self.__is_exists(node):
                    return
                if not node.HasChildNodes:
                    return
                return node.FirstChild.Value            
            except:
                return
            
    def __is_exists(self,root):
        if root:
            return True
        return False


    