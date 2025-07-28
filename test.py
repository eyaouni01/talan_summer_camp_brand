import torch

print("✅ GPU disponible :", torch.cuda.is_available())

if torch.cuda.is_available():
    print("Nom du GPU :", torch.cuda.get_device_name(0))
else:
    print("Aucun GPU détecté, exécution sur CPU.")
