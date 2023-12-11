import json

# Paper Content
Title = ''
Abstract = ''
Introduction = ''

if __name__ == '__main__':
    with open('parsedFile.json') as json_file:
        parsed_json = json.load(json_file)

    Title = parsed_json['Title']
    Abstract = parsed_json['Abstract']
    for section in parsed_json['Content']:
        if section['Title'] == 'Introduction':
            Introduction = section['Content']
            break

    # print(parsed_json)
    # print('#')
    # print(Title, '\n', Abstract, '\n', Introduction)
