class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
            
class LinkedList:
    def __init__(self):
        self.head = None

class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8

class HashTable:
    """
    A hash table that with `capacity` slots
    that accepts string keys
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.loaded_count = 0
        self.slots = [None]*capacity
        self.max_load_factor = 0.7


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.
        """
        return self.capacity

    
    def get_load_factor(self):
        """
        Return the load factor for this hash table.
        """
        return self.loaded_count / self.capacity 
    
    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit
        Implement this, and/or DJB2.

https://en.wikipedia.org/wiki/Fowler%E2%80%93Noll%E2%80%93Vo_hash_function
        Implements FNV hashing for strings.
        
        For example, for the kv pair 'Jud' - Cheeseburger'
        the key 'Jud' gets hashed."""
        
        FNV_offset_basis = 14695981039346656037
        FNV_prime = 1099511628211
        
        bytes_of_data = key.encode()
        
        # initial value of hash
        my_hash = FNV_offset_basis
        
        for b in bytes_of_data:
            my_hash = b * FNV_prime
            my_hash = b ^ my_hash # XOR   
            
        return my_hash
    
    
    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.fnv1(key) % self.capacity
#         return self.djb2(key) % self.capacity



    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.
        """
        
        # make a node to put in linked_list
        new_entry = HashTableEntry(key,value)

        # hash value and choose a slot (a linked list) to which to add
        slot = self.hash_index(key)
         
        # if there is no linked list, create one
        if self.slots[slot] is None:
            self.slots[slot] = LinkedList()
            
        # now there is a linked list, with a head
        self.slots[slot].head = new_entry

        self.loaded_count += 1  # keep count of entries for load manangement

        return value
    
    
    def get(self, key_sought):
        """
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        """
        
        slot = self.hash_index(key_sought)
        
        # if there is no linked list at the index, there cannot
        # be a match for the key
        if self.slots[slot] is None:
            return None
        
        # traverse
        cur = self.slots[slot].head
        
        while cur is not None:
            if cur.key == key_sought:
                return cur.value
            cur = cur.next
        
        # If we get here, no match for the key sought was found in
        # the linked list
        return None
    
    
    
    
    def delete(self, key_sought):
        """
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        """
        slot = self.hash_index(key_sought)
#         print(slot)
        
        # if there is no linked list at the index, there cannot
        # be a match for the key
        if self.slots[slot] is None:
            return f"No entry matching key; {key_sought}"
        
        # the list has at least one node.
        linked_list = self.slots[slot]
        cur = linked_list.head
            
        if cur.key == key_sought:
            linked_list.head = linked_list.head.next
            self.loaded_count -= 1  # keep count of entries for load manangement
            return "Record removed."
        
        prev = cur
        cur = cur.next
        
        while cur is not None:
            if cur.key == key_sought: # Found it.
                prev.next = cur.next #removes pointer to deleted node
                self.loaded_count -= 1  # keep count of entries for load manangement
                return "Record removed."
                
            else: # Keep looking.
                prev = prev.next
                cur = cur.next
                    
        return f"No entry matching key; {key_sought}"
    
    def djb2(self, key):
        """
        DJB2 hash, 32-bit
        Implement this, and/or FNV-1.
        """
        pass

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.
        """
        larger_table = HashTable(new_capacity)

        for linked_list in self.slots:
            if linked_list is not None:
                cur = linked_list.head
                while cur is not None:
                    larger_table.put(cur.key, cur.value)
                    cur = cur.next
                
        self = larger_table
        return f'Resized to capacity: {self.capacity}'



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
            
class LinkedList:
    def __init__(self):
        self.head = None
        
    def insert_at_head(self, node): # consing
        node.next = self.head
        self.head = node
        
        
    def find(self, value):
        cur = self.head
        
        # traverse
        while cur is not None:
            if cur.value == value:
            return cur
        cur = cur.next
    
        # if we got here, nothing found
        return None
        
        def delete(self, value):
            cur = self.head
            
            if cur.value == value:
                self.head = self.head.next
                return cur
            
            prev = cur
            cur = cur.next
            
            while cur is not None:
                if cur.value == value:
                    prev.next = cur.next #removes pointer to deleted node
                    return cur
                
                else: 
                    prev = prev.next
                    cur = cur.next
                    
            return None  # didn't find it
            
                
    
        
    