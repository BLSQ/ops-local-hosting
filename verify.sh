#! /bin/bash
# Verifies that files passed in are valid for docker-compose
set -e

check_file() {
    local file=$1
    docker-compose --file "$file" config --quiet 2>&1 \
        | sed "/variable is not set. Defaulting/d"
    return "${PIPESTATUS[0]}"
}

check_files() {
    local all_files=( "$@" )
    has_error=0
    for file in "${all_files[@]}" ; do
        if [[ -f "$file" ]]; then
            if ! check_file "$file" ; then
                echo "ERROR: $file"
                has_error=1
            fi
        fi
    done
    return $has_error
}

if ! check_files "$@" ; then
    echo "Some compose files failed"
fi



for i in $(find ./playbooks/docker -name "docker-compose.yml" 2>/dev/null | grep docker-compose.yml); do # Not recommended, will break on whitespace
    echo "checking $i"
    check_file "$i"
done

exit $has_error