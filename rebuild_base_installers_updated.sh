#!/bin/bash

# Ths will update the base installers used by the Clearinghouse 
# from what is currently available in the working copy of the 
# required repos. See constants below.
#
# You will need sudo privileges to use this. Don't run this as sudo, 
# it will invoke sudo when it needs it.
#
# Usage: ./rebuild_base_installers.sh VERSION_STRING


VERSION=$1

USER=cib

SOFTWARE_UPDATE_URL=http://blackbox.poly.edu/updatesite/
PUBLIC_KEY_FILE=/home/cib/custominstallerbuilder/repy_runtime/cib.publickey
PRIVATE_KEY_FILE=/home/cib/custominstallerbuilder/repy_runtime/cib.privatekey

e=`cat $PUBLIC_KEY_FILE | cut -d' ' -f 1`
n=`cat $PUBLIC_KEY_FILE | cut -d' ' -f 2`
SOFTWARE_UPDATE_KEY="{'e':$e, 'n':$n}"

REPO_PARENT_DIR=/home/cib/custominstallerbuilder/DEPENDENCIES/

BASE_INSTALLER_DIRECTORY=/home/cib/custominstallerbuilder/html/static/installers/base

BASE_INSTALLER_ARCHIVE_DIR=/home/cib/custominstallerbuilder/html/static/installers/base/old_base_installers

if [ "$VERSION" == "" ]; then
  echo "You must supply a version string."
  echo "usage: $0 version"
  exit 1
fi

if [ "$SOFTWARE_UPDATE_URL" == "" ]; then
  echo "SOFTWARE_UPDATE_URL isn't set."
  exit 1
fi

if [ ! -d "$BASE_INSTALLER_DIRECTORY" ]; then
  echo "BASE_INSTALLER_DIRECTORY doesn't exist."
  exit 1
fi

if [ ! -d "$BASE_INSTALLER_ARCHIVE_DIR" ]; then
  echo "BASE_INSTALLER_ARCHIVE_DIR doesn't exist."
  exit 1
fi

if [ ! -d "$REPO_PARENT_DIR" ]; then
  echo "REPO_PARENT_DIR doesn't exist."
  exit 1
fi

if [ "`grep -F "$VERSION" $REPO_PARENT_DIR/nodemanager/nmmain.py`" == "" ]; then
  echo "You need to set the version string in $REPO_PARENT_DIR/nodemanager/nmmain.py"
  exit 1
fi

UPDATE_URL_FOUND=$(grep -F "softwareurl = \"$SOFTWARE_UPDATE_URL\"" $REPO_PARENT_DIR/softwareupdater/softwareupdater.py)

if [ "$UPDATE_URL_FOUND" == "" ]; then
  echo "Did not find the correct update url in $REPO_PARENT_DIR/softwareupdater/softwareupdater.py"
  exit 1
fi

UPDATE_KEY_FOUND=$(grep -F "$SOFTWARE_UPDATE_KEY" $REPO_PARENT_DIR/softwareupdater/softwareupdater.py)

if [ "$UPDATE_KEY_FOUND" == "" ]; then
  echo "Did not find the correct update key in $REPO_PARENT_DIR/softwareupdater/softwareupdater.py"
  exit 1
fi

echo "Archiving old base installers to $BASE_INSTALLER_ARCHIVE_DIR"
echo "Warning: failure after this point may leave user $USER with no base installers!"
sudo mv -f $BASE_INSTALLER_DIRECTORY/seattle_* $BASE_INSTALLER_ARCHIVE_DIR

echo "Building new base installers at $BASE_INSTALLER_DIRECTORY"
sudo python $REPO_PARENT_DIR/dist/make_base_installers.py \
  a \
  $REPO_PARENT_DIR \
  $PUBLIC_KEY_FILE \
  $PRIVATE_KEY_FILE \
  $BASE_INSTALLER_DIRECTORY \
  $VERSION

if [ "$?" != "0" ]; then
  echo "Building base installers failed."
  exit 1
fi

echo "Changing base installer symlinks used by user $USER."


sudo chown $USER  $BASE_INSTALLER_DIRECTORY
if [  "$?" != "0" ]; then
  echo "cannot create symlinks for user $USER, check if you have root privileges"
  exit 1
fi
pushd $BASE_INSTALLER_DIRECTORY

if [ ! -f "seattle_${VERSION}_android.zip" ] || [ ! -f "seattle_${VERSION}_linux.tgz" ] || [ ! -f "seattle_${VERSION}_mac.tgz" ] || [ ! -f "seattle_${VERSION}_win.zip" ]; then
  echo "The base installers don't appear to have been created."
  exit 1
fi

if [ $USER != "`whoami`" ]; then
  echo"Cannot create symlink for user $USER, Current user `whoami` does not have sufficient privileges"
fi

echo "starting to create symlinks to the installers...."

sudo chown $USER seattle_*

sudo -u $USER ln -s -f seattle_${VERSION}_linux.tgz seattle_linux.tgz
sudo -u $USER ln -s -f seattle_${VERSION}_mac.tgz seattle_mac.tgz
sudo -u $USER ln -s -f seattle_${VERSION}_win.zip seattle_win.zip
sudo -u $USER ln -s -f seattle_${VERSION}_android.zip seattle_android.zip
popd

echo "New base installers created and installed for user $USER."
