import requests
import json
import os
import pickle
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile
from pathlib import Path

chains = ['mainnet', 'kovan', 'rinkeby', 'ropsten', 'goerli']
URL_CHANGELOG = "https://changelog.makerdao.com/"

class Release:
    """release class: holds chain, like kovan, and versioning"""
    def __init__(self, chain, version, contracts=None, abipath=None):
        self.chain = chain
        self.version = version
        self.contracts = contracts
        self.abipath = abipath

    def readable(self):
        return self.chain + "/" + self.version

    def get_chain(self):
        return self.chain

    def get_version(self):
        return self.version

    def get_contracts(self):
        return self.contracts

    def get_abi_path(self):
        return self.abipath

    def get_abi(self, name):
        return load_abi(self.abipath, name)


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


loaded_releases = Releases()


def load_abi(path, name):
    filename = None
    for abi_path in Path(path).rglob('*.abi'):
        filename = abi_path.absolute()
        if abi_path.name == name:
            break
    if filename is not None:
        with (open(filename, "r")) as openfile:
            return openfile.read()


def list_branches():
    return chains


def load():
    filename = os.path.dirname(__file__) + '/releases.obj'
    try:
        with (open(filename, "rb")) as openfile:
            loaded_releases = pickle.load(openfile)
            return loaded_releases
    except pickle.UnpicklingError as e:
        print("unpickling error")
        return None
    except (AttributeError, EOFError, ImportError, IndexError) as e:
        print("todo")
        return None
    except FileNotFoundError:
        print("\nFile " + filename + " does not exist?. Run  command.\n")
    return None


def fetch():
    try:
        result = requests.get(URL_CHANGELOG)
        get_releases(result.content)
    except requests.exceptions.RequestException as e:
        raise e


def fetch_contracts(url):
    try:
        response = requests.get(url)
        return json.loads(response.content)
    except requests.exceptions.RequestException as e:
        raise e


def download_abi_zip(chain, version):
    # https://changelog.makerdao.com/releases/mainnet/1.0.4/abi/mainnet_abi_1.0.4.zip
    # mainnet_abi_1.0.4.zip
    url = URL_CHANGELOG + "releases/" + chain + "/" + version + "/abi/" + chain + "_abi_" + version + ".zip"
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise e
    if response.status_code != 200:
        if response.status_code == 404:
            print("Nothing at: " + url)
            return None
        raise Exception("Failed to download abi zip file. Status code: " + str(response.status_code))
    return response


def unzip_downloaded_zip(response, path):
    with ZipFile(BytesIO(response.content)) as my_zip_file:
        ZipFile.testzip(my_zip_file)
        for contained_file in my_zip_file.namelist():
            info = ZipFile.getinfo(my_zip_file, contained_file)
            ZipFile.extract(my_zip_file, info, path)


def parse_releases(rels):
    for r in rels:
        result = r.split("/")
        try:
            verify_string_format(result)
        except Exception as e:
            raise e
        try:
            chain = result[2]
            version = result[3]
            contracts = fetch_contracts(URL_CHANGELOG + "releases/" + chain + "/" + version + "/contracts.json")
        except Exception as e:
            raise e
        try:
            path = os.path.dirname(__file__) + '/abis/' + chain + '/' + version
            response = download_abi_zip(chain, version)
            if response is not None:
                unzip_downloaded_zip(response, path)
        except Exception as e:
            raise e
        release = Release(chain, version, contracts, path)
        loaded_releases.add_release(release)
    return


def get_releases(c):
    soup = BeautifulSoup(c, 'html.parser')
    prelim = [x.get('href')for x in soup.find_all('a') if x.get('href')]
    releases = [x for x in prelim if x.find("releases") > 0]
    for c in chains:
        rels = [x for x in releases if x.find(c) > 0]
        try:
            parse_releases(rels)
        except Exception as e:
            raise e
    filename = os.path.dirname(__file__) + '/releases.obj'
    filehandler = open(filename, 'wb')
    pickle.dump(loaded_releases, filehandler)


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
    releases = load()
    r = releases.get_chain_latest("mainnet")
    contracts = r.get_contracts()
    print(contracts["MCD_FLIP_ETH_A"])
    print(r.get_abi("Flipper.abi"))


if __name__ == "__main__":
    main()
