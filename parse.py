import json
import os
from PIL import Image
import openpyxl

# Paper Content
title = ''
abstract = ''
introduction = ''
section_list = []
conclusion = ''
reference_list = []
paragraph_list = []
image_list = []
chart_list = []

# specify the input json dir
json_dir = 'parsedFile.json'
# specify the output dir
output_dir = './output'

# alter this to see the run result
DISPLAY_MODE = True


class Paragraphs:
    def __init__(self, name, content):
        self.name = name
        self.content = content


def getParagraphs(json_obj):
    if isinstance(json_obj, dict):
        ttl = json_obj.get("Title", "")
        cont = json_obj.get("Content", "")

        paragraph_list.append(Paragraphs(ttl, cont))
        below = json_obj.get("Below", [])
        for content_item in below:
            getParagraphs(content_item)
    elif isinstance(json_obj, list):
        for content_item in json_obj:
            getParagraphs(content_item)


if __name__ == '__main__':
    with open(json_dir) as json_file:
        parsed_json = json.load(json_file)

    # '''
    # first pass
    # '''
    # title = parsed_json.get('Title', '')
    # abstract = parsed_json.get('Abstract', '')
    # for section in parsed_json.get('Content', []):
    #     if section.get('Title', '') == 'INTRODUCTION':
    #         introduction = section.get('Content', '')
    #         break
    # # presented by #title ##subtitle, but `conclusion` and `reference` is not included
    # for section in parsed_json.get('Content', []):
    #     section_list.append('#' + section['Title'])
    #     if len(section['Below']) != 0:
    #         for subSection in section['Below']:
    #             section_list.append('##' + subSection['Title'])
    # if '#CONCLUSION' in section_list:
    #     section_list.remove('#CONCLUSION')
    # if '#REFERENCES' in section_list:
    #     section_list.remove('#REFERENCES')
    #
    # for section in reversed(parsed_json.get('Content',[])):
    #     if section['Title'] == 'CONCLUSION':
    #         conclusion = section['Content']
    #         break
    # idx = conclusion.find('Acknowledgments')
    # if idx != -1:
    #     conclusion = conclusion[:idx]
    #
    # reference = parsed_json
    #
    # if DISPLAY_MODE:
    #     margin = '\n---------\n'
    #     print(title, margin, abstract, margin, section_list, margin, introduction, margin, conclusion)
    #
    # '''
    # second pass
    # '''
    #
    # for section in parsed_json['Content']:
    #     if section['Title'] != 'INTRODUCTION':
    #         getParagraphs(section)
    #
    # if DISPLAY_MODE:
    #     print('## Paragraph content shows below ## \n')
    #     for item in paragraph_list:
    #         print('name: ', item.name, '\n content:', item.content)
    #
    # page_num = 0
    '''
    first pass
    '''
    title = parsed_json.get('Title', '')
    abstract = parsed_json.get('Abstract', '')
    for section in parsed_json.get('Content', []):
        if section.get('Title', '') == 'INTRODUCTION':
            introduction = section.get('Content', '')
            break

    # presented by #title ##subtitle, but `conclusion` and `reference` is not included
    section_list = ['#' + section.get('Title', '') for section in parsed_json.get('Content', [])]
    section_list += ['##' + subSection.get('Title', '') for section in parsed_json.get('Content', []) if
                     len(section.get('Below', [])) != 0
                     for subSection in section['Below']]

    section_list = [item for item in section_list if item not in ['#CONCLUSION', '#REFERENCES']]

    for section in reversed(parsed_json.get('Content', [])):
        if section.get('Title', '') == 'CONCLUSION':
            conclusion = section.get('Content', '')
            break

    idx = conclusion.find('Acknowledgments')
    if idx != -1:
        conclusion = conclusion[:idx]

    for section in reversed(parsed_json.get('Content', [])):
        reference = ''
        if section.get('Title', '') == 'REFERENCES':
            reference = section.get('Content', '')
            reference_list = reference.split('\n')
            break
    # remove reference first emtpy element
    if reference_list[0] == '':
        reference_list = reference_list[1:]

    # if DISPLAY_MODE:
    #     margin = '\n---------\n'
    #     print(title, margin, abstract, margin, section_list, margin, introduction, margin, conclusion, margin, reference_list)

    '''
    second pass
    '''

    # Content of the paper
    for section in parsed_json.get('Content', []):
        if section.get('Title', '') != 'INTRODUCTION':
            getParagraphs(section)

    if DISPLAY_MODE:
        print('## Paragraph content shows below ## \n')
        for item in paragraph_list:
            print('name: ', item.name, '\n content:', item.content)

    page_num = 0

    try:
        sub_dir = os.listdir(output_dir)
        page_num = len(sub_dir)
        if page_num == 0:
            print('No pages inside \n')
        sub_dir = sorted(sub_dir, key=lambda x: int(x))

        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.lower().endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    img = Image.open(file_path)
                    image_list.append(img)
                elif file.lower().endswith('.xlsx'):
                    file_path = os.path.join(root, file)
                    chart = openpyxl.load_workbook(file_path)
                    chart_list.append(chart)
    except FileNotFoundError:
        print(f"Error: The folder '{output_dir}' does not exist.")

    if DISPLAY_MODE:
        print(f'The size of each list is {len(image_list)}, {len(chart_list)}')

