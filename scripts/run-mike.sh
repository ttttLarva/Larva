set -ex
MIKE="mike"
CN_SITE="_site"
LATEST_VERSION="latest"
OUTPUT_BRANCH="docs_output"

CN_OPTIONS="--prefix ${CN_SITE} -b ${OUTPUT_BRANCH}"

# master
${MIKE} delete --all ${CN_OPTIONS}
git checkout master
${MIKE} deploy master ${LATEST_VERSION} -u ${CN_OPTIONS}
${MIKE} set-default ${LATEST_VERSION} ${CN_OPTIONS}