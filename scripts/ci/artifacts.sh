# Build wheel and set the $share_folder to the artifacts folder

echo "before build.sh"
. $(cd $(dirname $0); pwd)/build.sh
echo "after build.sh"
share_folder=$(cd $(dirname $0); cd ../../artifacts; pwd)