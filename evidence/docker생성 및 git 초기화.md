# 컨테이너 생성 및 테스트

전 미션 응용할 겸 파이썬 퀴즈 게임을 도커 안에서 실행하도록 도커 컨테이너를 구성하였습니다.

```powershell
PS E:\git_repo\python_quizgame> docker compose up -d --build
[+] Building 1.9s (13/13) FINISHED                                                                     
 => [internal] load local bake definitions                                                        0.0s
 => => reading from stdin 525B                                                                    0.0s
 => [internal] load build definition from Dockerfile                                              0.0s
 => => transferring dockerfile: 189B                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.10.0-slim                             1.2s
 => [auth] library/python:pull token for registry-1.docker.io                                     0.0s
 => [internal] load .dockerignore                                                                 0.0s
 => => transferring context: 2B                                                                   0.0s
 => [1/5] FROM docker.io/library/python:3.10.0-slim@sha256:ad540a471260fee5e5e1a99ee2acf142efe8c  0.0s
 => => resolve docker.io/library/python:3.10.0-slim@sha256:ad540a471260fee5e5e1a99ee2acf142efe8c  0.0s
 => [internal] load build context                                                                 0.0s
 => => transferring context: 116B                                                                 0.0s
 => CACHED [2/5] WORKDIR /app                                                                     0.0s
 => CACHED [3/5] COPY requirements.txt .                                                          0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                               0.0s
 => CACHED [5/5] COPY . .                                                                         0.0s
 => exporting to image                                                                            0.1s
 => => exporting layers                                                                           0.0s
 => => exporting manifest sha256:6275dd0fdb487413b4b687f696e1547d6c20391b219b6e86ecdb7924fd6e92d  0.0s
 => => exporting config sha256:402ebc11e65bfee894640b250212d0959543772144e2964c0935cd085a9eedea   0.0s
 => => exporting attestation manifest sha256:c83fe30e0d0c751413b7d13d7a1711855c5b3d931109232002d  0.0s
 => => exporting manifest list sha256:3cfff6ae8e704902036fb555cbbafd0baa5e8b39bfe086e758af3cb8ef  0.0s
 => => naming to docker.io/library/python_quizgame-app:latest                                     0.0s
 => => unpacking to docker.io/library/python_quizgame-app:latest                                  0.0s
 => resolving provenance for metadata file                                                        0.0s
[+] up 2/2
 ✔ Image python_quizgame-app       Built                                                           2.1s
 ✔ Container python_quizgame-app-1 Started                                                         0.3s
PS E:\git_repo\python_quizgame>
```

# Git init / commit / push

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