#!/bin/sh
echo "清理文件夹"
rm -rf *.spk
rm -rf *.tgz
BUILDDIR=$(cd `dirname $0`;pwd)
echo $BUILDDIR
echo "1.生成package.tgz"

cd $BUILDDIR/package
tar -czf $BUILDDIR/package.tgz *

echo "2.生成$1.SPK"
cd $BUILDDIR
tar -cf $BUILDDIR/$1.spk package.tgz scripts WIZARD_UIFILES CHANGELOG INFO LICENSE PACKAGE_ICON.PNG