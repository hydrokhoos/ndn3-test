#!/bin/sh
NUM_CONTENTS=1000

if ! $(type "bc" > /dev/null 2>&1); then
  apt-get install -y bc
fi

cd /
mkdir -p test-contents

if [ ! -d "CID-generator" ]; then
  git clone https://github.com/hydrokhoos/CID-generator.git
  pip install py-cid py-multihash
fi

cd /test-contents
rm -f *
echo "Creating test contents"
for i in `seq -w $NUM_CONTENTS`
do
  touch $i.txt
  echo "$i" > $i.txt
  mv $i.txt $(python3 /CID-generator/gen_cid.py $i.txt)
  printf '\rCreated %s/%s' "$i" "$NUM_CONTENTS"
done
echo "\nTest contents created"

echo "Putting contents"
for file in *
do
  python3 /send_publish.py -c $file -p /$PEERID
done

echo "\nDone!"
