import fileinput
from typing import List


class PacketDecoder:
    def __init__(self, package_bits: bin):
        self.packages = package_bits
        self.version_numbers = []

    def read_packets(self):
        still_reading = True
        current_operator = None
        while still_reading:
            if len(self.packages) == 0 or all([True if int(n) == 0 else False for n in self.packages]):
                still_reading = False
                break
            if current_operator:
                self.process_operator(current_operator)
                current_operator = None
            else:
                packet = self.read_packet()
                if packet['type_nr'] != 4:
                    current_operator = packet

    def process_operator(self, operator):
        current_operator = operator
        current_operator['subpackage_lengths'] = 0
        if current_operator['length_type_id'] == 1:  # n subpackets
            for _ in range(0, current_operator['n_subpackets']):
                packet = self.read_packet()
                if packet['type_nr'] != 4:
                    sub_operator = self.process_operator(packet)
                    current_operator['subpackage_lengths'] += sub_operator['subpackage_lengths']
                current_operator['subpackage_lengths'] += packet['package_length']
        elif current_operator['length_type_id'] == 0:  # total length
            while current_operator['subpackage_lengths'] != current_operator['total_length_subpackets']:
                packet = self.read_packet()
                if packet['type_nr'] != 4:
                    sub_operator = self.process_operator(packet)
                    current_operator['subpackage_lengths'] += sub_operator['subpackage_lengths']
                current_operator['subpackage_lengths'] += packet['package_length']
        return current_operator

    def read_packet(self):
        version_number, type_nr = self.parse_version_and_type()
        packet = {
            'version_number': version_number,
            'type_nr': type_nr
        }
        if type_nr != 4:
            packet.update(self.parse_operator())
        elif type_nr == 4:
            packet.update(self.parse_literal())
        return packet

    def parse_version_and_type(self) -> (int, int):
        version_number = self.get_number()
        self.version_numbers.append(version_number)
        type_nr = self.get_number()
        return version_number, type_nr

    def get_number(self) -> int:
        """
        return 3 bit number to int, e.g. version number or type_nr
        pops numbers from self.packages
        """
        number = ''
        for _ in range(0, 3):
            number += self.packages.pop(0)
        return int(number, 2)

    def parse_literal(self) -> dict:
        total_number = ''
        package_length = 6
        done_reading = False
        while not done_reading:
            package_length += 5
            leading_value = int(self.packages.pop(0))
            done_reading = not bool(leading_value)  # when leading value == 0, stop reading next loop
            for _ in range(0, 4):
                total_number += self.packages.pop(0)
        return {'literal': int(total_number, 2),
                'package_length': package_length}

    def parse_operator(self):
        operator = {
            'length_type_id': int(self.packages.pop(0)),
            'contains': '',
            'n_subpackets': '',
            'total_length_subpackets': '',
            'package_length': 7
        }
        if operator['length_type_id'] == 0:
            operator['contains'] = 'total_length_subpackets'
            operator['package_length'] += 15
            for _ in range(0, 15):
                operator['total_length_subpackets'] += self.packages.pop(0)
            operator['total_length_subpackets'] = int(operator['total_length_subpackets'], 2)
        elif operator['length_type_id'] == 1:
            operator['contains'] = 'n_subpackets'
            operator['package_length'] += 11
            for _ in range(0, 11):
                operator['n_subpackets'] += self.packages.pop(0)
            operator['n_subpackets'] = int(operator['n_subpackets'], 2)
        return operator


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    binary_length = len(input_list[0]) * 4
    input_bin = bin(int(input_list[0], 16))[2:].zfill(binary_length)
    input_bin_list = list(input_bin)
    package_decoder = PacketDecoder(input_bin_list)
    package_decoder.read_packets()
    total = sum(package_decoder.version_numbers)
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
