from node import Node
from member import Member
from reaction_force import ReactionForce
from applied_force import AppliedForce

# Contains all lists and dictionaries

class State:
    def __init__(self):
        self.nodes = []
        self.members = []
        self.reaction_forces = []
        self.applied_forces = []
        self.id_counter = 1
        

    def add_object(self, obj):
        if isinstance(obj, Node):
            self.nodes.append(obj)
        elif isinstance(obj, Member):
            self.members.append(obj)
        elif isinstance(obj, ReactionForce):
            self.reaction_forces.append(obj)
        elif isinstance(obj, AppliedForce):
            self.applied_forces.append(obj)

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
    
