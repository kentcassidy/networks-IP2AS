
# Opens and parses contents of the Autonomous System table.
# Each line is converted to a touple of variable types, which are appended to a single output list.
def parse_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            ip, mask, as_number = line.split(sep=' ')
            ip1, ip2, ip3, ip4 = ip.split(sep='.')
            ip_bin = format(int(ip1), '08b') + format(int(ip2), '08b') + format(int(ip3), '08b') + format(int(ip4), '08b')
            data.append((ip, ip_bin, mask, as_number))
    return data


# The trie data structure allows a tree to be easily indexed and accessed by the value of the ip prefix.
# Each trie node includes the Autonomous System that corresponds to its ip, as well as a binary and decimal
# representation of its ip for easy access. Though there is redundancy between the value of the trie index
# and the AS ip, the search function below does not retain the value of the index - only the latest working value
# as it continues its search.
class TrieNode:
    def __init__(self):
        self.children = {}
        self.as_number = ""
        self.mask = ""
        self.as_ip_bin = ""
        self.as_ip_dec = ""
        self.end = False


# The trie data structure. Creation of the tree is within main, where each parsed AS element navigates down the tree and is stored.
# Each child represents a single bit along the ip prefix, making this trie binary.
# The search function compares each bit in the desired ip with each bit in the AS list, until the child indicates it is at end / leaf node with no children.
# Though the search function does not exactly remember the latest successful index, the data is accessed and retained from the last compatible node.
# If there are no further matching "longest prefixes", the search will return the previous successful match, should it exist.
class BinaryIPTrie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, ip_dec, ip_bin, masklen, as_number):
        current = self.root
        for i in range(int(masklen)):
            if current.as_number == "":
                current.as_number = as_number
                current.mask = masklen
            char = ip_bin[i] 
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        # At end of latest ip prefix, retain the values for reaccess
        current.end = True
        current.as_number = as_number
        current.mask = masklen
        current.as_ip_bin = ip_bin
        current.as_ip_dec = ip_dec

    def search(self, ip):
        current = self.root
        for i in range(len(ip)):
            char = ip[i]
            if (current.as_number != "" and i >= int(current.mask)):
                as_number = current.as_number
                masklen = current.mask
                as_ip_dec = current.as_ip_dec
            if char not in current.children:
                if current.as_number != "":
                    return as_number, masklen, as_ip_dec
                else:
                    return "Nothing found", 0
            current = current.children[char]
        return "Nothing found", 0

# Main first constructs the trie using inputs from the AS DB file.
# Main then reads the IP list file by line, once more converts the ip into binary
# (while retaining decimal notation for easy access / printing), then searches, prints.
def main():
    filename = "DB_091803_v1.txt"
    data = parse_file(filename)
    trie = BinaryIPTrie()
    for item in data:
        trie.insert(*item)

    inputfile = "IPlist.txt"
    with open(inputfile, 'r') as file:
        for line in file:
            ip1, ip2, ip3, ip4 = line.split(sep='.')
            ip_str = line
            # 08b prepends 0s to each integer conversion in order to conform each segment to 8 bits.
            # This is important for trie navigation
            ip = format(int(ip1), '08b') + format(int(ip2), '08b') + format(int(ip3), '08b') + format(int(ip4), '08b')
            as_number, masklen, as_ip = trie.search(ip)
            if (masklen != 0):
                print((as_ip + "/" + masklen + " " + as_number.rstrip() + " " + ip_str.rstrip()).rstrip())
            else: # This line is for errors or missing AS, which we do not expect in this assignment.
                print((ip_str.rstrip() + " does not have a corresponding AS").rstrip())


if __name__ == '__main__':
    main()
