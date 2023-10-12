from global_variables import *

class Edge():
    def __init__(self, id, line_id, line_id2, type, position, status, nodes):
        self._edge_id = id
        self._line_id = line_id
        self._line_id2 = line_id2
        self._type = type
        self._position = position
        self._canvas_position = 0
        self._status = status
        self._nodes = nodes

    @property
    def id(self):
         return self._edge_id
    
    @property
    def line_id(self):
         return self._line_id
    
    @line_id.setter
    def line_id(self, line_id):
         self._line_id = line_id
    
    @property
    def line_id2(self):
         return self._line_id2 
       
    @line_id2.setter
    def line_id2(self, line_id2):
         self._line_id2 = line_id2
    
    @property
    def type(self):
         return self._type
       
    @type.setter
    def type(self, type):
         self._type = type
    
    @property
    def status(self):
         return self._status

    @property
    def position(self):
        return  self._position
    
    @property
    def canvas_position(self):
        return  self._canvas_position
    
    @property
    def nodes(self):
        return  self._nodes

    @status.setter
    def status(self, status):
         self._status = status
    
    def show_all(self):
        return str(self._edge_id) + ' '+ str(self._line_id) + ' '+ str(self._type) + ' '+str(self._position)+ ' '+str(self._status)
