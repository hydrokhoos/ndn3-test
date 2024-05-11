#!/bin/sh
sleep 3
ndnsec key-gen /$CONTAINER_NAME | ndnsec cert-install -
ndnsec cert-dump -i /$CONTAINER_NAME > default.ndncert
sudo mkdir -p /usr/local/etc/ndn/keys
sudo mv default.ndncert /usr/local/etc/ndn/keys/default.ndncert

echo "Waiting for the Router"
until nlsrc -R $ROUTER_PREFIX -k routing > /dev/null
do
  sleep 1
done
echo "Router is up"

nlsrc -R $ROUTER_PREFIX -k advertise /$CONTAINER_NAME
python3 /producer.py &

echo "PC is ready"

sleep infinity
