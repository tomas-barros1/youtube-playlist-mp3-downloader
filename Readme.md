# YouTube Playlist Downloader

[English](#english) | [Português](#português)

## Português

### Descrição

Um aplicativo com interface gráfica para baixar playlists do YouTube e converter automaticamente para MP3. O programa detecta automaticamente cookies dos navegadores instalados para permitir o download de playlists privadas/restritas e vídeos com restrição de idade.

### Características

- Interface gráfica amigável
- Barra de progresso em tempo real
- Conversão automática para MP3
- Suporte a cookies de múltiplos navegadores
- Lembra a última pasta utilizada
- Suporte a playlists públicas e privadas
- Capacidade de baixar vídeos com restrição de idade (usando cookies do navegador)

### Instalação e Uso

#### Método 1: Executável (Recomendado)

1. Baixe o arquivo executável da [página de releases](https://github.com/tomas-barros1/youtube-playlist-mp3-downloader/releases/tag/1.0)
2. Execute o programa baixado
3. Cole o link da playlist do YouTube
4. Selecione a pasta de destino
5. Clique em "Baixar"

#### Método 2: Código Fonte (Para desenvolvedores)

Se você preferir executar o código fonte:

1. Instale Python 3.6+
2. Instale FFmpeg
3. Clone o repositório
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute: `python baixar_playlist_youtube2.py`

### Pré-requisitos

Para o executável:

- FFmpeg instalado no sistema
- Um navegador compatível instalado (Chrome, Firefox, Edge, Opera, Brave, Safari ou Vivaldi)

### Navegadores Suportados

O programa utiliza automaticamente os cookies dos seguintes navegadores para baixar vídeos restritos:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Opera
- Brave
- Safari (macOS)
- Vivaldi

## English

### Description

A GUI application to download YouTube playlists and automatically convert them to MP3. The program automatically detects cookies from installed browsers to allow downloading age-restricted videos and private/restricted playlists.

### Features

- User-friendly graphical interface
- Real-time progress bar
- Automatic MP3 conversion
- Multi-browser cookie support
- Remembers last used folder
- Support for public and private playlists
- Ability to download age-restricted videos (using browser cookies)

### Installation and Usage

#### Method 1: Executable (Recommended)

1. Download the executable from the [releases page](https://github.com/tomas-barros1/youtube-playlist-mp3-downloader/releases/tag/1.0)
2. Run the downloaded program
3. Paste the YouTube playlist link
4. Select destination folder
5. Click "Download"

#### Method 2: Source Code (For developers)

If you prefer to run from source:

1. Install Python 3.6+
2. Install FFmpeg
3. Clone the repository
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python baixar_playlist_youtube2.py`

### Prerequisites

For the executable:

- FFmpeg installed on system
- A compatible browser installed (Chrome, Firefox, Edge, Opera, Brave, Safari, or Vivaldi)

### Supported Browsers

The program automatically uses cookies from these browsers to download restricted videos:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Opera
- Brave
- Safari (macOS)
- Vivaldi
