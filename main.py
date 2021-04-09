from tika import parser
import boto3
import easygui


def open_file():
    input_file = easygui.fileopenbox(filetypes=["*.docx"])
    return input_file


def play_sound(text, filename, client):
    response = client.synthesize_speech(Text=text, VoiceId='Joanna', OutputFormat='mp3')

    body = response['AudioStream'].read()

    with open(filename, 'wb') as file:
        file.write(body)


def main():
    client = boto3.client('polly')
    filepath = open_file()
    filename = filepath.split('\\')[-1]
    filename = ''.join(filename.split('.')[0])
    raw = parser.from_file(filepath)
    text = raw['content']
    n = 3000
    df = [''.join(text[x:x + n]).strip() for x in range(0, len(text), n)]
    for item in df:
        play_sound(item,
                   filename=filename + str(df.index(item)) + '.mp3',
                   client=client)


if __name__ == '__main__':
    main()
