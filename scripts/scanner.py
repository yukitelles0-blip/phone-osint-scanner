import requests
import json
import sys
import os
from datetime import datetime

def normalize_phone(phone: str) -> str:
    """Remove não dígitos e garante formato internacional."""
    digits = ''.join(filter(str.isdigit, phone))
    return digits

def get_numverify_data(phone: str) -> dict:
    """
    Obtém dados de enriquecimento (operador, localização, tipo de linha)
    usando a API pública da NumVerify.
    """
    url = f"https://api.numverify.com/v1/validate?number={phone}"
    headers = {'Accept': 'application/json'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "valid": data.get('valid'),
            "carrier": data.get('carrier', {}).get('name'),
            "country": data.get('country', {}).get('name'),
            "location": data.get('location', {}).get('city'),
            "line_type": data.get('line_type')
        }
    except Exception as e:
        return {"error": str(e)}

def search_github_exposure(phone: str) -> list:
    """
    Busca o número em repositórios públicos do GitHub.
    Útil para encontrar configs vazadas, logs ou placeholders.
    """
    url = f"https://api.github.com/search/code?q={phone}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "OSINT-Scanner"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        
        results = []
        for item in items[:5]:  # Limita a 5 resultados para não poluir
            results.append({
                "repo": item.get('repository', {}).get('full_name'),
                "path": item.get('path'),
                "url": item.get('html_url')
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def generate_social_links(phone: str) -> dict:
    """Gera links diretos para WhatsApp e Telegram."""
    return {
        "whatsapp": f"https://wa.me/{phone}",
        "telegram": f"tg://resolve?phone={phone}",
        "sms": f"sms:+{phone}"
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: python scanner.py <phone_number> [output_dir]")
        print("Exemplo: python scanner.py 5511999999999 data/results")
        sys.exit(1)
    
    phone = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "data/results"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[INFO] Iniciando varredura OSINT para: {phone}")
    clean_phone = normalize_phone(phone)
    
    # Coleta de dados
    enrichment = get_numverify_data(clean_phone)
    github_exposure = search_github_exposure(clean_phone)
    social_links = generate_social_links(clean_phone)
    
    # Compilação dos resultados
    results = {
        "target": clean_phone,
        "timestamp": datetime.now().isoformat(),
        "enrichment": enrichment,
        "github_exposure": github_exposure,
        "social_links": social_links
    }
    
    # Geração do nome do arquivo
    filename = f"{clean_phone}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file = os.path.join(output_dir, filename)
    
    # Salvamento
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Resultados salvos em: {output_file}")
    print("\n--- RESUMO ---")
    print(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
