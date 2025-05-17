import re

class ParseTreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"{self.value} -> {self.children}"

def tokenize(sentence):
    tokens = re.findall(r'\b\w+\b', sentence.lower())
    return tokens

class SimpleEnglishParser:
    def __init__(self):
        # Define the grammar
        self.grammar = {
            'S': [['NP', 'VP']],
            'NP': [['PN'], ['Det', 'Adj', 'N'], ['Det', 'N']],  # Noun phrase including proper nouns
            'VP': [['Aux', 'Adj'], ['V', 'NP'], ['Aux', 'NP']],  # Allows linking verb followed by NP
            'Det': ['the', 'a', 'an'],  # Determiners
            'N': ['cat', 'dog', 'man', 'woman', 'girl'],  # Nouns
            'Adj': ['big', 'brown', 'lazy'],  # Adjectives
            'PN': ['kelly', 'alice', 'bob'],  # Proper nouns
            'V': ['eats', 'sleeps', 'sits'],  # Verbs
            'Aux': ['is', 'are']  # Auxiliary verbs
        }

    def analyze_sentence(self, sentence):
        tokens = tokenize(sentence)
        is_valid, parse_tree = self.parse(tokens, 'S')
        return parse_tree if is_valid else "Invalid sentence structure."

    def parse(self, tokens, symbol):
        if len(tokens) == 0:
            return False, None

        if symbol not in self.grammar:
            if len(tokens) == 1 and tokens[0] == symbol:
                return True, ParseTreeNode(symbol)
            return False, None

        for production in self.grammar[symbol]:
            remaining_tokens = tokens[:]
            children = []
            valid = True

            for sym in production:
                if remaining_tokens:
                    if remaining_tokens[0] in self.grammar.get(sym, []):
                        children.append(ParseTreeNode(remaining_tokens.pop(0)))
                    elif sym == 'PN' and remaining_tokens[0] in self.grammar['PN']:
                        children.append(ParseTreeNode(remaining_tokens.pop(0)))
                    else:
                        is_valid, child_tree = self.parse(remaining_tokens, sym)
                        if not is_valid:
                            valid = False
                            break
                        children.append(child_tree)

            if valid:
                return True, ParseTreeNode(symbol, children)

        return False, None

# Main block for testing
if __name__ == "__main__":
    parser = SimpleEnglishParser()

    while True:
        user_input = input("Enter a sentence to analyze (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        result = parser.analyze_sentence(user_input)
        print(f"Sentence: '{user_input}' -> {result}")