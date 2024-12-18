import gym
from gym import spaces
import numpy as np

class DocumentWorkflowEnv:
    def __init__(self):
        # Define the valid document types
        self.document_types = [
            "Promotion Request",
            "Change of Work Schedule Request"
        ]
        # Define the approvers for each document type
        self.approvers = {
            "Promotion Request": "Manager Finance",
            "Change of Work Schedule Request": "Manager RH"
        }
        self.current_document = None

    def reset(self):
        # nbdew b default state
        self.current_document = None
        return [0]  # Index placeholder

    def step(self, action):
        # The action corresponds to a document type index
        document_type = self.document_types[action]
        approver = self.approvers[document_type]
        
        # For testing, print the routing
        print(f"Document Type: {document_type}, Assigned to: {approver}")
        return [action], 0, True, {}  # State, reward, done, info
