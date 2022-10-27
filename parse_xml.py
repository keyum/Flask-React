import csv
import os
import time
from multiprocessing import Process
from pathlib import Path

from lxml import etree as lxml_etree

REVENUE_THRESHOLD = 100000
xmls_dir = "./xmls/"
csv_output_dir = "./backend/csv"
target_tags = ['TotalRevenueAmt', 'CYTotalRevenueAmt']
company_name_tag = "BusinessNameLine1Txt"

DEBUG = False


class Extractor:
    """
    Extracts company the name if revenue > 100000
    """
    def __init__(self):
        pass

    def xml_files_from_directory(self, xmls_dir):
        xml_files = []
        files = os.listdir(xmls_dir)
        try:
            for f in files:
                if f.endswith('.xml'):
                    xml_files.append(f)
                else:
                    print("The directory does NOT contain any xml file.")
                    break
            print(f"{xmls_dir} has {len(xml_files)} xml files")
            return xml_files
        except Exception as e:
            print(e)

    def filter_xml(self, xml_file, target_tags):
        targets = []
        output_dir = Path(csv_output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_csv = os.path.join(str(output_dir), os.path.dirname(xml_file).split('/')[-1] + '.csv')
        if DEBUG:
            print(f"output csv -> {output_csv}")

        if len(target_tags) != 0:
            namespace = self._get_namespace(xml_file)
            targets = [(namespace + i) for i in target_tags]
        else:
            print("target_tags are empty!")
            exit(0)
        for event, element in lxml_etree.iterparse(xml_file):
            if element.tag == (namespace + company_name_tag):
                company_name = element.text
            if element.tag == targets[0] or element.tag == targets[1]:
                if DEBUG:
                    print(f'{event}----{element.tag}----{element.text}')
                if int(element.text) > REVENUE_THRESHOLD:
                    self.__write_csv(output_csv, company_name)
                    if DEBUG:
                        print(f"{xml_file} --- {company_name} --- {element.text}")
            else:
                element.clear(keep_tail=True)

    def filter_xmls(self, xmls, targets):
        for xml in xmls:
            self.filter_xml(xml, targets)

    def _get_namespace(self, xml_file):
        xml_as_bytes = self.__read_xml(xml_file)
        tree = lxml_etree.fromstring(xml_as_bytes)
        root_tag = lxml_etree.QName(tree)
        namespace = "{" + root_tag.namespace + "}"
        return namespace

    def __read_xml(self, xml_file):
        with open(xml_file, 'rb') as xml:
            return xml.read()

    def __write_csv(self, csv_file, company_name):
        # newline = ''
        with open(csv_file, 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([company_name])


if __name__ == '__main__':
    # list all the files inside a directory
    processes = []
    all_xmls = []

    extractor = Extractor()
    sub_dirs = os.listdir(xmls_dir)
    for dir in sub_dirs:
        sub_dirs_path = xmls_dir + dir
        if os.path.isdir(sub_dirs_path):
            if DEBUG:
                print(sub_dirs_path)
            xmls = extractor.xml_files_from_directory(sub_dirs_path)
            print(f"Extracting from {sub_dirs_path} ... ")
            t0 = time.time()
            p = Process(target=extractor.filter_xmls, args=([(sub_dirs_path + "/" + xml) for xml in xmls], target_tags))
            p.start()
            processes.append(p)

    for process in processes:
        process.join()
        print(f"{p}  took {time.time() - t0} seconds to finish.")
