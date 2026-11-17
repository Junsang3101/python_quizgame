# Git init / commit / push

본래 도커에서 만들어 보려다 불필요 한 것 같아 제외하였습니다.
  
Github에 빈 저장소를 만든 뒤 로컬 환경에서 `git init` 으로 초기화 한 뒤 `git switch -c main` 로 새 브랜치를 만들어 `git add .` 로 스태이징 한 후 `git commit -m` 로 커밋을 만든 뒤 `git remote add` 로 `git push` 할 위치를 잡아준 후 `git push -u origin main` 로 첫 푸쉬해 upstream 설정을 해주었습니다.

``` powershell
PS E:\git_repo\python_quizgame> docker compose ps -a
NAME                    IMAGE                                                                     COMMAND           SERVICE   CREATED          STATUS                          PORTS
python_quizgame-app-1   sha256:6fb12b499ffff70318a8aa71bbceed6d36b567c74df00c8f209c729ee8f01a46   "python app.py"   app       12 minutes ago   Exited (2) About a minute ago   
PS E:\git_repo\python_quizgame> git init
Initialized empty Git repository in E:/git_repo/python_quizgame/.git/
PS E:\git_repo\python_quizgame> git switch -c main
Switched to a new branch 'main'
PS E:\git_repo\python_quizgame> git add .
PS E:\git_repo\python_quizgame> git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   .env
        new file:   app/Dockerfile
        new file:   app/requirements.txt
        new file:   app/src/main.py
        new file:   compose.yaml
        new file:   "evidence/\354\264\210\352\270\260\355\231\224.md"

PS E:\git_repo\python_quizgame> git commit -m "도커 파이썬 앱 초기화"
[main (root-commit) 19c6eae] 도커 파이썬 앱 초기화
 6 files changed, 17 insertions(+)
 create mode 100644 .env
 create mode 100644 app/Dockerfile
 create mode 100644 app/requirements.txt
 create mode 100644 app/src/main.py
 create mode 100644 compose.yaml
 create mode 100644 "evidence/\354\264\210\352\270\260\355\231\224.md"
PS E:\git_repo\python_quizgame> git remote -v
PS E:\git_repo\python_quizgame> git remote add origin https://github.com/junsang3101/python_quizgame.git
PS E:\git_repo\python_quizgame> git push
fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

PS E:\git_repo\python_quizgame> git push -u origin main
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 12 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (9/9), 827 bytes | 275.00 KiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: This repository moved. Please use the new location:
remote:   https://github.com/Junsang3101/python_quizgame.git
To https://github.com/junsang3101/python_quizgame.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
PS E:\git_repo\python_quizgame> 
```

# 필요 없는 도커 삭제후 스태이징

도커 복습 목적으로 도커 안에서 만들고 있었으나, 불필요해 삭제하고 `git add` 해줌

```powershell
PS E:\git_repo\python_quizgame> git add .
PS E:\git_repo\python_quizgame> git status
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        deleted:    .env
        new file:   .gitignore
        deleted:    app/Dockerfile
        deleted:    compose.yaml
        renamed:    app/src/__init__.py -> src/__init__.py
        renamed:    app/requirements.txt -> src/__main__.py
        renamed:    app/src/cli.py -> src/cli.py
        renamed:    app/data/default_quizzes.json -> src/data/default_quizzes.json
        renamed:    app/src/quizgame.py -> src/quizgame.py
```

# commit 해서 새 브랜치로 push 함

커밋하고 새 브랜치에 커밋했음

```powershell
PS E:\git_repo\python_quizgame> git commit -m "파이썬 말고 필요없는 도커 버림" 
[main 386f642] 파이썬 말고 필요없는 도커 버림
 9 files changed, 7 insertions(+), 21 deletions(-)
 delete mode 100644 .env
 create mode 100644 .gitignore
 delete mode 100644 app/Dockerfile
 delete mode 100644 compose.yaml
 rename {app/src => src}/__init__.py (100%)
 rename app/requirements.txt => src/__main__.py (100%)
 rename {app/src => src}/cli.py (84%)
 rename {app => src}/data/default_quizzes.json (100%)
 rename {app/src => src}/quizgame.py (94%)
PS E:\git_repo\python_quizgame> git switch -c python-only
Switched to a new branch 'python-only'
PS E:\git_repo\python_quizgame> git branch
  main
* python-only
PS E:\git_repo\python_quizgame> git status 
On branch python-only
nothing to commit, working tree clean
PS E:\git_repo\python_quizgame> git push -u origin python-only
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 12 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (9/9), 2.35 KiB | 800.00 KiB/s, done.
Total 9 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
remote: This repository moved. Please use the new location:
remote:   https://github.com/Junsang3101/python_quizgame.git
remote: 
remote: Create a pull request for 'python-only' on GitHub by visiting:
remote:      https://github.com/Junsang3101/python_quizgame/pull/new/python-only
remote: 
To https://github.com/junsang3101/python_quizgame.git
 * [new branch]      python-only -> python-only
branch 'python-only' set up to track 'origin/python-only'.
```

# 기존 브랜치가 가르키는 commit 제거

`git switch -c` 전에 커밋해서 기존 main 브랜치에 커밋이 남아버림,  
그래서 기존 브랜치의 커밋을 `git reset --keep origin/main`으로 지워줌  
기본 브랜치 또한 GitHub 에서 변경해줌

```powershell
PS E:\git_repo\python_quizgame> git branch -vv
  main        386f642 [origin/main: ahead 1] 파이썬 말고 필요없는 도커 버림
* python-only 386f642 [origin/python-only] 파이썬 말고 필요없는 도커 버림
PS E:\git_repo\python_quizgame> git switch main
Switched to branch 'main'
Your branch is ahead of 'origin/main' by 1 commit.
  (use "git push" to publish your local commits)
PS E:\git_repo\python_quizgame> git reset --keep origin/main
PS E:\git_repo\python_quizgame> git branch -vv
* main        ae2ac83 [origin/main] cli 메뉴 모듈을 만들고 .gitignore 추가함 quizzes.json 도 default_quiz.json으로 수정함
  python-only 386f642 [origin/python-only] 파이썬 말고 필요없는 도커 버림
PS E:\git_repo\python_quizgame> git switch python-only
Switched to branch 'python-only'
Your branch is up to date with 'origin/python-only'.
PS E:\git_repo\python_quizgame> git status 
On branch python-only
Your branch is up to date with 'origin/python-only'.

nothing to commit, working tree clean
PS E:\git_repo\python_quizgame> 
```

![기본 브랜치 변경](../evidence/기본%20브랜치%20변경.png)