def build_prompt(user_text: str, csv_snippet: str) -> str:
    return f"""Guess the calories and macros (proteins,fats, carbs) of the food the user of a calories tracking application reported with the following text:
<eaten-food>{user_text}</eaten-food>
Help yourself with sections of a CSV I included in the chat, if any.
<csv>{csv_snippet}</csv>

Proceed like this:
1. Estimate the different aliments in the description, and the full weight of the each food the user eaten, if no specific amount was written (otherwise use the specified amount). When doing so, first estimate and write down how many calories there is in a single item (for instance one apple), then multiply for the number specified by the user.
2. Split foods in their components. Like 100 grams of pasta with tomatoes is two items (if not three because of the oil), and so forth.
3. Then adjust the calories and macros depending on the table specification (for instance if the table is for 100 grams, and the weight of what the user eaten is 10, of course we need to adjust). Finally make sure that the macros and the calories are correctly proportional.
Consider that 1 gram of carbo have 4 kcal, 1 gram of proteins 3.5 kcal, 1 gram of fat 9 kcal.
5. In the estimate of ingredients and quantities, consider the potential country the user lives based on the used query language.

Steps to follow to produce the reply:
- First do a step of reasoning where all the macros per 100 grams of products are shown, plus the reasoning steps needed to provide a good answer.
- Report the final answer as in the following example (note that the example may not be accurate, it's just for formatting).
The json will have the TOTAL of calories and macros.
- Don't write anything past </reply>, but write your reasoning before <reply>.
- For the "text" section, use the same language used in the user food description in <eaten-food>.
- For each item in the text, use an appropriate emoji.
<reply>
<text> 
[emoji]120 grams dry pasta, ~440 calories (~88g carbs, ~15g protein, ~2g fat)
[emoji] 35 grams tomato, ~6 calories (~1.4g carbs, ~0.3g protein, ~0.1g fat)
...
</text>
<json>
{{
kcal: ..., 
proteins: ..., 
carbos: ..., 
fats:...
}}
</json>
</reply>"""
