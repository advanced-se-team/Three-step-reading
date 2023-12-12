import json

# Paper Content
title = ''
abstract = ''
introduction = ''
section_list = []
conclusion = ''

if __name__ == '__main__':
    with open('parsedFile.json') as json_file:
        parsed_json = json.load(json_file)

    '''
    first pass
    '''
    title = parsed_json['Title']
    abstract = parsed_json['Abstract']
    for section in parsed_json['Content']:
        if section['Title'] == 'INTRODUCTION':
            introduction = section['Content']
            break
    # presented by #title ##subtitle, but `conclusion` and `reference` is not included
    for section in parsed_json['Content']:
        section_list.append('#' + section['Title'])
        if len(section['Below']) != 0:
            for subSection in section['Below']:
                section_list.append('##' + subSection['Title'])
    if '#CONCLUSION' in section_list:
        section_list.remove('#CONCLUSION')
    if '#REFERENCES' in section_list:
        section_list.remove('#REFERENCES')

    for section in reversed(parsed_json['Content']):
        if section['Title'] == 'CONCLUSION':
            conclusion = section['Content']
            break
    idx = conclusion.find('Acknowledgments')
    if idx != -1:
        conclusion = conclusion[:idx]

    # for display
    margin = '\n---------'
    print(title, margin, abstract, margin, section_list, margin, introduction, margin, conclusion)

