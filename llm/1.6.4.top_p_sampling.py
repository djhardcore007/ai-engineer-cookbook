import numpy as np


def top_p_sampling(input_ids, logits, p):
    """
    Perform top-p (nucleus) sampling on the given logits.
    Args:
        input_ids (list): The input token IDs.
        logits (list): The logits from the model.
        p (float): The cumulative probability threshold for top-p sampling.

    Returns:
        int: The sampled token ID.
    """


    # Convert logits to numpy array for easier manipulation
    logits = np.array(logits)

    # Sort logits and their indices in descending order
    sorted_indices = np.argsort(logits)[::-1]
    sorted_logits = logits[sorted_indices]

    # Apply softmax to get probabilities
    exp_logits = np.exp(sorted_logits - np.max(sorted_logits))
    probabilities = exp_logits / exp_logits.sum()

    # Compute cumulative probabilities
    cumulative_probs = np.cumsum(probabilities)

    # Find the cutoff index where cumulative probability exceeds p
    cutoff_index = np.searchsorted(cumulative_probs, p) + 1

    # Select the top tokens based on the cutoff
    top_indices = sorted_indices[:cutoff_index]
    top_probs = probabilities[:cutoff_index]
    top_probs /= top_probs.sum()  # Normalize probabilities

    # Sample from the top tokens based on the computed probabilities
    sampled_index = np.random.choice(top_indices, p=top_probs)

    return sampled_index