from ndn.encoding import Name
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cid")
parser.add_argument("-p", "--provider_record")
args = parser.parse_args()

app = NDNApp()

router_groups = 3

async def main(cid, provider_record):
    if provider_record[0] == '/':
        provider_record = provider_record[1:]

    try:
        cid_temp = int(hashlib.sha256(cid.encode()).hexdigest(), 16)
        # cid_temp = int(cid[-6:], base=32)
        data_name, meta_info, content = await app.express_interest(
            f'/{cid_temp % router_groups + 1}/provide/{cid}/{provider_record}',
            must_be_fresh=True,
            can_be_prefix=True,
            lifetime=6000,
        )
        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)

    except InterestNack as e:
        # A NACK is received
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # Interest times out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to NFD is broken
        print(f'Canceled')
    except ValidationFailure:
        # Validation failure
        print(f'Data failed to validate')
    finally:
        app.shutdown()

app.run_forever(after_start=main(args.cid, args.provider_record))
