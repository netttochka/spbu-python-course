import random
from typing import Optional, Iterator, Tuple, Any
from collections.abc import MutableMapping


class TreapNode:
    """
    Represents a node in the Treap structure.

    Attributes:
        key: The key of the node, which is an integer.
        value: The value associated with the key.
        priority: The priority of the node (used for balancing the Treap).
        left: Left child node.
        right: Right child node.
    """

    def __init__(self, key: int, value: Any, priority: Optional[int] = None):
        self.key: int = key
        self.value: Any = value
        self.priority: int = (
            priority if priority is not None else random.randint(1, 2**31 - 1)
        )
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None


class Treap(MutableMapping):
    """
    A Treap (also known as Cartesian Tree) is a data structure that combines binary search tree and heap properties.
    It supports efficient insertion, deletion, and searching.

    Implements MutableMapping, so it supports dictionary-like operations.
    """

    def __init__(self, root: Optional[TreapNode] = None):
        self.root: Optional[TreapNode] = root

    def split(
        self, node: Optional[TreapNode], key: int
    ) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """
        Splits the Treap into two sub-treaps: one with keys smaller than the given key,
        and the other with keys greater or equal to the given key.

        Args:
            node: The current root node to start splitting.
            key: The key at which to split the tree.

        Returns:
            A tuple containing the two resulting sub-trees.
        """
        if node is None:
            return None, None
        elif key < node.key:
            left, node.left = self.split(node.left, key)
            return left, node
        else:
            node.right, right = self.split(node.right, key)
            return node, right

    def merge(
        self, left_node: Optional[TreapNode], right_node: Optional[TreapNode]
    ) -> Optional[TreapNode]:
        """
        Merges two Treaps into one, maintaining the Treap properties.

        Args:
            left_node: The root node of the first sub-tree.
            right_node: The root node of the second sub-tree.

        Returns:
            The root node of the merged Treap.
        """
        if right_node is None:
            return left_node
        if left_node is None:
            return right_node
        elif left_node.priority > right_node.priority:
            left_node.right = self.merge(left_node.right, right_node)
            return left_node
        else:
            right_node.left = self.merge(left_node, right_node.left)
            return right_node

    def insert(self, node: Optional[TreapNode], key: int, value: Any) -> TreapNode:
        """
        Inserts a new node into the Treap or updates the value of an existing node.

        Args:
            node: The current root node.
            key: The key of the node to insert.
            value: The value associated with the key.

        Returns:
            The updated root node of the Treap.
        """
        if not node:
            return TreapNode(key, value)
        if key == node.key:
            node.value = value
        elif key < node.key:
            node.left = self.insert(node.left, key, value)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self.insert(node.right, key, value)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        return node

    def __len__(self) -> int:
        """
        Returns the number of elements in the Treap.
        """
        return self._size(self.root)

    def _size(self, node: Optional[TreapNode]) -> int:
        """
        Calculates the size (number of nodes) in the Treap.

        Args:
            node: The node to start counting from.

        Returns:
            The number of nodes in the subtree rooted at `node`.
        """
        if node is None:
            return 0
        return 1 + self._size(node.left) + self._size(node.right)

    def __contains__(self, key: Any) -> bool:
        """
        Checks if the key exists in the Treap.

        Args:
            key: The key to search for.

        Returns:
            True if the key exists, False otherwise.
        """
        return self._find(self.root, key) is not None

    def __setitem__(self, key: int, value: Any) -> None:
        """
        Sets the value for the given key in the Treap.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        self.root = self.insert(self.root, key, value)

    def __getitem__(self, key: int) -> Any:
        """
        Retrieves the value associated with the given key.

        Args:
            key: The key whose associated value is to be retrieved.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        value = self._find(self.root, key)
        if value is None:
            raise KeyError(f"Key {key} not found")
        return value

    def __delitem__(self, key: int) -> None:
        """
        Deletes the key-value pair from the Treap.

        Args:
            key: The key to delete.

        Raises:
            KeyError: If the key is not found.
        """
        self.root = self._delete(self.root, key)

    def _find(self, node: Optional[TreapNode], key: int) -> Any:
        """
        Searches for the key in the Treap and returns its associated value.

        Args:
            node: The node to start the search from.
            key: The key to search for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def _delete(self, node: Optional[TreapNode], key: int) -> Optional[TreapNode]:
        """
        Deletes the node with the given key from the Treap.

        Args:
            node: The current root node.
            key: The key to delete.

        Returns:
            The updated root node of the Treap after deletion.

        Raises:
            KeyError: If the key is not found.
        """
        if node is None:
            raise KeyError(f"Key {key} not found")
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            node = self.merge(node.left, node.right)
        return node

    def __iter__(self) -> Iterator:
        """
        Returns an iterator for the Treap that traverses the keys in ascending order.
        """
        return self._inorder_iter(self.root)

    def _inorder_iter(self, node: Optional[TreapNode]) -> Iterator:
        """
        Helper method for inorder traversal (ascending order).

        Args:
            node: The node to start the traversal from.

        Yields:
            The keys of the Treap in ascending order.
        """
        if node:
            yield from self._inorder_iter(node.left)
            yield node.key
            yield from self._inorder_iter(node.right)

    def __reversed__(self) -> Iterator:
        """
        Returns an iterator for the Treap that traverses the keys in descending order.
        """
        return self._reverse_inorder_iter(self.root)

    def _reverse_inorder_iter(self, node: Optional[TreapNode]) -> Iterator:
        """
        Helper method for reverse inorder traversal (descending order).

        Args:
            node: The node to start the traversal from.

        Yields:
            The keys of the Treap in descending order.
        """
        if node:
            yield from self._reverse_inorder_iter(node.right)
            yield node.key
            yield from self._reverse_inorder_iter(node.left)

    def _rotate_right(self, node: TreapNode) -> TreapNode:
        """
        Performs a right rotation on the given node to maintain the Treap's heap property.

        Args:
            node: The node to rotate.

        Returns:
            The new root of the subtree after the rotation.
        """
        if node.left is None:
            return node
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node: TreapNode) -> TreapNode:
        """
        Performs a left rotation on the given node to maintain the Treap's heap property.

        Args:
            node: The node to rotate.

        Returns:
            The new root of the subtree after the rotation.
        """
        if node.right is None:
            return node
        right = node.right
        node.right = right.left
        right.left = node
        return right
