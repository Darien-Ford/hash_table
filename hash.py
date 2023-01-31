from typing import TypeVar, List, Tuple

Type = TypeVar("Type")
Node = TypeVar("Node")
HashTable = TypeVar("HashTable")


class Node:
    """
    Node Class
    """

    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: Type, deleted: bool = False) -> None:
        """
        Initializes node
        :param key: node's key
        :param value: node's value
        :param deleted: boolean indicating if node has been deleted
        """

        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        """
        Represents the node as a string
        :return: string representation of the node
        """

        return f"node({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other_node: Node) -> bool:
        """
        Equality operator
        :param other_node: node being compared with this one
        :return: boolean that represents equality
        """

        return self.key == other_node.key and self.value == other_node.value

    def __iadd__(self, other_value: Type) -> None:
        """
        Addition assignment operator
        :param other_value: value being added to this one
        """
        self.value += other_value


class HashTable:
    """
    Hash Table Class
    """

    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    prime_numbers = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        """
        Initializes hash table
        :param capacity: capacity of the hash table
        """

        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        i = 0

        while HashTable.prime_numbers[i] <= self.capacity:
            i += 1

        self.prime_index = i - 1

    def __str__(self) -> str:
        """
        Represents the hash table as a string
        :return: string representation of the hash table
        """

        string = ""
        bin_num = 0

        for item in self.table:
            string += "[" + str(bin_num) + "]: " + str(item) + '\n'
            bin_num += 1

        return string

    __repr__ = __str__

    def __eq__(self, other_table: HashTable) -> bool:
        """
        Equality operator
        :param other_table: hash table being compared with this one
        :return: boolean that represents equality
        """

        if self.capacity != other_table.capacity or self.size != other_table.size:
            return False

        for i in range(self.capacity):

            if self.table[i] != other_table.table[i]:
                return False

        return True

    def __len__(self) -> int:
        """
        Getter function for the size of Hash Table
        :return: int that is size of Hash Table
        """

        return self.size

    def __setitem__(self, key: str, value: Type) -> None:
        """
        Sets the value of a node with given key to given value
        :param key: key of node to set
        :param value: value to set node to
        """

        self._insert(key, value)

    def __getitem__(self, key: str) -> Type:
        """
        Looks up value associated with given key in Hash Table
        Raises KeyError if key not found
        :param key: key of node with value to return
        :return: int that is value associated with key
        """

        if self._get(key):
            return self._get(key).value

        raise KeyError("Item not found.")

    def __delitem__(self, key: str) -> None:
        """
        Deletes the value associated with given key in Hash Table
        Raises KeyError if key not found
        :param key: key of node to be deleted
        """

        if self._get(key):
            self._delete(key)

        else:
            raise KeyError("Item not found.")

    def __contains__(self, key: str) -> bool:
        """
        Determines if a node with the given key is in the Hash Table
        :param key: key of node being looked for
        :return: boolean representing if the node is in the Hash Table
        """

        return self._get(key) is not None

    def _hash_1(self, key: str) -> int:
        """
        Converts a string into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item, None if key is an empty string
        """

        if not key:
            return None

        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        Converts a string into a hash
        :param key: key to be hashed
        :return: a hashed value, None if key is an empty string
        """

        if not key:
            return None

        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.prime_numbers[self.prime_index]
        hashed_value = prime - (hashed_value % prime)

        if hashed_value % 2 == 0:
            hashed_value += 1

        return hashed_value

    def _hash(self, key: str, inserting: bool = False) -> int:
        """
        Computes an index for a key using double hashing
        :param key: key to find index for
        :param inserting: boolean representing if node is going to be inserted
        :return: int representing index for given key
        """

        i = 0
        hash_bin = (self._hash_1(key) + i * self._hash_2(key)) % len(self.table)
        bin_item = self.table[hash_bin]

        if inserting:

            while bin_item:

                if bin_item.value is None or bin_item.key == key:
                    break

                i += 1
                hash_bin = (self._hash_1(key) + (i * self._hash_2(key))) % self.capacity
                bin_item = self.table[hash_bin]

        else:

            while hash_bin:

                if not bin_item or bin_item.key == key:
                    break

                i += 1
                hash_bin = (self._hash_1(key) + (i * self._hash_2(key))) % self.capacity
                bin_item = self.table[hash_bin]

        return hash_bin

    def _insert(self, key: str, value: Type) -> None:
        """
        Inserts node with given key and value into Hash Table
        Updates value of node with given key if already in Hash Table
        Resizes Hash Table if load factor >= 0.5
        :param key: key of node being inserted into Hash Table
        :param value: value of node being inserted into Hash Table
        """

        index = self._hash(key, True)

        if self.table[index]:
            self.table[index].value = value
            self.table[index].key = key

        else:
            self.table[index] = Node(key, value)
            self.size += 1

        load_factor = self.size / self.capacity

        if load_factor >= .5:
            self._grow()

    def _get(self, key: str) -> Node:
        """
        Finds the node with the given key in the Hash Table
        :param key: key of node to find
        :return: node with given key, None if not in Hash Table
        """

        return self.table[self._hash(key)]

    def _delete(self, key: str) -> None:
        """
        Removes node with given key from Hash Table
        :param key: key of the node to remove
        """

        n = self.table[self._hash(key)]
        n.key, n.value, n.deleted = None, None, True
        self.size -= 1

    def _grow(self) -> None:
        """
        Doubles capacity of Hash Table
        Rehashes all nodes except deleted ones
        """

        new_capacity = self.capacity * 2
        new_hashtable = HashTable(new_capacity)

        for i in range(self.capacity):
            n = self.table[i]

            if n and not n.deleted:
                new_hashtable._insert(n.key, n.value)

        self.capacity = new_capacity
        self.size = new_hashtable.size
        self.table = new_hashtable.table
        self.prime_index = new_hashtable.prime_index

    def update(self, pairs: List[Tuple[str, Type]] = []) -> None:
        """
        Updates/Inserts nodes into Hash Table from list
        :param pairs: list of (key, value) tuples to insert
        """

        for i in range(len(pairs)):
            self._insert(pairs[i][0], pairs[i][1])

    def keys(self) -> List[str]:
        """
        Makes list of keys in Hash Table
        :return: list of keys
        """

        hash_keys = []

        for i in range(self.capacity):

            if self.table[i]:
                hash_keys.append(self.table[i].key)

        return hash_keys

    def values(self) -> List[Type]:
        """
        Makes list of values in Hash Table
        :return list of values
        """

        hash_values = []

        for i in range(self.capacity):

            if self.table[i]:
                hash_values.append(self.table[i].value)

        return hash_values

    def items(self) -> List[Tuple[str, Type]]:
        """
        Makes list of (key, value) tuples in Hash Table
        :return: list of items
        """

        hash_items = []

        for i in range(self.capacity):

            if self.table[i]:
                key = self.table[i].key
                value = self.table[i].value
                hash_items.append((key, value))

        return hash_items

    def clear(self) -> None:
        """
        Clears Hash Table of all nodes
        """

        for i in range(self.capacity):

            if self.table[i]:
                self.table[i] = None

        self.size = 0
