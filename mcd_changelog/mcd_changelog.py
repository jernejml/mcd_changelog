import requests
import json
from bs4 import BeautifulSoup

chains = ['mainnet', 'kovan', 'rinkeby', 'ropsten', 'goerli']
URL_CHANGELOG = "https://changelog.makerdao.com/"


class Release:
    """release class: holds chain, like kovan, and versioning"""
    def __init__(self, chain, version, contracts=None):
        self.chain = chain
        self.version = version
        self.contracts = contracts

    def readable(self):
        return self.chain + "/" + self.version

    def get_chain(self):
        return self.chain

    def get_version(self):
        return self.version

    def get_contracts(self):
        return self.contracts


class Releases:
    """List of Release classes"""
    def __init__(self):
        self.releases = []
        self.count = 0

    def __iter__(self):
        return iter(self.releases)

    def add_release(self, rel):
        self.releases.append(rel)
        self.count = self.count + 1

    def get_releases(self):
        return self.releases

    def get_count(self):
        return self.count

    def get_chain_releases(self, chain='mainnet'):
        if chain not in chains:
            raise Exception("Unknown chain. Try 'print(list_branches())'")
        return [r for r in self.releases if r.chain == chain]

    def get_chain_latest(self, chain='mainnet'):
        if chain not in chains:
            raise Exception("Unknown chain. Try 'print(list_branches())'")
        candidates = [r for r in self.releases if r.chain == chain]
        return [r for r in candidates if r.version == max([r.version for r in candidates])][0]


all_releases = Releases()


def list_branches():
    return chains


def fetch():
    try:
        result = requests.get(URL_CHANGELOG)
        return result.content
    except requests.exceptions.RequestException as e:
        raise e


def fetch_contracts(url):
    try:
        response = requests.get(url)
        return json.loads(response.content)
    except requests.exceptions.RequestException as e:
        raise e


def parse_release_string(rels):
    for r in rels:
        result = r.split("/")
        try:
            verify_string_format(result)
        except Exception as e:
            raise e
        try:
            contracts = fetch_contracts(URL_CHANGELOG + "releases/" + result[2] + "/" + result[3] + "/contracts.json")
        except Exception as e:
            raise e
        rel = Release(result[2], result[3], contracts)

        all_releases.add_release(rel)
    return


def get_releases(c):
    soup = BeautifulSoup(c, 'html.parser')
    prelim = [x.get('href')for x in soup.find_all('a') if x.get('href')]
    releases = [x for x in prelim if x.find("releases") > 0]
    for c in chains:
        rels = [x for x in releases if x.find(c) > 0]
        try:
            parse_release_string(rels)
        except Exception as e:
            raise e
    return all_releases


def verify_string_format(strings):
    if len(strings) is not 5:
        raise Exception("Parsed string length is not 5")
    if strings[0] is not '':
        raise Exception("First cut expected to be empty string")
    if strings[1] is 'releases':
        raise Exception("Second cut is not 'releases'")
    if strings[2] not in chains:
        raise Exception("Third cut should be known chain")
    # version
    if len(strings[3].split(".")) is not 3:
        if not (strings[3].split(".")[0].isdigit() and
                strings[3].split(".")[1].isdigit() and
                strings[3].split(".")[2].isdigit()):
            raise Exception("Version string not in format x.y.z, where x y z are digits")


def main():
    c = fetch()
    releases = get_releases(c)
    r = releases.get_chain_latest("kovan")
    contracts = r.get_contracts()
    print(contracts["MCD_FLIP_ETH_A"])


if __name__ == "__main__":
    main()
