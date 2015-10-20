#!/bin/bash

# This script shall be called from the repository directory

echo creating release $1
pushd ..

LOCALES=( de fr )

for LOCALE in "${LOCALES[@]}"
do
    echo "Compiling translation for " $LOCALE
    lrelease-qt4 i18n/qgepplugin_$LOCALE.ts i18n/qgepplugin-js_$LOCALE.ts -qm i18n/qgepplugin_$LOCALE.qm
done

echo "Compiling files for release"
make

sed -i "s/version=.*$/version=$1/" metadata.txt
popd

sed "s/__version__/$1/" <../scripts/data/plugins.xml.template >plugins.xml
NOW=`date -Iseconds -u`
sed -i "s/__now__/$NOW/" plugins.xml
ln -s .. qgepplugin
zip -r qgepplugin-$1.zip qgepplugin/ -x qgepplugin/repository\* qgepplugin/.gitignore
rm qgepplugin

git add .
git commit -m "Release $1"
git push
