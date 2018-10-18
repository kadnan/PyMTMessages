import re


def parse_first_block(msg):
    block_entries = []
    labeled_entries = []

    regex = r"{1:(\w{1})(\d+)(\w{12})(\d{4})(\d+)}"
    matches = re.finditer(regex, msg, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum += 1

        for groupNum in range(0, len(match.groups())):
            groupNum += 1
            block_entries.append(match.group(groupNum))

    if len(block_entries) == 5:
        labeled_entries.append({'Applid': block_entries[0]})
        labeled_entries.append({'Servid': block_entries[1]})
        labeled_entries.append({'LTaddrBlk1': block_entries[2]})
        labeled_entries.append({'Sesno': block_entries[3]})
        labeled_entries.append({'Osn': block_entries[4]})
    return {'BLOCK 1': labeled_entries}


def parse_2nd_block(msg):
    block_entries = []
    labeled_entries = []

    regex = '{\d{1}:(\w{1})(\d{3})(\d{4})(\d{6})(\w{12})(\d{4})(\d{6})(\d{6})(\d{4})(\w{1})'
    matches = re.finditer(regex, msg, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum += 1

        for groupNum in range(0, len(match.groups())):
            groupNum += 1
            block_entries.append(match.group(groupNum))
    if len(block_entries) >= 10:
        labeled_entries.append({'Inoutind': block_entries[0]})
        labeled_entries.append({'Msgtype': block_entries[1]})
        labeled_entries.append({'Intime': block_entries[2]})
        labeled_entries.append({'Indate': block_entries[3]})
        labeled_entries.append({'LTaddrBlk2': block_entries[4]})
        labeled_entries.append({'Ssesno': block_entries[5]})
        labeled_entries.append({'Isn': block_entries[6]})
        labeled_entries.append({'Outdate': block_entries[7]})
        labeled_entries.append({'Outtime': block_entries[8]})
        labeled_entries.append({'Msgprior': block_entries[9]})
    return {'BLOCK 2': labeled_entries}


def parse_3rd_block(msg):
    block_entries = []
    labeled_entries = []

    regex = '{\d+:(MT101 \d+\s+\w{2}\s\d+)'
    matches = re.finditer(regex, msg, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum += 1

        for groupNum in range(0, len(match.groups())):
            groupNum += 1
            block_entries.append(match.group(groupNum))
    if len(block_entries) > 0:
        labeled_entries.append({'Tag108': block_entries[0]})
    return {'BLOCK 3': labeled_entries}


def parse_4th_block(msg):
    block_entries = []
    labeled_entries = []

    # regex = ':20:(\d+)\n?:28D:(\d\/\d)\n?:50H:\/(\w+.?\w+.?\w+)(\n\w+)?\n?:30:(\d{6})\n?:21:(\w+)\n?:32B:(\w+),?\n?:50L:(\w+)\n?:59:\/(\w+\n\w+?)\n?:71A:(\w+)\n?-}'
    regex = '{4:\n?:20:(\d+)\n?:28D:(\d\/\d)\n?:50H:\/(\w+.?\w+.?\w+\n\w+)?\n?:30:(\d{6})\n?:21:(\w+)\n?:32B:(\w+),?\n?:50L:(\w+)\n?:59:\/(\w+\n\w+?)\n?:71A:(\w+)\n?-}'
    matches = re.finditer(regex, msg, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum += 1

        for groupNum in range(0, len(match.groups())):
            groupNum += 1
            block_entries.append(match.group(groupNum))

    if len(block_entries) >= 9:
        labeled_entries.append({'Senders Reference': block_entries[0]})
        labeled_entries.append({'Message Index/Total': block_entries[1]})
        labeled_entries.append({'50H - Ordering Customer': block_entries[2]})
        labeled_entries.append({'30 - Requested Execution Date': block_entries[3]})
        labeled_entries.append({'21 - Transaction Reference': block_entries[4]})
        labeled_entries.append({'32B - Currency/Transaction Amount': block_entries[5]})
        labeled_entries.append({'50L - Instructing Party': block_entries[6]})
        labeled_entries.append({'59 - Beneficiary': block_entries[7]})
        labeled_entries.append({'71A - Details of Charges': block_entries[8]})
    return {'BLOCK 4': labeled_entries}


def parse_5th_block(msg):
    block_entries = []
    labeled_entries = []

    regex = '{5:{MAC:(\w+)}{CHK:(\w+)}{TNG:(\w+|)}'
    matches = re.finditer(regex, msg, re.MULTILINE)

    for matchNum, match in enumerate(matches):
        matchNum += 1

        for groupNum in range(0, len(match.groups())):
            groupNum += 1
            block_entries.append(match.group(groupNum))

    if len(block_entries) >= 3:
        labeled_entries.append({'MAC': block_entries[0]})
        labeled_entries.append({'CHK': block_entries[1]})
        labeled_entries.append({'TNG': block_entries[2]})
    return {'BLOCK 5': labeled_entries}


def parse(message_text):
    mt_message = []

    try:

        if message_text is not None:
            mt_message.append(parse_first_block(message_text))
            mt_message.append(parse_2nd_block(message_text))
            mt_message.append(parse_3rd_block(message_text))
            mt_message.append(parse_4th_block(message_text))
            mt_message.append(parse_5th_block(message_text))
    except Exception as ex:
        print('Exception in parse')
        print(str(ex))
    finally:
        return mt_message


if __name__ == '__main__':
    data = None
    with open('101.txt', encoding='utf8') as f:
        data = f.read()
        result = parse(data)
        print(result)
