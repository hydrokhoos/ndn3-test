from Crypto.PublicKey import RSA
import hashlib
import multibase

def generate_peer_id():
    # 2048ビットのRSA鍵を生成
    key = RSA.generate(2048)

    # DERフォーマットで公開鍵をエクスポート
    pub_key = key.publickey().export_key(format='DER')

    # 公開鍵からSHA256ハッシュを計算
    pub_key_hash = hashlib.sha256(pub_key).digest()

    # PeerIDを生成 (マルチコーデックプレフィックス 0x12 はSHA256を意味し、ハッシュサイズの0x20も含める)
    peer_id = b'\x12\x20' + pub_key_hash

    # Base58 BTCエンコーディングを使用してPeerIDをエンコード
    encoded_peer_id = multibase.encode('base58btc', peer_id)

    return encoded_peer_id

if __name__ == '__main__':
    # PeerIDを生成して表示
    print(generate_peer_id().decode('utf-8'))
