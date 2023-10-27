import json
from tkinter import *
from operator import add
import numpy as np
import os
import time
from Quantum_Node import Node
from Quantum_Edge import Edge, QuantumEdgeEncoder
from Drag_and_drop_manager import DragManager
from global_variables import *
from PIL import Image,ImageTk
from src.Utils import start, setGlobalValues, periodic_update
from src.dto.dto import insert, select, fetchallRows


class Quantum_Network():
    def __init__(self):
        self.window = Tk()
        self.window.title('Quantum Key Distribution Network') 
        self.canvas_size = size_of_board
        self.mode = transmission

        self.window.state('zoomed')

       

        # Create left and right frames

        self.left_frame = Frame(self.window, width= self.canvas_size+500, height=self.canvas_size+100)

        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = Frame(self.window, width=self.canvas_size+500, height=200)

        self.right_frame.grid(row=1, column=0, padx=10, pady=10, sticky='W')

        self.canvas = Canvas(self.left_frame, width=self.canvas_size+500, height=self.canvas_size+100)
        self.canvas.pack(fill = "both", expand = True)
        path = os.path.dirname(__file__)
        my_file = path+'/map2.jpeg'
        img= ImageTk.PhotoImage(Image.open(my_file))    
        self.canvas.create_image( 0, 0, image = img, anchor = "nw")
        #self.canvas.bind('<Button-1>', self.click)
        #self.canvas.bind('<Double-Button-1>', self.doubleclick)

        left_buttons_frame = Frame(self.right_frame)

        left_buttons_frame.grid(column=0, row=0, sticky="NW")

        right_buttons_frame = Frame(self.right_frame)

        right_buttons_frame.grid(column=1, row=0, sticky="NE")

        self.ksu_id_var=StringVar()

        self.name_var=IntVar()
        self.name_var.set(5)
        self.setup_board()
        
        self.switch_btn_text = 'Switch to arrangement mode'

        self.switch_mode_btn = Button(left_buttons_frame,text = self.switch_btn_text, command = self.switch_mode)

        name_label = Label(left_buttons_frame, text = 'Enter the grid size:')

        name_entry = Entry(left_buttons_frame,textvariable = self.name_var)

        sub_btn=Button(left_buttons_frame,text = 'Submit', command = self.submit)

        start_transition_btn = Button(right_buttons_frame,text = 'Start transition', command = self.callTransitionButtonClick)

        reset_btn = Button(right_buttons_frame,text = 'Reset', command = self.reset)

        name_label.grid(row=0,column=0, padx=5, sticky='W')

        name_entry.grid(row=0,column=1, padx=5, sticky='W')

        sub_btn.grid(row=0,column=2, padx= 5, sticky='W')

        start_transition_btn.grid(row=0, column=3, padx=5, sticky='E')

        reset_btn.grid(row=0, column=4, padx=5, sticky='E')

        self.switch_mode_btn.grid(row=1, column=0, padx=5,sticky='W')

        replay_btn = Button(right_buttons_frame,text = 'Replay', command = self.replay)

        replay_btn.grid(row=1,column=4, padx=5, sticky='E')

        ksu_id_label = Label(left_buttons_frame, text = 'Give the KSU ID:')

        ksu_id_entry = Entry(left_buttons_frame,textvariable = self.ksu_id_var)

        ksu_id_label.grid(row=3, column=1, padx=5, sticky='W')

        ksu_id_entry.grid(row=3, column=2, padx=5, sticky='W')

        back_btn = Button(right_buttons_frame,text = 'Back', command = self.back)

        back_btn.grid(row=3,column=5, padx=5, sticky='E')

        self.window.mainloop()
    
    def get_mode(self):
        return self.mode

    def delete_canvas(self):
        self.canvas.delete('all')
    
    def switch_mode(self):
        if self.mode == transmission:
            self.mode = rearrange
            self.switch_mode_btn.configure(text='Switch to transmission mode')
        else:
            self.mode = transmission
            self.switch_mode_btn.configure(text='Switch to reaarangement mode')

    def submit(self):
        global number_of_dots
        number_of_dots=self.name_var.get()
        global size_of_board
        size_of_board =number_of_dots * 100
        self.canvas_size = number_of_dots * 100
        self.delete_canvas()
        path = os.path.dirname(__file__)
        my_file = path+'/map2.jpeg'
        img= ImageTk.PhotoImage(Image.open(my_file))    
        self.canvas.create_image( 0, 0, image = img, anchor = "nw")
        self.setup_board()
        self.window.mainloop()

    def reset(self):
        self.delete_canvas()
        path = os.path.dirname(__file__)
        my_file = path+'/map2.jpeg'
        img= ImageTk.PhotoImage(Image.open(my_file))    
        self.canvas.create_image( 0, 0, image = img, anchor = "nw")
        self.setup_board()
        self.window.mainloop()
    
    def end_selection(self):
        end_node = next(x for x in self.node_list if x.id == self.edge_list[-1].nodes[1])
        self.update_node_color(end_node, dot_selected_color)
        [x.color != dot_selected_color and self.update_node_color(x, dot_disable_color) for x in self.node_list]

    def callTransitionButtonClick(self):
        global replay_option
        replay_option = "Click_Button"
        self.transition()

    def callTransitionFromReplay(self):
        global replay_option
        replay_option = "Replay"
        self.transition()

    def callTransitionFromBack(self):
        global replay_option
        replay_option = "Back"
        self.transition()

    def transition(self):
        global gate_count, gate_order, channel_order, channel_count, replay_option
        self.end_selection()
        json_String = self.convertToJson(self.edge_list)
        # print(json_String)
        # print(self.edge_list)
        # print(self.ksu_id_var.get())

        for i in range(len(self.edge_list)):
            channel_count = 0
            if replay_option == "Back":
                channel_order_temp = channel_order[::-1]

            else:
                channel_order_temp = channel_order
            setGlobalValues(channel_order_temp, channel_count, self.window)
            edge_coords = self.canvas.coords(self.edge_list[i].line_id)
            ball_coords = [edge_coords[0], edge_coords[1]]
            end_ball_coords = [edge_coords[2], edge_coords[3]]
            start_node = next(x for x in self.node_list if x.id == self.edge_list[i].nodes[0]).position
            if start_node != ball_coords:
                end_ball_coords = ball_coords
                ball_coords = [edge_coords[2],edge_coords[3]]
            ball = self.canvas.create_oval(ball_coords[0],ball_coords[1],ball_coords[0],ball_coords[1], fill=qbit_color, outline=qbit_color, width=10)
            ydiff = end_ball_coords[1] - ball_coords[1]
            xdiff = end_ball_coords[0] - ball_coords[0]
            xdiff = 0.1 if xdiff == 0 else xdiff
            slope = ydiff / xdiff
            i=0
            while ball_coords != end_ball_coords:
                if(channel_count == 0):
                    channel_count = periodic_update()
                time.sleep(0.1)
                xinc = 0
                yinc = 0
                i+=1
                yinc = round(0 if slope == 0  else ydiff * (i / 100))
                xinc = round(xdiff * (i / 100) if slope == 0 else yinc / slope)
                ball_coords[0] += xinc
                ball_coords[1] += yinc
                if xinc < 0 and ball_coords[0] < end_ball_coords[0] or xinc > 0 and ball_coords[0] > end_ball_coords[0]:
                    ball_coords[0] -= xinc
                    xinc =  end_ball_coords[0]-ball_coords[0]
                    ball_coords[0] = end_ball_coords[0]
                if yinc < 0 and ball_coords[1] < end_ball_coords[1] or yinc > 0 and ball_coords[1] > end_ball_coords[1]:
                    ball_coords[1] -= yinc
                    yinc =  end_ball_coords[1]-ball_coords[1]
                    ball_coords[1] = end_ball_coords[1]
                # print(ball_coords, xinc, yinc)
                self.canvas.move(ball,xinc,yinc)
                self.canvas.update()
            self.canvas.delete(ball)
        if(replay_option == "Click_Button"):
            insert(json_String, self.ksu_id_var.get())

    def replay(self):
        global replay_option
        replay_option = "Replay"
        rows = select(self.ksu_id_var.get())
        # print(rows)
        results = json.loads((rows[0])[0])
        # print(len(results))
        self.edge_list = []
        self.edge_list_temp = []
        for result in results:
            nodes = result['_nodes']
            start_node = next(x for x in self.node_list if x.id == nodes[1])
            end_node = next(x for x in self.node_list if x.id == nodes[0])
            self.make_edge_between_nodes(start_node, end_node)
        # print(self.edge_list)
        start(self.window)
        self.callTransitionFromReplay()

    def back(self):
        print(self.edge_list)
        self.edge_list_temp = self.edge_list
        if(len(self.edge_list) > 0):
            result = self.edge_list[len(self.edge_list) - 1]
            self.edge_list = []
            if(isinstance(result, Edge)):
                nodes = result.nodes
            print(nodes)
            start_node = next(x for x in self.node_list if x.id == nodes[0])
            end_node = next(x for x in self.node_list if x.id == nodes[1])
            self.make_edge_between_nodes(start_node, end_node)
            self.callTransitionFromBack()
        self.edge_list = self.edge_list_temp


    def setup_board(self):
        self.edge_list =[]
        self.node_list =[]
        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                id1 = 0
                id2 = 0
                if j != number_of_dots-1:
                    id1 = self.canvas.create_line(start_x, end_x, start_x, end_x+distance_between_dots, fill='black', width=2, dash = (2, 2))
                if i != number_of_dots-1:
                    id2 = self.canvas.create_line(start_x, end_x,start_x+distance_between_dots, end_x, fill='black', width=2, dash=(2, 2))
                oval_id = self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2, end_x+dot_width/2, fill=dot_color, outline=dot_color)
                node = Node(str(i)+str(j), oval_id, [start_x, end_x], -1, 0, [id1, id2])
                dnd = DragManager(self.get_mode)
                dnd.add_dragable(node, self.canvas)
                self.canvas.tag_bind(oval_id, f"<Button-1>", self.node_click)
                self.node_list.append(node)
        for node in self.node_list:
            id = node.id
            if int(id[0]) > 0:
                up_node = next(x for x in self.node_list if x.id == str(int(id[0])-1)+str(id[1]))
                node.connections_update(up_node.connections[1])
            if int(id[1]) > 0:
                left_node = next(x for x in self.node_list if x.id == str(id[0])+str(int(id[1])-1))
                node.connections_update(left_node.connections[0])

    def mainloop(self):
        self.window.mainloop()
    
    def compare_node_width(self,node, position):
        x_start_position = node.position[0]-dot_width
        x_end_position = node.position[0]+dot_width
        y_start_position = node.position[1]-dot_width
        y_end_position = node.position[1]+dot_width
        return x_start_position < position[0] and x_end_position > position[0] and y_start_position <position[1] and y_end_position > position[1]

    def convert_grid_to_logical_position(self, grid_position): 
        clicked_node = next(x for x in self.node_list if self.compare_node_width(x, grid_position))
        return clicked_node
    
    def update_node_color(self, node, dot_color):
        self.canvas.itemconfig(node.oval_id, fill= dot_color, outline= dot_color )
        node.color = dot_color
        self.canvas.tag_raise(node.oval_id)

    def include_edge_error(self, edge):
        if edge.id == 2:
            self.canvas.after(3000, self.canvas.delete, edge.line_id)
            self.canvas.after(6000, lambda :self.delete_edge(edge))
            #self.row_status[edge.position[1]][edge.position[0]] = 0
        
    def update_node_selection(self, clicked_node):
        # make all node colours to disable except already selected nodes
        [x.color != dot_selected_color and self.update_node_color(x, dot_disable_color) for x in self.node_list]
        # make selection status to 1 for initial selection else +1 as new edge will be created and update selection color
        clicked_node.prev_selection_status = True
        if clicked_node.status > 0:
            clicked_node.status += 1
        else:
            clicked_node.status = 0
            self.update_node_color(clicked_node, dot_selection_color)
        # update adjacent nodes selection status and colors    
        [r,c] = [int(clicked_node.id[0]), int(clicked_node.id[1])]
        for nodeid in [str(r)+str(c-1), str(r)+str(c+1), str(r-1)+str(c), str(r+1)+str(c)]:
            adjacent_node = next((x for x in self.node_list if x.id == nodeid), 0)
            if adjacent_node and adjacent_node.status <= 0:
                adjacent_node.color != dot_selected_color and self.update_node_color(adjacent_node, dot_color)
                adjacent_node.status = 0

    def delete_edge(self,edge):
        self.canvas.delete(edge.line_id2)
        node2 = str(int(edge.position[0])+1)+str(edge.position[1]) if edge.type == row else str(edge.position[0])+str(int(edge.position[1])+1)
        node_id = [str(edge.position[0])+str(edge.position[1]), node2]
        for node in self.node_list:
            if node.id in node_id:
               node.edges-=1
               if node.edges < 1 and node.color != dot_selection_color:
                   self.update_node_color(node, dot_disable_color)
        
    def find_adjecent_selected_node(self, clicked_node):
        [r,c] = [int(clicked_node.id[0]), int(clicked_node.id[1])]
        for nodeid in [str(r)+str(c-1), str(r)+str(c+1), str(r-1)+str(c), str(r+1)+str(c)]:
            adjacent_node = next((x for x in self.node_list if x.id == nodeid), 0)
            if adjacent_node and adjacent_node.prev_selection_status:
                return adjacent_node
            
    def get_edge_connection(self, clicked_node, adjacent_node):
        for node_connection in clicked_node.connections:
            if node_connection and node_connection in adjacent_node.connections:
                return node_connection
            
    def make_edge_between_nodes(self, clicked_node, adjacent_node):
        node_connection = self.get_edge_connection(clicked_node, adjacent_node)
        [sx, sy, ex, ey] = self.canvas.coords(node_connection)
        line_id = self.canvas.create_line(sx, sy, ex, ey, fill=edge_color, width=edge_width)
        line_id2 = self.canvas.create_line(sx, sy, ex, ey, fill=edge_color, width=edge_width, dash=(2,2))
        row_id = adjacent_node.id+clicked_node.id
        edge = Edge(row_id, line_id, line_id2, row, [sx, sy, ex, ey], 0, [adjacent_node.id, clicked_node.id] )
        self.edge_list.append(edge)
        self.include_edge_error(edge)
        self.update_node_color(adjacent_node, dot_selected_color)

    def update_nodes(self, clicked_node):
        if clicked_node.status == 0:
            adjacent_node = self.find_adjecent_selected_node(clicked_node)
            #make edges
            self.make_edge_between_nodes(clicked_node, adjacent_node)
        self.update_node_selection(clicked_node)
        if (len(self.edge_list)) == 0:
            start(self.window)

    def node_click(self, event):
        if self.mode == transmission:
            event_position = [event.x, event.y]
            clicked_node = self.convert_grid_to_logical_position(event_position)
            self.update_nodes(clicked_node)

    def convertToJson(self, edge_list):
        json_String = "["
        for i in edge_list:
            json_String = json_String + i.to_json()
            json_String = json_String + ","
        json_String = json_String[:-1] + "]"
        return json_String


game_instance = Quantum_Network()
game_instance.mainloop()
