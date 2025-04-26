import re
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_name = "sonoisa/t5-base-japanese"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def clean_text(text: str) -> str:
    """
    ノイズ除去用の前処理関数：タグやURLを除去
    """
    text = re.sub(r'\[.*?\]', '', text)  # [画像]系のタグ除去
    text = re.sub(r'https?://\S+', '', text)  # URL除去
    text = re.sub(r'\s+', ' ', text)  # 連続空白除去
    return text.strip()

def summarize_text(text, fallback_title=None):
    """
    要約生成：短文にはfallbackとしてタイトル使用、max_length自動調整
    """
    if not text or len(text.strip()) < 50:
        if fallback_title:
            text = fallback_title
        else:
            return "※ 要約対象の本文が短すぎます"

    text = clean_text(text)

    input_text = f"summarize: {text}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    # 自動で max_length を調整（入力より小さめに）
    input_length = input_ids.shape[1]
    max_len = max(40, int(input_length * 0.8))
    min_len = max(20, int(input_length * 0.3))

    summary_ids = model.generate(
        input_ids,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        num_beams=4
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
