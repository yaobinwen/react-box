#!/bin/bash

# Add /* eslint-disable */ to `*_pb.js` files that are generated by
# `google-protobuf` to avoid React.js lint errors.
for PB_FILE in $(find src -name "*_pb.js" -type f); do
    echo '/* eslint-disable */' | cat - "${PB_FILE}" > temp && mv temp "${PB_FILE}"
done