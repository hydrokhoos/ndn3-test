#!/bin/sh
NUM_CONTENTS=1000
RESULT_FILE=/ndn-find-provs-peer.csv

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
  printf '\rCreated: %s/%s' "$i" "$NUM_CONTENTS"
done
echo "\nTest contents created"

: > /hash_cid.py
echo "import hashlib" >> /hash_cid.py
echo "import sys" >> /hash_cid.py
echo "cid_tmp = int(hashlib.sha256(sys.argv[1].encode()).hexdigest(), 16)" >> /hash_cid.py
echo "print(cid_tmp % 3 + 1)" >> /hash_cid.py

: > /hashInterestNames.txt
for file in *
do
  printf '\rGenerating CID: %s' "${file}"
  hashCid=$(python3 /hash_cid.py $file)
  echo "/$hashCid/get/$file" >> /hashInterestNames.txt
done
echo "\nCIDs Generated"

echo "Searching contents"
echo "findprovs[ms],findpeer[ms]" > $RESULT_FILE
FILE_NAME=/hashInterestNames.txt && while read intName
do
  start_time=$(date +%s%3N)
  temp=$(ndnpeek -pP $intName)
  mid_time=$(date +%s%3N)
  peerID=$(echo $temp | cut -c4-50) # remove [' and ']
  ndnpeek -pP $peerID/info
  end_time=$(date +%s%3N)

  findprovs=$(($mid_time - $start_time))
  findpeer=$(($end_time - $mid_time))
  echo "$findprovs,$findpeer" >> $RESULT_FILE
  echo ""
done < ${FILE_NAME}

echo "\nDone!"
