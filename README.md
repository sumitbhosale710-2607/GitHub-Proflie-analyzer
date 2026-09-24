<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:090915,30:3B0764,65:6C63FF,100:4F46E5&height=200&section=header&text=GitHub%20Profile%20Analyzer&fontSize=48&fontColor=ffffff&animation=twinkling&fontAlignY=42&desc=Analyze%20any%20GitHub%20profile%20—%20score%2C%20stats%2C%20languages%2C%20top%20repos&descAlignY=65&descSize=16&descColor=c4b5fd" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&duration=3500&pause=800&color=A78BFA&center=true&vCenter=true&width=800&lines=Analyze+any+GitHub+profile+instantly;Profile+score+out+of+100;Top+languages+%7C+Star+charts+%7C+Activity;Built+with+Python+%2B+Streamlit" alt="Typing SVG"/>

<br/><br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub%20API-181717?style=for-the-badge&logo=github&logoColor=white)

<br/>

![No API Key](https://img.shields.io/badge/No%20API%20Key%20Required-22C55E?style=flat-square)
![Free](https://img.shields.io/badge/100%25%20Free-7C3AED?style=flat-square)
![Open Source](https://img.shields.io/badge/Open%20Source-4F46E5?style=flat-square)

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20What%20It%20Does&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

Enter any GitHub username and instantly get a complete breakdown of their profile. No API key, no login, no setup — just a username.

<div align="center">

| Feature | Details |
|---|---|
| **Profile Score** | Calculated score out of 100 based on 9 real criteria |
| **Language Chart** | Interactive pie chart of top languages across all repos |
| **Top Repos** | Bar chart of most-starred repositories |
| **Score Breakdown** | Exactly what's helping and hurting the score |
| **Improvement Tips** | Personalised suggestions based on what's missing |
| **Recently Updated** | Latest repos with stars, forks, language, date |
| **Stats Overview** | Repos, stars, forks, followers, following, account age |

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20How%20the%20Score%20Works&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

<div align="center">

| Criteria | Max Points |
|---|---|
| Has a bio | 10 |
| Has a portfolio/website | 10 |
| Has a profile README repo | 15 |
| 10+ followers | 10 |
| 5+ public repos | 10 |
| Active in last 30 days | 15 |
| Stars earned across repos | 15 |
| Account 1+ years old | 10 |
| Custom avatar set | 5 |
| **Total** | **100** |

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20Getting%20Started&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

**Step 1 — Clone the repo**

```bash
git clone https://github.com/Premnath-06/github-profile-analyzer.git
cd github-profile-analyzer
```

**Step 2 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 3 — Run the app**

```bash
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501`. Type any GitHub username and hit **Analyze →**.

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20Architecture&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

```
github-profile-analyzer/
  github_api.py      ← fetches raw data from GitHub public API
  analyzer.py        ← processes data, calculates score & insights
  charts.py          ← builds all Plotly interactive visualizations
  app.py             ← Streamlit UI, ties everything together
  requirements.txt
  README.md
```

Each file has a single responsibility. Clean separation of concerns.

```
User enters username
        ↓
github_api.py — fetches user, repos, events
        ↓
analyzer.py   — calculates score, languages, top repos
        ↓
charts.py     — builds gauge, pie, bar charts
        ↓
app.py        — displays everything in the browser
```

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20Tech%20Stack&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

<div align="center">
<img src="https://skillicons.dev/icons?i=python&theme=dark" />
</div>

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub%20REST%20API-181717?style=for-the-badge&logo=github&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2C2D72?style=for-the-badge)

</div>

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:4F46E5,50:7C3AED,100:6C63FF&height=3" width="100%"/>

<br/>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=transparent&color=7C3AED&height=60&text=◈%20Built%20By&fontSize=32&fontColor=A78BFA&animation=fadeIn&fontAlign=50" width="100%"/>
</div>

<div align="center">

Built by [sumitbhosale710-2607](https://github.com/sumitbhosale710-2607) — CS student and game developer learning Python by building real tools.

[![GitHub](https://img.shields.io/badge/GitHub-Premnath--06-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Premnath-06)

</div>

<br/>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=15&duration=4000&pause=2000&color=6C63FF&center=true&vCenter=true&width=700&lines=Built+with+Python+%2B+Streamlit+%2B+GitHub+API.+Zero+setup.+Just+run+it." alt="Footer"/>

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4F46E5,50:7C3AED,100:090915&height=150&section=footer&animation=twinkling" width="100%"/>

</div>
