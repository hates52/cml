import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import spacy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Načtení CSV souboru
df = pd.read_csv('dataset/dataset.csv')

# Předzpracování JSON logů
df['log'] = df['log'].apply(json.loads)

# Tokenizace logů
nlp = spacy.load('en_core_web_sm')
df['tokenized_log'] = df['log'].apply(lambda x: [token.text for token in nlp(x)])

# Kategorizace podle aplikací
label_encoder = LabelEncoder()
df['category'] = label_encoder.fit_transform(df['aplikace'])

# Rozdělení na trénovací a testovací sady
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Uložení připravených dat do CSV
train_df.to_csv('model/train_data.csv', index=False)
test_df.to_csv('model/test_data.csv', index=False)

# Příprava dat pro trénování
class CustomDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return torch.tensor(self.texts[idx]), torch.tensor(self.labels[idx])

# Příprava dat
train_texts = train_df['tokenized_log']
train_labels = train_df['category']

# Vytvoření a příprava dat do DataLoaderu
train_dataset = CustomDataset(train_texts, train_labels)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Definice jednoduchého modelu
class SimpleModel(nn.Module):
    def __init__(self, input_size, output_size):
        super(SimpleModel, self).__init__()
        self.embedding = nn.Embedding(input_size, 128)
        self.fc = nn.Linear(128, output_size)

    def forward(self, x):
        x = self.embedding(x)
        x = x.mean(dim=1)  # Průměr všech tokenů
        x = self.fc(x)
        return x

# Inicializace modelu, loss funkce a optimalizačního algoritmu
model = SimpleModel(input_size=len(vocab), output_size=len(label_encoder.classes_))
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Trénování modelu
num_epochs = 10
for epoch in range(num_epochs):
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Uložení do více souborů
# Uložení váh modelu
torch.save(model.state_dict(), 'model/model_weights.pth')

# Uložení architektury modelu
torch.save(model, 'model/model_architecture.pth')
