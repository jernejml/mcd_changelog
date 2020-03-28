**build wheel:**

```
python setup.py bdist_wheel
cd dist
pip install mcd_changelog-<...>.whl
```

**usage:**

```
import mcd_changelog

c = mcd_changelog.fetch()
releases = mcd_changelog.get_releases(c)
for r in releases:
    print(r.readable())

r = releases.get_chain_latest("kovan")
contracts = r.get_contracts()
print(contracts["MCD_FLIP_ETH_A"])
```


