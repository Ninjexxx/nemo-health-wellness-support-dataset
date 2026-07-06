# Arquitetura

Este projeto sera organizado como um pipeline simples de geracao de dados sinteticos.

## Fluxo planejado

```text
configuracao -> exemplos-base/prompts -> validacao -> exportacao -> relatorio de revisao
                                  -> NeMo Data Designer
```

## Componentes

### Configuracao

Centraliza caminhos, nomes de arquivos e parametros de geracao. Isso evita valores espalhados pelo codigo e facilita repetir experimentos.

### Prompts

Define instrucoes e templates usados para gerar dados sinteticos. Separar prompts do codigo ajuda a revisar seguranca, qualidade e intencao dos exemplos.

### Exemplos-base

Define exemplos sinteticos revisados manualmente antes da geracao automatica. Eles funcionam como referencia do formato e da qualidade esperada.

### Geracao

Executa o pipeline usando exemplos-base locais ou NeMo Data Designer em modo preview. O modo local e o padrao para testes rapidos; o modo `nemo-preview` usa modelo externo e deve ser executado conscientemente.

### Validacao

Confere se os registros gerados seguem o formato esperado e nao violam regras basicas do projeto, como uso de dados reais ou nomes de empresas reais.

### Exportacao

Salva os dados sinteticos em `data/synthetic/`. Arquivos gerados nao devem ser versionados por padrao.

### Relatorio de revisao

Gera uma versao Markdown em `reports/latest_dataset_review.md` para facilitar leitura e revisao humana dos exemplos gerados.

## Decisoes iniciais

- Comecar com `requirements.txt` para reduzir complexidade enquanto o framework esta sendo estudado.
- Usar `src/` para separar codigo-fonte de documentacao e dados.
- Manter dados gerados fora do Git por padrao.
- Criar documentacao desde o inicio para que o projeto seja compreensivel no GitHub.
