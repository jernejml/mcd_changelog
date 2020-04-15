Parse releases at https://changelog.makerdao.com/

- beta
- dependent on webpage availability
- dependent on maker devs not changing web page structure 
- dependent on prompt webpage update after (new) releases
- no verifying on-chain 
- not uploaded to PyPi
- no docs
- no unit tests
- only tested on author's (windows) dev environment


**build wheel:**

```
python setup.py bdist_wheel
cd dist
pip install mcd_changelog-<...>.whl
```

**usage:**

```
import mcd_changelog

mcd_changelog.fetch()
releases = mcd_changelog.get_releases()
r = releases.get_chain_latest("mainnet")
contracts = r.get_contracts()
print(contracts["MCD_FLIP_ETH_A"])
print(r.get_abi("Flipper.abi"))
```


