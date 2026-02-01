# 🏰 Roguelike Wizard Arena

Um jogo **Roguelike 2D** desenvolvido em Python, focado em **Lógica de Programação**, **Orientação a Objetos** e **Geração Procedural**.

> 🚧 **Projeto desenvolvido para o Desafio Técnico da Kodland.**

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Engine](https://img.shields.io/badge/Engine-Pygame_Zero-red?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Backend_%26_Logic-green?style=for-the-badge)

## 🎯 Sobre o Projeto
Este projeto não é apenas um jogo, é uma demonstração de arquitetura de software aplicada a games. O objetivo foi criar um sistema robusto onde a lógica (backend) funciona independentemente da camada visual (frontend).

O jogo utiliza uma **Matriz (Grid System)** para movimentação e colisão, em vez de física de pixels, garantindo precisão matemática típica de jogos táticos.

### ✨ Funcionalidades Principais
- **Sistema de Grid:** Movimentação baseada em células (x, y) e não em pixels arbitrários.
- **POO (Programação Orientada a Objetos):** Classes modulares para `Hero`, `Enemy` e `Boss`, utilizando herança para compartilhar comportamentos.
- **Geração Procedural:** Os inimigos e obstáculos são posicionados aleatoriamente a cada nova execução ou fase.
- **Asset Pipeline Automatizado:** Inclui um script (`setup.py`) capaz de gerar assets gráficos e sonoros placeholder (programaticamente) caso os arquivos originais não estejam presentes.
- **Progressão de Dificuldade:** Sistema de níveis com aumento de inimigos e Boss Fight final.

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.11+**: Linguagem principal.
* **Pygame Zero (pgzero)**: Framework para renderização gráfica e input.
* **Pillow (PIL)**: Biblioteca de manipulação de imagem (usada no script de geração de assets).
* **Math & Random**: Módulos nativos para cálculos vetoriais e lógica aleatória.

---

## 🚀 Como Rodar o Jogo

### Pré-requisitos
Você precisa ter o [Python](https://www.python.org/) instalado.

### 1. Instalação das Dependências
Abra o terminal na pasta do projeto e execute:

```bash
pip install pgzero pillow
