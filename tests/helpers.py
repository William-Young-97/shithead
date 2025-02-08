def fake_input_sequence(responses):
    responses_iter = iter(responses)
    def inner(prompt):
        return next(responses_iter)
    return inner

def fake_output(message):
    pass