from node import Node
from member import Member
from reaction_force import ReactionForce
from applied_force import AppliedForce
import math
import numpy as np

# Contains all lists and dictionaries

class State:
    def __init__(self):
        self.nodes = []
        self.members = []
        self.reaction_forces = []
        self.applied_forces = []
        self.id_counter = 1
        self.max_force = 0
        

    def add_object(self, obj):
        if isinstance(obj, Node):
            if obj not in self.nodes:
                self.nodes.append(obj)
        elif isinstance(obj, Member):
            if obj not in self.members:
                self.members.append(obj)
        elif isinstance(obj, ReactionForce):
            if obj not in self.reaction_forces:
                self.reaction_forces.append(obj)
        elif isinstance(obj, AppliedForce):
            if obj not in self.applied_forces:
                self.applied_forces.append(obj)

    def delete(self, node):
        self.nodes.remove(node)
        for member in self.members[:]:
            if member.node1 == node or member.node2 == node:
                self.members.remove(member)
                
        for force in self.reaction_forces[:]:
            if force.endnode == node:
                self.reaction_forces.remove(force)
                
        for force in self.applied_forces[:]:
            if force.endnode == node:
                self.applied_forces.remove(force)

    def show_forces(self):
        A = self.calculate_supports()
        for i,member in enumerate(self.members):
            member.visualize_force = True
            member.force = A[i]
            member.max_force = self.max_force
            member.visualize_method = "line"

    def stop_showing_forces(self):
        for member in self.members:
            member.visualize_force = False


    def paint_objects(self, painter):
        # Draw members
        for member in self.members:
            member.paint(painter)

        # Draw nodes
        for node in self.nodes:
            node.paint(painter)

        # Draw applied forces
        for force in self.applied_forces:
            force.paint(painter)

        # Draw reaction forces
        for reaction in self.reaction_forces:
            reaction.paint(painter)

    # Return unit vector of every node and their connections
    def generate_matrix(self):
        c = len(self.members) + len(self.reaction_forces)
        n = len(self.nodes)
        rows = 2 * n
        cols = c
        matrix = np.zeros((rows, cols))

        for j,member in enumerate(self.members):
            idx1 = self.nodes.index(member.node1)
            idx2 = self.nodes.index(member.node2)

            x1, y1 = member.node1.position
            x2, y2 = member.node2.position

            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx**2 + dy**2)
            if length == 0:
                continue
            ux = dx/length
            uy = dy/length

            matrix[2 * idx1][j] += ux
            matrix[2 * idx1+1][j] += uy
            matrix[2 * idx2][j] -= ux
            matrix[2 * idx2+1][j] -= uy

        for j,force in enumerate(self.reaction_forces, start=len(self.members)):
            node_x, node_y = force.endnode.position
            point_x, point_y = force.endpoint.position
            force_magnitude = force.magnitude

            idx = self.nodes.index(force.endnode)

            rx = (point_x - node_x) * force_magnitude
            ry = (point_y - node_y) * force_magnitude

            length = math.hypot(rx, ry)
            if length == 0:
                continue

            ux = rx/length
            uy = ry/length

            matrix[2*idx][j] = ux
            matrix[2*idx + 1][j] = uy

        return matrix
        
    def generate_force_array(self):
        n = len(self.nodes)
        rows = 2 * n
        force_array = np.zeros((rows, 1))

        for force in self.applied_forces:
            node_x, node_y = force.endnode.position
            point_x, point_y = force.endpoint.position
            force_magnitude = force.magnitude
            force_value = force.force

            idx = self.nodes.index((force.endnode))

            dx = (node_x - point_x) * force_magnitude
            dy = (node_y - point_y) * force_magnitude

            length = math.hypot(dx, dy)
            if length == 0:
                continue
            ux = dx/length
            uy = dy/length

            Fx = ux * force_value
            Fy = uy * force_value

            force_array[2 * idx][0] += Fx
            force_array[2 * idx + 1][0] += Fy

        return force_array
    
    def calculate_supports(self):
        A = self.generate_matrix()
        F = self.generate_force_array()
        try:
            A_inv = np.linalg.pinv(A)
            X = np.dot(A_inv, F)
            self.member_forces_array = X

            for n in X:
                if abs(n) > self.max_force:
                    self.max_force = abs(n)

            return X

        except np.linalg.LinAlgError:
            print("Matrix is singular, cannot compute supports.")
            return None


                










# Get methods
    def get_node_at(self,pos):
        for node in self.nodes:
            if node.position == pos:
                return node
        return None
    
    def get_node_by_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None
    
    def get_member_at(self, node1, node2):
        for member in self.members:
            if (member.node1 == node1 and member.node2 == node2) or (member.node1 == node2 and member.node2 == node1):
                return member
        return None
    
    def get_member_by_id(self, id):
        for member in self.members:
            if member.id == id:
                return member
        return None
    
