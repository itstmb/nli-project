import os

from utilities.logger import log
import utilities.interpreter as setup
import utilities.util as util


# generate country vector from database
def generate(saving_path):
    log('Generating <' + setup.feature + ',' + setup.domain + '> country vector')

    for domain_dir in os.scandir(setup.database):
        if domain_dir.name == 'europe_data' and setup.domain == 'in':
            countries = process_dir(domain_dir)
        elif domain_dir.name == 'non_europe_data' and setup.domain == 'out':
            countries = process_dir(domain_dir)

    util.save_file(saving_path, countries)


def process_dir(domain_dir):
    countries = []

    for country_dir in os.scandir(domain_dir):
        country_name = str.split(os.path.basename(country_dir), '.')[1]  # fetch country from dir (exm: Albania)
        for i in range(len(next(os.walk(country_dir))[1])):
            countries.append(country_name)

    return countries