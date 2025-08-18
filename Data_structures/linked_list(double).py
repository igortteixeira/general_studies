class Node:

#This class is for each node (element) of the list. Each element will have 2 attributes.
	def __init__(self,value=None,next_value=None,prev_value=None):
		self.value = value
		self.next_value = next_value
		self.prev_value = prev_value



class LinkedList:
	def __init__(self):
		self.head = None



	def insert_at_end(self, value):

		if self.head is None:
		    self.head = Node(value,None,None)

		else:

			current_node = self.head

			while current_node.next_value:
				current_node = current_node.next_value

			current_node.next_value = Node(value,None,current_node)


	def present_values(self):

		current_node = self.head
		print("=======================================================")
		print(current_node.value)

		while current_node.next_value:
			current_node = current_node.next_value
			print("=======================================================")
			print(f"Current: {current_node.value}")
			print(f"Previous: {current_node.prev_value.value}")


example = LinkedList()

for i in range(0,16):
	example.insert_at_end(i)

example.present_values()

