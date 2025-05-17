class ParseTreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"{self.value} -> {self.children}"
class SimpleEnglishParser:
    def __init__(self):
        # Define the grammar for the parser
        self.grammar = {
            'Determiner': ['the', 'a', 'an'],
            'Noun': ['cat', 'dog', 'man', 'woman'],
            'ProperNoun': ['Alice', 'Bob'],
            'Verb': ['eats', 'sleeps', 'sits'],

        }

    def tokenize(self, sentence):
        # Convert the sentence to lowercase and split into tokens
        return sentence.lower().split()

    def is_noun_phrase(self, tokens):
        # Check if the tokens form a valid noun phrase
        if len(tokens) == 2 and tokens[0] in self.grammar['Determiner'] and tokens[1] in self.grammar['Noun']:
            return True  # Valid noun phrase found
        if len(tokens) == 1 and tokens[0] in self.grammar['ProperNoun']:
            return True  # Valid noun phrase found
        return False  # Not a valid noun phrase

    def is_verb_phrase(self, tokens):
        # Check if the tokens form a valid verb phrase
        if len(tokens) == 1 and tokens[0] in self.grammar['Verb']:
            return True  # Valid verb phrase found
        if len(tokens) == 2 and tokens[0] in self.grammar['Verb'] and self.is_noun_phrase([tokens[1]]):
            return True  # Valid verb phrase found
        return False  # Not a valid verb phrase

    def analyze_sentence(self, sentence):
        # Tokenize the input sentence
        tokens = self.tokenize(sentence)  # Get the tokens from the sentence, that is, separates the sentence to tokens
        if len(tokens) == 0:  # Check if there are no tokens
            return "Empty sentence."

        # Check for valid noun phrase (first part of the sentence)
        noun_phrase = tokens[:2]  # Assume the first two tokens form the noun phrase
        if not self.is_noun_phrase(noun_phrase):
            return "Invalid noun phrase."

        # Check for valid verb phrase (remaining part of the sentence)
        verb_phrase = tokens[2:]  # Remaining tokens form the verb phrase
        if not self.is_verb_phrase(verb_phrase):
            return "Invalid verb phrase."

        #return "Valid sentence structure."  # If both phrases are valid
        # Build the parse tree
        root = ParseTreeNode("Sentence", [
            ParseTreeNode("NounPhrase", [ParseTreeNode(noun_phrase[0]), ParseTreeNode(noun_phrase[1])]),
            ParseTreeNode("VerbPhrase", [ParseTreeNode(verb_phrase[0])])
        ])

        return root  # Return the parse tree

# Main block for testing
if __name__ == "__main__":
    parser = SimpleEnglishParser()  # Create an instance of the parser

    # Test cases
    test_sentences = [
        "the cat eats",
        "Alice sleeps",
        "a dog sits",
        "the man",
        "Bob",
        "the dog",
        "sleeps the cat",
        "cat eats",
        "the cat sleeps quickly",
        ""
    ]

    # Evaluate each test sentence
    for sentence in test_sentences:
        result = parser.analyze_sentence(sentence)  # Analyze the sentence
        print(f"Sentence: '{sentence}' -> {result}")  # Print the result