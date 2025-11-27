def greedy_search(logits, max_len=20, pad_token_id=0, eos_token_id=1):
    """
    Perform greedy search decoding.

    Args:
        logits (list of list of float): The logits for each token at each time step.
        max_len (int): Maximum length of the generated sequence.
        pad_token_id (int): Token ID for padding.
        eos_token_id (int): Token ID for end-of-sequence.

    Returns:
        list of int: The generated token IDs.
    """
    generated_ids = []
    for step in range(max_len):
        # Get the logits for the current step
        step_logits = logits[step]
        
        # Select the token with the highest logit
        next_token_id = step_logits.index(max(step_logits))
        generated_ids.append(next_token_id)
        
        # Stop if we reach the end-of-sequence token
        if next_token_id == eos_token_id:
            break

    # Pad the sequence if it's shorter than max_len
    while len(generated_ids) < max_len:
        generated_ids.append(pad_token_id)

    return generated_ids
    