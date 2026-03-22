from typing import List, Optional
from .call import EmergencyCall

class AVLNode:
    def __init__(self, call: EmergencyCall):
        self.call = call
        self.left = None
        self.right = None
        self.height = 1

class AVLTreeDispatch:
    def __init__(self):
        self.root = None
        self.rotations = 0
        self.call_map = {} # map ID to Node for O(log N) operations with map lookup

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        self.rotations += 1
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        return x

    def left_rotate(self, x):
        self.rotations += 1
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = max(self.get_height(x.left), self.get_height(x.right)) + 1
        y.height = max(self.get_height(y.left), self.get_height(y.right)) + 1
        return y

    def _insert(self, node, call: EmergencyCall):
        if not node:
            return AVLNode(call)

        # Using our custom __lt__: True meaning 'smaller' in Python's eyes,
        # but logically it's higher priority. So if call < node.call, it goes left.
        # This makes the "minimum" element strictly the highest priority.
        if call < node.call:
            node.left = self._insert(node.left, call)
        else:
            node.right = self._insert(node.right, call)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left Left Case
        if balance > 1 and call < node.left.call:
            return self.right_rotate(node)
        # Right Right Case
        if balance < -1 and not call < node.right.call:
            return self.left_rotate(node)
        # Left Right Case
        if balance > 1 and not call < node.left.call:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        # Right Left Case
        if balance < -1 and call < node.right.call:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, call: EmergencyCall):
        self.root = self._insert(self.root, call)
        self.call_map[call.id] = call

    def _min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self._min_value_node(node.left)

    def _delete_node(self, root, call: EmergencyCall):
        if not root:
            return root

        # Same logic for finding the node to delete
        # Because we can have duplicate priorities effectively (different calls but maybe same? No, call handles identity)
        # Actually our `__lt__` makes it robust. Let's just traverse
        # To delete we need the exact node.
        if call < root.call:
            root.left = self._delete_node(root.left, call)
        elif root.call < call:
            root.right = self._delete_node(root.right, call)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self._min_value_node(root.right)
            root.call = temp.call
            root.right = self._delete_node(root.right, temp.call)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, call_id: str):
        if call_id in self.call_map:
            call = self.call_map[call_id]
            self.root = self._delete_node(self.root, call)
            del self.call_map[call_id]

    def extract_max(self) -> Optional[EmergencyCall]:
        # Highest priority is the "minimum" element according to our __lt__
        # So we go all the way left
        if not self.root:
            return None
        min_node = self._min_value_node(self.root)
        call = min_node.call
        self.delete(call.id)
        return call

    def update_severity(self, call_id: str, new_severity: int):
        if call_id in self.call_map:
            call = self.call_map[call_id]
            self.delete(call_id)
            call.severity = new_severity
            self.insert(call)

    def _inorder(self, node, res, limit):
        if node and len(res) < limit:
            self._inorder(node.left, res, limit)
            if len(res) < limit:
                res.append(node.call)
            self._inorder(node.right, res, limit)

    def top_k(self, k: int) -> List[EmergencyCall]:
        res = []
        self._inorder(self.root, res, k)
        return res

    def total_height(self) -> int:
        return self.get_height(self.root)
