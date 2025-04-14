from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from language_tool_python import LanguageTool

class LangCheckerModule:
    def __init__(self):
        self.grammar_check = LanguageTool("en-US")
        self.tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

    def correct_spelling(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        outputs = self.model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text

    def correct_grammar(self, text):
        matches = self.grammar_check.check(text)
        found_mistakes = []
        for mistake in matches:
            start_offset = mistake.offset
            end_offset = start_offset + mistake.errorLength
            incorrect_word = text[start_offset:end_offset]
            found_mistakes.append(incorrect_word)
        return found_mistakes

if __name__ == "__main__":
    obj = LangCheckerModule()
    message = "Helo world. Plese give me banan. mashine"
    print(obj.correct_spelling(message))
    print(obj.correct_grammar(message))