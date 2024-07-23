from transformers import pipeline
pipe = pipeline("text-classification", model="krishkpatil/bert-classifier")

def check_for_confidential_info(message):

    output = pipe([message], padding=False, truncation=True, max_length=256)
    output=output[0]["label"]
    if output=="LABEL_0":
        return 'public'
    elif output=="LABEL_1":
        return 'confidential'
    elif output=="LABEL_2":
        return 'sensitive'
