import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config

def load_model(config_path, weights_path):
    # Načtěte konfiguraci modelu
    config = GPT2Config.from_json_file(config_path)
    
    # Načtěte váhy modelu
    model = GPT2LMHeadModel(config)
    model.load_state_dict(torch.load(weights_path))
    
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')  # Nebo můžete použít svůj vlastní tokenizer
    
    return model, tokenizer

def generate_response(model, tokenizer, input_text, max_length=50):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

if __name__ == "__main__":
    # Změňte cesty k souborům konfigurace a vahám modelu na své vlastní soubory
    config_path = 'model/model_architecture.pth'
    weights_path = 'model/model_weights.pth'
    
    # Načtěte model
    model, tokenizer = load_model(config_path, weights_path)

    print("ChatGPT: Ahoj! Pro ukončení chatu napište 'exit'.")

    while True:
        user_input = input("Ty: ")
        if user_input.lower() == 'exit':
            print("ChatGPT: Ukončuji chat. Nashledanou!")
            break

        response = generate_response(model, tokenizer, user_input)
        print(f"ChatGPT: {response}")
