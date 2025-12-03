import numpy as np


def top_k_sampling(input_ids, logits, k):
    """
    Perform top-k sampling on the given logits.

    Args:
        input_ids (list): The input token IDs.
        logits (list): The logits for the next token prediction.
        k (int): The number of top tokens to consider for sampling.
    Returns:
        int: The sampled token ID from the top-k tokens.
    """
    # Convert logits to numpy array for easier manipulation
    logits = np.array(logits)

    # Get the indices of the top-k logits
    top_k_indices = np.argsort(logits)[-k:]

    # Get the top-k logits
    top_k_logits = logits[top_k_indices]

    # Apply softmax to get probabilities
    exp_logits = np.exp(top_k_logits - np.max(top_k_logits))
    probabilities = exp_logits / exp_logits.sum()

    # Sample from the top-k tokens based on the computed probabilities
    sampled_index = np.random.choice(top_k_indices, p=probabilities)

    return sampled_index
    