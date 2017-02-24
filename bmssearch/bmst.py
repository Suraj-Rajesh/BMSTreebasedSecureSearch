class Node(object):

    def __init__(self, vsm_hash = None, filename = None, children = None, encrypted_vsm_hash_1 = None, encrypted_vsm_hash_2 = None):
        self.filename = filename
        self.children = children
        # vsm_hash is:
        #     list: for internal nodes
        #     dict: for file nodes
        self.vsm_hash = vsm_hash
        self.encrypted_vsm_hash_1 = encrypted_vsm_hash_1
        self.encrypted_vsm_hash_2 = encrypted_vsm_hash_2

    # file_list should be an empty list
    def get_file_nodes(self, file_list):

        if self:
            if self.left is None or self.right is None:
                file_list.append(self.filename)
            if self.left:
                self.left.get_file_nodes(file_list)
            if self.right:
                self.right.get_file_nodes(file_list)

        return file_list

    # Search for file nodes containing query indices
    # NOTE: & on set's is intersection
    def search(self, query_indices, file_nodes):

        if self:
            if self.left is None and self.right is None and bool(set(query_indices) & set(self.vsm_hash)):
                file_nodes.append(self)
            if self.left and bool(set(query_indices) & set(self.vsm_hash)):
                self.left.search(query_indices, file_nodes)
            if self.right and bool(set(query_indices) & set(self.vsm_hash)):
                self.right.search(query_indices, file_nodes)

        return file_nodes
