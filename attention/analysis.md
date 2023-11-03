# Analysis

## Layer 10, Head 10

Layer 10, Head 10 seems to be paying attention to adjectives that defines the [MASK]. 
Note that for the [MASK] it attends the most to the adjective ("white" or "old"). 
Also, even with sentences with more different structures, such as "That is a white [MASK]" 
and "That [MASK] is white.", this result is visble.

Example Sentences:
- His [MASK] was old.
- That is a white [MASK]
- That [MASK] is white.

![His MASK was old.](images/Attention_Layer10_Head10%20-%20His%20[MASK]%20was%20old.png)
![That is a white MASK.](images/Attention_Layer10_Head10%20-%20That%20is%20a%20white%20[MASK].png)
![That MASK is white.](images/Attention_Layer10_Head10%20-%20That%20[MASK]%20is%20white.png)

## Layer 5, Head 8

For Layer 5, Head 8, I initially noticed that it attends to the determiner of the [MASK] but 
it also seems to be paying attention to the demonstrative pronouns (this, that, these, those) in the sentence.
If we reverse the order, "Those [MASK] are his.", we can still see the attention to the word "those".
Although a bit more blurry, the results can also be seen in Layer 7, Head 12 and Layer 8, Head 12

Example Sentences:
- Those are his [MASK].
- That is my [MASK].
- Those [MASK] are his.

![Those are his MASK.](images/Attention_Layer5_Head8%20-%20Those%20are%20his%20[MASK].png)
![That is my MASK.](images/Attention_Layer5_Head8%20-%20That%20is%20my%20[MASK].png)
![Those MASK are his.](images/Attention_Layer5_Head8%20-%20Those%20[MASK]%20are%20his.png)