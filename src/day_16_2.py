import fileinput
from functools import reduce
from typing import List


class TransmissionDecoder:
    def __init__(self, packets):
        self.packets = packets

    def evaluate_bits_transmission(self):
        return self.go_through_hierarchy(self.packets[0])

    def go_through_hierarchy(self, packet):
        packet["collected_literals"] = []
        for subpacket in packet["subpackets"]:
            if subpacket["type_nr"] == 4:
                packet["collected_literals"].append(subpacket["literal"])
            else:
                outcome = self.go_through_hierarchy(subpacket)
                packet["collected_literals"].append(outcome)
        packet["outcome"] = self.apply_operation(packet["type_nr"], packet["collected_literals"])
        return packet["outcome"]

    def apply_operation(self, type_nr, literals_list):
        """
        Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they
        only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their
        sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater
        than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than
        the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 7 are equal to packets - their value is 1 f the value of the first sub-packet is equal to the
        value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        :param type_nr:
        :param literals_list:
        :return:
        """
        if type_nr == 0:
            return sum(literals_list)
        elif type_nr == 1:
            return reduce((lambda x, y: x * y), literals_list)
        elif type_nr == 2:
            return min(literals_list)
        elif type_nr == 3:
            return max(literals_list)
        elif type_nr == 5:
            return 1 if literals_list[0] > literals_list[1] else 0
        elif type_nr == 6:
            return 1 if literals_list[0] < literals_list[1] else 0
        elif type_nr == 7:
            return 1 if literals_list[0] == literals_list[1] else 0
        else:
            raise Exception(f"Command {type_nr} not found")


class PacketParser:
    def __init__(self, package_bits: bin):
        self.packages = package_bits
        self.version_numbers = []
        self.packets = []

    def read_packets(self):
        current_operator = None
        while True:
            if len(self.packages) == 0 or all([True if int(n) == 0 else False for n in self.packages]):
                break
            if current_operator:
                self.process_operator(current_operator)
                current_operator = None
            else:
                packet = self.read_packet()
                self.packets.append(packet)
                if packet['type_nr'] != 4:
                    current_operator = packet
        return self.packets

    def process_operator(self, operator):
        current_operator = operator
        current_operator['subpackage_lengths'] = 0
        current_operator['subpackets'] = []

        if current_operator['length_type_id'] == 1:  # n subpackets
            for _ in range(0, current_operator['n_subpackets']):
                packet = self.read_packet()
                if packet['type_nr'] != 4:
                    packet = self.process_operator(packet)
                    current_operator['subpackage_lengths'] += packet['subpackage_lengths']
                current_operator['subpackage_lengths'] += packet['package_length']
                current_operator['subpackets'].append(packet)

        elif current_operator['length_type_id'] == 0:  # total length
            while current_operator['subpackage_lengths'] != current_operator['total_length_subpackets']:
                packet = self.read_packet()
                if packet['type_nr'] != 4:
                    packet = self.process_operator(packet)
                    current_operator['subpackage_lengths'] += packet['subpackage_lengths']
                current_operator['subpackage_lengths'] += packet['package_length']
                current_operator['subpackets'].append(packet)
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
    package_decoder = PacketParser(input_bin_list)
    packets = package_decoder.read_packets()
    transmission_decoder = TransmissionDecoder(packets)
    total = transmission_decoder.evaluate_bits_transmission()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
