# QuoraChallenges-Ontology
**Topic based Fast Searching Problem**

My solution for Ontology question in Quora Challenges.

The challenge is to search quickly how many sentences in a given topic from the dataset match a new sentence in the same topic. Complete problem description can be found here - https://www.quora.com/about/challenges#ontology

The solution is to construct a Multinode Tree inside a Trie. Multinode tree is used for saving the topics hierarchy and Trie for prefix matching the new sentence with existing sentences in the dataset.
