class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ""

    def calc_prob(data):
        symbols = dict()
        for element in data:
            if symbols.get(element) == None:
                symbols[element] = 1
            else:
                symbols[element] += 1
        return symbols

    codes = dict()

    def calc_codes(node, val=""):
        newVal = val + str(node.code)
        if node.left:
            calc_codes(node.left, newVal)
        if node.right:
            calc_codes(node.right, newVal)
        if not node.left and not node.right:
            Node.codes[node.symbol] = newVal
        return Node.codes

    def Output_Encoded(data, coding):
        encoding_output = []
        for c in data:
            encoding_output.append(coding[c])
        string = "".join([str(item) for item in encoding_output])
        return string

    def Total_Gain(data, coding):
        before_compression = len(data) * 8
        after_compression = 0
        symbols = coding.keys()
        for symbol in symbols:
            count = data.count(symbol)
            after_compression += count * len(coding[symbol])
        print("Space usage before compression (in bits):", before_compression)
        print("Space usage after compression (in bits):", after_compression)

    def Huffman_Encoding(data):
        symbol_with_probs = calc_prob(data)
        symbols = symbol_with_probs.keys()
        probabilities = symbol_with_probs.values()
        print("symbols: ", symbols)
        print("probabilities: ", probabilities)
        nodes = []
        for symbol in symbols:
            nodes.append(Node(symbol_with_probs.get(symbol), symbol))

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.prob)
            right = nodes[0]
            left = nodes[1]
            left.code = 0
            right.code = 1
            newNode = Node(
                left.prob + right.prob, left.symbol + right.symbol, left, right
            )
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(newNode)

        huffman_encoding = calc_codes(nodes[0])
        print("symbols with codes", huffman_encoding)
        Total_Gain(data, huffman_encoding)
        encoded_output = Output_Encoded(data, huffman_encoding)
        return encoded_output, nodes[0]

    def Huffman_Decoding(encoded_data, huffman_tree):
        tree_head = huffman_tree
        decoded_output = []
        for x in encoded_data:
            if x == "1":
                huffman_tree = huffman_tree.right
            elif x == "0":
                huffman_tree = huffman_tree.left
            try:
                if (
                    huffman_tree.left.symbol == None
                    and huffman_tree.right.symbol == None
                ):
                    pass
            except AttributeError:
                decoded_output.append(huffman_tree.symbol)
                huffman_tree = tree_head

        string = "".join([str(item) for item in decoded_output])
        return string
