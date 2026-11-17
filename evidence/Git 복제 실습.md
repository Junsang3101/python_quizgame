# Git 복제 실습

다른 디렉토리에서 저장소를 `git clone` 으로 복제해봤습니다.

```powershell
PS E:\git_repo\python_quizgame> cd .. 
PS E:\git_repo> mkdir temp_1


    디렉터리: E:\git_repo


Mode                 LastWriteTime         Length Name                                                                                                                                                                                   
----                 -------------         ------ ----                                                                                                                                                                                   
d-----      2026-11-18   오전 3:08                temp_1                                                                                                                                                                                 


PS E:\git_repo> cd .\temp_1\
PS E:\git_repo\temp_1> git clone https://github.com/junsang3101/python_quizgame
Cloning into 'python_quizgame'...
remote: Enumerating objects: 162, done.
remote: Counting objects: 100% (162/162), done.
remote: Compressing objects: 100% (107/107), done.
remote: Total 162 (delta 76), reused 131 (delta 45), pack-reused 0 (from 0)
Receiving objects: 100% (162/162), 167.23 KiB | 6.43 MiB/s, done.
Resolving deltas: 100% (76/76), done.
PS E:\git_repo\temp_1> cd .\python_quizgame\
PS E:\git_repo\temp_1\python_quizgame> ls


    디렉터리: E:\git_repo\temp_1\python_quizgame


Mode                 LastWriteTime         Length Name                                                                                                                                                                                   
----                 -------------         ------ ----                                                                                                                                                                                   
d-----      2026-11-18   오전 3:08                evidence                                                                                                                                                                               
-a----      2026-11-18   오전 3:08             41 .gitignore                                                                                                                                                                             
-a----      2026-11-18   오전 3:08           4840 cli.py                                                                                                                                                                                 
-a----      2026-11-18   오전 3:08           1362 default_quizzes.json                                                                                                                                                                   
-a----      2026-11-18   오전 3:08           1256 json_store.py                                                                                                                                                                          
-a----      2026-11-18   오전 3:08           9290 quizgame.py                                                                                                                                                                            
-a----      2026-11-18   오전 3:08           2657 README.md                                                                                                                                                                              
-a----      2026-11-18   오전 3:08           1987 state.json                                                                                                                                                                             
-a----      2026-11-18   오전 3:08              0 __init__.py                                                                                                                                                                            
-a----      2026-11-18   오전 3:08             61 __main__.py                                                                                                                                                                            


PS E:\git_repo\temp_1\python_quizgame>
```