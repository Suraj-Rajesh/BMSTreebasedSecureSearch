from operator import itemgetter

from bmssearch.helpers.operations import matrix_multiplication

class Node(object):

    def __init__(self, vsm_hash = None, filename = None, children = None, encrypted_vsm_hash_1 = None, encrypted_vsm_hash_2 = None):
        self.filename = filename
        self.children = children
        self.encrypted_vsm_hash_1 = encrypted_vsm_hash_1
        self.encrypted_vsm_hash_2 = encrypted_vsm_hash_2

        # vsm_hash is None in BMSTree
        self.vsm_hash = vsm_hash

    # Search for file nodes containing query indices
    # encrypted_query_indices: list of query indices[m1iq1, m2iq2]
    def search(self, encrypted_query_indices, file_nodes, top_k):

        if self:
            # Check if file node
            if self.children is None:
                # Get score
                score = matrix_multiplication(self.encrypted_vsm_hash_1, encrypted_query_indices[0]) + matrix_multiplication(self.encrypted_vsm_hash_2, encrypted_query_indices[1])
                # If score is really small, implies it should be ideally zero, but due to numerical varaitions in matrix inverse, they are showing up as extremely small values
                if score < 1e-6:
                    score = 0

                if len(file_nodes) < top_k and score != 0:
                    # Add (filename, score) to list
                    file_nodes.append((self.filename, score))

                if len(file_nodes) == top_k and score != 0:
                    minimum =  min(file_node[1] for file_node in file_nodes)
                    
                    # If my score is greater than minimum
                    if score > minimum:
                        # Replace minimum and add this new file node to list of file nodes
                        for index, file_node in enumerate(file_nodes):
                            if file_node[1] == minimum:
                                file_nodes[index] = (self.filename, score)
                                break
            else:
                # Internal node
                child_node_score = dict()

                for child in self.children:
                    # Calculate similarity score
                    score = matrix_multiplication(self.encrypted_vsm_hash_1, encrypted_query_indices[0]) + matrix_multiplication(self.encrypted_vsm_hash_2, encrypted_query_indices[1])

                    # Check if needs processing or to ignore
                    
                    # First check if file nodes exists
                    if file_nodes:
                        if not (score < min(file_node[1] for file_node in file_nodes) and len(file_nodes) == top_k):
                            # Children's similarity scores mapped
                            child_node_score[child] = score
                    else:
                        # Children's similarity scores mapped
                        child_node_score[child] = score

                # Sort in descending order of scores
                child_node_processing_order = sorted(child_node_score.items(), key = itemgetter(1), reverse = True)
                child_node_processing_order = [child_node_list[0] for child_node_list in child_node_processing_order]

                for child_node in child_node_processing_order:
                    child_node.search(encrypted_query_indices, file_nodes, top_k)

        return file_nodes
