set -e

if [[ ! -d $1 ]]
then
    echo "Creates a tarball of the plugin for distribution"
    echo "Usage:"
    echo "    $0 <plugin-directory>"
    exit 1
fi

tar cz -f $1.tar.gz $1

echo "Wrote plugin tarball: $1.tar.gz"
