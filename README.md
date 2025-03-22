<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->

<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/Sveji/Sukar-Marshrutar">
     <img src="https://cdn.discordapp.com/attachments/926932859170725909/1352838746512560128/logo.png?ex=67df78c3&is=67de2743&hm=96a69283580fd2072f2e48dd0a361aa283fa04ae86f02a46404cf4d1ede4cef2&"  width="250" height="250">
     </a>
    <h1 align="center">FyleX</h1>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Content</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#built-with">Made with: </a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

FyleX е твоят умен асистент за разпознаване на нередности в документи. Нашият екип се фокусира върху финансите – защото, нека бъдем честни, кой всъщност чете дребния шрифт?

Всеки е попадал в капана на „малките детайли“ – подписваш нещо, пропускаш един ред и изведнъж се оказваш горд собственик на „незадължителна“ такса или абонамент за нещо, което дори не знаеш какво е. А ако нещо звучи прекалено добре, вероятно… е време да се усъмниш.

Тук се появява FyleX. Платформата анализира текстовете от документи или имейли, подчертава съмнителните фрази и обяснява защо трябва да им обърнеш внимание. Това става чрез комбинация от интелигентен анализ на езика с attention-based bidirectional LSTM модел и наш собствен Tokenizer, вдъхновен от GPT-4. Предоставяме и анализ.

И най-хубавото? Направили сме приложението лесно достъпно дори и за по-възрастните потребители, които често са изправени пред пречки особено в сферата на онлайн финансите!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Made with

- ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
- ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
- ![Less.js](https://img.shields.io/badge/Less-1D365D?style=for-the-badge&logo=less&logoColor=white)
- ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
- ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
- ![Hugging Face](https://img.shields.io/badge/HuggingFace-FFCC4D?style=for-the-badge&logo=huggingface&logoColor=black)
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
- ![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

* **Npm and Node**
  Download from [nodejs.org](https://nodejs.org/).
* **Python and pip**
  Download from [python.org](https://www.python.org/downloads/).
* **Docker**
  Download from [docker.com](https://www.docker.com/).

# Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Sveji/FyleX.git
   cd FyleX/
    ```
2. Set up a virtual environment
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
## Installation with Docker

1. Navigate to the ml folder and set up the .env file
   ```sh
   cd ml/
   cp .env.example .env
   ```
2. Go back to the root directory
   ```sh
    cd ../
    ```
3. Navigate to the server folder and set up the .env file

    ```sh
    cd server/
    cp .env.example .env
    ```
4. Go back to the root directory
5. Navigate to the client folder and set up the .env file
   ```sh
   cd client/
   cp .env.example .env
   ```
6. Go back to the root directory
   ```sh
    cd ../
    ```
7. Compose the Docker containers
8. ```sh
    docker-compose up --build -d
    ```
9. The frontend will be available at http://localhost:3000


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Deep Learning

<div align="center">
 <a href="https://github.com/Sveji/Sukar-Marshrutar">
     <img src="https://media.discordapp.net/attachments/1214498824526241822/1352826043353796679/bubu.png?ex=67df6cef&is=67de1b6f&hm=d3fc89768e29d47fdc3b5b7b3bee93daaec799fd873c8150736ddebdd104004a&=&format=webp&quality=lossless&width=758&height=875"  width="500" height="600">
  </a>
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->


[contributors-url]: https://github.com/Sveji/FyleX/graphs/contributors
[license-shield]: https://img.shields.io/github/license/Sveji/FyleX.svg?style=for-the-badge
[license-url]: hhttps://github.com/Sveji/FyleX/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[less.js]: https://img.shields.io/badge/less.js-20232A?style=for-the-badge&logo=less&logoColor=61DAFB
[less-url]: https://reactjs.org/
[Django-]: https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=django&logoColor=61DAFB
[Django-url]: https://www.djangoproject.com/
[Tensorflow]: https://img.shields.io/badge/Tensorflow-20232A?style=for-the-badge&logo=tensorflow&logoColor=FF8000
[Tensorflow-url]: https://www.tensorflow.org/
