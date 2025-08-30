# 📸 Frame Capturer

Aplicativo desenvolvido para **captura e categorização de frames em vídeos**, projetado especialmente para auxiliar pesquisadores da área de medicina veterinária na **produção de bases de dados de imagens de animais sob estímulos de dor**.

O sistema permite a seleção manual de frames relevantes, definição de áreas de interesse e organização das imagens em categorias específicas, de forma simples e controlada, com suporte a atalhos de teclado e integração com VLC para reprodução de vídeos.

---

## 🔎 Descrição Geral

O **Frame Capturer** tem como objetivo:
- Extrair imagens de arquivos de vídeo (`.mp4`, `.mov`);
- Permitir que o usuário selecione manualmente frames relevantes;
- Definir **recortes personalizados** dentro do frame para posterior análise;
- Organizar os recortes automaticamente em categorias:  
  - `Indolor`  
  - `Pouca dor`  
  - `Muita dor`  
  - `Incerto`

Destina-se principalmente a **pesquisadores em medicina veterinária**, mas pode ser utilizado em outros contextos que exijam análise manual de frames.

---

## 🖥️ Interface e Funcionalidades

### 📂 Janela Inicial
- Área de reprodução de vídeos com suporte via `python-vlc`;
- **Controles de reprodução**:
  - ▶️ Play/Pause  
  - ⏩ Avançar frame  
  - ⏪ Retroceder frame  
  - Barra de rolagem do vídeo  
  - Controle de velocidade (0.25x, 0.5x, 1x, 2x, 4x)  
- **Botões principais**:
  - **Abrir vídeo** – carrega arquivos `.mp4` ou `.mov`;  
  - **Capturar frame** – abre a janela de recorte e categorização;  
  - **Menu de salvamento** – gerencia os recortes salvos;  
  - **Escolher novas teclas de atalho** – remapeia atalhos de teclado;  
  - **Fechar programa** – encerra a aplicação.  

---

### ✂️ Janela de Captura de Frame
- Exibição do frame selecionado em área rolável;
- Definição da **área de recorte** com salvamento automático nas categorias:
  - Indolor  
  - Pouca dor  
  - Muita dor  
  - Incerto
- Funções adicionais:
  - **Inverter imagem (180°)** – corrige orientação do frame quando necessário;
  - **Concluir** – fecha a janela e retorna à tela inicial.  

> 🔎 **Observações Importantes**  
> - Recortes só podem ser feitos da esquerda para a direita e de cima para baixo;
> - Recortes se reajustam automaticamente para um formato quadrado (visando padronização)
> - Arquivo `JSON` em `Augmentation/` armazena coordenadas dos recortes (10 frames vizinhos anteriores e posteriores);  
> - **Não manipular manualmente** o diretório `Augmentation` ou recortes salvos via Explorer, para isso, utilizar o MENU DE SALVAMENTO.  

---

### 💾 Menu de Salvamento
- Lista todos os recortes salvos relacionados ao vídeo em reprodução;
- Permite **excluir recortes** (imagem + entrada no arquivo JSON);
- Organização automática por categorias.

---

### ⌨️ Atalhos de Teclado
- `o` – Abrir vídeo  
- `Espaço` – Play/Pause  
- `s` – Avançar frame  
- `a` – Retroceder frame  
- `q` – Sair do programa  

> ⚙️ Usuário pode redefinir os atalhos pelo menu dedicado.  

---

## ⚙️ Pré-requisitos e Instalação

- Sistema Operacional: **Windows**  
- Python **3.9** ou **3.11** (recomendado)  
- VLC instalado  

Dependências Python:
- `opencv-python`  
- `PyQt5`  
- `numpy`  
- `python-vlc`  

### Instalação Automática
Na primeira execução o programa tenta instalar automaticamente as dependências.  
Se houver falha, execute manualmente o script (via terminal ou por um duplo clique):

\`\`\`bash
Dependencias.bat
\`\`\`

---

## ▶️ Modo de Uso

1. Abra o programa (diretório `\dist`)  
2. Clique em **Abrir vídeo** e selecione um arquivo compatível  
3. Utilize os controles ou atalhos para navegar até o frame desejado  
4. Clique em **Capturar Frame** para abrir a janela de recorte  
5. Salve as áreas de interesse em uma das categorias disponíveis  
6. Gerencie os recortes salvos pelo **Menu de Salvamento**  

---

## ⚠️ Erros Comuns

| Erro | Causa provável | Solução |
|------|----------------|---------|
| ❌ Erro ao abrir vídeo | Extensão inválida | Verifique se o arquivo é `.mp4` ou `.mov` |
| ❌ Aplicativo não abre | Python, VLC ou dependências ausentes | Reinstale dependências ou execute `Dependencias.bat` |
| ❌ Recortes não aparecem no menu | Alteração manual do nome do vídeo | Utilize sempre o nome original |
| ❌ Travamento ou fechamento inesperado | Instabilidade de código | Contatar desenvolvedor |

---

## 🆕 Atualizações / Changelog

- **v0.4.0-beta**
  - Otimização da captura de frames e atualização do arquivo JSON por meio de batches, agora toda a operação de verificação é feita apenas com arquivos referentes ao vídeo atual em reprodução
  - Modificações consideráveis nas funções FrameCapture e Model

- **v0.3.0-beta**
  - Otimização da captura de frames e atualização do arquivo JSON via hashcode
  - Modificações consideráveis nas classes FrameCapture e Model
  
- **v0.2.1-beta**
  - Inserção de `QMessageBox` para informar erros ao usuário  

- **v0.2.0-beta**
  - Adicionado botão para inverter imagem (180°)  
  - Correções em bugs de navegação  

---

## 👨‍💻 Autores / Contribuidores

- Marcio Salmazo Ramos – **Desenvolvedor principal**  
  📧 marcio.salmazo19@gmail.com  
- Daniel Duarte Abdala  
- Matheus Morais Neves  

---
