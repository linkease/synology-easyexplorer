#!/bin/sh
BUILDDIR=$(cd `dirname $0`;pwd)

VAR=$1
ARCH=
case "$VAR" in
    *_x86)
        ARCH=x86
        cp $BUILDDIR/x86/INFO $BUILDDIR/
        cp $BUILDDIR/x86/easyexplorer $BUILDDIR/package/bin/
        ;;
    *_arm)
        ARCH=arm
        cp $BUILDDIR/arm/INFO $BUILDDIR/
        cp $BUILDDIR/arm/easyexplorer $BUILDDIR/package/bin/
        ;;
    *)
        echo "not support arch, usage: ./pkg.sh easyexplorer_x86"
        exit 1
        ;;
esac


chmod 755 $BUILDDIR/package/bin/easyexplorer
echo "arch is" $ARCH
echo "1.清理文件夹"
rm -rf $VAR
rm -rf *.tgz

echo "2.生成package.tgz"
cd $BUILDDIR/package
tar -czf $BUILDDIR/package.tgz *

echo "3.生成$1.SPK"
cd $BUILDDIR
tar -cf $BUILDDIR/$1.spk package.tgz scripts WIZARD_UIFILES CHANGELOG INFO LICENSE PACKAGE_ICON.PNG
