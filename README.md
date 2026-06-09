# 📸 Ferramenta Geradora de Datasets

Aplicativo desenvolvido em Python para viabilizar a extração, seleção e rotulagem de frames provenientes de arquivos de vídeo. Seu principal objetivo é apoiar a construção de conjuntos de dados estruturados e adequadamente anotados, etapa essencial para o treinamento, validação e avaliação de modelos computacionais voltados à detecção, classificação e quantificação automática de padrões visuais.

O sistema integra recursos para reprodução de vídeos, navegação precisa entre quadros e categorização automatizada das imagens extraídas. Adicionalmente, disponibiliza mecanismos para definição de regiões de interesse (Regions of Interest — ROIs), extração direcionada de conteúdo visual e organização hierárquica dos arquivos gerados. Essas funcionalidades permitem padronizar o processo de anotação, reduzir o esforço operacional associado à curadoria dos dados e aumentar a eficiência na construção de bases de imagens destinadas a aplicações de visão computacional e aprendizado de máquina.

## Dados pessoais
**Nome:** Marcio Salmazo Ramos \
**Redes sociais e contato:**

| [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marcio-ramos-b94669235) | [![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/marcio.salmazo) | [![Gmail](https://img.shields.io/badge/Gmail-333333?style=for-the-badge&logo=gmail&logoColor=red)](mailto:contato.marcio.salmazo19@gmail.com) | [![GitHub](https://img.shields.io/badge/GitHub-0077B5?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Marcio-Salmazo) |
|---|---|---|---|


## 📂 Estrutura do Repositório


***O repositório está organizado em diretórios, de acordo com a seguinte estrutura:***

├── **Main Project/**\
├── **Old Project Backup/**\
├── **Documentation and notes.docx/**\
├── **README**\
└── ...

- **Main Project/:** contém o código-fonte da versão atual da aplicação, desenvolvida a partir da reestruturação completa da implementação original. Esta versão adota uma arquitetura mais modular e escalável, priorizando a separação de responsabilidades, a manutenibilidade do código e a facilidade de extensão de funcionalidades futuras. O diretório concentra os componentes ativos do projeto, incluindo módulos de processamento, interface gráfica, gerenciamento de dados e demais recursos necessários à execução da ferramenta.


- **Old Project Backup/:** reúne a implementação original da aplicação, juntamente com arquivos auxiliares, versões históricas, materiais de suporte e documentação associada ao desenvolvimento inicial. Esta versão foi concebida antes da adoção de uma arquitetura modular e utilizava a biblioteca VLC como componente principal para reprodução dos vídeos. O código foi preservado para fins de referência, rastreabilidade do processo de desenvolvimento e comparação entre diferentes abordagens arquiteturais empregadas ao longo do projeto.


- **Documentation and Notes.docx:** documento que agrega anotações técnicas, registros de desenvolvimento, estudos preliminares e decisões de projeto tomadas durante a implementação da ferramenta. O material inclui observações sobre estratégias adotadas, desafios encontrados, alternativas avaliadas e aspectos metodológicos relevantes para a evolução da aplicação, servindo como complemento à documentação formal do repositório.


## ⚙️ Pré-requisitos e Instalação

1. **Clonagem do repositório:** 
        
        git clone https://github.com/Marcio-Salmazo/Projeto-video-player.git

2. **Instação de dependências (win):**

    - Ter instalado o Python nas versões **3.9** ou **3.11** (recomendado). 
    - Criar e ativar o ambiente virtual na pasta raíz do projeto (Abrir o terminal na pasta raíz do projeto):
          
          >> python -m venv .venv\
          >> .venv\Scripts\activate
    
    - Instalar dependências:
          
          >> pip install -r '.\Main Project\Requirements.txt'
          
## ⚙️ Execução da aplicação

1. Após a configuração do ambiente, a aplicação poderá ser iniciada a partir do módulo principal localizado no diretório *'Main Project/Main.py'*. No estágio atual de desenvolvimento, recomenda-se a execução da aplicação por meio de uma IDE compatível com Python, para maior controle acerca da execução.


2. A implementação original da ferramenta, preservada no diretório .\Old Project Backup\, também pode ser executada para fins de consulta, comparação ou reprodução de versões anteriores do sistema. Entretanto, essa versão possui dependências específicas e requer configurações adicionais, incluindo a instalação da biblioteca VLC e a atualização dos caminhos das DLLs utilizados pelo código-fonte para integração com o reprodutor multimídia.

## ⚙️ Funcionalidades da aplicação 

1. **Controles de reprodução do vídeo:**

    * Play/Pause -- Inicia ou interrompe a reprodução do vídeo, possibilitando a inspeção visual do conteúdo em tempo real.
    * Botão `Open Video` -- Permite selecionar e carregar arquivos de vídeo para processamento e extração de frames.
    * Barra de rolagem -- Possibilita o deslocamento rápido para diferentes posições do vídeo, facilitando a localização de eventos específicos sem a necessidade de reprodução sequencial.
    * Avanço e retrocesso frame-a-frame -- Permite navegar individualmente entre quadros consecutivos, oferecendo controle preciso para seleção de imagens em momentos específicos do vídeo.
    * Botão `Save ROI` -- Realiza a captura e o armazenamento da região de interesse selecionada no frame atual, associando-a à classe definida pelo usuário.


2. **Seleção da ROI:** A ferramenta permite a definição manual de uma Região de Interesse (Region of Interest — ROI) diretamente sobre o frame exibido (em tempo de reprodução). Após a seleção, apenas a área delimitada é considerada para o processo de extração e armazenamento da imagem. 


3. **Definição da quantidade e dos rótulos de classe:** A aplicação oferece suporte à criação de categorias personalizadas para organização das imagens extraídas. A área lateral denominada `Classes` permite ao usuário incluir, remover, renomear ao analisar arquivos armazenados nos diretórios da base (De acordo com a categoria).


4. **Armazenamento dos frames e estrutura da base de dados:** Os frames capturados são armazenados automaticamente de acordo com a classe selecionada pelo usuário, por meio do botão `Save ROI`. Além do armazenamento organizado das imagens, o sistema preserva a consistência da nomenclatura dos arquivos gerados, contribuindo para a rastreabilidade dos dados e para a reprodução dos experimentos realizados.


## ⚠️ Alertas de falhas

❌ **Erro ao abrir vídeo:** Provável causa pode estar relacionada À extensão do vídeo. Recomenda-se o uso das extensões `.mp4` ou `.mov` para maior garantia de compatibilidade.


## 🆕 Atualizações / Changelog

- **Versão 0.1.0 - Criação do módulo MVP referente à reestruturação da aplicação:** Contém as ferramentas básicas para reprodução do vídeo e a implementação do recurso inicial de seleção da ROI e armazenamento de frames. 


- **Versão 0.2.0 - Carregamento de bases pré-existentes e ajuste de classes:** Permite ao usuário selecionar uma base de dados pré-existente ou iniciar estruturar um novo *dataset*. Adicionalmente foram implementadas ferramentas para gestão de classes (Adição, Exclusão e Renomeação). 

---

## 👨‍💻 Autores / Contribuidores

- Marcio Salmazo Ramos – **Desenvolvedor principal**  
  📧 marcio.salmazo19@gmail.com  
- Daniel Duarte Abdala  
- Matheus Morais Neves  

---
