from collections import deque as dq

#empty() – Returns whether the stack is empty – Time Complexity: O(1)
#size() – Returns the size of the stack – Time Complexity: O(1)
#top() – Returns a reference to the topmost element of the stack – Time Complexity: O(1)
#push(a) – Inserts the element ‘a’ at the top of the stack – Time Complexity: O(1)
#pop() – Deletes the topmost element of the stack – Time Complexity: O(1)

#An example of stacks (LIFO) is historic on browsers. We can alt+< to go to last element.
#Or on text editors for ctrl+z function

example = dq()

example.append(1)
example.append(2)
example.append(3)

print(example)

example.pop()
example.pop()

print(example)
