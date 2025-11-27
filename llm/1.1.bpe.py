import re, collections

text = "How are u today? How Howler? Howery uu"

def get_vocab(text):
    vocab = collections.defaultdict(int)
    for w in text.strip().split():
        vocab[" ".join(list(w)) + " </w>"] += 1
    return vocab

def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for w, freq in vocab.items():
        symbols = w.split()
        for i in range(len(symbols)-1):
            pairs[(symbols[i], symbols[i+1])]
    return pairs


def merge_vocab(pair, vocab_cur):
    vocab_new = {}
    bigram = re.escape(" ".join(pair))
    
    # u only allow chars before not after
    p = re.compile(
        r'(?<!\S)' + bigram + r'(?!\S)'
    )

    for v_cur in vocab_cur:
        v_new = p.sub("".join(pair), v_cur)
        vocab_new[v_new] = vocab_cur[v_cur]
    return vocab_new


def get_tokens(vocab):
    tokens = collections.defaultdict(int)
    for w, freq in vocab.items():
        word_tokens = w.split()
        for token in word_tokens:
            tokens[token] += freq
    return tokens


if __name__ == "__main__":
    vocab = get_vocab(text)
    print("------vocab-----")
    print(vocab)
    tokens = get_tokens(vocab)
    print(f"tokens: {tokens}")
    print(f"# of tokens: {len(tokens)}")
    print("===============")
    num_merges = 100
    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        # merge the pairs w highest freq
        best = max(pairs, key=pairs.get)

        new_token = "".join(best)
        vocab = merge_vocab(best, vocab)

        print(f"iter: {i}")
        print(f"best pair: {best}")

        tokens[new_token] = pairs[best]
        tokens[best[0]] -= pairs[best]
        tokens[best[1]] -= pairs[best]
        print(f"token: {tokens}")
        print(f"# tokens: {len(tokens)}")
        print(f"vocab: {vocab}")
        print("==============")