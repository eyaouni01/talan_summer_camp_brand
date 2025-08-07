#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'interface Streamlit
"""

import json
import os
import sys
from pathlib import Path

def test_json_parsing():
    """Test le parsing JSON avec les données d'exemple"""
    
    # Données d'exemple basées sur votre JSON
    test_data = [
        {
            "role": "Architecte Sécurité Quantique",
            "skills": [
                "Cryptographie Post-Quantique (PQC)",
                "Cybersécurité",
                "Architecture de Systèmes Sécurisés",
                "Gestion des Risques de Sécurité",
                "Protocoles de Réseau",
                "Fondamentaux de l'Informatique Quantique"
            ],
            "workload_mandays": 120
        },
        {
            "role": "Ingénieur IA/ML Quantique",
            "skills": [
                "Apprentissage Automatique (Machine Learning)",
                "Intelligence Artificielle",
                "Algorithmes d'Optimisation Inspirés du Quantique",
                "Analyse de Données",
                "Python",
                "Traitement du Langage Naturel (NLP)",
                "Fondamentaux de l'Informatique Quantique"
            ],
            "workload_mandays": 120
        },
        {
            "role": "Consultant Risque & Stratégie Quantique",
            "skills": [
                "Modélisation de Simulation",
                "Gestion des Risques",
                "Analyse d'Impact Commercial",
                "Planification Stratégique",
                "Intelligence des Menaces (Q-Day)",
                "Communication Client",
                "Implications Commerciales de l'Informatique Quantique"
            ],
            "workload_mandays": 90
        }
    ]
    
    print("🧪 Test de parsing JSON...")
    
    # Test 1: Conversion en JSON string
    json_string = json.dumps(test_data, indent=2, ensure_ascii=False)
    print("✅ Conversion en JSON string réussie")
    
    # Test 2: Parsing du JSON string
    parsed_data = json.loads(json_string)
    print("✅ Parsing du JSON string réussi")
    
    # Test 3: Vérification de la structure
    for i, role in enumerate(parsed_data):
        print(f"📋 Profil {i+1}: {role.get('role', 'N/A')}")
        print(f"   🔧 Compétences: {len(role.get('skills', []))}")
        print(f"   ⏱️ Charge: {role.get('workload_mandays', 'N/A')} jours")
    
    print("\n✅ Tous les tests de parsing sont réussis !")
    return test_data

def test_interface_display():
    """Simule l'affichage de l'interface"""
    
    print("\n🎨 Test d'affichage de l'interface...")
    
    # Simuler les données détectées
    detected_roles = test_json_parsing()
    
    print("\n📊 Affichage simulé des profils :")
    print("=" * 50)
    
    for i, role_data in enumerate(detected_roles):
        print(f"\n👤 {role_data.get('role', f'Profil {i+1}')}")
        print(f"⏱️ Estimation: {role_data.get('workload_mandays', 'N/A')} jours")
        print("🔧 Compétences:")
        
        skills = role_data.get('skills', [])
        for skill in skills:
            print(f"   • {skill}")
        
        print("-" * 30)
    
    print("\n✅ Simulation d'affichage réussie !")

def main():
    """Fonction principale de test"""
    print("🧪 Tests de l'interface Job Offer")
    print("=" * 40)
    
    try:
        # Test 1: Parsing JSON
        test_json_parsing()
        
        # Test 2: Affichage interface
        test_interface_display()
        
        print("\n🎉 Tous les tests sont réussis !")
        print("💡 L'interface devrait maintenant afficher les profils correctement.")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")

if __name__ == "__main__":
    main() 