import torch


def pred(input_ids):
    """Mock prediction function that returns random logits."""
    batch_size, seq_len = input_ids.shape
    generate = torch.randn(size=(batch_size, 1, 50257), device=input_ids.device) # Assuming vocab size of 50257
    return generate


def beam_search(input_ids, max_len, num_beams):
    """Performs beam search decoding."""
    batch_size = input_ids.size(0)

    expand_size = num_beams
    expanded_return_idx = (
        torch.arange(batch_size).view(-1, 1).repeat(1, expand_size).view(-1)
    )
    input_ids = input_ids.index_select(0, expanded_return_idx)
    print(input_ids)

    batch_beam_size, cur_len = input_ids.shape
    beam_scores = torch.zeros((batch_size, num_beams), dtype=torch.float)
    beam_scores[:, 1:] = -1e9
    beam_scores = beam_scores.view(size=(batch_size * num_beams,))
    
    next_tokens = torch.zeros(size=(batch_size, num_beams), dtype=torch.long)
    next_indices = torch.zeros(size=(batch_size, num_beams), dtype=torch.lon)

    while cur_len < max_len:
        logits = pred(input_ids) # (batch_size, seq_len, vocab_size)
        next_token_logits = logits[:, -1, :]

        # normalize logits to log probabilities
        next_token_scores = torch.nn.functional.log_softmax(next_token_logits, dim=-1)
        # add the previous beam scores
        next_token_scores += beam_scores[:, None].expand_as(next_token_scores)
        # reshape for beam search
        next_token_scores = next_token_scores.view(batch_size, num_beams * 50257)

        # get the top num_beams scores and their indices
        next_token_scores, next_tokens = torch.topk(next_token_scores, num_beams, dim=1, largest=True, sorted=True)
        next_tokens = next_tokens % 50257
        next_indices = next_tokens // 50257
        

        def process(input_ids, next_scores, next_tokens, next_indices, num_beams):
            next_beam_scores = torch.zeros((batch_size, num_beams), dtype=next_scores.dtype)
            next_beam_tokens = torch.zeros((batch_size, num_beams), dtype=next_tokens.dtype)
            next_beam_indices = torch.zeros((batch_size, num_beams), dtype=next_indices.dtype)
            
            for batch_idx in range(batch_size):
                beam_idx = 0
                for beam_token_rank, (next_token, next_score, next_index) in enumerate(
                    zip(next_tokens[batch_idx], next_scores[batch_idx], next_indices[batch_idx])
                ):
                    batch_beam_idx = batch_idx * num_beams + next_index.item()

                    next_beam_scores[batch_idx, beam_idx] = next_score
                    next_beam_tokens[batch_idx, beam_idx] = next_token
                    next_beam_indices[batch_idx, beam_idx] = batch_beam_idx
                    beam_idx += 1
            return next_beam_scores.view(-1), next_beam_tokens.view(-1), next_beam_indices.view(-1)
        
        beam_scores, beam_tokens, beam_indices = process(
            input_ids, next_token_scores, next_tokens, next_indices, num_beams
        )
        return input_ids, beam_scores
    
if __name__ == "__main__":
    input_ids = torch.randint(0, 100, (3, 1))
    print(input_ids)
    input_ids, beam_scores = beam_search(input_ids, max_len=10, num_beams=3)
    print("Final input_ids:", input_ids)