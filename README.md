# networks-IP2AS
This project was a collaboration between myself and a classmate who goes by Mynti, for our computer networking assignment.

IP2AS is a tool that analyzes then maps a given IP address to its corresponding AS number.
The script will parse the list of IP addresses from "IPlist.txt", then declare if it aligns with any of the subnets defined in "DB_091803_v1.txt".

To perform this task, we needed a firm understanding of IP formatting and subnet masking. In our case, we implemented this technique using a trie data structure for efficient mapping.
This tool executes tasks that are fundamental to modern BGP operations, and reflects our understanding of CIDR-based IP parsing.
