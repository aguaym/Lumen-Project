# Aplicação Web – Digitalizador de Negativos

Acesse o mockup [aqui](https://chipper-cocada-50dee2.netlify.app/)

## Objetivo

Criar uma aplicação web simples para controlar um sistema de digitalização de negativos de fotos.

O sistema físico roda em um Raspberry Pi com um programa em Python responsável por:

- controlar motor
- controlar câmera
- capturar imagens
- processar e salvar imagens

A aplicação web será apenas uma interface para:

1. iniciar/parar o processo de digitalização
2. visualizar imagens já capturadas

---

## Requisitos gerais

- Interface simples (não precisa design avançado)
- Foco em funcionalidade
- Deve funcionar como uma página web única (SPA simples ou múltiplas páginas simples)
- Atualizações podem ser simuladas (mock, sem backend real)

---

## Funcionalidades principais

### 1. Controle de digitalização

O usuário pode iniciar o processo de digitalização de negativos.

#### Comportamento:

- Botão: **"Iniciar digitalização"**

- Ao clicar:
  - muda estado para "em execução"
  - exibe mensagem: "Digitalizando..."
  - desabilita botão de iniciar
  - habilita botão "Cancelar"

- Durante execução:
  - mostrar indicador visual (texto ou loading simples)
  - impedir novo início do processo

- Botão: **"Cancelar"**
  - para o processo
  - volta ao estado inicial

- Quando finalizar:
  - exibir mensagem: "Processo finalizado"
  - reabilitar botão de iniciar

---

### 2. Visualização de imagens

O usuário pode visualizar todas as imagens já capturadas.

#### Comportamento:

- Mostrar uma galeria de imagens
- As imagens podem ser mockadas (ex: placeholders)
- Exibir em formato de grid
- Cada imagem pode ser clicável para ampliar (opcional)

#### Regras:

- Deve funcionar mesmo durante a digitalização
- Atualização pode ser manual (botão "Atualizar") ou automática simulada

---

## Telas

### Tela principal

A aplicação pode ter uma única tela com duas seções:

#### Seção 1 – Controle

- Botão "Iniciar digitalização"
- Botão "Cancelar"
- Status atual:
  - "Parado"
  - "Em execução"
  - "Finalizado"

#### Seção 2 – Galeria

- Lista/grid de imagens
- Botão "Atualizar" (opcional)

---

## Estados da aplicação

### Estados possíveis:

- idle (parado)
- running (em execução)
- finished (finalizado)

### Regras de estado:

- idle → running (ao iniciar)
- running → finished (quando terminar)
- running → idle (ao cancelar)
- finished → idle (após nova ação ou reset visual)

---

## Regras importantes

- Não permitir iniciar se já estiver rodando
- Permitir visualizar imagens a qualquer momento
- Interface deve refletir claramente o estado atual
- Código deve ser simples e organizado

---

## Tecnologias esperadas

- HTML
- CSS
- JavaScript (puro, sem frameworks)
- Sem backend real (simular comportamento com JS)

---

## Extras (opcional)

- Simular tempo de processamento (ex: 5 segundos)
- Simular novas imagens sendo adicionadas
- Animação simples de loading

---

## Objetivo final

Gerar um mockup funcional onde:

- o usuário consegue clicar para iniciar/cancelar
- o estado muda visualmente
- a galeria de imagens é exibida
- tudo funciona apenas no frontend (simulado)
