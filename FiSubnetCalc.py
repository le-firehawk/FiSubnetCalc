# FiSubnetCalc, property of le_firehawk is pure Python, arithmic software intended for personal use only.
# Copyright (C) 2021 le_firehawk

# FiSubnetCalc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# FiSubnetCalc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# To contact the owner of FiSubnetCalc, use the following:
# Email: firehawk@opayq.net

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/gpl-3.0.html>


#
import random
import sys
import time
#


def animated_print(string):
    """Function for animating output"""
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    print("")


verbose_mode = False
if len(sys.argv) == 2:
    if sys.argv[-1].strip() == "-v":
        verbose_mode = True
else:
    verbose_mode = input("Enable verbose mode? [Y|N]: ")
    if "y" in verbose_mode.lower():
        verbose_mode = True
ip_addr, used_dd_chunks = input("Enter IP Address: "), []
temp_addr, valid = ip_addr.split("."), True
for segment in temp_addr:
    if int(segment) > 255:
        valid = False
if ip_addr.strip() == "" or ip_addr.count(".") != 3 or not valid:
    animated_print("Invalid IP address entered!")
    exit()
subnet_mask = input("Enter Subnet Mask: ")
use_vlsm = input("Use VLSM? [Y|N]: ")
if "y" in use_vlsm.lower():
    use_vlsm = True
else:
    use_vlsm = False


def to(type, input_value, **kwargs):
    """Transforms list variable to str, and vice versa"""
    if type.strip().lower() == "list":
        if type(input_value) == list:
            return input_value
        elif type(input_value) == str:
            seperator = kwargs.get("sep", " ")
            return input_value.split(seperator)
    elif type.strip().lower() == "str":
        temp = ""
        for x in input_value:
            temp += f"{x}."
        return temp[:-1]


def calculate_binary(subnet_mask, **kwargs):
    """Transforms a dotted decimal subnet mask into binary format"""
    reverse = kwargs.get("reverse", False)
    if not reverse:
        subnet_mask, subnet_binary = subnet_mask.split(".", 4), ""
        for iter, dd_chunk in enumerate(subnet_mask):
            try:
                dd_chunk = int(dd_chunk)
            except ValueError:
                animated_print("Invalid subnet mask entered!")
                exit()
            try:
                if dd_chunk < 255 and int(subnet_mask[iter+1]) > 0:
                    animated_print("Invalid subnet mask entered!")
                    exit()
            except IndexError:
                pass
            if dd_chunk == 255:
                subnet_binary += "11111111."
            elif dd_chunk > 255:
                animated_print("Invalid subnet mask entered!")
                exit()
            else:
                temp_chunk = [0, 0, 0, 0, 0, 0, 0, 0]
                while dd_chunk > 0:
                    if dd_chunk - 128 >= 0:
                        temp_chunk[0] = 1
                        dd_chunk -= 128
                    elif dd_chunk - 64 >= 0:
                        temp_chunk[1] = 1
                        dd_chunk -= 64
                    elif dd_chunk - 32 >= 0:
                        temp_chunk[2] = 1
                        dd_chunk -= 32
                    elif dd_chunk - 16 >= 0:
                        temp_chunk[3] = 1
                        dd_chunk -= 16
                    elif dd_chunk - 8 >= 0:
                        temp_chunk[4] = 1
                        dd_chunk -= 8
                    elif dd_chunk - 4 >= 0:
                        temp_chunk[5] = 1
                        dd_chunk -= 4
                    elif dd_chunk - 2 >= 0:
                        temp_chunk[6] = 1
                        dd_chunk -= 2
                    elif dd_chunk - 1 >= 0:
                        temp_chunk[7] = 1
                        dd_chunk -= 1
                for index, b_data in enumerate(temp_chunk):
                    try:
                        if temp_chunk[index-1] == 0 and b_data == 1 and index > 0:
                            animated_print("Invalid subnet mask entered!")
                            exit()
                    except IndexError:
                        pass
                    subnet_binary += str(b_data)
                subnet_binary += "."
        if subnet_binary.endswith("."):
            subnet_binary = subnet_binary[:-1]
        return subnet_binary
    else:
        binary_subnet, subnet_dd_mask = subnet_mask.split("."), [0, 0, 0, 0]
        for iter, binary_chunk in enumerate(binary_subnet):
            # binary_chunk = int(binary_chunk)
            for i, binary_num in enumerate(binary_chunk):
                if binary_num == "1":
                    if i == 0:
                        subnet_dd_mask[iter] += 128
                    elif i == 1:
                        subnet_dd_mask[iter] += 64
                    elif i == 2:
                        subnet_dd_mask[iter] += 32
                    elif i == 3:
                        subnet_dd_mask[iter] += 16
                    elif i == 4:
                        subnet_dd_mask[iter] += 8
                    elif i == 5:
                        subnet_dd_mask[iter] += 4
                    elif i == 6:
                        subnet_dd_mask[iter] += 2
                    elif i == 7:
                        subnet_dd_mask[iter] += 1
        return subnet_dd_mask


def calculate_prefix(subnet_mask, **kwargs):
    """Returns the CIDR Notation of a subnet mask, and vice versa"""
    prefix = kwargs.get("prefix", None)
    if prefix != None and subnet_mask == None:
        temp_value, temp_binary, str_binary = int(prefix.replace("/", "")), [], ""
        for _ in range(temp_value):
            temp_binary.append("1")
        while len(temp_binary) < 32:
            temp_binary.append("0")
        insert_exception = 0
        for i, char in enumerate(temp_binary):
            if (i % 8) / 2 == 0 and i != 0:
                temp_binary.insert(i + insert_exception, "_")
                insert_exception += 1
        for char in temp_binary:
            str_binary += char
        if str_binary.endswith("_"):
            str_binary = str_binary[:-1]
        comparison_binary, subnet_mask = str_binary.split("_"), [0, 0, 0, 0]
        for i, chunk in enumerate(comparison_binary):
            if chunk.count("0") == 0:
                subnet_mask[i] = 255
            else:
                for j, binary in enumerate(chunk):
                    if int(binary) == 1:
                        if j == 0:
                            subnet_mask[i] += 128
                        elif j == 1:
                            subnet_mask[i] += 64
                        elif j == 2:
                            subnet_mask[i] += 32
                        elif j == 3:
                            subnet_mask[i] += 16
                        elif j == 4:
                            subnet_mask[i] += 8
                        elif j == 5:
                            subnet_mask[i] += 4
                        elif j == 6:
                            subnet_mask[i] += 2
                        elif j == 7:
                            subnet_mask[i] += 1
        str_subnet_mask = ""
        for dd_chunk in subnet_mask:
            str_subnet_mask += f"{int(dd_chunk)}."
        if str_subnet_mask.endswith("."):
            str_subnet_mask = str_subnet_mask[:-1]
        return str_subnet_mask, prefix
    else:
        prefix = f"/{subnet_mask.count('1')}"
        return subnet_mask, prefix


def calculate_wildcard_mask(subnet_mask):
    """Returns a wildcard mask based on the dotted decimal subnet mask"""
    wildcard_mask = ""
    for dd_segment in subnet_mask.split("."):
        wildcard_mask += f"{255 - int(dd_segment)}."
    return wildcard_mask[:-1]


def calculate_all_possible_subnets(prefix, ip_addr, subnet_binary):
    """Executes key functions to aggregate the IP and binary data for output"""
    subnet_list = []
    needed_ip, max_portions = calculate_missing_segment(ip_addr, prefix)
    current_subnet_index, subnet_count, address_range, host_range, host_bits, subnet_bits = calculate_host_range(prefix, ip_addr, subnet_binary)
    for index in range(subnet_count):
        network_address, first_host_number = calculate_network_address(needed_ip, index, subnet_binary, prefix, address_range, host_range, host_bits, subnet_bits, subnet_count, current_subnet_index)
        first_host_address = f"{network_address.split('.')[0]}.{network_address.split('.')[1]}.{network_address.split('.')[2]}.{first_host_number}"
        broadcast_address, end_host_address = calculate_broadcast_address(needed_ip, int(prefix.replace("/", "")), network_address, subnet_binary, index, address_range, host_range, host_bits, subnet_bits, current_subnet_index, subnet_count)
        subnet_list.append([index, network_address, first_host_address, end_host_address, broadcast_address])
    current_subnet_details = subnet_list[current_subnet_index-1]
    return current_subnet_details, subnet_list, subnet_count, address_range, host_range, host_bits, subnet_bits, current_subnet_index


def calculate_missing_segment(ip_addr, prefix):
    """Based on the CIDR notation, determines the portion of an IP address that can change according to the network section of the subnet mask"""
    if int(prefix.replace("/", "")) in range(0, 9):
        needed_ip, max_portions = ip_addr[::-1].split(".")[-1][::-1], 3
    elif int(prefix.replace("/", "")) in range(9, 18):
        needed_ip, max_portions = ip_addr[::-1].split(".", 2)[-1][::-1], 2
    elif int(prefix.replace("/", "")) in range(18, 25):
        needed_ip, max_portions = ip_addr[::-1].split(".", 1)[-1][::-1], 1
    elif int(prefix.replace("/", "")) > 24:
        needed_ip, max_portions = ip_addr[::-1].split(".", 1)[-1][::-1], 0
    else:
        needed_ip, max_portions = ip_addr, 0
    if ip_addr.split(".")[2].strip() != "0":
        max_portions -= 1
    return needed_ip, max_portions


def calculate_host_range(prefix, ip_addr, subnet_binary):
    """Calculates the total number of addresses and hosts that a subnet can handle, along with the subnet the given IP resides in"""
    host_bits = subnet_binary.count("0")
    binary_segments, subnet_bits = subnet_binary.split("."), 0
    for binary_segment in binary_segments:
        if binary_segment.count("1") < 8:
            subnet_bits += binary_segment.count("1")
    total_available_addresses = pow(2, host_bits)
    host_addresses, subnet_count = total_available_addresses - 2, pow(2, subnet_bits)
    for subnet_index in range(1, subnet_count + 1):
        if int(ip_addr.split(".")[-1]) in range(total_available_addresses * (subnet_index - 1), total_available_addresses * subnet_index):
            current_subnet_index = subnet_index
    return current_subnet_index, subnet_count, total_available_addresses, host_addresses, host_bits, subnet_bits


def calculate_broadcast_address(ip, prefix, network_address, subnet_binary, iteration, address_range, host_range, host_bits, subnet_bits, current_subnet_index, subnet_count):
    """Returns the dotted decimal broadcast address and end host address"""
    address_array = [0, address_range]
    binary_segments, dd_segments, temp_network_address = subnet_binary.split("."), ip.split("."), []
    for i, binary_segment in enumerate(binary_segments):
        if binary_segment.count("1") == 8:
            temp_network_address.append(dd_segments[i])
        elif binary_segment.count("0") == 8:
            temp_network_address.append("0")
        else:
            segment_count = 0
            for j, binary_value in enumerate(binary_segment):
                if int(binary_value) == 1:
                    segment_count += parse_binary_addition(int(binary_value), j)
            temp_network_address.append(segment_count)
    while address_array[1] > 510:
        if address_array[1] > 510:
            address_array[0] += 1
            address_array[1] -= 255
    if int(address_array[1]) > 255:
        address_array[1] += (255 - address_array[1])
    if int(address_array[0]) > 255:
        address_array[0] += (255 - address_array[0])
    if subnet_binary.split(".")[-1].count("1") == 0:
        address_array[1] += 1
    if int(ip.split(".")[-1]) == int(temp_network_address[2]):
        broadcast_address = ip+f".{(int(network_address.split('.')[3]) - 1) + int(address_array[1])}"
    else:
        broadcast_address = ip+f".{int(temp_network_address[2]) + int(address_array[0])}.{(int(network_address.split('.')[3]) - 1) + int(address_array[1])}"
    last_host_address, output = [f"{segment}." for segment in broadcast_address.split(".")[0:-1]], ""
    for segment in last_host_address:
        output += segment
    output += str(int(broadcast_address.split(".")[-1])-1)
    return broadcast_address, output


def parse_binary_addition(binary_value, index):
    """Based on the binary representative value for dotted decimal subnet masks, returns the appropiate increment"""
    binary_dict = {0: 128, 1: 64, 2:32, 3:16, 4:8, 5:4, 6:2, 7:1}
    if binary_value == 1:
        return binary_dict.get(index, 0)


def transform_hosts(total_available_addresses):
    """Parses host address ranges greater than 255 by incrementing the adjacent dotted decimal segment"""
    if total_available_addresses > 255:
        address_list = [0, 0, 0, total_available_addresses]
        while address_list[3] > 256:
            address_list[2] += 1
            address_list[3] -= 256
        while address_list[2] > 256:
            address_list[1] += 1
            address_list[2] -= 256
        while address_list[1] > 255:
            address_list[0] += 1
            address_list[1] -= 257
    else:
        address_list = [0, 0, 0]
        address_list.append(total_available_addresses)
    return address_list


def calculate_network_address(needed_ip, iteration, subnet_binary, prefix, total_available_addresses, host_addresses, host_bits, subnet_bits, subnet_count, current_subnet_index):
    """Returns the dotted decimal network and first usable host address"""
    network_dd_portion = ""
    available_address_list = transform_hosts(total_available_addresses)
    for i, dd_chunk in enumerate(available_address_list):
        if dd_chunk != 0:
            network_dd_portion += f".{dd_chunk * iteration}"
        if i == len(available_address_list) - 1:
            first_host = (dd_chunk * iteration) + 1
    return f"{needed_ip}{network_dd_portion}", first_host


def reduce_by(reduction, network_address):
    """Re-calculates a dotted decimal IP address with the subtraction of an amount of addresses"""
    temp_address_list = network_address.split(".")
    if reduction <= 256 and int(temp_address_list[-1]) - reduction >= 0:
        new_address = f"{temp_address_list[0]}.{temp_address_list[1]}.{temp_address_list[2]}.{int(temp_address_list[3]) - reduction}"
    elif reduction <= 256:
        new_address = f"{temp_address_list[0]}.{temp_address_list[1]}.{int(temp_address_list[2]) - 1}.{(int(temp_address_list[3]) - reduction) + 255}"
    return new_address


def calculate_class(prefix):
    """Returns the class of a subnet mask based on the CIDR notation"""
    if prefix in range(8):
        subnet_class = "WTF?!?! Your subnet is soooo big!"
    elif prefix in range(8, 16):
        subnet_class = "Class A"
    elif prefix in range(16, 24):
        subnet_class = "Class B"
    elif prefix in range(24, 32):
        subnet_class = "Class C"
    else:
        subnet_class = "Undefined"
    return subnet_class


def invert(value):
    """Inverts a dotted decimal IP address by chunk, for the ARPA in-addr"""
    value = value.split(".")
    return f"{value[-1]}.{value[-2]}.{value[-3]}.{value[-4]}"


def calculate_optimal_subnets(LAN_required_host_array, subnet_count, subnet_bits, host_range, address_range, subnet_binary):
    """Returns a list of subnets for a VLSM network, with the relevant information grouped by subnet"""
    binary_array, binary_dict, new_binary_list = subnet_binary.split("."), {1: 1.8, 2: 1.7, 4: 1.6, 8: 1.5, 16: 1.4, 32: 1.3, 64: 1.2, 128: 1.1, 254: 1.0}, []
    for host_requirement in LAN_required_host_array:
        binary_index = binary_dict.get(host_requirement, None)
        if binary_index == None:
            for i, dict_value in enumerate(binary_dict.items()):
                if dict_value[0] - 2 in range(host_requirement, (dict_value[0] - 2) * 2):
                    binary_index = [int(str(dict_value[1]).split(".")[1]), dict_value[0]]
                    break
        binary_segment = ["", f"{'1' * int(binary_index[0])}{'0' * (8 - int(binary_index[0]))}"]
        observe_binary = subnet_binary.split(".")
        for i, section in enumerate(observe_binary):
            if section.count("0") == 8:
                observe_binary[i] = "11111111"
        new_binary_subnet_address = f"{observe_binary[0]}.{observe_binary[1]}.{observe_binary[2]}.{binary_segment[-1]}"
        new_binary_list.append([new_binary_subnet_address, binary_index[1], binary_index[1] - 2])
    return new_binary_list


def get_vlsm_details(ip_addr, subnet_mask, prefix, subnet_binary):
    """Accepts input and executes functions to gather necessary information on VLSM network"""
    LAN_required_host_array = []
    try:
        subnet_count = int(input("How many subnets (or LANs) are required? ").strip())
    except KeyboardInterrupt:
        mated_print("\nYou need to enter a number dude")
        exit()
    except:
        animated_print("You need to enter a number dude")
        exit()
    for LAN in range(subnet_count):
        LAN_required_host_array.append(int(input(f"How many hosts on LAN {LAN+1}? ").strip()))
    current_subnet_index, _, address_range, host_range, host_bits, subnet_bits = calculate_host_range(prefix, ip_addr, subnet_binary)
    if sum(LAN_required_host_array) > host_range:
        print(f"There are not {sum(LAN_required_host_array)} available addresses on subnet mask {subnet_mask} ({prefix})! It only supports {host_range}!")
        exit()
    optimal_subnets = calculate_optimal_subnets(LAN_required_host_array, subnet_count, subnet_bits, host_range, address_range, subnet_binary)
    for i, subnet in enumerate(optimal_subnets):
        subnet_dd_mask = calculate_binary(subnet[0], reverse=True)
        optimal_subnets[i].append([f"{dd_chunk}." for dd_chunk in subnet_dd_mask])
    return optimal_subnets, LAN_required_host_array


def main(ip_addr, subnet_mask):
    """Central function that executes other sub-functions and handles majority of program output"""
    if "/" in subnet_mask:
        subnet_mask, prefix = calculate_prefix(None, prefix=subnet_mask)
    else:
        prefix = None
    print(subnet_mask)
    subnet_binary = calculate_binary(subnet_mask)
    if prefix == None:
        subnet_binary, prefix = calculate_prefix(subnet_binary)
    if use_vlsm:
        try:
            optimal_subnets, hosts_per_subnet = get_vlsm_details(ip_addr, subnet_mask, prefix, subnet_binary)
            _, _, total_available_addresses, host_addresses, _, _ = calculate_host_range(prefix, ip_addr, subnet_binary)
            animated_print(f"\nVLSM Structure for {subnet_mask}")
            animated_print(f"Total Available Addresses: {total_available_addresses}")
            animated_print(f"Total Available Hosts: {host_addresses - ((2 * len(optimal_subnets)) - 2)}")
            animated_print(f"Short Form: {ip_addr}{prefix}\n\n")
            subnet_guide, new_subnet_order = [], []
            for i, subnet in enumerate(optimal_subnets):
                subnet_guide.append(subnet[1])
            for index in range(len(subnet_guide)):
                new_subnet_order.append([subnet_guide.index(max(subnet_guide)), max(subnet_guide)])
                subnet_guide[subnet_guide.index(max(subnet_guide))] = 0
            sorted_subnets = []
            for i in range(len(optimal_subnets)):
                sorted_subnets.append(optimal_subnets[new_subnet_order[i][0]])
            needed_ip, max_portions = calculate_missing_segment(ip_addr, prefix)
            gradual_ip = needed_ip+ ".0" * (3 - needed_ip.count("."))
            for i, subnet in enumerate(sorted_subnets):
                _, prefix = calculate_prefix(subnet[0])
                subnet_mask = f"{subnet[3][0]}{subnet[3][1]}{subnet[3][2]}{subnet[3][3][:-1]}"
                current_subnet_details, subnet_list, _, _, _, host_bits, subnet_bits, _ = calculate_all_possible_subnets(prefix, ip_addr, subnet[0])
                if i == 0:
                    network_address, first_host_number = calculate_network_address(needed_ip, i, subnet[0], prefix, subnet[1], subnet[2], host_bits, subnet_bits, len(sorted_subnets), i)
                    first_host_address = f"{network_address.split('.')[0]}.{network_address.split('.')[1]}.{network_address.split('.')[2]}.{first_host_number}"
                    broadcast_address, end_host_address = calculate_broadcast_address(needed_ip, int(prefix.replace("/", "")), network_address, subnet[0], i, subnet[1], subnet[2], host_bits, subnet_bits, i, len(sorted_subnets))
                else:
                    network_address, first_host_address = f"{broadcast_address.split('.')[0]}.{broadcast_address.split('.')[1]}.{broadcast_address.split('.')[2]}.{int(broadcast_address.split('.')[3]) + 1}", f"{broadcast_address.split('.')[0]}.{broadcast_address.split('.')[1]}.{broadcast_address.split('.')[2]}.{int(broadcast_address.split('.')[3]) + 2}"
                    broadcast_address, end_host_address = f"{network_address.split('.')[0]}.{network_address.split('.')[1]}.{network_address.split('.')[2]}.{int(network_address.split('.')[3]) + (subnet[1] - 1)}", f"{network_address.split('.')[0]}.{network_address.split('.')[1]}.{network_address.split('.')[2]}.{int(network_address.split('.')[3]) + (subnet[1] - 2)}"
                animated_print(f"Subnet: {i+1}")
                animated_print(f"Subnet Mask: {subnet_mask}")
                if verbose_mode == True:
                    animated_print(f"Wildcard Mask: {calculate_wildcard_mask(subnet_mask)}")
                    animated_print(f"CIDR Notation: {prefix}")
                    animated_print(f"Subnet Class: {calculate_class(int(prefix.replace('/', '')))}")
                    animated_print(f"Binary Subnet Mask: {subnet[0]}")
                    animated_print(f"Subnet Bits (Bits Borrowed): {subnet_bits}")
                animated_print(f"Addresses Used: {hosts_per_subnet[i]}")
                animated_print(f"Max. Addresses: {subnet[1]}, Max. Hosts: {subnet[2]}")
                if verbose_mode == True:
                    animated_print(f"Host Bits: {host_bits}/32")
                animated_print(f"Network Address: {network_address}")
                animated_print(f"First Host Address: {first_host_address}")
                animated_print(f"Last Host Address: {end_host_address}")
                animated_print(f"Broadcast Address: {broadcast_address}\n")
            if int(broadcast_address.split(".")[-1].strip()) < 255:
                animated_print(f"Leftover address range {broadcast_address} - {broadcast_address.split('.')[0]}.{broadcast_address.split('.')[1]}.{broadcast_address.split('.')[2]}.255")
                animated_print(f"{255 - int(broadcast_address.split('.')[-1])} Addresses, or {253 - int(broadcast_address.split('.')[-1])} hosts!")
        except SystemExit:
            pass
        except:
            print("Error! This program is still under development, so it ain't perfect. Attempting VLSM on CIDR's under /24 are not yet fully supported")
            raise
    else:
        wildcard_mask = calculate_wildcard_mask(subnet_mask)
        subnet_class = calculate_class(int(prefix.replace("/", "")))
        if int(prefix.replace("/", "")) > 30:
            animated_print(f"The Subnet address {subnet_mask} ({prefix}) is invalid! The highest possible subnet mask is 255.255.255.252 (/30)!")
            exit()
        current_subnet_details, subnet_list, subnet_count, address_range, host_range, host_bits, subnet_bits, current_subnet_index = calculate_all_possible_subnets(prefix, ip_addr, subnet_binary)
        if current_subnet_details == None:
            animated_print(f"Could not find the given IP address within any subnet! Defaulting to first subnet!")
            index, network_address, first_host_address, end_host_address, broadcast_address = subnet_list[0]
            ip_addr = first_host_address
        else:
            index, network_address, first_host_address, end_host_address, broadcast_address = current_subnet_details
        animated_print("\033[1m\033[5m*** Network Details ***\033[0m")
        animated_print(f"IP Address: {ip_addr}")
        animated_print(f"Subnet Mask: {subnet_mask}")
        if verbose_mode == True:
            animated_print(f"Wildcard Mask: {wildcard_mask}")
            animated_print(f"CIDR Notation: {prefix}")
            animated_print(f"Subnet Class: {subnet_class}")
            animated_print(f"Binary Subnet Mask: {subnet_binary}")
        animated_print(f"Number of Subnets: {subnet_count}")
        if verbose_mode == True:
            animated_print(f"Subnet Bits (Bits Borrowed): {subnet_bits}")
        animated_print(f"Max. Addresses: {address_range}, Max. Hosts: {host_range}")
        if verbose_mode == True:
            animated_print(f"Host Bits: {host_bits}/32")
        animated_print("\033[1m\033[5m*** Relevant Subnet Breakdown ***\033[0m")
        animated_print(f"In Subnet: {current_subnet_index}/{subnet_count}")
        animated_print(f"Network Address: {network_address}")
        if ip_addr.strip() == network_address.strip():
            print("^^ This is you! ^^")
        animated_print(f"First Host Address: {first_host_address}")
        if ip_addr.strip() == first_host_address.strip():
            print("^^ This is you! ^^")
        elif ip_addr.strip() != end_host_address.strip() and ip_addr.strip() != broadcast_address.strip() and int(ip_addr.split(".")[-1]) in range(int(first_host_address.split(".")[-1]), int(end_host_address.split(".")[-1])):
            print("<< You are in this range >>")
        animated_print(f"Last Host Address: {end_host_address}")
        if ip_addr.strip() == end_host_address.strip():
            print("^^ This is you! ^^")
        animated_print(f"Broadcast Address {broadcast_address}")
        if ip_addr.strip() == broadcast_address.strip():
            print("^^ This is you! ^^")
        animated_print(f"Short Form: {ip_addr}{prefix}")
        animated_print(f"ARPA in-addr: {invert(ip_addr)}.in-addr.arpa")
        print("")
        if subnet_count > 1:
            try:
                display_all_subnets = input("Would you like to display all subnets? [Y|N]: ")
            except KeyboardInterrupt:
                animated_print("\nFinished!")
                exit()
        else:
            display_all_subnets = "n"
        if "y" in display_all_subnets.lower():
            print("\n")
            iteration_index, presence_indicated = 0, False
            while iteration_index < subnet_count:
                presence_actively_indicated = False
                subnet_index, network_address, first_host_address, end_host_address, broadcast_address = subnet_list[iteration_index]
                print(f"Subnet {subnet_index + 1} (Total {subnet_count})")
                print(f"Network Address: {network_address}")
                if ip_addr.strip() == network_address.strip():
                    print("^^ This is you! ^^")
                    presence_indicated, presence_actively_indicated = True, True
                print(f"First Host Address: {first_host_address}")
                if ip_addr.strip() == first_host_address.strip():
                    print("^^ This is you! ^^")
                    presence_indicated, presence_actively_indicated = True, True
                elif ip_addr.strip() != end_host_address.strip() and ip_addr.strip() != broadcast_address.strip() and iteration_index == current_subnet_index and not presence_indicated and int(ip_addr.split(".")[-1]) in range(int(first_host_address.split(".")[-1]), int(end_host_address.split(".")[-1])):
                    print("<< You are in this range >>")
                    presence_indicated, presence_actively_indicated = True, True
                print(f"Last Host Address: {end_host_address}")
                if ip_addr.strip() == end_host_address.strip():
                    print("^^ This is you! ^^")
                    presence_indicated, presence_actively_indicated = True, True
                print(f"Broadcast Address {broadcast_address}")
                if ip_addr.strip() == broadcast_address.strip():
                    print("^^ This is you! ^^")
                    presence_indicated, presence_actively_indicated = True, True
                try:
                    proceed = input("(F)irst << (P)revious < | > (N)ext >> (L)ast: ")
                except KeyboardInterrupt:
                    animated_print("\nExiting!")
                    exit()
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                sys.stdout.flush()
                time.sleep(0.5)
                if presence_actively_indicated:
                    erase_range = 6
                else:
                    erase_range = 5
                if iteration_index < subnet_count:
                    for _ in range(erase_range):
                        sys.stdout.write("\033[F")
                        sys.stdout.write("\033[K")
                        sys.stdout.flush()
                    if presence_actively_indicated:
                        print("")
                    if "p" in proceed.lower() and iteration_index > 0:
                        iteration_index -= proceed.lower().count("p")
                    elif "p" in proceed.lower():
                        pass
                    elif "n" in proceed.lower() and iteration_index < subnet_count:
                        iteration_index += proceed.lower().count("n")
                    elif "n" in proceed.lower():
                        animated_print("Finished!")
                        exit()
                    elif "f" in proceed.lower():
                        iteration_index = 0
                    elif "l" in proceed.lower():
                        iteration_index = subnet_count - 1
                    elif iteration_index == subnet_count:
                        pass
                    else:
                        iteration_index += 1
                    if iteration_index < 0 or iteration_index > subnet_count:
                        animated_print("Index invalid! Resolving...")
                        if iteration_index < 0:
                            iteration_index = 0
                        else:
                            iteration_index = subnet_count
                else:
                    animated_print("Finished!")


main(ip_addr, subnet_mask)
