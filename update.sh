rm -rf ./MusictraterPkgver

git clone https://gitee.com/TriM-Organization/Musicreater -b pkgver MusictraterPkgver

cd ./MusictraterPkgver

python3 -O -m compileall -b .

find . -name "*.py"|xargs rm -rf

find . -name "__pycache__" |xargs rm -rf 

rm -rf ./.git

rm ./.gitignore
