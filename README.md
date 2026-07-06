# Synthetic Health & Wellness Assistant Evaluation Dataset

Projeto de portfolio para gerar dados sinteticos destinados a avaliacao de assistentes de IA em cenarios de saude e bem-estar.

Este projeto usa NVIDIA NeMo Data Designer para criar exemplos controlados, documentados e seguros. O objetivo nao e criar aconselhamento medico real, mas sim produzir dados sinteticos para testar comportamento, seguranca, limites e qualidade de respostas de assistentes.

## Principios

- Nao usar nomes de empresas reais.
- Nao usar dados reais de usuarios.
- Usar apenas dados sinteticos.
- Evitar informacoes pessoalmente identificaveis.
- Documentar decisoes de arquitetura.
- Separar configuracao, prompts, geracao e saida dos dados.

## Estrutura

```text
src/synthetic_health_eval/
  config.py
  export.py
  prompts.py
  schema.py
  seed_examples.py
  generate_dataset.py

data/synthetic/
  .gitkeep

docs/
  architecture.md
  sources.md
```

## Status

Base inicial do projeto com exemplos sinteticos locais validados, fontes de referencia documentadas e dataset card.

## Uso planejado

1. Definir categorias de avaliacao.
2. Criar prompts sinteticos seguros.
3. Gerar registros com NeMo Data Designer.
4. Validar formato e criterios de seguranca.
5. Exportar o dataset sintetico.

## Como testar

Modo local, sem chamar API:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m synthetic_health_eval.generate_dataset
```

Modo opcional com NeMo Data Designer preview:

```powershell
$env:PYTHONPATH='src'
$env:NVIDIA_API_KEY='your-nvidia-api-key-here'
.venv\Scripts\python.exe -m synthetic_health_eval.generate_dataset --source nemo-preview --num-records 5
```

Voce tambem pode criar um arquivo local `.env` com base em `.env.example`.

Testes automatizados:

```powershell
$env:PYTHONPATH='src'
.venv\Scripts\python.exe -m unittest discover -s tests
```

## Aviso

Os dados gerados por este projeto sao sinteticos e nao devem ser usados como orientacao medica.
