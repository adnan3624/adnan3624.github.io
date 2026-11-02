# Marketing Data Analyst Portfolio
Static site (HTML, CSS, JS). No build step needed to host.

## Before publishing
1. Search and replace `Your Name`, `you@example.com`, the LinkedIn and GitHub URLs, and `https://your-username.github.io/portfolio` (also in sitemap.xml and robots.txt).
2. Put your CV at `assets/documents/CV.pdf`.
3. Replace the profile photo placeholder in the About section with an image in `assets/images/`.
4. Confirm the three results on the homepage before sharing.

## Deploy on GitHub Pages
1. On github.com click New repository, name it `portfolio` (or `your-username.github.io` for a root URL), set it Public, create it.
2. Upload every file and folder from this project (Add file > Upload files), then commit to `main`.
3. Open Settings > Pages. Under Build and deployment choose Deploy from a branch, branch `main`, folder `/ (root)`, Save.
4. After about a minute the site is live at `https://your-username.github.io/portfolio/`. Open every page and the CV download.
5. To update: edit files on GitHub or push from Git. Pages redeploys on each commit.

`build.py` regenerates all HTML (edit the content at the top, run `python3 build.py`).
