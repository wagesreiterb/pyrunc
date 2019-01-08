# pyrunc
runc implementation in python - only for testing


test with:
\# ~/go/src/github.com/opencontainers/runtime-tools$ RUNTIME="./pyrunc.py" validation/create/create.t

runc default root dir is /run/runc/{container-id}/state.json

to start a container invoke runc run {container-id} in a directory with
+ rootfs
+ config.json

