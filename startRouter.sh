#!/bin/sh
ndnsec key-gen /$CONTAINER_NAME | ndnsec cert-install -
ndnsec cert-dump -i /$CONTAINER_NAME > default.ndncert
sudo mkdir -p /usr/local/etc/ndn/keys
sudo mv default.ndncert /usr/local/etc/ndn/keys/default.ndncert

echo "Start NFD"
nfd --config /usr/local/etc/ndn/nfd.conf 2> /nfd.log &
sleep 1

echo "Create faces"
for neighbor in $NEIGHBORS
do
  nfdc face create tcp4://$neighbor persistency permanent
done

echo "Start NLSR"
nlsr -f /usr/local/etc/ndn/nlsr.conf &

# Provider Record Holder
# python3 /main.py 2> /pymain.log &
# nlsrc advertise /$ROUTER_GROUP_NUM

echo "Router is ready"

sleep infinity
