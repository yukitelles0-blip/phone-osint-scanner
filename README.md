# Phone OSINT Scanner

Ferramenta de OSINT (Open Source Intelligence) para extrair dados públicos a partir de um número de telefone.

## Funcionalidades

- **Enriquecimento:** Identifica operadora, país, cidade e tipo de linha.
- **Exposição Pública:** Busca o número em repositórios públicos do GitHub.
- **Links Sociais:** Gera links diretos para WhatsApp, Telegram e SMS.
- **Automatização:** Roda via GitHub Actions sob demanda ou agendado.

## Como Usar

### Via GitHub Actions (Recomendado)

1. Vá para a aba `Actions` do seu repositório.
2. Selecione o workflow `Phone OSINT Scanner`.
3. Clique em `Run workflow`.
4. Insira o número de telefone no formato internacional (ex: `5511999999999`).
5. Aguarde a conclusão do job.
6. Baixe os resultados em JSON na seção `Artifacts`.

### Via Linha de Comando

```bash
pip install -r requirements.txt
python roteiros/scanner.py 5511999999999
